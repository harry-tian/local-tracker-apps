from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


COOKING_TIME_CHOICES = [
    ("", "Select cooking time"),
    ("< 15 min", "< 15 min"),
    ("15-30 min", "15-30 min"),
    (">30 min", ">30 min"),
]

DIFFICULTY_CHOICES = [
    ("", "Select difficulty"),
    ("Easy", "Easy"),
    ("Medium", "Medium"),
    ("Hard", "Hard"),
]


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    cooking_time = models.CharField(
        max_length=20, choices=COOKING_TIME_CHOICES, blank=True, default=""
    )
    difficulty = models.CharField(
        max_length=10, choices=DIFFICULTY_CHOICES, blank=True, default=""
    )
    steps = models.TextField(blank=True, help_text="Cooking steps (one per line or freeform)")
    notes = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="recipes")
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient", blank=True, related_name="recipes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_notes = models.CharField(max_length=100, blank=True, help_text="e.g. 2 cups, 1 tsp")

    class Meta:
        unique_together = [["recipe", "ingredient"]]
