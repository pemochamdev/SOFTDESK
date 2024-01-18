from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.IsAuthenticatedOrReadOnly):


    def has_permission(self, request, view):

        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsProjectAuthor(permissions.BasePermission):
    
    message = 'pas authoriser'
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            
            return bool(request.user == obj.author)


class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user



class IsContributorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        
        # Verifie s le user est un contributeur du project associe a l'object
        if request.method in permissions.SAFE_METHODS:
            # Les users peuvent voir 
            return True
        # Verifie si le user est un contributeur du project
        return obj.contributors.filter(id = request.user.id).exists()