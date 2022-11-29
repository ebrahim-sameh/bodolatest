from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import ReferralCode, ReferralRelationship
from .serializers import RefferCodeSerializer
from user.serializers import UserSerializer
from user.models import User

class RefferCodeJsonListView(ListAPIView):
    def get(self, request):
        # getting querry set with referral codes for user who make request
        queryset = ReferralCode.objects.filter(user=request.user)
        data = RefferCodeSerializer(queryset, many=True)
        return Response(data.data, status=status.HTTP_200_OK)


class ReferralUserListView(ListAPIView):
    def get(self, request):
        # getting querry set with referral codes for user who make request
        qs = list(ReferralRelationship.objects.filter(employer=request.user).values_list('employee', flat=True))
        queryset = User.objects.filter(id__in=qs)
        data = UserSerializer(queryset, many=True)
        return Response(data.data, status=status.HTTP_200_OK)

class InvitedUserListView(ListAPIView):
    def get(self, request):
        username = request.GET.get('username')
        # getting querry set with referral codes for user who make request
        qs = list(ReferralRelationship.objects.filter(employer__username=username).values_list('employee', flat=True))
        queryset = User.objects.filter(id__in=qs)
        data = UserSerializer(queryset, many=True)
        return Response(data.data, status=status.HTTP_200_OK)