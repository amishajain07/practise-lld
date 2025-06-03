from fastapi import FastAPI

from notificationservice import NotificationService

app = FastAPI()

# add singleton class wala
svc = NotificationService()

@app.post('/addusers')
def add_user(username: str):
    # svc = NotificationService()
    svc.register_user(username)
    return "success"

@app.get('/fetch/users')
def get_all_users():
    userslist = [x.username for x in svc.registered_users.values()]
    return userslist

@app.post('/addnotification')
def add_notif(content: str):
    svc.add_notification(content)
    return "success"
    
@app.get('/fetch/notifications')
def get_all_notification():
    # notiflist = [x for x in svc.notifications.values()]
    return svc.notifications

@app.post('/notifyall')
def notify_all(notification_id: str):
    svc.notify_all_via_email(notification_id)
    return "Success"