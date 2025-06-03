from abc import ABC, abstractmethod

from notification import Notification
from user import User

class NotificationChannel(ABC):
    @abstractmethod
    def send_notification(self, notification):
        pass


class SMSChannel(NotificationChannel):
    def send_notification(self, notification: Notification, user: User):
        print(
            f"""
            Hey {user.username},
                {notification.content}
            """
        )
        return "success"

class EmailChannel(NotificationChannel):
    def send_notification(self, notification: Notification, user: User):
        print(
            f"""
            Hey {user.username},
                {notification.content}
            """
        )
        return "success"