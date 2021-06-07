from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('inventory', views.inventory, name='inventory'),
    path('inventory_add', views.inventory_add, name='inventory_add'),
    path('logout', views.logout, name='logout'),
    path('dashboard_inventory', views.dashboard_inventory, name='dashboard_inventory'),
    path('dashboard_inventory_edit', views.dashboard_inventory_edit, name='dashboard_inventory_edit'),
    path('dashboard_inventory_add', views.dashboard_inventory_add, name='dashboard_inventory_add'),
    path('dashboard_inventory_delete', views.dashboard_inventory_delete, name='dashboard_inventory_delete'),
    path('dashboard_create_order',views.dashboard_create_order,name='dashboard_create_order'),
    path('inventory_search',views.inventory_search,name='inventory_search'),
    path('pdf_download',views.pdf_download,name='pdf_download')

]
