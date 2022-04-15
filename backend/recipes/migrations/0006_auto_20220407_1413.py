# Generated by Django 2.2.19 on 2022-04-07 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20220406_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='component', to='recipes.Ingredient', verbose_name='Ингредиент')),
            ],
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.Component', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.DeleteModel(
            name='Quantity',
        ),
        migrations.AddField(
            model_name='component',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='component', to='recipes.Recipe', verbose_name='Рецепт'),
        ),
    ]