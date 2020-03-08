# -*- encoding: utf-8 -*-


from django import forms

from app.models import Author, Book, LibraryUser, BookLoan


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ))


"""
class LibraryUserForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    """


class LibraryUserForm(forms.ModelForm):
    class Meta:
        model = LibraryUser
        fields = ['name', 'age']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'})
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'onBlur': "getAuthor()"}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control datetimepicker'})
        }


class BookForms(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['authors', "name", "pages", "published_date", "isbn"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'onBlur': "getBook()"}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control datetimepicker'}),
            # data-style="select-with-transition" multiple title="Choose City" data-size="7"
            'authors': forms.SelectMultiple(attrs={'class': 'selectpicker',
                                                   'data-style': "select-with-transition",
                                                   'title': "autores", 'data-size': "7"})
        }


class BookLoanForms(forms.ModelForm):
    class Meta:
        model = BookLoan
        fields = ['user', "book", "date_end", "date_start"]
        widgets = {
            'date_end': forms.DateInput(attrs={'class': 'form-control datetimepicker'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control datetimepicker'}),
            'user': forms.Select(attrs={'class': 'selectpicker',
                                        'data-style': "select-with-transition",
                                        'title': "Usuario", 'data-size': "7"}),
            'book': forms.Select(attrs={'class': 'selectpicker',
                                        'data-style': "select-with-transition",
                                        'title': "libro", 'data-size': "7"})
        }


class LiberateBook(forms.Form):
    id2 = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
