from django.urls import path

from .views import stores, store, products, product


urlpatterns = [
    path('', stores),
    path('<uuid:id>', store),
    
    path('<uuid:store>/products/', products),
    path('<uuid:store>/products/<uuid:id>', product)
]
