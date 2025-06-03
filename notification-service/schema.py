from enum import Enum

class NotificationStatus(str, Enum):
    CREATED = "Created"
    UPDATED = "Updated"
    SENT = "Sent"
    FAILED = "Failed"
    OUTSTANDING = "Outstanding"

class ChannelSchema:
    SMS = 'sms'
    EMAIL = 'email'