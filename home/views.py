from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.contrib import messages 
from django.db.models import Sum  
from .forms import referenceForm, StaffForm, Book_modelForm, StaffPaymentForm ,StaffWorkForm, SaleForm, OutputForm, LoginForm
from . import models
from django.contrib.auth.decorators import login_required
from .models import Staff,Staff_work, Sale, Product, staff_payments, reference, Output

def home(request):
    books = models.Book_model.objects.filter(isDeleted=False)
    book_category = models.reference.objects.filter(name="Kitob turi")
    search = request.GET.get('search', None)
    category_filter = request.GET.get('category', None)

    if search:
        books = books.filter(name__icontains=search)

    if category_filter:
        books = books.filter(category__value=category_filter)

    context = {
        "books": books,
        "book_category": book_category
    }

    return render(request, 'index.html', context=context)


# Reference
def reference_view(request):
    reference_models = models.reference.objects.filter(is_deleted=False)
    reference_values = {}

    # Ma'lumotlarni to'plash
    for item in reference_models:
        if item.name not in reference_values:
            reference_values[item.name] = [{'id': item.id, 'value': item.value}]
        else:
            reference_values[item.name].append({'id': item.id, 'value': item.value})

    return render(request, "reference.html", {"reference_values": reference_values})

def reference_delete(request, pk):
    model = models.reference.objects.get(pk=pk)
    reference.isDeleted = True
    model.save()  # <-- Bazaga o‘zgarishni saqlash
    return redirect('reference')  # <-- Sahifaga qaytish

def reference_create(request):
    if request.method == "POST":
        forms = referenceForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('reference')
        
    forms = referenceForm()
    context = {
        "form": forms
    }
    return render(request, "reference_create.html", context=context)

#Output
def output_list(request):
    output_list = Output.objects.all()
    return render(request, 'output.html', {'output_list': output_list})

def output_create(request):
    if request.method == 'POST':
        form = OutputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('output_list')
    else:
        form = OutputForm()
    return render(request, 'output_create.html', {'form': form})

def output_edit(request, pk):
    output = Sale.objects(Output, pk=pk)
    if request.method == 'POST':
        form = OutputForm(request.POST, instance=output)
        if form.is_valid():
            form.save()
            return redirect('output_list')
    else:
        form = OutputForm(instance=output)
    return render(request, 'output/output_form.html', {'form': form})

def output_delete(request, pk):
    output = Output.objects.get(pk=pk)
    output.delete()
    return redirect('output')

#Sale
def sale_view(request):
    """Sotuvlar ro'yxatini ko'rsatish"""
    sales = Sale.objects.select_related('product').all()
    return render(request, 'sale.html', {'sales': sales})

def sale_create(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = int(request.POST.get("quantity", 0))

        try:
            product = Product.objects.get(id=product_id)
            if quantity > product.stock:
                messages.error(request, "Omborda yetarli mahsulot yo'q")
            else:
                sale = Sale.objects.create(
                    product=product,
                    quantity=quantity,
                    total_price=product.price * quantity
                )
                messages.success(request, "Sotuv muvaffaqiyatli qo'shildi!")
                return redirect("sale")
        except Product.DoesNotExist:
            messages.error(request, "Tanlangan mahsulot topilmadi.")
    else:
        products = Product.objects.all()
        return render(request, "sale_create.html", {"products": products})



def sale_edit(request, pk):
    """Sotuvni tahrirlash"""
    sale = Sale.objects.get(pk=pk)  # Xato shu yerda edi
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            messages.success(request, "Sotuv muvaffaqiyatli tahrirlandi!")
            return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)
    
    return render(request, 'sale_edit.html', {'form': form, 'sale': sale})


def sale_delete(request, pk):
    """Sotuvni o'chirish"""
    sale = Sale.objects.get(pk=pk)  # Xato shu yerda edi
    if request.method == 'POST':
        product = sale.product
        product.stock += sale.quantity  # Ombor miqdorini qayta tiklash
        product.save()
        sale.delete()  # Sotuvni o'chirish
        messages.success(request, "Sotuv muvaffaqiyatli o'chirildi!")
        return redirect('sale')

#Product
def product_list(request):
    products = Product.objects.filter(isDeleted=False)  # Bu yerda to'g'ri maydonni ishlatyapsizmi?
    return render(request, 'product.html', {'products': products})



from django.shortcuts import render, redirect
from .forms import ProductForm

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()  
            return redirect('product')  
    else:
        form = ProductForm()  

    return render(request, 'product_create.html', {'form': form})

def product_edit(request, pk):
    product =  Product.objects.get() 
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  
            return redirect('product')  
    else:
        form = ProductForm(instance=product)  

    return render(request, 'product_edit.html', {'form': form, 'product': product})

