from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create_ad/', views.add_notice_view, name='create_ad'),
    path('filter/', views.filter_form, name='filter_post'),  # здесь filter_post
    path('filter/results/', views.filter_result, name='filter_result'),
    path('detail/<int:notice_id>/', views.detail, name='detail'),
]