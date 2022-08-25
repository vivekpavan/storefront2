from cgitb import lookup
from xml.etree.ElementInclude import include
from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename = 'products')
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)

products_router = routers.NestedDefaultRouter(router,'products',lookup = 'product')
products_router.register('reviews',views.ReviewViewSet,basename = 'product-reviews')

carts_router = routers.NestedDefaultRouter(router,'carts',lookup = 'cart')
carts_router.register('items',views.CartItemViewSet,basename='cart-items')
# URLConf
urlpatterns = router.urls + products_router.urls  + carts_router.urls