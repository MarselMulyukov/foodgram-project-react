import io

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas, pdfmetrics
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import Component, Favorite, Ingredient, Purchase, Recipe, Tag
from .permissions import IsOwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeMinifiedSerializer,
                          RecipeSerializer, TagSerializer)

User = get_user_model()


class TagViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    @action(
        ["post", "delete"], detail=True, permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == "POST":
            favorite, created = Favorite.objects.get_or_create(
                recipe=recipe,
                user=user
            )
            if created:
                data = RecipeMinifiedSerializer(instance=recipe).data
                return Response(data, status=status.HTTP_201_CREATED)
            error_message = {"error": "Already in favorites"}
        elif request.method == "DELETE":
            favorite = Favorite.objects.filter(recipe=recipe, user=user)
            if favorite:
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            error_message = {"error": "Was not in favorites"}
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    @action(
        ["post", "delete"], detail=True, permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == "POST":
            purchase, created = Purchase.objects.get_or_create(
                recipe=recipe,
                user=user
            )
            if created:
                data = RecipeMinifiedSerializer(instance=recipe).data
                return Response(data, status=status.HTTP_201_CREATED)
            error_message = {"error": "Already in shopping cart"}
        elif request.method == "DELETE":
            purchase = Purchase.objects.filter(recipe=recipe, user=user)
            if purchase:
                purchase.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            error_message = {"error": "Was not in shopping cart"}
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = Component.objects.filter(
            recipe__is_in_shopping_cart__user=request.user
        ).values(
            "ingredient__name", "ingredient__measurement_unit"
        ).order_by(
            "ingredient__name"
        ).annotate(
            ingredient_total=Sum("amount")
        )
        return self.canvas_method(ingredients)

    @staticmethod
    def canvas_method(dictionary):
        buffer = io.BytesIO()
        canvas = Canvas(buffer)
        begin_position_x, begin_position_y = 30, 730
        pdfmetrics.registerFont(TTFont("FreeSans", "data/FreeSans.ttf"))
        canvas.setFont("FreeSans", 25)
        canvas.setTitle("Список покупок")
        canvas.drawString(
            begin_position_x, begin_position_y + 40, "Список покупок: ")
        canvas.setFont("FreeSans", 18)
        for number, item in enumerate(dictionary, start=1):
            if begin_position_y < 100:
                begin_position_y = 730
                canvas.showPage()
                canvas.setFont("FreeSans", 18)
            canvas.drawString(
                begin_position_x,
                begin_position_y,
                f"{number}. {item['ingredient__name']} - "
                f"{item['ingredient_total']}"
                f"{item['ingredient__measurement_unit']}"
            )
            begin_position_y -= 30
        canvas.showPage()
        canvas.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename="shopping_cart.pdf")
