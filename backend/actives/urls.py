from django.urls import path
from . import views

urlpatterns = [
    path('active/', views.save_active),
    path('active/timeline/<int:user_pk>/', views.get_my_timelines),
    path('active/detail/<int:active_pk>/', views.get_active_detail_info),
    path('active/analysis/<int:user_pk>/<str:search_type>/<str:start_date>/<str:end_date>/', views.get_my_active),
]