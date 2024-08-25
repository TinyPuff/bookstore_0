from django.urls import path
from .views import OrdersPageView, go_to_gateway_view, callback_gateway_view


urlpatterns = [
    path('', OrdersPageView.as_view(), name='orders'),
    # path('go-to-gateway/', go_to_gateway_view, name='gtg'),
    # path('callback-gateway/', callback_gateway_view, name='callback-gateway'),
]