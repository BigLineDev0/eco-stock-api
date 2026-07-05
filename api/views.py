from rest_framework.viewsets import ModelViewSet
from api.serializers import MoveProductSerializer, ProductSerializer, WarehouseSerializer
from api.models import Product, Warehouse

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

class WarehouseViewSet(ModelViewSet):
    """
    ViewSet pour gérer les entrepôts.
    """
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=["get"])
    def audit(self, request, pk=None):
        """
        Retourne le nombre total de produits présents dans un entrepôt.
        """

        warehouse = self.get_object()
        
        total_products =  warehouse.products.count()
        
        return Response(
            {
                "warehouse": warehouse.name,
                "location": warehouse.location,
                "capacity": warehouse.capacity,
                "total_products": total_products,
            },
            status=status.HTTP_200_OK,
        )
        
class ProductViewSet(ModelViewSet):
    """
    ViewSet pour gérer les produits.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =  [IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=["post"])
    def move(self, request, pk=None):
        """
        Déplacer un produit vers un autre entrepôt.
        """

        product = self.get_object()

        # Vérifier si le produit est périmé
        if product.expiration_date < timezone.now().date():
            return Response(
                {
                    "error": "Impossible de déplacer un produit périmé."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        
        serializer = MoveProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        warehouse = serializer.validated_data["warehouse"]

        product.warehouse = warehouse
        product.save()

        return Response(
            {
                "message": "Produit déplacé avec succès.",
                "product": product.name,
                "new_warehouse": warehouse.name,
            },
            status=status.HTTP_200_OK,
        )