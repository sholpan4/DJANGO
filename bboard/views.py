from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView
from django.views.generic.base import TemplateView, RedirectView
from django.template import loader
from django.template.loader import get_template, render_to_string
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from precise_bbcode.bbcode import get_parser

from .forms import BbForm, RubricForm, RubricBaseFormSet, SearchForm
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


# class BbIndexView(LoginRequiredMixin, ListView):
class BbIndexView(ListView):
    model = Bb
    template_name = 'index.html'
    context_object_name = 'bbs'
    paginate_by = 1
    paginate_orphans = 2

    def get_queryset(self):
        return Bb.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    #     return context


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
        # context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(
            pk=self.kwargs['rubric_id'])
        return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.all()
        return context


class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.all()
        return context


class RubricCreateView(CreateView):
    template_name = 'create_rubric.html'
    form_class = RubricForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.all()
        return context


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubric'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubric'] = Rubric.objects.all()
        return context


def detail(request, pk):
    parser = get_parser()
    bb = Bb.objects.get(pk=pk)
    parsed_content = parser.render(bb.content)
    pass


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

def edit(request, pk):
    bb = Bb.objects.get(pk=pk)

    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            if bbf.has_changed():
                bbf.save()
            # return HttpResponseRedirect(
            #         reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk})
            # )
            return HttpResponseRedirect(
                reverse('bboard:detail', kwargs={'pk': pk})
            )
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_form.html', context)
    else:
        bbf = BbForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)


    # bbf = BbForm(request.POST)
    # # if bbf.is_valid():
    # #     pass
    # # else:
    # #     pass
    # if bbf.errors:
    #     title_errors = bbf.errors['title']
    #     form_errors = bbf.errors[NON_FIELD_ERRORS]
    # bb = bbf.save(commit=False)
    # if not bb.kind:
    #     bb.kind = 's'
    #
    # bb.save()
    # return HttpResponseRedirect(
    #     reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk})
    # )

def add_save(request):
    bbf = BbForm(request.POST)
    if bbf.is_valid():
        bbf.save()
        return HttpResponseRedirect(
                reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk})
        )
    else:
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)


def commit_handler():
    print("C O M M I T E D")


def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, RubricForm,
                                         can_order=True, extra=3, can_delete=True, formset=RubricBaseFormSet)

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)

        if formset.is_valid():
            instance = formset.save(commit=False)
            for obj in formset:
                if obj.cleaned_data:
                    sp = transaction.savepoint()

                    try:
                        rubric = obj.save(commit=False)
                        rubric.order = obj.cleaned_data[ORDERING_FIELD_NAME]
                        rubric.save()
                        transaction.savepoint_commit(sp)
                        print("C O M M I T E D", rubric)
                    except:
                        transaction.savepoint_rollback(sp)
                        transaction.commit()
                        print("N O T   C O M M I T E D")

                    # transaction.on_commit(commit_handler)

            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('bboard:rubrics')

    else:
        formset = RubricFormSet()

    context = {'formset': formset}

    return render(request, 'bboard/rubrics.html', context)


# @transaction.non_atomic_requests
# @transaction.atomic
# @login_required
# @user_passes_test(lambda user: user.is_staff)
# @permission_required('bboard.view_rubric')
def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)

    # if request.user.is_authenticated:
    #     pass
    # else:
    #     return redirect_to_login(reverse('bboard:rubrics'))
    # if request.user.is_anonymous:
    # if request.user.has_perm('bboard.add_rubric'):
    # if request.user.has_perms('bboard.add_rubric', 'bboard.change_rubric'):
    request.user.get_user_permissions()

    if request.method == 'POST':
        formset = BbsFormSet(request.POST, instance=rubric)

        if formset.is_valid():
            # with transaction.atomic():
            formset.save()
            return redirect('bboard:index')
    else:
        formset = BbsFormSet(instance=rubric)

    context = {'formset': formset, 'current_rubric': rubric}
    return render(request, 'bboard/bbs.html', context)


def search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            current_rubric = sf.cleaned_data['rubric']
            # bbs = Bb.objects.filter(title__icontains=keyword, rubric=rubric_id)
            bbs = Bb.objects.filter(title__iregex=keyword, rubric=rubric_id)
            context = {'bbs': bbs, 'current_rubric': current_rubric, 'keyword': keyword}
            return render(request, 'bboard/search_results.html', context)
    else:
        sf = SearchForm()
    context = {'form': sf}
    return render(request, 'bboard/search.html', context)


def my_login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        # Вход выполнен
    else:
        # Вход не выполнен
        pass


def my_logout(request):
    logout(request)
    # return redirect('')


if __name__ == '__main__':
    admin = User.objects.get(name='admin')
    if admin.check_password('password'):
        # пароли совпадают
        pass
    else:
        # пароли не совпадают
        pass


    # admin.set_password('newpassword')
    # admin.save()
