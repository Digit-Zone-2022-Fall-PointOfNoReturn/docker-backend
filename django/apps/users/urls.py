from django.urls import path

from .views import users, user


urlpatterns = [
    path('', users),
    path('<uuid:id>', user)
]
