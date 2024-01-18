from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
TYPES_CHOICES = (
    ("back-end", 'BACKEND'),
    ("front-end", 'FRONTEND'),
    ("ios", 'IOS'),
    ("android", 'ANDROID'),
)

PRIORITY_CHOICES = (
    ('low', 'LOW'),
    ('medium', 'MEDIUM'),
    ('high', 'HIGH'),
)

TAGS_CHOICES = (
    ('bug', "BUG"),
    ('improvement', "IMPROVEMENT"),
    ('task', "TASK"),
)

STATUS_CHOICES = (
    ('todo', 'TODO'),
    ('wip', 'WIP'),
    ('done', 'DONE'),
)

ROLE_CHOICES = (
    ('author','AUTHOR'),
    ('admin', 'ADMIN'),
)

PERMISSION_CHOICES = (
    ('read', 'READ'),
    ('contributor', 'CONTRIBUTOR')
)


class Project(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'project_author')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    type = models.CharField(max_length = 20, choices = TYPES_CHOICES)
    description = models.TextField()
    contributor = models.ManyToManyField(settings.AUTH_USER_MODEL, through='contributor')
    created_at = models.DateTimeField(auto_now_add = True)
    
    
    class Meta:
        ordering = ("-created_at",)

    
    
    def __str__(self):
        return f"{self.title} by {self.author}"

    
    
    # def save(self,  *args, **kwargs):
    #     if self.title:
    #         self.slug = slugify(self.title)



class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'project_contributor')
    permission = models.CharField(max_length  =12, choices = PERMISSION_CHOICES)
    role = models.CharField(max_length  =12, choices = ROLE_CHOICES)
    
    


class Issues(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    
    date_created = models.DateTimeField(auto_now_add = True)
    priority = models.CharField(max_length  =12, choices = PRIORITY_CHOICES)
    tag = models.CharField(max_length  =12, choices = TAGS_CHOICES)
    status = models.CharField(max_length  =12, choices = STATUS_CHOICES)
    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'project_issues')
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,related_name = 'issue_author' )
    assignee_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,related_name = 'issue_assignee_user' )



class Comment(models.Model):
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,related_name = 'comment_author' )
    issue = models.ForeignKey(Issues, on_delete = models.CASCADE, related_name = "comment")
    