from django.db import models
from .mixins import DynamicModelMixin


class DynamicModel(DynamicModelMixin, models.Model):

    model_name = models.CharField(max_length=200)
    fields = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.model_name)

    def model(self):
        fields = self.define_fields(self.get_fields())
        return self.get_model(str(self.model_name), fields)

    def get_fields(self):
        return self.fields.split(',')