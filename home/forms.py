from django import forms
from .models import reference, Staff , Staff_work ,Book_model, staff_payments, Product, Sale, Gender, Output

class referenceForm(forms.ModelForm):  
    class Meta:
        model = reference
        fields = ['name', 'value']  
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),  
            "value": forms.TextInput(attrs={"class": "form-control"}),  
        }

class GenderForm(forms.ModelForm):
    class Meta:
        model = Gender
        fields = ['name']   
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),  
            "value": forms.TextInput(attrs={"class": "form-control"}),  
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'position', 'email', 'phone', 'gender']
        widgets = {
            'gender': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'background-color: #f3f3f3;',  
                'aria-label': 'Gender',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingizni kiriting'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lavozimingizni kiriting'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Elektron pochta manzilingizni kiriting'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefon raqamingizni kiriting'
            }),
        }
    
    gender = forms.ModelChoiceField(
        queryset=reference.objects.filter(name="Jinsi"),
        empty_label="Tanlang"
    )
    gender = forms.ModelChoiceField(queryset=reference.objects.filter(name="Jinsi"), empty_label="Tanlang")
        
        

class Book_modelForm(forms.ModelForm):
    class Meta:
        model = Book_model
        fields = ['name', 'category', 'price', 'quantity', 'description', 'image']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control rounded-3'}),
            'category': forms.Select(attrs={'class': 'form-control rounded-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Kitob narxini kiriting'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Miqdor kiriting'}),
            'description': forms.Textarea(attrs={'class': 'form-control rounded-3', 'placeholder': 'Kitob haqida qisqacha tavsif'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control rounded-3'}),
        }


    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Kitob nomi kiritilishi kerak.")
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Narx musbat bo'lishi kerak.")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Miqdor musbat bo'lishi kerak.")
        return quantity
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    from django import forms
from .models import reference, Staff, Book_model

class referenceForm(forms.ModelForm):
    class Meta:
        model = reference
        fields = ['name', 'value']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter value'}),
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name' , 'position' , 'email' , 'phone' , 'gender']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'F I SH kiriting',
                'required': 'required'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lavozimni tanlang',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Elektron pochta manzilni kiriting',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefon raqamni kiriting',
                'required': 'required'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            })
        }


class Book_modelForm(forms.ModelForm):
    class Meta:
        model = Book_model
        fields = ['name', 'category', 'price', 'quantity', 'image', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4}),
        }
        
class StaffPaymentForm(forms.ModelForm):
    class Meta:
        model = staff_payments
        fields = ["staff", "price"]
        widgets = {
            "staff": forms.Select(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = Staff.objects.filter(isDeleted=False)


class StaffWorkForm(forms.ModelForm):
    class Meta:
        model = Staff_work  
        fields = ['staff', 'time_work', 'price']  
        widgets = {
            'staff': forms.Select(attrs={'class': 'form-control'}),  
            'time_work': forms.NumberInput(attrs={'class': 'form-control'}), 
            'price': forms.NumberInput(attrs={'class': 'form-control'}), 
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['isDeleted']  # Bu orqali `isDeleted`ni formadan chiqarib tashlaysiz
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mahsulot nomi'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mahsulot tavsifi'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Narx'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ombor miqdori'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kategoriya'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity']  # Foydalanuvchidan kiritiladigan maydonlar
        labels = {
            'product': 'Mahsulot',
            'quantity': 'Sotilayotgan miqdor',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        
        # Ombordagi mahsulot miqdorini tekshirish
        if product and quantity > product.stock:
            raise forms.ValidationError("Omborda yetarli mahsulot yo'q.")
        
class OutputForm(forms.ModelForm):
    class Meta:
        model = Output
        fields = ['name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        
class OutputForm(forms.ModelForm):
    class Meta:
        model = Output
        fields = ['name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kitob nomi'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Kitob tavsifi'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qiymati'}),
        }
        
        
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)