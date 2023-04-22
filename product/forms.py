from django import forms

from .models import Product

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'description', 'price', 'image')
        # widgets is a dictionary that contains the fields as keys and the widgets as values
        widgets = {
            'category': forms.Select(attrs={
            'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
            'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
            'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
            'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
            'class': INPUT_CLASSES
            }),

        }


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image', 'is_sold')
        # widgets is a dictionary that contains the fields as keys and the widgets as values
        widgets = {
            'name': forms.TextInput(attrs={
            'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
            'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
            'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
            'class': INPUT_CLASSES
            }),
            # is_sold is a boolean field, so we need to use a checkbox
            'is_sold': forms.CheckboxInput(),
        }
    