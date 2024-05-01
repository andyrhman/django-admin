import traceback
from decouple import config
from django.core.files.storage import default_storage
from rest_framework import exceptions, generics, mixins, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin.pagination import CustomPagination
from products.models import Product
from products.serializers import ProductSerializer
from users.authentication import JWTAuthentication

# Create your views here.
class ProductGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin,
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    
    queryset = Product.objects.all().order_by("-updated_at")
    serializer_class = ProductSerializer
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
    
    def post(self, request):
        try:
            return Response(self.create(request).data)
        except exceptions.ValidationError as e:
            # Generate a more user-friendly message that includes the field name
            errors = {key: value[0] for key, value in e.detail.items()}
            first_field = next(iter(errors))
            field_name = first_field.replace('_', ' ').capitalize()
            if 'required' in errors[first_field]:
                message = f"{field_name} is required."
            else:
                message = f"{field_name} error: {errors[first_field]}"
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            if config('DEBUG', cast=bool):
                traceback.print_exc()
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        try:
            return Response(self.partial_update(request, pk).data, status=status.HTTP_202_ACCEPTED)
        except Exception:
            if config('DEBUG', cast=bool):
                traceback.print_exc()
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            return Response(self.destroy(request, pk).data, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            if config('DEBUG', cast=bool):
                traceback.print_exc()
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)
    
class FileUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    parser_classes = (MultiPartParser,)   
    
    def post(self, request):
        file = request.FILES['image']
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)
        
        return Response({"url": "http://localhost:8000/api" + url})
    
    