from import_export import resources
from .models import AddressBook

class AddressResource(resources.ModelResource):
    class Meta:
        model = AddressBook