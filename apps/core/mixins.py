from django.core.mail import send_mail
from django.conf import settings

from_email = settings.EMAIL_HOST_USER


class EmailSendingMixin(object):
    def __init__(self, admin_email, supplier_email, admin_message, supplier_message):
        self.admin_email = admin_email
        self.supplier_email = supplier_email
        self.admin_message = admin_message
        self.supplier_message = supplier_message

    
    def welcome_supplier(self):
        try:
            subject = "Welcome To Copy Cat"
            send_mail(subject, self.supplier_message, from_email, [self.supplier_email])
        except Exception as e:
            raise e
    
    def admin_notification(self):
        try:
            subject = "New Supplier"
            send_mail(subject, self.admin_message, from_email, [self.admin_email])
        except Exception as e:
            raise e


esm = EmailSendingMixin(admin_email, supplier_email, admin_message, supplier_message)
esm.welcome_supplier()
esm.admin_notification()