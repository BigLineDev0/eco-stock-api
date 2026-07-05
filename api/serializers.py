from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api.models import Product, Warehouse

class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location', 'capacity']
        read_only_fields = ['id']
        
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'expiration_date', 'status', 'warehouse']
        read_only_fields = ['id']
        
        
class MoveProductSerializer(serializers.Serializer):
    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all()
    )

    def validate_warehouse(self, warehouse):
        if warehouse.products.count() >= warehouse.capacity:
            raise serializers.ValidationError(
                "Cet entrepôt est plein."
            )
        return warehouse