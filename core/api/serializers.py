from rest_framework import serializers

from core.models import Project, Comment, Contributor, Issues



class ContributorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
      model = Contributor
      fields = "__all__"


class CommentSerializer(serializers.HyperlinkedModelSerializer):

   class Meta:
      model = Comment
      fields = "__all__"




class ProjectSerializer(serializers.HyperlinkedModelSerializer):

   author = serializers.ReadOnlyField(source='author.username')
   contributors = serializers.SerializerMethodField(read_only=True)
   issues = serializers.SerializerMethodField(read_only=True)
   comment = serializers.SerializerMethodField(read_only=True)

   class Meta:
      model = Project
      fields = ('id', 'author','title', 'description','type', 'contributors', 'comment', 'issues')
      
   

   def get_contributors(self, obj):
      contributors = list(
         contributor.email for contributor in obj.contributors.get_queryset().only('email')
      )
      return contributors

   def get_comment(self, obj):
      projects = list(

         project.description for project in obj.project.get_queryset().only('description')
      )
      return projects
   

   def get_issues(self, obj):
      issues = list(
         issue.title for issue in obj.project_issues.get_queryset().only('title')
      )
      return issues
   

class IssuesSerializer(serializers.HyperlinkedModelSerializer):
    
   user = serializers.ReadOnlyField(source='user.username')


   class Meta:
      model = Issues
    #    fields = "__all__"
      exclude = ['slug']
