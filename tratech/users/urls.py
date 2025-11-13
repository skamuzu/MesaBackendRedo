from django.urls import path
from . import views

urlpatterns = [
    path("webhook", views.clerk_webhook, name="clerk-webhook"),
]
