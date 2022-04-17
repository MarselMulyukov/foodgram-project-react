from django.contrib import admin

from .models import Component, Ingredient, Recipe, Tag


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1
    model.__str__ = lambda self: ""


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author",)
    list_filter = ("name", "author", "tags")
    inlines = (ComponentInline, )
    fields = ("name", "author", "image", "cooking_time", "text",
              "tags", "favorited",)
    readonly_fields = ("favorited",)

    def favorited(self, obj):
        return obj.is_favorited.all().count()
    favorited.short_description = "Сколько человек добавили в избранное"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit",)
    list_filter = ("name",)


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
