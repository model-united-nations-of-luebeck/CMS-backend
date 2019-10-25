from rest_framework.permissions import DjangoModelPermissions
import copy

class MUNOLDjangoModelPermission(DjangoModelPermissions):
    '''
    Using the DjangoModelPermissions extended by the view action.
    This allows to set the permissions per User or Group in the admin interface manually.
    One can set permissions for single actions (add, change, delete, view) and for single models.
    For further reference see: 
    https://github.com/encode/django-rest-framework/blob/master/rest_framework/permissions.py
    and
    https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions
    '''
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']