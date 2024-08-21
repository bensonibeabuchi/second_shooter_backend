from rest_framework import serializers
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import ShotList, ConsentForm, Project
from users.models import *

class IsOwnerOrCollaborator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user in obj.collaborators.all()


class ShotListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShotList
        fields = ['id', 'shot_description', 'shot_type', 'image_reference', 'is_done']
        # fields = '__all__'


class ConsentFormSerializer(serializers.ModelSerializer):
    photographer_name = serializers.CharField(source='photographer_name.first_name', read_only=True)
    
    class Meta:
        model = ConsentForm
        fields = ['id', 'subject_name', 'age', 'photographer_name', 'date', 'agency_logo', 'agency_name', 'subject_address', 'subject_photograph', 'subject_signature']


class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'email', ]  # Include other fields as needed

class ProjectSerializer(serializers.ModelSerializer):
    shot_list = ShotListSerializer(many=True, required=False)
    consent_form = ConsentFormSerializer(many=True, required=False)
    collaborators = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all(), required=False
    )
    collaborator_details = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'project_name', 'project_description', 'slug', 
            'shot_list', 'user', 'project_type', 'consent_form', 
            'collaborators', 'collaborator_details'
        ]
    def get_collaborator_details(self, obj):
        return CollaboratorSerializer(obj.collaborators.all(), many=True).data

    def create(self, validated_data):
        shot_list_data = validated_data.pop('shot_list', [])
        consent_form_data = validated_data.pop('consent_form', [])
        collaborators_data = validated_data.pop('collaborators', [])

        project = Project.objects.create(**validated_data)

        for shot_data in shot_list_data:
            shot_list_item = ShotList.objects.create(**shot_data)
            project.shot_list.add(shot_list_item)

        for consent_data in consent_form_data:
            consent_data['photographer_name'] = self.context['request'].user
            consent_form_item = ConsentForm.objects.create(**consent_data)
            project.consent_form.add(consent_form_item)

        for collaborator in collaborators_data:
            project.collaborators.add(collaborator)

        return project

    def update(self, instance, validated_data):
        shot_list_data = validated_data.pop('shot_list', [])
        consent_form_data = validated_data.pop('consent_form', [])
        collaborators_data = validated_data.pop('collaborators', [])

        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.project_description = validated_data.get('project_description', instance.project_description)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.project_type = validated_data.get('project_type', instance.project_type)

        instance.shot_list.clear()
        for shot_data in shot_list_data:
            shot_list_item, created = ShotList.objects.update_or_create(id=shot_data.get('id'), defaults=shot_data)
            instance.shot_list.add(shot_list_item)

        instance.consent_form.clear()
        for consent_data in consent_form_data:
            consent_data['photographer_name'] = self.context['request'].user
            consent_form_item, created = ConsentForm.objects.update_or_create(id=consent_data.get('id'), defaults=consent_data)
            instance.consent_form.add(consent_form_item)

        instance.collaborators.clear()
        for collaborator in collaborators_data:
            instance.collaborators.add(collaborator)

        instance.save()
        return instance
