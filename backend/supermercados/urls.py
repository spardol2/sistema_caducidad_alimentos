from django.urls import path

from .views import (
    SupermercadoDetailView,
    SupermercadoListCreateView,
)


urlpatterns = [
    path(
        '',
        SupermercadoListCreateView.as_view(),
        name='supermercado-list-create'
    ),
    path(
        '<int:pk>/',
        SupermercadoDetailView.as_view(),
        name='supermercado-detail'
    ),
]