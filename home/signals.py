from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from .models import staff_payments, Staff_work, Staff, Book_model, Cost

# Cost modeliga oid signal
@receiver([post_save, post_delete], sender=Cost)
def signal_quantity(sender, instance, **kwargs):
    # Correcting the typo from 'objekt' to 'objects'
    cost_list = Cost.objects.filter(name=instance.name)
    
    # Correcting the typo from 'objekt' to 'objects'
    book = Book_model.objects.get(name=instance.name)
    
    cost_quantity = 0
    
    for i in cost_list:
        cost_quantity += i.quantity
        
    book.quantity = cost_quantity
    book.save()

# Staff modeliga oid signal
@receiver([post_save, post_delete], sender=staff_payments)
@receiver([post_save, post_delete], sender=Staff_work)
def signal_staff_balance(sender, instance, **kwargs):
    print("----------------------------------------------")
    staff = Staff.objects.get(pk=instance.staff.pk)
    staff_payments_list = staff_payments.objects.filter(staff=staff)
    staff_work_list = Staff_work.objects.filter(staff=staff)

    total_payment_sum = 0
    total_work_sum = 0

    for payment in staff_payments_list:
        total_payment_sum += payment.price

    for work in staff_work_list:
        total_work_sum += work.price

    staff.balance = total_work_sum - total_payment_sum
    staff.save()
