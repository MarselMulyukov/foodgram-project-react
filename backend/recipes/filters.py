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
    is_favorited = filters.BooleanFilter(method="common_method")
    is_in_shopping_cart = filters.BooleanFilter(
        method="common_method")

    class Meta:
        model = Recipe
        fields = ("tags", "author",)

    def common_method(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(**{f"{name}__user": self.request.user})
        return queryset
