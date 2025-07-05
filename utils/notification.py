# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from notification.models.notification_model import Notification
# from authentication.models import User
# def send_notification(sender, receiver, message):
#     # Create a notification record in the database
#     notification = Notification.objects.create(
#         sender=sender,
#         receiver=receiver,
#         message=message,
#         is_read=False
#     )
    
#     channel_layer = get_channel_layer()
#     group_name = f'user_{receiver.id}'
#     async_to_sync(channel_layer.group_send)(
#         group_name,
#         {
#             'type': 'send_notification',
#             'notification': message
#         }
#     )

# def notify_admins(sender, message):
#     admin_users = User.objects.filter(role=User.Role.ADMIN)
    
#     for admin in admin_users:
#         send_notification(
#             sender=sender,
#             receiver=admin,
#             message=message
#         )