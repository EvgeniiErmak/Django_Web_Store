from django.urls import path
from .views import product_detail
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('contacts/submit/', views.submit_feedback, name='submit_feedback'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]
