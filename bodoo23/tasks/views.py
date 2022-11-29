from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import InviteTask, SurveyTask, SocialMediaTask
from user.models import Profile, GlobalVar
from tasks.models import TaskUserRel
from tasks.serializers import TaskUserRelSerializer
from django.db.models.functions import Coalesce
from django.db.models import Sum, Value as V
from referral_system.models import ReferralRelationship


class TaskListView(ListAPIView):
    serializer_class = TaskUserRelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_level = Profile.objects.get(user=self.request.user).level
        return TaskUserRel.objects.filter(user=self.request.user, task__task_level__levels=user_level)

    def post(self, request, *args, **kwargs):
        user = request.user
        id = request.data.get('id')
        status = request.data.get('status')
        TaskUserRel.objects.filter(user=self.request.user, id=id).update(status=status)
        qs = TaskUserRel.objects.filter(user=self.request.user, id=id)[0]
        model = qs.task.content_type.model
        model_id = qs.task.object_id
        if model == 'invitetask':
            reward = InviteTask.objects.filter(id=model_id)[0].reward
            print(reward)
        elif model == 'surveytask':
            reward = SurveyTask.objects.filter(id=model_id)[0].reward
            print(reward)
        elif model == 'socialmediatask':
            reward = SocialMediaTask.objects.filter(id=model_id)[0].reward
            print(reward)
        else:
            reward = 0
        user_profile = Profile.objects.filter(user=user)[0]
        user_profile.value = user_profile.value + reward
        user_profile.balance = user_profile.balance + reward
        user_profile.save()
        # Finding 1st Employer/Inviter and adding 10% reward to his balance
        inviter_qs = ReferralRelationship.objects.filter(employee=self.request.user)
        global_qs = GlobalVar.objects.all()[0]
        if inviter_qs:
            inviter1 = ReferralRelationship.objects.filter(employee=self.request.user)[0].employer
            inviter_profile = Profile.objects.filter(user=inviter1)[0]
            inviter_profile.value = inviter_profile.value + (float(reward) * float(global_qs.lane1percentage/100))
            inviter_profile.balance = inviter_profile.balance + (float(reward) * float(global_qs.lane1percentage/100))
            inviter_profile.save()

        # Finding 2nd Employer/Inviter and adding 10% reward to his balance
        inviter_qs2 = ReferralRelationship.objects.filter(employee=inviter1)
        if inviter_qs2:
            inviter2 = ReferralRelationship.objects.filter(employee=inviter1)[0].employer
            inviter_profile = Profile.objects.filter(user=inviter2)[0]
            inviter_profile.value = inviter_profile.value + (float(reward) * float(global_qs.lane2percentage/100))
            inviter_profile.balance = inviter_profile.balance + (float(reward) * float(global_qs.lane2percentage/100))
            inviter_profile.save()

        # Finding 2nd Employer/Inviter and adding 10% reward to his balance
        inviter_qs3 = ReferralRelationship.objects.filter(employee=inviter2)
        if inviter_qs3:
            inviter3 = ReferralRelationship.objects.filter(employee=inviter2)[0].employer
            inviter_profile = Profile.objects.filter(user=inviter3)[0]
            inviter_profile.value = inviter_profile.value + (float(reward) * float(global_qs.lane3percentage/100))
            inviter_profile.balance = inviter_profile.balance + (float(reward) * float(global_qs.lane3percentage/100))
            inviter_profile.save()

        return Response("action performed successfully")


class RewardHistoryView(ListAPIView):
    # serializer_class = TaskUserRelSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        # user = request.user
        user_profile = Profile.objects.filter(user=user)[0]
        qs = TaskUserRel.objects.filter(user=user, status=True)
        # qs = TaskUserRel.objects.filter(user=user, status=True).aggregate(
        #             calories=Coalesce(Sum('calories'), V(0)))
        serializer = TaskUserRelSerializer(qs, many=True)
        for data in serializer.data:
            print(data)
            data['balance'] = user_profile.balance
            data['value'] = user_profile.value
        return Response(serializer.data)
