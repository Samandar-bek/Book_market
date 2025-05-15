from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('book_model/', views.book_model, name='book_model'),  # book_model sahifasi
    # Reference
    path('reference/', views.reference_view, name='reference'),
    path('reference_create/', views.reference_create, name='reference_create'),
    path('reference_delete/<int:pk>/', views.reference_delete, name='reference_delete'),
    #Product
    path('product/', views.product_list, name='product'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('staff/', views.staff_view, name='staff'),
    path('staff_payment/create/', views.staff_payment_create, name='staff_payment_create'),
    #Output
    path('output/', views.output_list, name='output'),  # Outputlar ro'yxati
    path('output/create/', views.output_create, name='output_create'),  # Yangi Output yaratish
    path('output/edit/<int:pk>/', views.output_edit, name='output_edit'),  # Outputni tahrirlash
    path('output/delete/<int:pk>/', views.output_delete, name='output_delete'),  # Outputni o'chirish
    #Sale
    path('sale/', views.sale_view, name='sale'),
    path('sale/create/', views.sale_create, name='sale_create'),
    path('sale/edit/<int:pk>/', views.sale_edit, name='sale_edit'),
    path('sale/delete/<int:pk>/', views.sale_delete, name='sale_delete'),
    # Hodimlar bo'limi

    path('staff/edit/<int:pk>/', views.staff_edit, name='staff_edit'),
    path('staff/view/', views.staff_view, name='staff_view'),
    path('staff/create/', views.staff_create, name='staff_create'),
    path('staff/work/create/', views.staff_work_create, name='staff_work_create'),
    path('staff/delete/<int:pk>/', views.staff_delete, name='staff_delete'),
    path('staff/work/view/', views.staff_work_view, name='staff_work_list'),
    path('staff/payment/edit/<int:pk>/', views.staff_payment_edit, name='staff_payment_edit'),
    path('staff/payment/delete/<int:pk>/', views.staff_payment_delete, name='staff_payment_delete'),
    # Book_model
    path('book_model_create/', views.book_model_create, name='book_model_create'),
    path('books/delete/<int:pk>/', views.book_model_delete, name='book_model_delete'),
    path('book/edit/<int:pk>/', views.book_model_edit, name='book_model_edit'),
    # Hisobot va foyda hisoblash
    path('income_calc/', views.income_calc_view, name='income_calc'),
    # Login
    path('login/', views.user_login, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
