from django.urls import path

from . import views

urlpatterns = [
    path("task/list/", views.TaskListView.as_view(), name='task-list'),
    path("reward-history/", views.RewardHistoryView.as_view(), name='reward-history')
]