def product_delete(request, pk):
    model = models.Product.objects.get(pk=pk)
    product = Product.objects.get(pk=pk)
    product.isDeleted = True
    product.save()
    return redirect('product')  

# Staff

from django.shortcuts import render

def staff_view(request):
    # Staff va Staff_work obyektlarini olish
    staff_list = Staff.objects.all()
    staff_work_list = Staff_work.objects.all()
    staff_payment_list = staff_payments.objects.all()  # staff_payment_listni qo'shish

    # Umumiy balansni hisoblash
    total_balance = sum(staff.balance for staff in staff_list)

    # Filtr parametrlari
    full_name = request.GET.get('full_name', '').strip()
    gender = request.GET.get('gender', '').strip()
    phone = request.GET.get('phone_number', '').strip()

    if full_name:
        staff_list = staff_list.filter(name__icontains=full_name)

    if gender:
        staff_list = staff_list.filter(gender__name__icontains=gender)

    if phone:
        staff_list = staff_list.filter(phone__icontains=phone)

    context = {
        "staff_list": staff_list,
        "staff_work_list": staff_work_list,
        "staff_payment_list": staff_payment_list,
        "total_balance": total_balance,
        "staff_payment": staff_payments,
    }

    return render(request, 'staff.html', context)

def staff_edit(request, pk):
    staff_instance = models.Staff.objects.get(pk=pk)

    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff_instance)
        if form.is_valid():
            form.save()  # Bu yerda saqlashdan oldin ForeignKey bog'lanishlarini tekshirib chiqing
            return redirect('staff_list')  # Agar barcha ma'lumotlar to'g'ri bo'lsa, ro'yxat sahifasiga yo'naltiramiz
    else:
        form = StaffForm(instance=staff_instance)

    return render(request, 'staff_edit.html', {'form': form})


def staff_create(request):
    # Hodim yaratish
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff')  # To'g'ri URL ga yo'naltirish
    else:
        form = StaffForm()

    return render(request, 'staff_create.html', {'form': form})

def staff_delete(request, pk):
    model = models.Staff.objects.get(pk=pk)
    model.delete()
    return redirect('staff')





# Book model
def book_model(request):
    book_list = models.Book_model.objects.filter(isDeleted=False)

    context = {
        'book_list': book_list
    }
    return render(request, 'book_model.html', context=context)

def book_model_edit(request, pk):
    # Kitobni olish
    Book_model = models.Book_model.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = Book_modelForm(request.POST, request.FILES, instance=Book_model)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kitob muvaffaqiyatli tahrirlandi!')
            return redirect('book_model')  # Kitoblar ro'yxati sahifasiga yo'naltirish
        else:
            messages.error(request, 'Formada xatolik bor! Iltimos, tekshirib qayta yuboring.')
    else:
        form = Book_modelForm(instance=Book_model)
    
    return render(request, 'book_model_edit.html', {'form': form, 'book_model': book_model})

def book_model_create(request):
    if request.method == 'POST':
        form = Book_modelForm(request.POST, request.FILES)  
        print(form.errors)
        if form.is_valid():
            form.save()  
            return redirect('book_model')  
    else:
        form = Book_modelForm()
    return render(request, 'book_model_create.html', {'form': form})
# views.py
def book_model_delete(request, pk):
    model = models.Book_model.objects.get(pk=pk)
    if request.method == 'POST':
        model.isDeleted = True  # Soft delete
        model.save()
        return redirect('book_model')
    return render(request, 'book_model_delete.html', {'model': model})




def income_calc_view(request):
    # Sanalar oralig'ini olish
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Filter qilish uchun shart
    date_filter = {}
    if start_date and end_date:
        date_filter['created_at__range'] = (start_date, end_date)

    # Xarajatlar (Cost modeli)
    cost_total_sum = models.Cost.objects.filter(**date_filter).aggregate(
        total=Sum('price') * Sum('quantity')
    )['total'] or 0

    # Chiqimlar (Output modeli)
    total_expense_sum = models.Output.objects.filter(**date_filter).aggregate(
        total=Sum('price')
    )['total'] or 0

    # Xodim to'lovlari (staff_payments modeli)
    staff_payment_sum = models.staff_payments.objects.filter(**date_filter).aggregate(
        total=Sum('price')
    )['total'] or 0

    sold_books_sum = models.Book_model.objects.filter(**date_filter).aggregate(
        total=Sum('price') * Sum('quantity')
    )['total'] or 0
    

    # Sof foyda hisoblash
    net_profit = sold_books_sum - (cost_total_sum + total_expense_sum + staff_payment_sum)

    # Kontekst ma'lumotlari
    context = {
        "cost_total_sum": cost_total_sum,
        "total_expense_sum": total_expense_sum,
        "staff_payment_sum": staff_payment_sum,
        "sold_books_sum": sold_books_sum,
        "net_profit": net_profit,
    }

    return render(request, 'income_calc.html', context=context) 
