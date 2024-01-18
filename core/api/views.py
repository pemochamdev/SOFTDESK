from core.api import serializers as seria_api
from core.models import Project, Contributor,Comment,Issues

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from core.api import permissions as permis_api



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = seria_api.ProjectSerializer
    permission_classes = [permis_api.IsProjectAuthor]
    

    def get_queryset(self):
        contributors = [project.contributor.through.objects.all() for project in self.queryset]

        contributors_project = []
        for contributor in contributors:
            for instance in contributor:
                if instance.user == self.request.user:
                    contributors_project.append(instance.project.id)
        return Project.objects.filter(id__in = contributors_project) | Project.objects.filter(author=self.request.user)


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = seria_api.ProjectSerializer
    permission_classes = [permis_api.IsProjectAuthor]

        
    


class AddContributorsToProjectView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = seria_api.ProjectSerializer


    def update(self, request, *args, **kwargs):
        project = self.get_object()
        contributor_id = request.data.get('contributor_id')
        contributor = Contributor.objects.get(pk = contributor_id)
        project.contributor.add(contributor)
        serializer = self.get_serializer(project)
        
        return Response(serializer.data)
    


class CreateCommentView(generics.CreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = seria_api.CommentSerializer

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(pk = project_id)
        serializer.save(project=project)



class DeleteProjectView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = seria_api.ProjectSerializer
    permission_classes = [permis_api.IsProjectAuthor]


class DeleteCommentView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = seria_api.ProjectSerializer
    permission_classes = [permis_api.IsCommentAuthor]