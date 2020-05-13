from rest_framework import serializers
from .models import *


class ActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activity
        exclude = ('created','modified' )

class MilestoneSerializer(serializers.ModelSerializer):
    project_start_date = serializers.SerializerMethodField()
    project_end_date = serializers.SerializerMethodField()
    class Meta:
        model = MileStone
        exclude = ('created','modified' )
    def get_project_start_date(self, obj):
        if not obj.project:
            return obj.project
        return obj.project.start_date

    def get_project_end_date(self, obj):
        if not obj.project:
            return obj.project
        return obj.project.end_date

class ProjectWeightageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectWeightage
        fields = ['weightage']