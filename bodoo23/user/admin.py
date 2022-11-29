from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect

from .models import User, Profile, LevelManagement, GlobalVar


@admin.register(User)
class UserAdmin(UserAdmin):
    change_form_template = "admin/custom_changeform.html"

    def response_change(self, request, obj):
        if "_make-unique" in request.POST:
            User.objects.create_reftoken(obj)
            self.message_user(request, "New referral code has been added successfully!")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    list_display = ["username", "email", "phone", "first_name", "last_name", "is_staff"]


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ["user", "created_at"]


class LevelManagementAdmin(admin.ModelAdmin):
    model = LevelManagement
    list_display = ["levels", "total_lvl_earnings", "lvl_fee", "lvl_tasks_no", "created_at"]

class GlobalVarAdmin(admin.ModelAdmin):
    model = GlobalVar
    list_display = ["timeoftrialperiod", "taskallowancetime",  "lane1percentage",  "lane2percentage",  "lane3percentage",  "created_at"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(LevelManagement, LevelManagementAdmin)
admin.site.register(GlobalVar, GlobalVarAdmin)
