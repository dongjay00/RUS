from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:user_pk>/', views.get_user_info),
    path('user/<str:account_email>/', views.is_user_in_db),
    path('user/', views.save_user_to_db),
    path('group/my/<int:user_pk>/', views.get_my_groups),
    path('group/list/<int:user_pk>/', views.get_all_groups),
    path('group/<int:group_pk>/', views.get_update_delete_group_info),
    path('group/member/<int:group_pk>/', views.get_group_members),
    path('group/member/count/<int:group_pk>/', views.get_group_member_count),
    path('group/create/<int:user_pk>/', views.create_group),
    path('group/image/', views.upload_group_image),
    path('group/member/<int:user_pk>/<int:group_pk>/', views.participate_leave_group),
]