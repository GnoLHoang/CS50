from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path('sortCate/', views.sortCate, name="sortCate"),
    path("detail/<int:id>", views.detail, name="detail"),
    path("removeFrom/<int:id>", views.removeFrom, name="removeFrom"),
    path("addTo/<int:id>", views.addTo, name="addTo"),
    path("bid/<int:id>", views.bid, name='bid'),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("addComment/<int:id>", views.comment, name="comment"),
    path("close/<int:id>", views.close, name="close"),
]
