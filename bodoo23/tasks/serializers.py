from rest_framework import  serializers
from tasks.models import TaskUserRel, InviteTask, SocialMediaTask, SurveyTask


class SocialMediaTaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = SocialMediaTask
		exclude = ("id", "created_at", "updated_at")


class SurveyTaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = SurveyTask
		exclude = ("id", "created_at", "updated_at")


class InviteTaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = InviteTask
		exclude = ("id", "created_at", "updated_at")


class TaskUserRelSerializer(serializers.ModelSerializer):
	task = serializers.SerializerMethodField()
	task_type = serializers.SerializerMethodField()

	class Meta:
		model = TaskUserRel
		fields = ("id", "task", "status", "task_type")

	def get_task(self, obj):
		try:
			if obj.task.content_type.name == 'survey task':
				return SurveyTaskSerializer(obj.task.content_object, many=False).data
			if obj.task.content_type.name == 'invite task':
				return InviteTaskSerializer(obj.task.content_object, many=False).data
			if obj.task.content_type.name == 'social media task':
				return SocialMediaTaskSerializer(obj.task.content_object, many=False).data
		except AttributeError:
			pass
		return ""

	def get_task_type(self, obj):
		try:
			return obj.task.content_type.name
		except Exception as e:
			pass
		return ""
