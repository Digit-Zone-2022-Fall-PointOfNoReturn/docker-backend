from django.urls import path

from .views import user


urlpatterns = [
    path('<int:id>', user)
]
