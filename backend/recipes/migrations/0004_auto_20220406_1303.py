# Generated by Django 2.2.19 on 2022-04-06 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220406_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='amounts', to='recipes.Ingredient', verbose_name='Ингредиент')),
            ],
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.Quantity', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.DeleteModel(
            name='Amount',
        ),
        migrations.AddField(
            model_name='quantity',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amounts', to='recipes.Recipe', verbose_name='Рецепт'),
        ),
    ]