from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import RecipeFilterForm, RecipeForm
from .models import Recipe


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 20

    def get_queryset(self):
        qs = Recipe.objects.all().order_by("-created_at").prefetch_related("tags", "ingredients")
        form = RecipeFilterForm(self.request.GET)
        if form.is_valid():
            # Search first (title, case-insensitive)
            if form.cleaned_data.get("search"):
                qs = qs.filter(title__icontains=form.cleaned_data["search"].strip())
            # Then filters
            if form.cleaned_data.get("ingredient"):
                qs = qs.filter(
                    recipeingredient__ingredient__name__icontains=form.cleaned_data["ingredient"]
                ).distinct()
            if form.cleaned_data.get("tag"):
                qs = qs.filter(tags=form.cleaned_data["tag"])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = RecipeFilterForm(self.request.GET)
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return Recipe.objects.prefetch_related("tags", "recipeingredient_set__ingredient")


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"
    success_url = reverse_lazy("recipe_list")


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"
    context_object_name = "recipe"
    success_url = reverse_lazy("recipe_list")


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = "recipes/recipe_confirm_delete.html"
    context_object_name = "recipe"
    success_url = reverse_lazy("recipe_list")
