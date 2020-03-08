from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from app.models import BookLoan, Book
from ..forms import BookLoanForms, LiberateBook


def get_lists():
    _all = BookLoan.objects.all()
    books = Book.objects.all()
    not_available_isbn = [e.book.isbn for e in
                          BookLoan.objects.filter(date_start__lte=datetime.now(), date_finish=None).all()]
    available = [book for book in books if book.isbn not in not_available_isbn]

    critical = BookLoan.objects.filter(date_finish__lte=datetime.now()).all()
    return {"all": _all, "available": available, "critical": critical}


@login_required(login_url="/login/")
def create(request):
    if request.method == "GET":
        form = BookLoanForms()
        objs = get_lists()
        return render(request, 'Library/book_loan.html',
                      {"form_liberate": LiberateBook(), "form": form, "objs": get_lists()})

    if request.method == "POST":
        form = BookLoanForms(request.POST)
        if form.is_valid():

            if form.cleaned_data["date_start"] > form.cleaned_data["date_end"]:
                return render(request, 'Library/book_loan.html',
                              {"form_liberate": LiberateBook(), "form": form,
                               "msg": {"status": "danger",
                                       "msg": "la fecha incial debe ser menor a la final",
                                       "objs": get_lists()}})

            if BookLoan.objects.filter(book__name=form.cleaned_data["book"].name,
                                       date_start__lte=form.cleaned_data["date_end"],
                                       date_finish=None).count() > 0:
                return render(request, 'Library/book_loan.html',
                              {"form_liberate": LiberateBook(), "form": form, "msg": {"msg": "el libro esta prestado",
                                                                                      "status": "danger"},
                               "objs": get_lists()})

            obj = BookLoan(**form.cleaned_data)

            obj.save()
            return render(request, 'Library/book_loan.html', {"form_liberate": LiberateBook(), "form": BookLoanForms(),
                                                              "msg": {"status": "success",
                                                                      "msg": "Se añadio el pedido"},
                                                              "objs": get_lists()

                                                              })


@login_required(login_url="/login/")
def get(request):
    if request.method == "GET":
        _id = request.GET.get("id", None)
        a = BookLoan.objects.filter(id=_id)
        if not a:
            return JsonResponse("[]", safe=False)
        a = serializers.serialize("json", a)
        return JsonResponse(a, safe=False)


@login_required(login_url="/login/")
def delete(request):
    if request.method == "POST":
        form = BookLoanForms(request.POST)
        _id = form.data['id']
        BookLoan.objects.filter(id=_id).delete()
        return render(request, 'Library/book_loan.html', {"form_liberate": LiberateBook(), "form": BookLoanForms(),
                                                          "msg": {"status": "success",
                                                                  "msg": "Se elimino el pedido"},
                                                          "objs": get_lists()
                                                          })


@login_required(login_url="/login/")
def update(request):
    if request.method == "POST":
        form = BookLoanForms(request.POST)
        msg = {"status": "danger",
               "msg": "No existe el pedido"}
        obj = BookLoan.objects.filter(id=form.data['id'])
        if form.cleaned_data["date_start"] > form.cleaned_data["date_end"]:
            msg = {"status": "danger",
                   "msg": "la fecha incial debe ser menor a la final"}
        elif obj:
            obj.update(**form.cleaned_data)
            msg = {"status": "success",
                   "msg": "Se modifico el pedido"}

        return render(request, 'Library/book_loan.html', {"form_liberate": LiberateBook(), "form": form,
                                                          "msg": msg,
                                                          "objs": get_lists()

                                                          })


@login_required(login_url="/login/")
def liberate(request):
    if request.method == "POST":
        form = LiberateBook(request.POST)
        msg = {"status": "danger",
               "msg": "No existe el pedido"}
        obj = BookLoan.objects.filter(id=form.data['id2'])
        if obj:
            obj.update(date_finish=datetime.date(datetime.now()))
            msg = {"status": "success",
                   "msg": "Se entrego el libro"}

        return render(request, 'Library/book_loan.html', {"form_liberate": form, "form": BookLoanForms(),
                                                          "msg": msg,
                                                          "objs": get_lists()

                                                          })
