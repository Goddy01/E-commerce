from django import forms
from .models import Product

class AddProductForm(forms.ModelForm):
    CATEGORY_CHOICES = (
        ("M", "MEN"), 
        ("W", "WOMEN"), 
        ("MC", "MALE CHILDREN"), 
        ("FC", "FEMALE CHILDREN"),
    )

    SIZE_CHOICES = (
        ("XS", "EXTRA SMALL"),
        ("S", "SMALL"),
        ("M", "MEDIUM"),
        ("L", "LARGE"),
        ("XL", "EXTRA LARGE"),
        ("XXL", "EXTRA EXTRA LARGE"),
        ("XXXL", "EXTRA EXTRA EXTRA LARGE"),
    )

    COLOR_CHOICES = (
        ("Green", "GREEN"),
        ("Blue", "BLUE"),
        ("Red", "RED"),
        ("Orange", "ORANGE"),
        ("Black", "BLACK"),
        ("Yellow", "WHITE"),
        ("Yellow", "YELLOW"),
        ("Purple", "PURPLE"),
        ("Brown", "BROWN"),
        ("Pink", "PINK"),
    )
    product_categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CATEGORY_CHOICES)
    product_sizes = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SIZE_CHOICES)
    product_colors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=COLOR_CHOICES)

    class Meta():
        model = Product
        fields = ('product_description', 'product_image3', 'product_image2', 'product_image1', 'product_colors', 'number_available', 'product_sizes', 'product_price', 'product_name', 'product_categories')
        # fields = '__all__'
    # instance = ""