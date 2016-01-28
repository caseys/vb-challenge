from celery import task

__all__ = [
    "send_birthday_greeting",
    "send_change_of_zipcode",
]

@task
def send_birthday_greeting(contact_id):
    """send a friendly birthday greeting to a Contact!

    :param int contact_id: a reference for ``Contact.id`` to look up and send the greeting
    """
    from .models import Contact
    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return
    contact.send_birthday_greeting()

@task
def send_change_of_zipcode(contact_id):
    """send an alert that someone's address changed!

    :param int contact_id: a reference for ``Contact.id`` to look up and send the greeting
    """
    from .models import Contact
    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return
    contact.send_change_of_zipcode()