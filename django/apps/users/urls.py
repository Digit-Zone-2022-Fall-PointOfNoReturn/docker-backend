from django.urls import path

from .views import users, user


urlpatterns = [
    path('', users),
    path('<int:id>', user)
]
