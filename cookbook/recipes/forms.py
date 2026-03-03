from django import forms

from .models import COOKING_TIME_CHOICES, DIFFICULTY_CHOICES, Ingredient, Recipe, Tag


class RecipeFilterForm(forms.Form):
    search = forms.CharField(required=False, label="Search by title")
    ingredient = forms.CharField(required=False, label="Filter by ingredient")
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.none(), required=False, empty_label="All tags", label="Filter by tag"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tag"].queryset = Tag.objects.all().order_by("name")


class RecipeForm(forms.ModelForm):
    tag_ids = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Tags",
    )
    ingredient_ids = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Ingredients",
    )
    new_ingredients = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Add new (comma-separated)"}),
        label="New ingredients",
    )
    new_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Add new tags (comma-separated)"}),
        label="New tags",
    )

    cooking_time = forms.ChoiceField(
        choices=COOKING_TIME_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "border border-slate-300 rounded-lg px-4 py-2"}),
    )
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "border border-slate-300 rounded-lg px-4 py-2"}),
    )

    class Meta:
        model = Recipe
        fields = ["title", "cooking_time", "difficulty", "steps", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tag_ids"].queryset = Tag.objects.all().order_by("name")
        self.fields["ingredient_ids"].queryset = Ingredient.objects.all().order_by("name")
        if self.instance and self.instance.pk:
            self.fields["tag_ids"].initial = self.instance.tags.all()
            self.fields["ingredient_ids"].initial = self.instance.ingredients.all()

    def save(self, commit=True):
        recipe = super().save(commit=commit)
        if not commit:
            return recipe
        tags = set(self.cleaned_data["tag_ids"])
        for name in [
            n.strip() for n in self.cleaned_data.get("new_tags", "").split(",") if n.strip()
        ]:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.add(tag)
        recipe.tags.set(tags)
        # Collect all ingredients to keep: selected + new from comma-separated
        keep_ingredients = set(self.cleaned_data["ingredient_ids"])
        new_names = [
            n.strip() for n in self.cleaned_data.get("new_ingredients", "").split(",") if n.strip()
        ]
        for name in new_names:
            ing, _ = Ingredient.objects.get_or_create(name=name)
            keep_ingredients.add(ing)
        # Replace recipe ingredients
        recipe.recipeingredient_set.exclude(ingredient__in=keep_ingredients).delete()
        for ing in keep_ingredients:
            recipe.recipeingredient_set.get_or_create(ingredient=ing, defaults={"quantity_notes": ""})
        return recipe
