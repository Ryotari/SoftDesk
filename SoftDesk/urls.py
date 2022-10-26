"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import SignupView
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from projects.views import ProjectViewset, ContributorViewset, IssueViewset, CommentViewset

router = routers.SimpleRouter()
router.register(r'projects/?', ProjectViewset, basename='projects')

users_router = routers.NestedSimpleRouter(router, r'projects/?', lookup='projects')
users_router.register(r'users/?', ContributorViewset, basename='users')

issues_router = routers.NestedSimpleRouter(router, r'projects/?', lookup='projects')
issues_router.register(r'issues/?', IssueViewset, basename='issues')

comments_router = routers.NestedSimpleRouter(issues_router, r'issues/?', lookup='issues')
comments_router.register(r'comments/?', CommentViewset, basename='comments')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('api/', include(router.urls)),
    path('api/', include(users_router.urls)),
    path('api/', include(issues_router.urls)),
    path('api/', include(comments_router.urls))
]
