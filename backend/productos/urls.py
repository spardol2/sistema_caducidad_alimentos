from django.urls import path

from .views import (
    BuscarProductoPorCodigoView,
    CategoriaDetailView,
    CategoriaListCreateView,
    InventarioDetailView,
    InventarioListCreateView,
    InventarioProximoVencimientoView,
    ProductoCodigoListCreateView,
    ProductoDetailView,
    ProductoListCreateView,
)


urlpatterns = [
    # Categorías
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

    # Búsqueda por código
    path(
        'buscar-codigo/',
        BuscarProductoPorCodigoView.as_view(),
        name='buscar-producto-codigo'
    ),

    # Inventario
    path(
        'inventario/',
        InventarioListCreateView.as_view(),
        name='inventario-list-create'
    ),
    path(
        'inventario/proximos-vencer/',
        InventarioProximoVencimientoView.as_view(),
        name='inventario-proximos-vencer'
    ),
    path(
        'inventario/<int:pk>/',
        InventarioDetailView.as_view(),
        name='inventario-detail'
    ),

    # Códigos de productos
    path(
        '<int:producto_id>/codigos/',
        ProductoCodigoListCreateView.as_view(),
        name='producto-codigo-list-create'
    ),

    # Productos
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