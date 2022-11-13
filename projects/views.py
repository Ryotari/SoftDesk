from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import (ProjectListSerializer,
                                ProjectDetailSerializer,
                                UserSerializer,
                                ContributorSerializer,
                                IssueListSerializer,
                                IssueDetailSerializer,
                                CommentSerializer)
from projects.permissions import (ProjectPermission,
                                ContributorPermission,
                                IssuePermission,
                                CommentPermission)

class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def get_queryset(self):
        projects_ids = [contributor.project.id for contributor in Contributor.objects.filter(user=self.request.user).all()]
        return Project.objects.filter(id__in=projects_ids)

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create':
            return self.detail_serializer_class
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['author'] = request.user.id
        request.data._mutable = False
        project = super().create(request, *args, **kwargs)
        contributor = Contributor.objects.create(
                            user=request.user,
                            project=Project.objects.filter(id=project.data['id']).first(),
                            role='AUTHOR')
        contributor.save()
        return Response(project.data)

    def update(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['author'] = request.user.id
        request.data._mutable = False
        return super().update(request, *args, kwargs)
        
class ContributorViewset(ModelViewSet):
    serializer_class = UserSerializer
    detail_serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ContributorPermission]

    def get_queryset(self):
        contributor_ids = [contributor.user.id for contributor in Contributor.objects.filter(project=self.kwargs['projects_pk'])]
        return User.objects.filter(id__in=contributor_ids)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            user_to_add = User.objects.filter(email=request.data['email']).first()
            if user_to_add:
                contributor = Contributor.objects.create(
                    user=user_to_add,
                    project=Project.objects.filter(id=self.kwargs['projects_pk']).first()
                )
                contributor.save()
                return Response()
            return Response(data={'error': 'User does not exist !'})
        except IntegrityError:
            return Response(data={'error': 'User already added !'})

class IssueViewset(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IssuePermission]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['projects_pk'])

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data["author"] = request.user.pk
        if not request.data['assignee']:
            request.data['assignee'] = request.user.pk
        request.data["project"] = self.kwargs['projects_pk']
        request.data._mutable = False
        return super().create(request, *args, **kwargs)

class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermission]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issues_pk'])

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['issue'] = self.kwargs['issues_pk']
        request.data['author'] = request.user.pk
        request.data._mutable = False
        return super().create(request, *args, **kwargs)