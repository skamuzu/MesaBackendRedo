# urls.py
from django.urls import path
from .views import ActionListView

urlpatterns = [
    path('api/actions/', ActionListView.as_view(), name='action-list'),
]
