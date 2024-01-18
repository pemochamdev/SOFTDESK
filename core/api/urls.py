from django.urls import path,include

from rest_framework import routers

from core.api import views

router  = routers.SimpleRouter()
router.register('project', views.ProjectViewSet, basename='projects')

urlpatterns = [
    # path('', views.ProjectViewSet.as_view(), name='project-list'),
    path('', include(router.urls)),
    path('project/<pk>/', views.ProjectDetailAPIView.as_view(), name='project-list'),
    path('<pk>/add-contributors/', views.AddContributorsToProjectView.as_view(), name='add-contributors'),
    path('<pk>/delete-comment/', views.DeleteCommentView.as_view(), name='delete-comment'),
    path('<pk>/delete-project/', views.DeleteProjectView.as_view(), name='delete-project'),
    path('<project_id>/comment/', views.CreateCommentView.as_view(), name='create-comment'),
]
