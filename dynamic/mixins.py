from django.contrib import admin
from django.db import models

from django.core.management import sql, color
from django.db import connection


class DatabaseMixin(object):
    """ Mixin class which contains methods that
        communicates to the db and creates db tables
        based on the model(dynamic model) specified.
    """
    def __init__(self, *args, **kwargs):
        return super(DatabaseMixin, self).__init__(*args, **kwargs)

    def create_db_table(self, model):
        """ Method that generates the sql schema and
            automatically creates the table in the db
        """
        ## STYLES
        # set the terminal colors in the sql statements
        style_ = color.no_style()

        # SEEN MODELS
        # list of existing models. this can be used
        # to prevent creating duplicate DB tables.
        seen_models = []

        with connection.cursor() as cursor:
            statements, ref = connection.creation.sql_create_model(
                model, style_, seen_models)

            # Execute table creation
            for statement in statements:
                cursor.execute(statement)

    def delete_db_table(self, model):
        """ Method that deletes the db table created
            based from the specified dynamic model.
        """
        ## TABLE INFO
        db_table = model._meta.db_table

        ## STYLES
        # set the terminal colors in the sql statements
        style_ = color.no_style()

        # REFERENCE MODELS
        # list of existing models. this can be used
        # to prevent deleting duplicate DB tables.
        reference_models = []

        with connection.cursor() as cursor:
            statements = connection.sql_destroy_model(model, reference_models, style_)

            for statement in statements:
                cursor.execute(statement) 


class DynamicModelMixin(DatabaseMixin):
    """ Mixin class which contains methods that
        is used to create/set dynamic models
    """
    def __init__(self, *args, **kwargs):
        return super(DynamicModelMixin, self).__init__(*args, **kwargs)

    def get_model(self, model_name, fields, meta_=None):
        """ Method that generates the model
        """
        ## SET META CLASS
        # define the meta class. using type('Meta', ...)
        # gives a dictproxy error during model creation
        # so let's just define it.
        class Meta:
            pass

        # meta class options
        if meta_ is not None:
            for key, value in meta_.iteritems():
                setattr(Meta, key, value)

        ## DEFINE APP LABEL
        # we will set the machine app as the app_label.
        # the app_label only serves as a placeholder of
        # our dynamic model to avoid conflict with django's
        # process
        setattr(Meta, 'app_label', 'dynamic')

        ## SET DYNAMIC FIELDS
        # initialize the field dictionary with a `__module__`
        # item to simulate declarations within a class
        module_ = 'dynamic.models'
        attrs = {'__module__': module_, 'Meta': Meta}
        if fields:
            # Add the fields
            attrs.update(fields)

        ## SET DYNAMIC MODEL CLASS
        # create a model class based on the parameters
        # and attributes given. this automatically
        # triggers ModelBase processing.
        return type(model_name, (models.Model,), attrs)

    def remember_model(self, model_name, fields):
        """ Save the model info to a table.
            this will be used to retrieve the
            dynamic models that has been created.
        """
        from .models import DynamicModel
        ## FIELDS
        # concatinate the field names separated by comma
        # and save it in a textfield.
        fields_ = ",".join(fields)
        
        return DynamicModel.objects.create(
            model_name=model_name, fields=fields_)


    def register_to_admin(self, model):
        """ Method that register the dynamic model
            to admin
        """
        ## SET ADMIN
        class Admin(admin.ModelAdmin):
            pass

        # this is equivalent to `class Admin(): pass`
        admin_opts = {}
        # set admin options
        for key, value in admin_opts:
            setattr(Admin, key, value)

        # register to admin panel
        admin.site.register(model, Admin)


    def define_fields(self, fields):
        """ Method that returns a dictionary of the
            fields and their property.

            NOTE: used only as an example because i'm lazy
        """
        dict_ = {}
        for field in fields:
            # Right now we will set all fields to be
            # textfield since we want it to be flexible
            dict_[field] = models.TextField(null=True, blank=True)

        return dict_
