from django.urls import path

from orders.views import ChartAPIView, ExportAPIView, OrderGenericAPIView

urlpatterns = [
    path('orders', OrderGenericAPIView.as_view()),
    path('orders/<str:pk>', OrderGenericAPIView.as_view()),
    path('export', ExportAPIView.as_view()),
    path('chart', ChartAPIView.as_view()),
]