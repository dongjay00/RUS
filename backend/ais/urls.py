from django.urls import path
from . import views

urlpatterns = [
    path('ai/image/', views.upload_image),
]