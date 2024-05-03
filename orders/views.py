import csv
import traceback
from django.http import HttpResponse
from requests import get
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decouple import config
from rest_framework.views import APIView
from admin.pagination import CustomPagination
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from users.authentication import JWTAuthentication

# Create your views here.
class OrderGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    
    queryset = Order.objects.all().order_by('-updated_at')
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        try:
            if pk:
                return Response(self.retrieve(request, pk).data)
            
            return Response(self.list(request).data)
        except Exception:
            if config('DEBUG', cast=bool):
                traceback.print_exc()
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
    
class ExportAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    
        
    def post(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=orders.csv"
        
        orders = Order.objects.all()
        writer = csv.writer(response)
        
        writer.writerow(["ID", "Name", "Email", "Product Title", "Price", "Quantity"])
        
        for order in orders:
            writer.writerow([order.id, order.name, order.email, "", "", ""])
            orderItems = OrderItem.objects.all()
            
            for item in orderItems:
                writer.writerow(["", "", "", item.product_title, item.price, item.quantity])
        
        return response 
        
        
        