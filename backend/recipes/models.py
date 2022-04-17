from django.db import models


class Tag(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    color = models.CharField(
        verbose_name="Цвет в HEX",
        max_length=7,
    )
    slug = models.CharField(
        verbose_name="Уникальный слаг",
        max_length=200,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=200,
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Component(models.Model):
    recipe = models.ForeignKey(
        "Recipe",
        verbose_name="Рецепт",
        on_delete=models.CASCADE,
        related_name="component",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингредиент",
        on_delete=models.PROTECT,
        related_name="component",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
    )

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецепта"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_ingredient"
            ),
        ]

    def __str__(self):
        return self.amount


class Recipe(models.Model):
    author = models.ForeignKey(
        "users.User",
        verbose_name="Автор",
        related_name="recipes",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="Название рецепта",
        max_length=200,
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="media/recipes/images",
    )
    text = models.TextField(
        verbose_name="Описание",
        max_length=2500,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through=Component,
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Тэги",
    )
    published = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-published",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        constraints = [models.UniqueConstraint(
            fields=["author", "name"],
            name="unique_authors_recipe"
        ), ]

    def __str__(self):
        return self.name


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="is_favorited",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="is_favorited",
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["user", "recipe"],
            name="unique_favorite"
        ), ]


class Purchase(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="is_in_shopping_cart",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="is_in_shopping_cart",
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["user", "recipe"],
            name="unique_purchase"
        ), ]
