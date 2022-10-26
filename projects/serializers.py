from rest_framework import serializers
from django.contrib.auth.models import User
from projects.models import (Project,
                            Contributor,
                            Issue,
                            Comment)

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id',
                'description',
                'author',
                'issue'
                ]

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class IssueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id',
                'title',
                'desc',
                'tag',
                'status',
                'project',
                'priority',
                'author',
                'assignee',
                ]
        #read_only_fields = ('project',)

class IssueDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id',
                'created_time',
                'title',
                'desc',
                'tag',
                'status',
                'project',
                'priority',
                'author',
                'assignee',
        ]

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
        #read_only_fields = ('author', 'id')

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