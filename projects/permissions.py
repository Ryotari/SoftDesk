from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404
from projects.models import Project, Contributor

"""class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, project):

        return bool(request.user.id == project.author.id)

class IsContributor(BasePermission):

    def has_object_permission(self, request, view, project):
        for contributor in Contributor.objects.filter(project=project.id):
            if request.user.id == contributor.user.id:
                return True
        return False

class DeleteAndUpdate(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return True
        elif view.action in ['update', 'partial_update', 'destroy']:
            return bool(request.user.id == obj.author.id)"""

def is_contributor(user, project):

    for contributor in Contributor.objects.filter(project=project.id):
        if user.id == contributor.user.id:
            return True
    return False

class ProjectPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return bool(is_contributor(request.user, obj))
        elif view.action in ['update', 'partial_update', 'destroy']:
            return bool(request.user == obj.author)

class ContributorPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return is_contributor(request.user, Project.objects.filter(id=view.kwargs['projects_pk']).first())

        elif view.action in ['update', 'partial_update', 'create', 'destroy']:
            return request.user == Project.objects.filter(id=view.kwargs['projects_pk']).first().author

class IssuePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list', 'create']:
            return is_contributor(request.user, obj.project)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author

class CommentPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list', 'create']:
            return is_contributor(request.user, obj.issue.project)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author