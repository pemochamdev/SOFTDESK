from django.contrib import admin

# Register your models here.
from core.models import Project, Contributor, Comment, Issues

# admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Contributor)
admin.site.register(Issues)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title", )}
    list_display = ('title', 'author')
    
