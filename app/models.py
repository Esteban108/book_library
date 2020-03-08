# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

# Create your models here.

"""
Un libro puede tener más de un autor.
3. Un usuario de la libreria puede llevarse prestado un libro hasta cierta fecha.

4. Formularios para crear, editar y eliminar Books, Authors y LibraryUsers

5. Formulario para prestar un libro a un usuario hasta cierta fecha (si está disponible)

6. Listados de libros disponibles para préstamo, otro de libros prestados y otro de libros que no han sido devueltos 
antes de la fecha tope de devolución.
"""


class LibraryUser(models.Model):
    name: str = models.CharField(max_length=200, primary_key=True)
    age: int = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)])
    created_date: datetime = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    name: str = models.CharField(max_length=200, primary_key=True)
    birth_date = models.DateField(null=True)
    created_date: datetime = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    authors: [Author] = models.ManyToManyField(Author, related_name='book_author')
    isbn: str = models.CharField(max_length=9, primary_key=True)
    name: str = models.CharField(max_length=200)
    pages: int = models.IntegerField()
    published_date = models.DateField()

    created_date: datetime = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.name}"


class BookLoan(models.Model):
    class Meta:
        unique_together = (('user', 'book', 'date_start'),)
    id = models.AutoField(primary_key=True)
    user: LibraryUser = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book: Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_start: datetime = models.DateField(default=timezone.now, blank=True)
    date_end: datetime = models.DateField()
    date_finish: datetime = models.DateField(default=None, null=True, blank=True)
