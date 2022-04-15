from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Component, Favorite, Ingredient, Purchase, Recipe,
                            Tag)
from recipes.serializers.component import IngredientSerializer
from recipes.serializers.tag import TagSerializer
from rest_framework import serializers
from users.serializers.user import CustomUserSerializer


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    ingredients = IngredientSerializer(many=True, source="component")
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time"
        )

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Purchase.objects.filter(user=user, recipe=obj).exists()
        return False

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("component")
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            amount = ingredient.pop("amount")
            id = ingredient.pop("ingredient")["id"]
            ingredient = get_object_or_404(Ingredient, id=id)
            Component.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount)
        return recipe

    def update(self, instance, validated_data, partial=True):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("component")
        for tag in instance.tags.all():
            if tag not in tags:
                instance.tags.remove(tag)
            else:
                tags.remove(tag)
        if tags:
            for tag in tags:
                instance.tags.add(tag)
        components = []
        for ingredient in ingredients:
            amount = ingredient.pop("amount")
            ingredient = get_object_or_404(
                Ingredient, id=ingredient.pop("ingredient")["id"])
            component, _ = Component.objects.get_or_create(
                ingredient=ingredient, recipe=instance, amount=amount)
            components.append(component)
        for component in instance.component.all():
            if component not in components:
                component.delete()
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time)
        instance.image = validated_data.get("image", instance.image)
        return instance

    def to_representation(self, obj):
        self.fields["tags"] = TagSerializer(many=True)
        return super().to_representation(obj)
