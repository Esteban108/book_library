from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from app.models import Author
from ..forms import AuthorForm


@login_required(login_url="/login/")
def create(request):
    if request.method == "GET":
        form = AuthorForm()
        return render(request, 'Library/author.html', {"form": form})

    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            # process form data
            obj = Author(**form.cleaned_data)
            obj.save()
            return render(request, 'Library/author.html', {"form": AuthorForm(),
                                                           "msg": {"status": "success",
                                                                   "msg": "Se añadio el author"}
                                                           })
        return render(request, 'Library/author.html', {"form": form})


@login_required(login_url="/login/")
def get(request):
    if request.method == "GET":
        name = request.GET.get("name", None)
        a = Author.objects.filter(name=name)
        if not a:
            return JsonResponse([], safe=False)
        a = serializers.serialize("json", a)
        return JsonResponse(a, safe=False)


@login_required(login_url="/login/")
def delete(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        name = form.data['name']
        Author.objects.filter(name=name).delete()
        return render(request, 'Library/author.html', {"form": AuthorForm(),
                                                       "msg": {"status": "success",
                                                               "msg": "Se elimino el author"}
                                                       })


@login_required(login_url="/login/")
def update(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        name = form.data['name']
        date = form.data['birth_date']
        date = datetime.strptime(date, '%d/%m/%Y')

        # process form data
        msg = {"status": "success",
               "msg": "Se modifico el author"}
        if Author.objects.filter(name=name).update(birth_date=date) == 0:
            msg = {"status": "danger",
                   "msg": "No existe el author"}

        return render(request, 'Library/author.html', {"form": AuthorForm({"birth_date": date, "name": name}),
                                                       "msg": msg
                                                       })
