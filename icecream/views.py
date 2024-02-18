# from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import IceCreamForm
from .models import IceCream


class IceCreamIndexView(ListView):
    model = IceCream
    template_name = 'icecream/icecream_index.html'
    context_object_name = 'icecreams'
    paginate_by = 1

    def get_queryset(self):
        return IceCream.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icecreams'] = IceCream.objects.all()
        return context


def create_ice_cream(request):
    if request.method == 'POST':
        form = IceCreamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('icecream:icecream_index')
    else:
        form = IceCreamForm()

    return render(request, 'icecream/create_icecream.html', {'form': form})
