from rest_framework import serializers

from core.models import Project, Comment, Contributor, Issues



class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
      model = Contributor
      fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):

   class Meta:
      model = Comment
      fields = "__all__"




class ProjectSerializer(serializers.ModelSerializer):

   author = serializers.ReadOnlyField(source='author.username')
   class Meta:
      model = Project
    #    fields = "__all__"
      exclude = ['slug']
   

   def get_contributors(self, obj):
      pass




class IssuesSerializer(serializers.ModelSerializer):
    
   user = serializers.ReadOnlyField(source='user.username')


   class Meta:
      model = Issues
    #    fields = "__all__"
      exclude = ['slug']
