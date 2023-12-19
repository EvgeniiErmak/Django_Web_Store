from django.urls import path
from .views import product_detail
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('contacts/submit/', views.submit_feedback, name='submit_feedback'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)