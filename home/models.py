from django.db import models, transaction
from datetime import datetime

class reference(models.Model):
    name  = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Gender(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Book_model(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(reference, on_delete=models.CASCADE, verbose_name="Kitob turi", related_name="book_category_references")
    price = models.FloatField(verbose_name="Kitob narxi")
    quantity = models.IntegerField(verbose_name="Kitob soni")
    image = models.ImageField(upload_to="media/", verbose_name="Kitob rasmi")
    description = models.TextField(verbose_name="Kitob tavsifi")
    created_at = models.DateField(auto_now_add=True, verbose_name="Yaratilgan sana")
    isDeleted = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class Staff(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    isDeleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Output(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)

class Staff_work(models.Model):
    staff = models.ForeignKey(Staff , on_delete=models.CASCADE)
    time_work = models.IntegerField()
    price = models.FloatField()
    isDeleted = models.BooleanField(default=False)

class Cost(models.Model):
    name = models.ForeignKey(
        Book_model,
        on_delete=models.CASCADE,
        related_name="cost_name_references"
    )
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)

class Income(models.Model):
    sold_book = models.ForeignKey(Book_model, on_delete=models.CASCADE, related_name="Income_category_references")
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)

class staff_payments(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="🧍‍♂️Hodimlar")
    price = models.FloatField(verbose_name="💲Maosh")
    created_at = models.DateField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for {self.staff.name} - {self.price} so'm"
    



class Product(models.Model):
    name = models.CharField(max_length=100)  
    description = models.TextField()  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    stock = models.IntegerField()  
    category = models.CharField(max_length=50)  
    image = models.ImageField(upload_to='product', blank=True, null=True) 
    isDeleted = models.BooleanField(default=False)  

    def __str__(self):
        return self.name


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')  
    quantity = models.PositiveIntegerField()  
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  
    sale_date = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        with transaction.atomic():  # Barcha operatsiyalarni bir vaqtning o‘zida bajarish
            product = self.product
            if self.quantity > product.stock:
                raise ValueError("Omborda yetarli mahsulot yo'q")

            self.total_price = self.quantity * product.price
            product.stock -= self.quantity
            product.save()

            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} dona sotildi"
    

