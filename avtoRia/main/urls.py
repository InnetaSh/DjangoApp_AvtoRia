from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create_ad/', views.add_notice_view, name='create_ad'),
    path('filter/', views.filter_form, name='filter_post'),
    path('filter/results/', views.filter_result, name='filter_result'),
    path('detail/<int:notice_id>/', views.detail, name='detail'),
    # path('user_profile', views.user_profile, name='user_profile'),
    path('all/', views.all_notice, name='all_notice'),
    path('my/', views.my_notice, name='my_notice'),
    path('24hour/', views.notice_24hour, name='hour24_notice'),
    path('favorites/', views.favorite_notice, name='favorite_notice'),
    path('favorite/add/<int:notice_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorite/remove/<int:notice_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('edit/<int:notice_id>/', views.edit_notice, name='edit_notice'),
    path('delete/<int:notice_id>/', views.delete_notice, name='delete_notice'),
]
