import secrets
from rest_framework import serializers
from .models import ReferralCode, ReferralRelationship

class ReferralSerializer(serializers.ModelSerializer):
    employer = serializers.SerializerMethodField(source='get_employer')

    def get_employer(self, obj):

        return obj.employer.username

    employee = serializers.SerializerMethodField(source='get_employee')

    def get_employee(self, obj):
        return obj.employee.username
    class Meta:
        model = ReferralRelationship
        fields = [
            "employer",
            "employee", 
            "refer_token"]

class RefferCodeSerializer(serializers.ModelSerializer):
    referral_code = ReferralSerializer(many=True, default="")
    class Meta:
        model = ReferralCode
        fields = [
            "token", 
            "user", 
            "referral_code"]
        