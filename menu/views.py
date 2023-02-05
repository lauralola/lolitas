"""
Menu App - Views
----------------
Views for Menu App.
"""
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from menu.models import Meal


class Menu(ListView):
    """
    A view that provides meals data
    """

    template_name = "menu.html"
    model = Meal
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['menu_list'] = Meal.objects.all()

        return context


    def test_func(self):
        item = self.get_object()
        return self.request.user == item.user
