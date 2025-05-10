from rest_framework import routers
from .views import *

urlpatterns = [

]

router = routers.SimpleRouter()
router.register(r'clothes', ClothesViewSet, basename='clothes')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'pos_orders', PosOrderViewSet, basename='pos-order')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'collections', CollectionViewSet, basename='collection')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'cart_items', CartItemViewSet, basename='cart-item')

urlpatterns += router.urls
