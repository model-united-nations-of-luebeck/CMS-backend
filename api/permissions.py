from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import School, MUNDirector, Delegate

class ReadOnly(BasePermission):
    '''
    Read-only permission.
    '''
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class IsParticipantThemself(BasePermission):
    '''
    Permission for participants to access their own data.
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH']:
            return hasattr(request.user, 'participant') and request.user.participant is not None
        return False

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'participant') and request.user.participant is not None:
            return obj == request.user.participant
        return False

class BelongsToSchool(BasePermission):
    '''
    Permission for schools to 
        - read and change data of their own school
        - read and change data of their delegates
        - read data of their MUN directors, add new ones and delete them
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return hasattr(request.user, 'school') and request.user.school is not None
        return False

    def has_object_permission(self, request, view, obj):
        # if the user is authenticated and has a school, check permissions based on the object type
        if hasattr(request.user, 'school') and request.user.school is not None:

            # if the object is a school, check if it matches the user's school
            if isinstance(obj, School):
                if request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH']:
                    return obj == request.user.school
                
            # if the object is a delegate, check if it belongs to the user's school
            elif isinstance(obj, Delegate):
                if request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH']:
                    return obj.school == request.user.school
            
            # if the object is an MUN Director, check if it belongs to the user's school
            elif isinstance(obj, MUNDirector):
                if request.method in ['GET', 'HEAD', 'OPTIONS', 'POST', 'DELETE']:
                    return obj.school == request.user.school
                
        # if the user is not authenticated or does not have a school, deny access
        return False
    
class IsOrganizer(BasePermission):
    '''
    Permission for organizers to access all data.
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            # TODO: Set organizer is_staff to True when authenticating
            return True
        return False

class IsAdmin(BasePermission):
    '''
    Permission for admins to access all data and manipulate users.
    '''
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False