from rest_framework import serializers
from .models import Profile, User, LevelManagement
from django.db import IntegrityError, transaction
from djoser.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from datetime import datetime

class UserprofileSerializer(serializers.ModelSerializer):
    """Serializer to view the details of user profile"""
    email = serializers.SerializerMethodField(source='get_email')
    username = serializers.SerializerMethodField(source='get_username')
    total_days = serializers.SerializerMethodField(source='get_total_days')
    lvl_tasks_no = serializers.SerializerMethodField(source='get_lvl_tasks_no')
    max_lvl_earnings = serializers.SerializerMethodField(source='get_max_lvl_earnings')

    def get_max_lvl_earnings(self, obj):
        qs = LevelManagement.objects.get(levels=obj.level)

        return qs.max_lvl_earnings

    def get_lvl_tasks_no(self, obj):
        qs = LevelManagement.objects.get(levels=obj.level)

        return qs.lvl_tasks_no

    def get_total_days(self, obj):
        day = (datetime.strptime(str(datetime.now()).split()[0], '%Y-%m-%d') - datetime.strptime(str(obj.user.date_joined).split()[0], '%Y-%m-%d')).days
        return day

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Profile
        fields = ('username', 'gender', 'DOB', 'image', 'address', 'email', 'grade', 'value', 'level', 'lvl_tasks_no', 'max_lvl_earnings', 'pro_status', 'trial_status', 'total_days', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    """Serializer to view the details of user profile"""

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'referral_token')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": "Unable to create account."
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user
