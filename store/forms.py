from django import forms
from .models import Product, OrderItem, BillingAddress

class AddProductForm(forms.ModelForm):
    CATEGORY_CHOICES = (
        ("M", "MEN"), 
        ("W", "WOMEN"), 
        ("MC", "MALE CHILDREN"), 
        ("FC", "FEMALE CHILDREN"),
    )


    product_categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CATEGORY_CHOICES)
    product_sizes = forms.CharField(widget=forms. TextInput({ "placeholder": "Enter each size separated with a comma."}))
    product_colors = forms.CharField(widget=forms. TextInput({ "placeholder": "Enter each color separated with a comma."}))

    class Meta():
        model = Product
        fields = ('product_description', 'product_image3', 'product_image2', 'product_image1', 'product_colors', 'number_available', 'product_sizes', 'product_price', 'product_name', 'product_categories')
        # fields = '__all__'


class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = '__all__'



# product_sizes = product.product_sizes.split(',')
# product_colors = product.product_colors.split(',')

class OrderItemForm(forms.ModelForm):
    def __init__(self, size_choices, color_choices, *args, **kwargs):
        # self.request = request
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['size'].choices = size_choices
        self.fields['color'].choices = color_choices
    # product_colors = Product.
    # product_sizes = 
    
    # for color in product_colors:
    #     COLOR_CHOICES.append((color, color))
    # for size in product_sizes:
    #     SIZE_CHOICES.append((size, size))
    size= forms.ChoiceField(label='Sizes: ', choices=(), required=True)
    color= forms.ChoiceField(label='Colors: ', choices=(), required=True)
    # quantity = forms.IntegerField(label='Quantity: ',required=True)

    class Meta:
        # size = forms.CharField(label='Sizes: ', widget=forms.ChoiceField)
        model = OrderItem
        fields = ('size', 'color', 'quantity')