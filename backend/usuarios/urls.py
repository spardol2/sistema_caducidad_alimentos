from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegistroUsuarioView


urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
]