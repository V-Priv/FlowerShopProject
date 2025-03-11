from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import CustomLoginView  # Изменено на CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Изменено на CustomLoginView
    path('register/', views.register, name='register'),
    path('order/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),  # Исправлен синтаксис
    path('order/<int:order_id>/confirm/', views.confirm_order, name='confirm_order'),  # Исправлен синтаксис
    path('order/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)