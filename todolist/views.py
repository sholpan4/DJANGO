from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


def task_list(request):
    tasks = Task.objects.all()
    paginator = Paginator(tasks, 2, orphans=2)

    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1

    # if 'page' in request.GET:
    #     page_num = request.GET['page']
    # else:
    #     page_num = 1

    page = paginator.get_page(page_num)

    context = {'page_obj': page, 'tasks': page.object_list}

    return render(request, 'task_list.html', context)

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todolist:task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})
