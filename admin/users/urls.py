from django.urls import path

from .views import redirect_admin

urlpatterns = [
    path('', redirect_admin, name='redirect_admin'),
]
