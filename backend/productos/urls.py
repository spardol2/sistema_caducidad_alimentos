from django.urls import path

from .views import (
    BuscarProductoPorCodigoView,
    CategoriaDetailView,
    CategoriaListCreateView,
    ProductoCodigoListCreateView,
    ProductoDetailView,
    ProductoListCreateView,
)


urlpatterns = [
    path(
        'categorias/',
        CategoriaListCreateView.as_view(),
        name='categoria-list-create'
    ),
    path(
        'categorias/<int:pk>/',
        CategoriaDetailView.as_view(),
        name='categoria-detail'
    ),
    path(
        'buscar-codigo/',
        BuscarProductoPorCodigoView.as_view(),
        name='buscar-producto-codigo'
    ),
    path(
        '<int:producto_id>/codigos/',
        ProductoCodigoListCreateView.as_view(),
        name='producto-codigo-list-create'
    ),
    path(
        '',
        ProductoListCreateView.as_view(),
        name='producto-list-create'
    ),
    path(
        '<int:pk>/',
        ProductoDetailView.as_view(),
        name='producto-detail'
    ),
]