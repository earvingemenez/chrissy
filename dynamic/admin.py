from django.contrib import admin
from .models import DynamicModel

## register static models
admin.site.register(DynamicModel)


## Register dynamic models
dmodels = DynamicModel.objects.all()

for model in dmodels:
    try:
        admin.site.register(model.model())
    except Exception as e:
        ## hide the error. this is a hack!
        # register models to admin dynamically
        # not this way.
        pass