from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from app.models import Book
from ..forms import BookForms


@login_required(login_url="/login/")
def create(request):
    if request.method == "GET":
        form = BookForms()
        return render(request, 'Library/book.html', {"form": form})

    if request.method == "POST":
        form = BookForms(request.POST)
        if form.is_valid():
            obj = Book()
            obj.name = form.cleaned_data["name"]
            obj.isbn = form.cleaned_data["isbn"]
            obj.published_date = form.cleaned_data["published_date"]
            obj.pages = form.cleaned_data["pages"]

            obj.save()
            #for e in form.cleaned_data["authors"]:
            obj.authors.set(form.cleaned_data["authors"])
            obj.save()

            return render(request, 'Library/book.html', {"form": BookForms(),
                                                         "msg": {"status": "success",
                                                                 "msg": "Se añadio el libro"}
                                                         })
        return render(request, 'Library/book.html', {"form": form})


@login_required(login_url="/login/")
def get(request):
    if request.method == "GET":
        isbn = request.GET.get("isbn", None)
        a = Book.objects.filter(isbn=isbn)
        if not a:
            return JsonResponse([], safe=False)
        a = serializers.serialize("json", a)
        return JsonResponse(a, safe=False)


@login_required(login_url="/login/")
def delete(request):
    if request.method == "POST":
        form = BookForms(request.POST)
        isbn = form.data['isbn']
        Book.objects.filter(isbn=isbn).delete()
        return render(request, 'Library/book.html', {"form": BookForms(),
                                                     "msg": {"status": "success",
                                                             "msg": "Se elimino el libro"}
                                                     })


@login_required(login_url="/login/")
def update(request):
    if request.method == "POST":
        form = BookForms(request.POST)
        isbn = form.data['isbn']
        date = form.data['published_date']
        date = datetime.strptime(date, '%d/%m/%Y')
        msg = {"status": "danger",
               "msg": "No existe el libro"}
        obj = Book.objects.get(isbn=isbn)
        if obj:
            obj.name = form.data["name"]
            obj.published_date = date
            obj.pages = form.data["pages"]
            obj.authors.remove()
            obj.authors.set(form.cleaned_data["authors"])
            obj.save()
            msg = {"status": "success",
                   "msg": "Se modifico el libro"}

        return render(request, 'Library/book.html', {"form": BookForms(),
                                                     "msg": msg
                                                     })
