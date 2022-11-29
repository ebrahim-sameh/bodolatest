from django.contrib import admin
from .models import *


admin.site.register(SurveyTask)
admin.site.register(SocialMediaTask)
admin.site.register(InviteTask)
admin.site.register(Task)
admin.site.register(TaskUserRel)