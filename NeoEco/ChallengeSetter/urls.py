from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quests/transport", views.decideTransportOperation, name="decideTransportOperation"),
    path("quests/volunteer", views.search_opportunities, name="search_opportunities"),
    path("quests/complete_quest", views.complete_quest, name="complete_quests"),
    path("user/register", views.register_user, name="register_user"),
    path("user/login", views.user_login, name="user_login"),
    path("user/group", views.addFriend, name="addFriend"),
    path("user/friends", views.getFriends, name="getFriends")
]