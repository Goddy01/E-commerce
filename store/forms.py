from django import forms
from .models import Product, BillingAddress, City

class AddProductForm(forms.ModelForm):
    CATEGORY_CHOICES = (
        ("M", "MEN"), 
        ("W", "WOMEN"), 
        ("MC", "MALE CHILDREN"), 
        ("FC", "FEMALE CHILDREN"),
    )

    # SIZE_CHOICES = (
    #     ("XS", "EXTRA SMALL"),
    #     ("S", "SMALL"),
    #     ("M", "MEDIUM"),
    #     ("L", "LARGE"),
    #     ("XL", "EXTRA LARGE"),
    #     ("XXL", "EXTRA EXTRA LARGE"),
    #     ("XXXL", "EXTRA EXTRA EXTRA LARGE"),
    # )

    # COLOR_CHOICES = (
    #     ("Green", "GREEN"),
    #     ("Blue", "BLUE"),
    #     ("Red", "RED"),
    #     ("Orange", "ORANGE"),
    #     ("Black", "BLACK"),
    #     ("Yellow", "WHITE"),
    #     ("Yellow", "YELLOW"),
    #     ("Purple", "PURPLE"),
    #     ("Brown", "BROWN"),
    #     ("Pink", "PINK"),
    # )
    product_categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CATEGORY_CHOICES)
    product_sizes = forms.CharField(widget=forms. TextInput({ "placeholder": "Enter each size separated with a comma."}))
    product_colors = forms.CharField(widget=forms. TextInput({ "placeholder": "Enter each color separated with a comma."}))

    class Meta():
        model = Product
        fields = ('product_description', 'product_image3', 'product_image2', 'product_image1', 'product_colors', 'number_available', 'product_sizes', 'product_price', 'product_name', 'product_categories')
        # fields = '__all__'
    # instance = ""


class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()