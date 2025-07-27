from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import School, MUNDirector, Delegate, Advisor

class ReadOnly(BasePermission):
    '''
    Read-only permission.
    '''
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class ParticipantAccess(BasePermission):
    '''
    Grants access to a participant's data if:
    1. the requesting user is authenticated and the participant themselves (authenticated via token)
    2. the requesting user is authenticated (not necessarily the participant themselves) and there is no personal data stored in the participant's object yet (checked by data_consent_time). If personal data is stored, the viewset should send a passwordless token to the participant's email address to authenticate them.

    Allows creating new Advisor objects.

    Denies access if the method is DELETE or the user is not authenticated.
    '''

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False  # Only allow authenticated requests 
        
        if request.method == "DELETE":
            return False # Deny DELETE requests
        
        # Restrict creation to Advisor objects only
        if request.method == "POST":
            model_class = getattr(getattr(view, 'queryset', None), 'model', None)
            if model_class != Advisor:
                return False
            
        return True

    def has_object_permission(self, request, view, obj):
        # Allow participant's own user to access/change their data
        if request.user == obj.user and request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH']:
            return True

        # Allow other authenticated users to access non-personal data
        if request.method in SAFE_METHODS:
            return True # Further checks will be done in the viewset
        
        # Deny access for all other cases
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
            # is_staff is set to True for organizers in the authentication process in AzureADJWTAuthentication
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