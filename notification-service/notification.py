from uuid import uuid4
from datetime import datetime

from user import User
from schema import NotificationStatus

class Notification:
    def __init__(self, content):
        self.id = str(uuid4())
        self.content = content
        self.status = NotificationStatus.OUTSTANDING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def update_status(self, isSuccessful: bool):
        if isSuccessful:
            self.status = NotificationStatus.SENT
        else:
            self.status = NotificationStatus.FAILED

    def __repr__(self):
        return f"[{self.status.value}] Notification(id={self.id})#, sent_to=yay)"
