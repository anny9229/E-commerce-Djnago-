from django.contrib import admin
from .models import Product,Customer,Cart,Payment,OrderPlaced
# Register your models here.
@admin.register(Product)
class productModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image','stock_status'] 
    list_filter = ('stock_status', 'category')
    search_fields = ('title',)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode'] 

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity'] 


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','paid']
    list_filter = ('paid', 'user')
    search_fields = ('user__username',)

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']
    list_filter = ['status', 'ordered_date']
    search_fields = ['user__username', 'customer__name', 'product__title']