from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView
from django.views.generic.base import TemplateView, RedirectView, View
from django.template import loader
from django.template.loader import get_template, render_to_string
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView, ProcessFormView

from .forms import BbForm, RubricForm, UserDetailsForm
from .models import Bb, Rubric


# def index(request):
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#     context = {'bbs': bbs, 'rubrics': rubrics}
#     return HttpResponse (
#         render_to_string('index.html', context, request)
#     )

class BbIndexView(ArchiveIndexView):
    model = Bb
    template_name = 'index.html'
    date_field = 'published'
    date_list_period = 'month'
    # поумолчанию year, можно не писать
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


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


class BbRubricListView(ListView):
    template_name = 'by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
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


class AllUsersView(ListView):
    template_name = 'all_users.html'

    def get(self, request):
        users = User.objects.all()
        return render(request, 'all_users.html', {'users': users})


class UserDetailView(DetailView):
    model = User
    template_name = 'user_details.html'

    def get(self, request):
        form = UserDetailsForm()
        return render(request, 'user_details.html', {'form': form})


# class UserDetailsFormView(View):
#     template_name = 'user_details_form.html'
# 
#     def post(self, request):
#         form = UserDetailsForm(request.POST)
#         if form.is_valid():
#             user_id = form.cleaned_data['user_id']
#             try:
#                 user = User.objects.get(id=user_id)
#                 return render(request, 'user_details.html', {'user': user})
#             except User.DoesNotExist:
#                 error_message = 'User with ID {} does not exist.' .format(user_id)
#                 return render(request, 'user_details_form.html', {'form': form, 'error_message': error_message})
#         return render(request, 'user_details_form.html', {'form': form})

