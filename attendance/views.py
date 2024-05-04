from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    class_list = [
        {'id': 1, 'class_date': '2024-01-01'},
        {'id': 2, 'class_date': '2024-02-01'},
        {'id': 3, 'class_date': '2024-03-01'},
    ]
    return render(request, "attendance/index.html", {'class_list': class_list})


def detail(request, class_num):
    class_list = [
        {'id': 1, 'class_date': '2024-01-01'},
        {'id': 2, 'class_date': '2024-02-01'},
        {'id': 3, 'class_date': '2024-03-01'},
    ]
    class_data = class_list[class_num - 1]
    current_name = request.POST.get('your_name')
    context = {'class_data': class_data, 'current_name': current_name}
    return render(request, "attendance/detail.html", context)
