from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import LibraryUser
from ..forms import LibraryUserForm


@login_required(login_url="/login/")
def create(request):
    if request.method == "GET":
        form_usr = LibraryUserForm()
        return render(request, 'Library/user.html', {"form": form_usr})

    if request.method == "POST":
        form = LibraryUserForm(request.POST)
        if form.is_valid():
            # process form data
            obj = LibraryUser(**form.cleaned_data)
            obj.save()
            return render(request, 'Library/user.html', {"form": LibraryUserForm(),
                                                         "msg": {"status": "success",
                                                                 "msg": "Se añadio el usuario"}
                                                         })
        return render(request, 'Library/user.html', {"form": form})


@login_required(login_url="/login/")
def delete(request):
    if request.method == "POST":
        form = LibraryUserForm(request.POST)
        name = form.data['name']
        LibraryUser.objects.filter(name=name).delete()
        return render(request, 'Library/user.html', {"form": LibraryUserForm(),
                                                     "msg": {"status": "success",
                                                             "msg": "Se elimino el usuario"}
                                                     })


@login_required(login_url="/login/")
def update(request):
    if request.method == "POST":
        form = LibraryUserForm(request.POST)
        name = form.data['name']
        age = int(form.data['age'])
        if 5 < age < 100:
            # process form data
            msg = {"status": "success",
                   "msg": "Se modifico el usuario"}
            if LibraryUser.objects.filter(name=name).update(age=age) == 0:
                msg = {"status": "danger",
                       "msg": "No existe el usuario"}

            return render(request, 'Library/user.html', {"form": LibraryUserForm({"age": age, "name": name}),
                                                         "msg": msg
                                                         })
        return render(request, 'Library/user.html', {"form": LibraryUserForm(),
                                                     "msg": {"status": "danger",
                                                             "msg": "Asegúrese de que este valor es mayor o igual a 5."}})