#Staff
def staff_payment_create(request):
    if request.method == 'POST':
        print(request.POST)  # Konsolda ma'lumotlar chop etiladi
        form = StaffPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form muvaffaqiyatli saqlandi!")  # Konsolda muvaffaqiyat xabari
            return redirect('staff')  # To'g'ri URL nomidan foydalaning
        else:
            print("Formda xatoliklar:", form.errors)  # Xatoliklar haqida ma'lumot konsolda
    else:
        form = StaffPaymentForm() 

    # Faol xodimlar va ularning to‘lovlari ro'yxatini olish  # Model nomi katta harf bilan

    return render(request, 'staff_payment_create.html', {'form': form,  })

def staff_payment_edit(request, pk):
    # staff_payment obyektini olish
    staff_payment = staff_payments.objects.get(pk=pk)  # `id=pk` ishlatib kerakli obyektni olish

    # Agar so'rov POST bo'lsa, forma orqali tahrirlash
    if request.method == 'POST':
        form = StaffPaymentForm(request.POST, instance=staff_payment)
        if form.is_valid():
            form.save()
            return redirect('staff')  # Sotuvlar ro'yxatiga qaytish
    else:
        form = StaffPaymentForm(instance=staff_payment)  # Formani mavjud ma'lumotlar bilan to'ldirish

    return render(request, 'staff_payment_edit.html', {'form': form, 'staff_payment': staff_payment})


def staff_payment_delete(request, pk):
    model = models.staff_payments.objects.get(pk=pk)
    model.isDeleted = True
    model.save()
    return redirect('staff')
    
def staff_work_create(request):
    if request.method == "POST":
        form = StaffWorkForm(request.POST)
        if form.is_valid():
            
            form.save()  
            return redirect('staff')  
    else:
        form = StaffWorkForm()

    staff_list = Staff.objects.all() 
    context = {
        'form': form,
        'staff_list': staff_list, 
    }
    return render(request, 'staff_work_create.html', context=context)




def staff_work_view(request):
    staff_work = Staff_work.objects.all()  # Barcha ish ma'lumotlari olinadi
    context = {
        'staff_work': staff_work  # 'staff_work' nomi bilan shablonga yuboriladi
    }
    return render(request, 'staff.html', context=context)



def staff_payment_list(request):
    staff_payment = models.staff_payments.objects.all()  # Model nomini tekshiring
    context = {
        'staff_payment_list': staff_payment  # 'staff_payment_list' nomi bilan shablonga yuboriladi
    }
    return render(request, 'staff_payment.html', context=context)



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Foydalanuvchini autentifikatsiya qilish
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Foydalanuvchini tizimga kiritish
            login(request, user)
            messages.success(request, 'Tizimga muvaffaqiyatli kirdingiz!')
            return redirect('home')  # `home` URL-ga yo'naltirish (o'zgartiring)
        else:
            # Xatolik xabarini ko'rsatish
            messages.error(request, 'Foydalanuvchi nomi yoki parol noto‘g‘ri!')
    return render(request, 'login.html')


# Hisobot
def hisobot(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Ma'lumotlar bazasidan qiymatlarni hisoblash
    total_purchase_sum = models.Purchase.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense_sum = models.staff_payments.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    staff_payment_sum = models.Staff.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    sold_books_sum = models.Book_model.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0

    # Sof foyda hisoblash
    net_profit = sold_books_sum - (total_purchase_sum + total_expense_sum + staff_payment_sum)

    # Shablonga ma'lumotlarni yuborish
    context = {
        'total_purchase_sum': total_purchase_sum,
        'total_expense_sum': total_expense_sum,
        'staff_payment_sum': staff_payment_sum,
        'sold_books_sum': sold_books_sum,
        'net_profit': net_profit,
    }

    return render(request, 'income_calc.html', context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Foydalanuvchini autentifikatsiya qilish
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)  # Foydalanuvchini tizimga kiriting
                return redirect('book_model')  # Agar muvaffaqiyatli kirgan bo'lsa, `book_model` ga yo'naltiradi
            else:
                # Foydalanuvchi yoki parol noto'g'ri
                return render(request, 'home/login.html', {'form': form, 'error': 'Noto\'g\'ri foydalanuvchi yoki parol'})
    else:
        form = LoginForm()
    return render(request, 'login_two.html', {'form': form})