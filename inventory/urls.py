from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('billing/', views.billing, name='billing'),
    path('export/', views.export_csv, name='export_csv'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('billing/edit/<int:bill_id>/', views.edit_bill, name='edit_bill'),
    path('billing/delete/<int:bill_id>/', views.delete_bill, name='delete_bill'),
 

]
