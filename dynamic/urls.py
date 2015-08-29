from django.conf.urls import include, url
from .views import CreateTableView

urlpatterns = [
    url(r'^create/$', CreateTableView.as_view(), name="create_table"),
]