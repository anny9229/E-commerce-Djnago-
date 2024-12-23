
from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, OrderPlaced, Payment, Product, Cart,STATE_CHOICES
from django.db.models import Count , Q
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

def contect(request):
    return render(request, 'app/contact.html')

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

class CtaegoryTitle(View):
     def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"You are successfully register")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/customerregistration.html',locals())
    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")            
        return render(request,'app/profile.html',locals())
    

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.user = request.user
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")   
        return redirect("address")
    

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request,'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
             value = p.quantity *  p.product.discounted_price
             famount = famount + value
        totalamount = famount + 40
        return render(request,'app/checkout.html',locals())

def plus_cart(request):
    try:
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
            if c:
                c.quantity += 1
                c.save()
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = 0
                for p in cart:
                    value = p.quantity * p.product.discounted_price
                    amount += value
                totalamount = amount + 40
                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart not found'}, status=404)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
def minus_cart(request):
    try:
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
            if c:
                c.quantity -= 1
                c.save()
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = 0
                for p in cart:
                    value = p.quantity * p.product.discounted_price
                    amount += value
                totalamount = amount + 40
                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart not found'}, status=404)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
def remove_cart(request):
    try:
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
            if c:
                c.delete()
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = 0
                for p in cart:
                    value = p.quantity * p.product.discounted_price
                    amount += value
                totalamount = amount + 40
                data = {
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart not found'}, status=404)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    addresses = Customer.objects.filter(user=user)
    totalamount = sum(item.total_cost for item in cart_items) + 40  # Rs. 40 as shipping cost

    if request.method == 'POST':
        selected_address_id = request.POST.get('custid')
        if not selected_address_id:
            messages.error(request, "Please select a shipping address.")
            return redirect('checkout')
        # Store in session to pass to payment view
        request.session['selected_address_id'] = selected_address_id
        request.session['total_amount'] = totalamount
        return redirect('payment')

    context = {
        'cart_items': cart_items,
        'addresses': addresses,
        'totalamount': totalamount,
    }
    return render(request, 'app/checkout.html', context)

@login_required
# views.py
@login_required
def payment(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    totalamount = request.session.get('total_amount', 0)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('checkout')

    if request.method == 'POST':
        address_choice = request.POST.get('address_choice')
        if address_choice == 'existing':
            selected_address_id = request.POST.get('custid')
            try:
                customer = Customer.objects.get(id=selected_address_id, user=user)
            except Customer.DoesNotExist:
                messages.error(request, "Selected address does not exist.")
                return redirect('payment')
        elif address_choice == 'custom':
            # Get custom address details
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            locality = request.POST.get('locality')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')

            # Validate required fields
            if not all([name, mobile, locality, city, state, zipcode]):
                messages.error(request, "Please fill all the address fields.")
                return redirect('payment')
            
            # Create new Customer entry
            customer = Customer.objects.create(
                user=user,
                name=name,
                mobile=mobile,
                locality=locality,
                city=city,
                state=state,
                zipcode=zipcode
            )
        else:
            messages.error(request, "Invalid address choice.")
            return redirect('payment')
        
        # Create a Payment object
        payment = Payment.objects.create(
            user=user,
            amount=totalamount,
            paid=False  # Cash on Delivery
        )
        
        # Create OrderPlaced entries for each cart item
        for item in cart_items:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                payment=payment
            )
        
        # Clear the cart
        cart_items.delete()
        
        messages.success(request, "Your order has been placed successfully.")
        return redirect('orders')  # Ensure you have an 'orders' view

    # Correctly use the imported STATE_CHOICES
    existing_addresses = Customer.objects.filter(user=user)
    context = {
        'cart_items': cart_items,
        'totalamount': totalamount,
        'existing_addresses': existing_addresses,
        'states': [choice[0] for choice in STATE_CHOICES],  # Use imported STATE_CHOICES
    }
    return render(request, 'app/payment.html', context)


@login_required
def orders(request):
    user = request.user
    orders = OrderPlaced.objects.filter(user=user).order_by('-ordered_date')
    context = {
        'orders': orders,
    }
    return render(request, 'app/orders.html', context)