from django.urls import path

from .views import (
    groups,
    group,
    group_store,
    group_store_carts,
    group_collecting_start,
    group_collecting_stop,
    group_collecting_drop,
    group_users,
    group_user,
    user_cart,
    cart_product
)


urlpatterns = [
    path('', groups),
    path('<uuid:id>', group),
    path('<uuid:group>/stores/<uuid:store>', group_store),
    path('<uuid:group>/stores/<uuid:store>/carts', group_store_carts),
    path('<uuid:group>/stores/drop', group_collecting_drop),
    path('<uuid:group>/stores/start', group_collecting_start),
    path('<uuid:group>/stores/stop', group_collecting_stop),
    path('<uuid:group>/users', group_users),
    path('<uuid:group>/users/<int:user>', group_user),
    path('<uuid:group>/users/<int:user>/stores/<uuid:store>/cart', user_cart),
    path('<uuid:group>/users/<int:user>/stores/<uuid:store>/products/<uuid:product>/cart', cart_product),
]
