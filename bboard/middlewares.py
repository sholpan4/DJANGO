from django.contrib.auth.models import User
from django.db.models import Count

from bboard.models import Rubric


def my_middleware(_next):
    # здесь можно выполнить сом инициализацию
    def core_middleware(request):
        # обработка клиентского запроса
        response = _next(request)
        print('РАБОТАЕТ')
        # обработка ответа
        return response
    return core_middleware


class MyMiddleware:
    def __init__(self, get_response):
        self._next = get_response
        # здесь можно выполнить сом инициализацию

    def __call__(self, request):
        # обработка клиентского запроса
        response = self._next(request)
        # обработка ответа
        return response


class RubricMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_template_response(self, request, response):
        response.context_data['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return response


def rubrics(request):
    return {'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)}


def users_context_processor(request):
    all_users = User.objects.all()
    return {'all_users': all_users}


def group_context_processor(request):
    user_groups = None
    if request.user.is_authenticated:
        user_groups = request.user.groups.all()
        return {'user_groups': user_groups}


class CustomContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        context_data = response.context_data
        context_data.update(users_context_processor(request))
        print('users_context_processor')
        context_data.update(group_context_processor(request))
        print('group_context_processor')
        return response
