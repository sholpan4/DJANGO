from django.db.models import Count
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.template import loader
from django.template.loader import get_template, render_to_string
from django.views.generic.edit import CreateView

from .forms import BbForm, RubricForm
from .models import Bb, Rubric  #находимся в bboard


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bbs': bbs, 'rubrics': rubrics}

    # bbs = Bb.objects.order_by('-published')
    # rubrics = Rubric.objects.all()
    # rubrics = Rubric.objects.filter(bb__isnull=False).distinct()

    # template = get_template('index.html')
    # return HttpResponse(
    #     # template.render(context=context, request=request))
    #     template.render(context, request))
    # return render(request, 'index.html', context)
    return HttpResponse (
        render_to_string('index.html', context, request)
    )


# def index(request):
#     rubrics = get_object_or_404(Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0))
#     bbs = get_list_or_404(Bb, rubric=rubrics)
#     context = {'bbs': bbs, 'rubric': rubrics}
#     return HttpResponse(render_to_string('index.html', context, request))


# def index(request):
#     bbs = Bb.objects.order_by('-published')
#     # rubrics = Rubric.objects.all()
#     # rubrics = Rubric.objects.filter(bb__isnull=False).distinct()
#     rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#     context = {'bbs': bbs, 'rubrics': rubrics}
#     return render(request, 'index.html', context)


# def by_rubric(request, rubric_id):
#     bbs = Bb.objects.filter(rubric=rubric_id)
#     # rubrics = Rubric.objects.all()
#     rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
#     return render(request, 'by_rubric.html', context)


class BbByRubricView(TemplateView):
    template_name = 'by_rubric.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        return context


# def add_and_save(request):
#     print(request.headers['Accept-Encoding'])
#     print(request.headers['accept-encoding'])
#     print(request.headers['accept_encoding'])
#     print(request.headers['Cookie'])
#     print(request.resolver_match)
#     print(request.body)
#
#     # if request.is_ajax():
#     # if request.headers.get('x-request-with') == 'XMLHttpRequest':
#
#     if request.method == 'POST':
#         bbf = BbForm(request.POST)
#         if bbf.is_valid():
#             bbf.save()
#             return HttpResponseRedirect(
#                 reverse('bboard:by_rubric',
#                         kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk})
#             )
#         else:
#             context = {'form': bbf}
#             return render(request, 'create.html', context)
#     else:
#         bbf = BbForm()
#         context = {'form': bbf}
#         return render(request, 'create.html', context)


class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.all()
        # context['rubrics'] = Rubric.objects.filter(bb__isnull=False).distinct()
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


class RubricCreateView(CreateView):
    template_name = 'create_rubric.html'
    form_class = RubricForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# def detail(request, bb_id):
#     try:
#         bb = Bb.objects.get(pk=bb_id)
#     except Bb.DoesNotExist:
#         # return HttpResponseNotFound('Такое объявление не существует')
#         raise Http404('Такое объявление не существует')
#     return HttpResponse()

# class BbDetailView(DetailView):
#     template_name = ''
#     form_class = BbSms
#     success_url = reverse_lazy



# def index_old(request):
#     template = loader.get_template('index.html')
#     bbs = Bb.objects.order_by('-published')
#     context = {'bbs': bbs}
#     return HttpResponse(template.render(context, request))