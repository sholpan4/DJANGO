import json
import os
from datetime import datetime

from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import StreamingHttpResponse, FileResponse, JsonResponse
from django.urls import resolve
from django.views.decorators.http import require_http_methods, require_GET

from bboard.models import Rubric, Bb
from samplesite.settings import BASE_DIR
from .forms import ImgForm
from .models import Img


FILES_ROOT = os.path.join(BASE_DIR, 'files')


# def index(request):
#     resp_content = ('Здесь будет', ' главная', ' страница', ' сайта')
#     resp = StreamingHttpResponse(resp_content, content_type='text/plain; charset=utf-8')
#     return resp

# def index(request):
#     # file_name = r'static/bg.jpg'
#     file_name = r'static/lesson_15.zip'
#     return FileResponse(open(file_name, 'rb'), as_attachment=True, filename='file.zip')   # readbytes

# def index(request):
#     data = {'title': 'Мотоцикл', 'content': 'Старый', 'price': 10000.0}
#     return JsonResponse(data, encoder=DjangoJSONEncoder) # специальные ответы

# если есть решение поделиться

# def index(request):
#     context = {'title': 'Тестовая страница'}
#     return render(request, 'test.html', context)

# def index(request):
#     r = get_object_or_404(Rubric, name="Транспорт")
#     return redirect('bboard:by_rubric', rubric_id=r.id)

# декораторы
# @require_http_methods(['GET', 'POST'])
# @require_GET()
# @require_POST()
# @require_safe() #get, head
# @gzip_page()
# def index(request):
#     rubric = get_object_or_404(Rubric, name="Транспорт")
#     bbs = get_list_or_404(Bb, rubric=rubric)
#
#     res = resolve('/2/')
#
#     context = {'title': 'Test side', 'bbs': bbs, 'res': res}
#
#     return render(request, 'test.html', context)


def index(request):
    imgs = []

    for entry in os.scandir(FILES_ROOT):
        imgs.append(os.path.basename(entry))

    context = {'title': 'Test side', 'imgs': imgs}

    return render(request, 'testapp/index.html', context)


def get(request, filename):
    fn = os.path.join(FILES_ROOT, filename)
    return FileResponse(open(fn, 'rb'), content_type='application/octet-stream')


def add(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['img']
            # fn = '%s%s' % (datetime.now().timestamp(), os.path.splitext(uploaded_file.name)[1])
            fn = f'{datetime.now().timestamp()}{os.path.splitext(uploaded_file.name)[1]}'
            fn = os.path.join(FILES_ROOT, fn)

            with open(fn, 'wb+') as destination:
                for chunk in uploaded_file.chunks():  # chunks(chunk_size=1024 or None default)
                    destination.write(chunk)

            return redirect('test:add')
    else:
        form = ImgForm()
    context = {'form': form}
    return render(request, 'testapp/add.html', context)


def delete(request, pk):
    img = Img.objects.get(pk=pk)
    img.img.delete() #путь обекта удалить
    img.delete() # сам объект удалить
    return redirect('test:add')

