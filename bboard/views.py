from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy

from .forms import BbForm
from .models import Bb, Rubric  #находимся в bboard
from django.template import loader
from django.views.generic.edit import CreateView



def index(request):
    bbs = Bb.objects.order_by('-published')
    # rubrics = Rubric.objects.all()
    rubrics = Rubric.objects.filter(bb__isnull=False).distinct()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'index.html', context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'by_rubric.html', context)


class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.all()
        context['rubrics'] = Rubric.objects.filter(bb__isnull=False).distinct()
        return context









def index_old(request):
    template = loader.get_template('index.html')
    bbs = Bb.objects.order_by('-published')
    context = {'bbs': bbs}
    return HttpResponse(template.render(context, request))