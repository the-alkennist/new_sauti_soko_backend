from rest_framework import permissions, viewsets, status
from rest_framework.response import Response


from products.models import Product, ProductCategory
from products.permissions import IsSellerOrAdmin
from products.serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
)


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product categories
    """

    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = (permissions.AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD products
    """

    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return ProductWriteSerializer

        return ProductReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            # self.permission_classes = (permissions.IsAuthenticated,)
            self.permission_classes = (permissions.AllowAny,)
        elif self.action in ("update", "partial_update", "destroy"):
            # self.permission_classes = (IsSellerOrAdmin,)
            self.permission_classes = (permissions.AllowAny,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        # Get product name from request data
        product_name = request.data.get('name')

        # Check if a product with the given name already exists
        existing_product = Product.objects.filter(name=product_name).first()
        if existing_product:
            return Response({'detail': 'Product with this name already exists.', 'id': existing_product.id}, status=status.HTTP_400_BAD_REQUEST)
        # If product with the given name doesn't exist, proceed with creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # If product with the given name doesn't exist, proceed with creation
        return super().create(request, *args, **kwargs)