from django.urls import path
from . import views

app_name = 'cafe_management'

urlpatterns = [
    path('', views.all_categories, name='all_categories'),
    path('login_worker/', views.login_worker, name="login_worker"),
    path('pay/', views.pay, name="pay"),
    path('update_order/', views.update_order, name='update_order'),
    path('warehouse/', views.warehouse, name='warehouse'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_warehouse/', views.update_warehouse, name='update_warehouse'),
    path('report/', views.report, name='report'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('<slug:category_slug>/', views.product_by_category, name='products_by_category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('delete_product/<slug:slug>/<int:id>/', views.delete_product, name='delete_product'),
]
