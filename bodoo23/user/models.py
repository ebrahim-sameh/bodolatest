from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
import os
from datetime import datetime
from django.db.models.signals import post_save

now = datetime.now()

GenderChoice = (
    ("M", "Male"),
    ("F", "Female"),
)


def upload_img_to(instance, filename):
    instance_dict = instance.__dict__
    filename_base, filename_ext = os.path.splitext(filename)
    return 'users/%s/%s%s' % (
        instance.user.id,
        now.strftime("%Y%m%d%H%M%S"),
        filename_ext.lower(),
    )


class User(AbstractUser):
    referral_token = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=False, null=True)
    # redefining standard user manager
    objects = UserManager()
    # here to be aded
    # add new required field "referral_token"
    REQUIRED_FIELDS = ["referral_token", "email", "phone"]
    tasks = models.ManyToManyField("tasks.Task", through="tasks.TaskUserRel")


class Profile(models.Model):
    gender = models.CharField(max_length=2, blank=True, null=True, choices=GenderChoice)
    DOB = models.DateField(blank=True, null=True)
    image = models.ImageField(default=None, blank=True, null=True, upload_to="images/", max_length=1000)

    address = models.CharField(max_length=255, default=None, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="user_profile", default=None)
    grade = models.IntegerField(default=1)
    value = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    balance = models.IntegerField(default=0)
    pro_status = models.BooleanField(default=False)
    paymentvertfication = models.BooleanField(default=False)
    trial_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class LevelManagement(models.Model):
    levels = models.IntegerField(default=1)
    max_lvl_earnings = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    total_lvl_earnings = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    lvl_fee = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    lvl_tasks_no = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.levels)


class GlobalVar(models.Model):
    timeoftrialperiod = models.IntegerField(default=0)
    taskallowancetime  = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    lane1percentage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    lane2percentage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    lane3percentage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.timeoftrialperiod)


def post_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, gender="", DOB="2022-10-03", address="", image="")


post_save.connect(post_save_user_profile, sender=User)
