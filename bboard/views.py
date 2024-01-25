from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView
from django.views.generic.base import TemplateView, RedirectView
from django.template import loader
from django.template.loader import get_template, render_to_string
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView

from .forms import BbForm, RubricForm
from .models import Bb, Rubric


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)

    paginator = Paginator(bbs, 2, orphans=2)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    context = {'rubrics': rubrics, 'page_obj': page, 'bbs': page.object_list}

    return render(request, 'index.html', context)


class BbIndexView(ListView):
    model = Bb
    template_name = 'index.html'
    context_object_name = 'bbs'
    paginate_by = 2
    paginate_orphans = 2

    def get_queryset(self):
        return Bb.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


# class BbIndexView(ArchiveIndexView):
#     model = Bb
#     template_name = 'index.html'
#     date_field = 'published'
#     date_list_period = 'month'
#     # поумолчанию year, можно не писать
#     context_object_name = 'bbs'
#     allow_empty = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#         return context


class BbMonthView(MonthArchiveView):
    model = Bb
    template_name = 'index.html'
    date_field = 'published'
    date_list_period = 'month'
    month_format = '%m'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbByRubricView(ListView):
    template_name = 'by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(
            pk=self.kwargs['rubric_id'])
        return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class RubricCreateView(CreateView):
    template_name = 'create_rubric.html'
    form_class = RubricForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


class BbRedirectView(RedirectView):
    url = '/'


# class BbPostView(MonthArchiveView):
#     model = Bb
#     template_name = 'index.html'
#     date_field = 'published'
#     date_list_period = 'month'
#     month_format = '%m'
#     context_object_name = 'bbs'
#     allow_empty = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['bbs'] = Bb.objects.order_by('-pub_date')
#         return context

