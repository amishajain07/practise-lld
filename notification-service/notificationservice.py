from datetime import datetime
from typing import Optional

from user import User
from notification import Notification
from schema import ChannelSchema
from channels import SMSChannel, EmailChannel, NotificationChannel

class NotificationService:
    def __init__(self):
        self.registered_users: dict[str,User] = {}
        self.notifications: dict[str, Notification] = {}
        self.channels: dict[ChannelSchema, NotificationChannel] = {
            ChannelSchema.SMS: SMSChannel(),
            ChannelSchema.EMAIL: EmailChannel()
        }

    def register_user(self, username):
        try:
            user = User(username)
            self.registered_users[user.id] = user
            print(f"User {username} added")
        except Exception as e:
            print(e)

    def add_notification(self, content:str):
        try:
            notification = Notification(content)
            self.notifications[notification.id] = notification
            print(f"Notification added with id: {notification.id}")
        except Exception:
            raise ValueError()

    def update_notification(self, notification_id, new_content):
        try:
            notification = self.notifications[notification_id]
            notification.content = new_content
            notification.updated_at = datetime.now()
            print(f"Notification updated for id: {notification_id}")
        except Exception:
            raise ValueError()

    def notify_email(self, user_id, notification_id):
        try:
            if user_id not in self.registered_users:
                raise ValueError("User not found")
            user = self.registered_users[user_id]
            if notification_id not in self.notifications:
                raise ValueError("Notification not found")
            notification = self.notifications[notification_id]
            res = self.channels[ChannelSchema.EMAIL].send_notification(notification, user)
            if res == "Success":
                print(f"Email sent to user: {user.username}")
            else:
                return ValueError()
        except Exception as e:
            print(e)

    def notify_all_via_email(self, notification_id: str):
        try:
            notification = self.notifications[notification_id]
            for user in self.registered_users.values():
                self.channels[ChannelSchema.EMAIL].send_notification(notification, user)
            return {
                'status': 200
            }
        except Exception as e:
            print(e)
            return 