from uuid import uuid4

class User:
    def __init__(self, username):
        self.id = str(uuid4())
        self.username = username
        # self.email = email
        # self.subscriptions if needed as, which user susbcriben for which
