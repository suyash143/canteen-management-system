from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('inventory', views.inventory, name='inventory'),
    path('inventory_add', views.inventory_add, name='inventory_add'),
    path('logout', views.logout, name='logout'),
    path('dashboard_inventory', views.dashboard_inventory, name='dashboard_inventory'),
    path('dashboard_inventory_edit', views.dashboard_inventory_edit, name='dashboard_inventory_edit'),
    path('dashboard_inventory_add', views.dashboard_inventory_add, name='dashboard_inventory_add'),
    path('dashboard_inventory_delete', views.dashboard_inventory_delete, name='dashboard_inventory_delete'),

]
