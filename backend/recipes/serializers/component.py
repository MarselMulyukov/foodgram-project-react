from recipes.models import Component
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id", required=True)
    name = serializers.StringRelatedField(
        source="ingredient.name")
    measurement_unit = serializers.StringRelatedField(
        source="ingredient.measurement_unit")

    class Meta:
        model = Component
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )
