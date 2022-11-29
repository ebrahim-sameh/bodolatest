from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from user.models import User
from django.db.models.signals import post_save, pre_save
from user.models import LevelManagement

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SocialMediaTask(TimeStampModel):
    post_url = models.URLField()
    action = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    endtime = models.DateTimeField()
    reward = models.DecimalField(max_digits=5, decimal_places=2)
    lock_time_boundary = models.IntegerField(default=1)
    lock_duration = models.IntegerField(default=1)


class SurveyTask(TimeStampModel):
    form_link = models.URLField()
    description = models.CharField(max_length=255)
    endtime = models.DateTimeField()
    reward = models.DecimalField(max_digits=5, decimal_places=2)
    lock_time_boundary = models.IntegerField(default=1)
    lock_duration = models.IntegerField(default=1)


class InviteTask(TimeStampModel):
    endtime = models.DateTimeField()
    qota = models.IntegerField(default=1)
    reward = models.DecimalField(max_digits=5, decimal_places=2)
    lock_time_boundary = models.IntegerField(default=1)
    lock_duration = models.IntegerField(default=1)


class Task(TimeStampModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    task_level = models.ForeignKey(LevelManagement, on_delete=models.CASCADE, null=True, blank=True, related_name='level_task')
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        try:
            if self.content_type.name == 'survey task':
                return f"{self.content_object.form_link} - {self.content_object.category} - {self.content_object.reward}"
            if self.content_type.name == 'invite task':
                return f"invite task - {self.content_object.reward}"
            if self.content_type.name == 'social media task':
                return f"{self.content_object.post_url} - {self.content_object.action} - {self.content_object.reward}"
        except Exception as e:
            print(str(e))
        return f"{self.id}"


class TaskUserRel(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "task",)

    def __str__(self):
        return f"{self.user} - {self.task}"


def post_save_create_ticket_key(sender, instance, created, **kwargs):
    if created:
        qs = User.objects.filter(is_superuser=False)
        for obj in qs:
            TaskUserRel.objects.create(user=obj, task=instance)
            print(obj.username)


post_save.connect(post_save_create_ticket_key, sender=Task)
