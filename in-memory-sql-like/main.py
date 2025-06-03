import uuid
from typing import Any
from datetime import datetime

class Record:
    def __init__(self, values: dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.values = values
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, new_values: dict[str, Any]):
        self.values.update(new_values)
        self.updated_at = datetime.now()

    
    def to_dict(self):
        return {
            "id": self.id,
            "values": self.values,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        record = cls[data["values"]]
        record.id = data["id"]
        record.created_at = datetime.fromisoformat(data["created_at"])
        record.updated_at = datetime.fromisoformat(data["updated_at"])
        return record

class Table:
    def __init__(self, tablename: str, tableschema: list[tuple[str,str]]):
        self.name = tablename
        self.schema = tableschema
        self.records: dict[str,Record] = {}
        self.col_to_type = {
            col: typ for col,typ in tableschema
        }
        self.created_at = datetime.now()
        self.indexes: dict[str, Any] = {} # New: col → val → rec_ids

    def _validate_record(self, values: dict[str, Any]):
        for col in values:
            if col not in self.col_to_type.items():
                return ValueError(f"Unknown column in {col}")
            
        for col, expectedtype in self.col_to_type.items():
            if col not in values:
                raise ValueError(f"Missing value for column {col}")
            val = values[col]
            if type(val) != expectedtype:
                raise TypeError(f"Expected {expectedtype} for column {col} but got {type(val)}")
    
    def insert_record(self, values: dict[str, Any]):
        self._validate_record(values)
        record = Record(values)
        self.records[record.id] = record

        for col, idx in self.indexes.items():
            val = record.values.get(col)
            if val not in idx:
                idx[val] = set()
            idx[val].add(record.id)
        return record
    
    def update_record(self, rec_id, newvalues: dict[str, Any]):
        if rec_id not in self.records:
            raise KeyError(f"Record {rec_id} does not exist")
        self.records[rec_id].update(newvalues)
        return self.records[rec_id]
    
    def delete_record(self, rec_id):
        if rec_id not in self.records:
            raise KeyError(f"Record {rec_id} does not exist")
        del self.records[rec_id]

    def get_record(self, rec_id):
        if rec_id not in self.records:
            raise KeyError(f"Record {rec_id} does not exist")
    
    def filter_records(self, conditions: dict[str, Any]):
        res = []
        for record in self.records.values():
            if all(record.values.get(col) == val for col, val in conditions.items()):
                res.append(record)
        return res

    def select_all_records(self):
        return list(self.records.values())
    

    def create_index(self, column):
        if column not in self.col_to_type:
            raise KeyError(f"Column {column} does not exist in table schme")
        index = {}
        for id_, record in self.records.items():
            val = record.values.get(column)
            if val not in index:
                index[val] = set()
            index[val].add(id_)
        self.indexes[column] = index

    def select_by_index(self, column, value):
        if column not in self.indexes:
            raise ValueError(f"No index on column {column}")
        
        matched_ids = self.indexes[column].get(value, set())
        return [
            self.records[id_] for id_ in matched_ids
        ]
    
    def to_dict(self):
        return {
            "name": self.name,
            "schema": self.schema,
            "records": {rec_id: rec.to_dict() for rec_id, rec in self.records.items()},
        }
    
    @classmethod
    def from_dict(cls, data):
        table = cls(data["name"], data["schema"])
        table.records = {rec_id: Record.from_dict(rec_data) for rec_id, rec_data in data["records"].items()}
        return table

class Database:
    def __init__(self, dbname):
        self.name = dbname
        self.tables: dict[str, Table] = {}
        self.created_at = datetime.now()

    def create_table(
            self, 
            tablename: str, 
            tableschema: list[tuple[str,str]]
        ):
        if tablename in self.tables:
            raise KeyError(f"Table {tablename} already exists")
        table = Table(tablename, tableschema)
        self.tables[tablename] = table
        return table

    def get_table(self, tablename:str):
        if tablename not in self.tables:
            raise KeyError(f"Table {tablename} does not exist")
        return self.tables[tablename]
    
    def drop_table(self, tablename):
        if tablename not in self.tables:
            raise KeyError(f"Table {tablename} does not exist")
        del self.tables[tablename]
    
    def to_dict(self):
        return {
            "name": self.name,
            "tables": {tbl_name: tbl.to_dict() for tbl_name, tbl in self.tables.items()}
        }
    
    @classmethod
    def from_dict(cls, data):
        db = cls(data["name"])
        db.tables = {tbl_name: Table.from_dict(tbl_data) for tbl_name, tbl_data in data["tables"].items()}
        return db

import json
class InMemDBManager:
    def __init__(self):
        self.databases: dict[str, Database] = {}

    def create_database(self, database_name: str):
        if database_name in self.databases:
            raise KeyError(f"Database {database_name} already exists")
        db = Database(database_name)
        self.databases[database_name] = db
        return db

    def drop_database(self, database_name: str) -> None:
        if database_name not in self.databases:
            raise KeyError(f"Database {database_name} does not exist")
        del self.databases[database_name]
    
    def get_database(self, database_name: str) -> Database:
        if database_name not in self.databases:
            raise KeyError(f"Database {database_name} does not exist")
        return self.databases[database_name]
    

    def save_to_file(self, filepath="db.json"):
        data = {
            dbname: db.to_dict() for dbname, db in self.databases.items()
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath="db.json"):
        with open(filepath, "r") as f:
            raw = json.load(f)
        self.databases = {
            dbname: Database.from_dict(dbdata) for dbname, dbdata in raw.items()
        }


mgr = InMemDBManager()
db = mgr.create_database("mydb")
users = db.create_table("users", [("id", "INT"), ("name", "STRING")])

# Insert record
record = users.insert_record({"id": 1, "name": "Alice"})
print(record.values)  # {'id': 1, 'name': 'Alice'}

# Update record
users.update_record(record.id, {"id": 1, "name": "Alicia"})

# Get all records
for rec in users.select_all_records():
    print(rec.id, rec.values)



# Assume your "users" table has columns: name (str), age (int)
users.insert_record({"name": "Alice", "age": 30})
users.insert_record({"name": "Bob", "age": 25})
users.insert_record({"name": "Alice", "age": 35})

# Select users where name is "Alice"
results = users.filter_records({"name": "Alice"})
for r in results:
    print(r.values)

# Output:
# {'name': 'Alice', 'age': 30}
# {'name': 'Alice', 'age': 35}



users.create_index("name")  # Build index on name

users.insert_record({"name": "Alic2e", "age": 130})
users.insert_record({"name": "Bo33eb", "age": 25})
users.insert_record({"name": "Alsfice", "age": 335})

results = users.select_by_index("name", "Alice")
for r in results:
    print(r.values)

# After operation
mgr.save_to_file()




# To refer later! advance filtering in case and order as well INCASE
def select_where_advanced(
    self,
    condition_groups: list[list[tuple[str, str, Any]]],
    order_by: str = None,
    ascending: bool = True,
    limit: int = None
) -> list[Record]:
    """
    Extended SELECT: supports filtering, ordering, and limiting.

    condition_groups: OR groups of AND conditions.
    order_by: column name to sort by.
    ascending: sort direction.
    limit: max number of records to return.
    """
    def match(record, condition_group):
        for col, op, val in condition_group:
            rec_val = record.values.get(col)

            if op == "==":
                if rec_val != val:
                    return False
            elif op == "!=":
                if rec_val == val:
                    return False
            elif op == ">":
                if not (rec_val > val):
                    return False
            elif op == "<":
                if not (rec_val < val):
                    return False
            elif op == ">=":
                if not (rec_val >= val):
                    return False
            elif op == "<=":
                if not (rec_val <= val):
                    return False
            elif op.lower() == "in":
                if rec_val not in val:
                    return False
            elif op.lower() == "like":
                # SQL-style LIKE: % = wildcard
                pattern = "^" + str(val).replace("%", ".*") + "$"
                if not re.match(pattern, str(rec_val)):
                    return False
            else:
                raise ValueError(f"Unsupported operator: {op}")
        
        return True

    # Filter
    results = []
    for record in self.records.values():
        for group in condition_groups:
            if match(record, group):
                results.append(record)
                break

    # Order
    if order_by:
        results.sort(key=lambda r: r.values.get(order_by), reverse=not ascending)

    # Limit
    if limit is not None:
        results = results[:limit]

    return results
