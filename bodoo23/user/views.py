import base64
import io

from django.core.files import File
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user import serializers
from .models import User, Profile, GlobalVar
from tasks.models import TaskUserRel, Task
from rest_framework.generics import ListAPIView
from referral_system.models import ReferralRelationship
from .serializers import UserSerializer


class ProfileView(APIView):

    def get(self, request, format=None):
        user = request.user
        qs = Profile.objects.filter(user=user)
        serializer = serializers.UserprofileSerializer(qs, many=True)
        qs1 = GlobalVar.objects.all()[0]
        for data in serializer.data:
            if data['total_days'] > qs1.timeoftrialperiod:
                data['trial_status'] = True
                qs[0].trial_status = True
                qs[0].save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        try:
            qs = Profile.objects.get(user=request.user)
        except Exception as e:
            return Response(str(e))
        image_url = request.data.get('image')
        if image_url:
            # converting bse64 string into file and save in database
            temp, imagestr = image_url.split(';base64,')
            ext = temp.split('/')[-1]
            image_data = base64.b64decode(imagestr)
            request.data['image'] = File(io.BytesIO(image_data), name='file.' + ext)
        partial = True
        serializer = serializers.UserprofileSerializer(qs, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("action performed successfully")


class Login(generics.GenericAPIView):
    serializer_class = TokenObtainPairSerializer

    # @classmethod
    # def get_token(cls, user):
    #     return RefreshToken.for_user(user)
    #
    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #
    #     refresh = self.get_token(self.user)
    #
    #     data['refresh'] = str(refresh)
    #     data['access'] = str(refresh.access_token)
    #     return data

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(str(e))
        data = serializer.validated_data
        user = User.objects.filter(username=request.data.get("username"))
        if not user[0].check_password(request.data.get("password")):
            return Response({"message": "Your password is invalid. Please try again."},
                            status=status.HTTP_401_UNAUTHORIZED)

        data['email'] = user[0].email
        data['phone'] = user[0].phone
        data['referral_token'] = user[0].referral_token
        data['DOB'] = user[0].user_profile.DOB
        data['address'] = user[0].user_profile.address
        data['gender'] = user[0].user_profile.gender
        data['profile_created_at'] = user[0].user_profile.created_at
        data['grade'] = user[0].user_profile.grade
        return Response(data, status=status.HTTP_200_OK)


class UserDetail(APIView):

    def get(self, request, format=None):
        user = request.GET.get('username')
        # user = request.user
        qs = Profile.objects.filter(user__username=user)
        serializer = serializers.UserprofileSerializer(qs, many=True)
        return Response(serializer.data)


class Signup(generics.GenericAPIView):
    serializer_class = serializers.UserCreateSerializer

    def post(self, request, *args, **kwargs):

        try:
            if not request.data.get('email'):
                return Response("Users must have an email address!", status=status.HTTP_200_OK)
            if request.data.get("username") and User.objects.filter(username=request.data.get("username")):
                return Response("Username already exist", status=status.HTTP_200_OK)
            if request.data.get("email") and User.objects.filter(email=request.data.get("email")):
                return Response("Email already exist", status=status.HTTP_200_OK)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            my_user = serializer.save()
            print(my_user)
            task_qs = Task.objects.all()
            for instance in task_qs:
                TaskUserRel.objects.create(user=my_user, task=instance)
        except Exception as e:
            return Response(str(e), status=status.HTTP_200_OK)
        return Response("action performed successfully", status=status.HTTP_200_OK)


class GlobalVarView(APIView):

    def get(self, request, format=None):
        qs = GlobalVar.objects.all()[0]
        context = {
            "timeoftrialperiod": qs.timeoftrialperiod,
            "taskallowancetime": qs.taskallowancetime,
            "lane1percentage": qs.lane1percentage,
            "lane2percentage": qs.lane2percentage,
            "lane3percentage": qs.lane3percentage,
            "invitemaxearning": qs.invitemaxearning,
            "subscribemaxearning": qs.subscribemaxearning,

        }
        return Response(context)


class SpecialUserView(ListAPIView):
    def get(self, request):
        username = request.GET.get('username')
        # getting querry set with referral codes for user who make request
        special_user_id = list(ReferralRelationship.objects.filter(employer__username=username, employee__user_profile__pro_status=True).values_list('employee', flat=True)[:5])
        normal_user_id = list(ReferralRelationship.objects.filter(employer__username=username, employee__user_profile__pro_status=False).values_list('employee', flat=True)[:5])
        normal_user_len = (len(normal_user_id) - len(special_user_id))

        queryset = User.objects.filter(id__in=special_user_id + normal_user_id[:normal_user_len])
        data = UserSerializer(queryset, many=True)
        return Response(data.data, status=status.HTTP_200_OK)
