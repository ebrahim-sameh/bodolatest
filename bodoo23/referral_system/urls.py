from django.urls import path

from . import views

urlpatterns = [
    path("get_tokens/", views.RefferCodeJsonListView.as_view(), name='get_tokens'),
    path("get_referral_user/", views.ReferralUserListView.as_view(), name='get_referral_user'),
    path("invited_user/", views.InvitedUserListView.as_view(), name='invited_user'),
]