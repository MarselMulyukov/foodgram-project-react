from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Follow
from recipes.serializers import RecipeMinifiedSerializer

User = get_user_model()


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return Follow.objects.filter(user=user, author=obj).exists()

    def get_recipes(self, obj):
        limit = int(
            self.context["request"].query_params.get("recipes_limit", 0)
        )
        queryset = obj.recipes.all()
        if limit:
            queryset = queryset[:limit]
        data = []
        for recipe in queryset:
            data.append(RecipeMinifiedSerializer(recipe).data)
        return data

    def get_recipes_count(self, obj):
        return len(obj.recipes.all())
