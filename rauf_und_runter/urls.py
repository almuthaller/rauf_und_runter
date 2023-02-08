from django.contrib import admin
from django.urls import path
from game import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("register", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("create_room", views.create_room, name="create_room"),
    path("create_rauf", views.create_rauf, name="create_rauf"),
    path("create_runter", views.create_runter, name="create_runter"),
    path("game", views.game, name="game"),
    path("changes", views.changes, name="changes"),
]
