import logging
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Expense, Profile

logger = logging.getLogger(__name__)


# ---------------- Expense signals ----------------

@receiver(pre_save, sender=Expense)
def set_default_date(sender, instance, **kwargs):
    if not instance.date:
        instance.date = now().date()

@receiver(pre_save, sender=Expense)
def validate_amount(sender, instance, **kwargs):
    if instance.amount <= 0:
        raise ValidationError("Expense amount must be greater than 0.")

@receiver(pre_save, sender=Expense)
def auto_categorize(sender, instance, **kwargs):
    if not instance.category or instance.category == 'Other':
        title = instance.title.lower()
        if "uber" in title or "bus" in title:
            instance.category = "Travel"
        elif "pizza" in title or "restaurant" in title:
            instance.category = "Food"

@receiver(post_save, sender=Expense)
def notify_expense_added(sender, instance, created, **kwargs):
    if created:
        logger.info(f"💰 New expense added: {instance.title} - ₹{instance.amount}")


# ---------------- Profile signals ----------------

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"👤 Profile created for {instance.username}")

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
