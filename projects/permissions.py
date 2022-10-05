from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404
from projects.models import Project

class IsAuthor(BasePermission):

    
    def has_object_permission(self, request, view, project):
        return bool(request.user.id == project.author.id)
