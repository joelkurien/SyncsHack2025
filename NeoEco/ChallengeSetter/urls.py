from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quests/transport", views.decideTransportOperation, name="decideTransportOperation")
]