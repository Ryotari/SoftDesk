from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from projects.models import Project, Contributor
from projects.serializers import (ProjectListSerializer,
                                ProjectDetailSerializer,
                                ContributorSerializer)
from projects.permissions import IsAuthor

class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        projects_ids = [contributor.project.id for contributor in Contributor.objects.filter(user=self.request.user).all()]
        return Project.objects.filter(id__in=projects_ids)

    def get_serializer_class(self):
        if self.action == 'retrieve':
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

class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        contributor_ids = [contributor.user.id for contributor in Contributor.objects.filter(project=self.kwargs['projects'])]
        return User.objects.filter(id__in=contributor_ids)