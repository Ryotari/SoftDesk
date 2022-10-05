from rest_framework import serializers
from projects.models import (Project,
                            Contributor,
                            Issue,
                            Comment)

class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']

class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id',
                'title',
                'type',
                'description',
                'author']
        read_only_fields = ('author', 'id')

class ProjectDetailSerializer(serializers.ModelSerializer):
    
    contributor = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id',
                'title',
                'type',
                'description',
                'author',
                'contributor']

    def get_contributor(self, instance):
        queryset = Contributor.objects.filter(project=instance.id)
        return ContributorSerializer(queryset, many=True).data