from django.conf import settings
from django.core.mail import send_mail
from django.db import models, transaction
from django.db.models.signals import post_save

from .tasks import *

class Contact(models.Model):
    """store contact information for emailing a user in the address book"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="A reference to the User for the purpose of his/her address book")
    first_name = models.TextField(help_text='The first name')
    last_name = models.TextField(help_text='The last name')
    email = models.EmailField(max_length=255, help_text='The email address')
    zipcode = models.CharField(max_length=10, help_text='The zip code')
    birthdate = models.DateField(null=True, blank=True, help_text='The birthday')

    @classmethod
    def send_birthday_greetings(cls, start_date):
        """send a birthday greeting to people!

        :param datetime.date start_date: the birthday date to send...probably ``datetime.date.today()``
        """
        for contact in cls.objects.filter(birthdate=start_date).all():
            send_birthday_greeting.delay(contact.id)

    @transaction.atomic()
    def change_zipcode(self, zipcode):
        """change the zipcode and send an alert to the ``Contact.user`` that it has changed
        
        :param str zipcode: The new zipcode
        """
        self.zipcode = zipcode
        self.save()
        
        ## in case we are sending out a ton of birhtday cards, we'll use a higher prioirty queue here
        #send_change_of_zipcode.delay(self.id)
        send_change_of_zipcode.apply_async(args=[self.id], queue='priority.high')


    def send_birthday_greeting(self):
        """send a birthday greeting to this ``Contact``"""
        subject = "Happy Birthday %s!" % self.first_name
        message = """Happy Birthday to You, %s!!""" % self.first_name
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])

    def send_change_of_zipcode(self):
        """send change of zipcode information to ``Contact.user``"""
        subject = "Zipcode Update Info"
        message = """Just to let you know, %s has change the zipcode to: %s""" % (self.first_name, self.zipcode,)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
