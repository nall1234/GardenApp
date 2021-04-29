from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('main', views.main),
    path('profile/<int:current_user>', views.profile, name="profile"),
    path('update/<int:current_user>', views.update, name="update"),
    #-----MARKETPLACE-----
    path('market', views.market),
    path('market/create', views.create_item),
    path('market/<int:item_id>', views.one_item),
    path('market/<int:item_id>/edit', views.edit_item),
    path('market/<int:item_id>/update', views.update_item),
    path('market/<int:item_id>/delete', views.delete_item),
    path('market/cart', views.my_cart),
    path('market/<int:item_id>/add', views.add_cart),
    path('market/<int:item_id>/remove', views.remove_cart),
    path('market/checkout', views.checkout),
]