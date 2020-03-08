# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from .views import *

urlpatterns = [
    re_path(r'^.*\.html', pages, name='pages'),

    # The home page
    path('', index, name='home'),

    path("user/", library_user.create),
    path("user/create", library_user.create),
    path("user/update", library_user.update),
    path("user/delete", library_user.delete),

    path("author/", author.create),

    path("author/create", author.create),
    path("author/update", author.update),
    path("author/delete", author.delete),

    url(r"^author/getAuthor/", author.get),

    url(r"^book/getBook/", book.get),
    path("book/", book.create),
    path("book/create", book.create),
    path("book/update", book.update),
    path("book/delete", book.delete),

    url(r"^book_loan/getBookLoan/", book_loan.get),
    path("book_loan/", book_loan.create),
    path("book_loan/create", book_loan.create),
    path("book_loan/update", book_loan.update),
    path("book_loan/liberate", book_loan.liberate),
    path("book_loan/delete", book_loan.delete),

    path('login/', login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]
