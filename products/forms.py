from django import forms
from .models import Product


PUBLISH_CHOICES = {
    #('', ''),
    ('publish', 'Publish'),
    ('draft', 'Draft'),
}
        
class ProductModelForm(forms.ModelForm):
    publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'price']
        widgets = {
            'description': forms.Textarea(
                attrs={'placeholder': 'New Description'}
                ),
            'title': forms.TextInput(
                attrs={'placeholder': 'Title'}
                )
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 1.00:
            return forms.ValidationError("Price must be greater then £1.00")
        elif price >= 99.99:
            raise forms.ValidationError("Price must be less then £100.00")
        else:
            return price
        
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError("Title must be longer then 3 characters")
        
                
    
    