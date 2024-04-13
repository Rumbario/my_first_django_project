from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    GENRE_CHOICES = [
        ('', 'Изберете жанр'),
        ('Трилър', 'Трилър'),
        ('Криминални романи', 'Криминални романи'),
        ('Фантастика, Фентъзи, Хорър', 'Фантастика, Фентъзи, Хорър'),
        ('Българска литература', 'Българска литература'),
        ('Биографична литература', 'Биографична литература'),
        ('Техническа литература', 'Техническа литература'),
        ('Образование', 'Образование'),
        ('Бизнес и икономика', 'Бизнес и икономика'),
        ('Здраве и диети', 'Здраве и диети'),
        ('Философска литература', 'Философска литература'),

    ]

    genre = forms.ChoiceField(choices=GENRE_CHOICES, required=True)

    class Meta:
        model = Book
        exclude = ['rating', 'uploaded_by']



class BookUpdateForm(BookForm):
    pass

