from django.urls import path

from .views import CompraDetailView, CompraListCreateView


urlpatterns = [
    path(
        '',
        CompraListCreateView.as_view(),
        name='compra-list-create'
    ),
    path(
        '<int:pk>/',
        CompraDetailView.as_view(),
        name='compra-detail'
    ),
]