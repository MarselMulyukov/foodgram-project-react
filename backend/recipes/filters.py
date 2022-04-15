from django_filters import rest_framework as filters

from .models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name="tags__slug")
    author = filters.AllValuesFilter(
        field_name="author")
    is_favorited = filters.BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="get_is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = ("tags", "author",)

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(is_favorited__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(is_in_shopping_cart__user=self.request.user)
        return queryset
