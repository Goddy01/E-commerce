from django import forms
from .models import Product, OrderItem, BillingAddress, Review, UsersRecentlyViewedProduct, WishList

class AddProductForm(forms.ModelForm):
    CATEGORY_CHOICES = (
        ("M", "MEN"), 
        ("W", "WOMEN"), 
        ("MC", "MALE CHILDREN"), 
        ("FC", "FEMALE CHILDREN"),
    )

    product_image1 = forms.ImageField(widget=forms.FileInput)
    product_image2 = forms.ImageField(widget=forms.FileInput, required=False)
    product_image3 = forms.ImageField(widget=forms.FileInput, required=False)
    product_categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CATEGORY_CHOICES)
    product_sizes = forms.CharField(widget=forms. TextInput({ "placeholder": "Enter each size separated with a comma."}))
    product_colors = forms.CharField(widget=forms. TextInput({ "placeholder": "Enter each color separated with a comma."}))

    class Meta():
        model = Product
        # fields = ('product_description', 'product_image3', 'product_image2', 'product_image1', 'product_colors', 'number_available', 'product_sizes', 'product_price', 'product_name', 'product_categories')
        exclude = ('seller', 'product_id', 'slug', 'num_of_reviews', 'average_rating', 'num_of_ratings', 'num_of_visits', 'last_visit', 'date_added')

    instance = ''


class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = '__all__'


class UsersRecentlyViewedProdutForm(forms.ModelForm):
    class Meta:
        model = UsersRecentlyViewedProduct
        exclude = ('time_visited', )
        ordering = ['time_visited']

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('user_review', 'rating')

class WishListForm(forms.ModelForm):
    class Meta:
        model = WishList
        fields = ('color', 'size')

class UpdateProductForm(forms.ModelForm):
    CATEGORY_CHOICES = (
        ("M", "MEN"), 
        ("W", "WOMEN"), 
        ("MC", "MALE CHILDREN"), 
        ("FC", "FEMALE CHILDREN"),
    )

    product_image1 = forms.ImageField(widget=forms.FileInput)
    product_image2 = forms.ImageField(widget=forms.FileInput, required=False)
    product_image3 = forms.ImageField(widget=forms.FileInput, required=False)
    product_categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CATEGORY_CHOICES)
    product_sizes = forms.CharField(widget=forms. TextInput({ "placeholder": "Enter each size separated with a comma."}))
    product_colors = forms.CharField(widget=forms. TextInput({ "placeholder": "Enter each color separated with a comma."}))
    
    class Meta():
        model = Product

        # fields = ('product_description', 'product_image3', 'product_image2', 'product_image1', 'product_colors', 'number_available', 'product_sizes', 'product_price', 'product_name', 'product_categories')

        exclude = ('seller', 'product_id', 'slug', 'num_of_reviews', 'average_rating', 'num_of_ratings')

    def save(self, commit=True):
        product = self.instance
        product.product_name = self.cleaned_data.get('product_name')
        product.product_description = self.cleaned_data.get('product_description')
        product.product_colors = self.cleaned_data.get('product_colors')
        product.discount = self.cleaned_data.get('discount')
        product.number_available = self.cleaned_data.get('number_available')
        product.product_price = self.cleaned_data.get('product_price')
        product.product_sizes = self.cleaned_data.get('product_sizes')
        product.product_colors = self.cleaned_data.get('product_colors')
        product.product_image1 = self.cleaned_data.get('product_image1')
        
        if self.cleaned_data['product_image2']:
            product.product_image2 = self.cleaned_data.get('product_image2')
        if self.cleaned_data['product_image3']:
            product.product_image3 = self.cleaned_data.get('product_image3')

        if commit:
            product.save()

        return product

    