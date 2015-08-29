from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


from .mixins import DynamicModelMixin
from .forms import CreateTableForm


class CreateTableView(DynamicModelMixin, TemplateView):
    """ Class based view that will automatically creates
        db table
    """
    template_name = 'create_db.html'
    context = {}

    def get(self, *args, **kwargs):
        self.context['form'] = CreateTableForm()

        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        data = self.request.POST

        form = CreateTableForm(data)
        if form.is_valid():
            ## FIELDS
            # get the fields data from the request
            raw_fields = form.cleaned_data.get('fields')
            # convert to list and define field types.
            # in this case we will set all fields to
            # textfield because i am lazy!.
            fields = self.define_fields(raw_fields.split(','))

            ## DYNAMIC MODEL
            # define dynamic model
            model_name = form.cleaned_data.get('model_name')
            model = self.get_model(str(model_name), fields)

            ## CREATE DB TABLE
            self.create_db_table(model)

            ## STORE DYNAMIC MODEL NAME
            # NOTE: this is a hack because i can't make
            # registering models to admin dynamically.. working
            # :( :( not enough time!
            self.remember_model(model_name, fields)

            return HttpResponseRedirect(reverse('create_table'))

        else:
            self.context['form'] = form
            return render(self.request, self.template_name, self.context)