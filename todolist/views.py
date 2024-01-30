from django.shortcuts import render
from django.template import loader


def index(request):
    template = loader.get_template(index_todo.html)
    return render(request,'index_todo.html')
