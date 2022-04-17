from django.db import transaction
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

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                "Рецепт не может быть без тегов."
            )

        unique_tags = set(tags)
        if len(unique_tags) != len(tags):
            raise serializers.ValidationError(
                "Теги не должны повторяться."
            )
        return tags

    def validate_ingredients(self, components):
        if not components:
            raise serializers.ValidationError(
                "Рецепт не может быть без ингредиентов."
            )
        ingredients = [
            component["ingredient"]["id"]
            for component in components
        ]
        if len(ingredients) != len(set(ingredients)):
            raise serializers.ValidationError(
                "Каждый ингредиент в рецепте должен быть уникальным."
            )
        return components

    def validate_name(self, name):
        if self.context["request"].method != "PATCH":
            author = self.context["request"].user
            if Recipe.objects.filter(author=author, name=name).exists():
                raise serializers.ValidationError(
                    "У вас уже есть рецепт с таким названием."
                )
        return name

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

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("component")
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        components = []
        for ingredient in ingredients:
            amount = ingredient.pop("amount")
            id = ingredient.pop("ingredient")["id"]
            ingredient = get_object_or_404(Ingredient, id=id)
            component = Component(
                recipe=recipe, ingredient=ingredient, amount=amount)
            components.append(component)
        Component.objects.bulk_create(components)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data, partial=True):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("component")
        instance.tags.set(tags)
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
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def to_representation(self, obj):
        self.fields["tags"] = TagSerializer(many=True)
        return super().to_representation(obj)
