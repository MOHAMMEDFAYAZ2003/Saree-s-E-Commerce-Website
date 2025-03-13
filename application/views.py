from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from .forms import SignUpForm, SignInForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .models import Product,Cart,Saree,SilkSaree,CottonSaree,FeaturedSaree,TrendingSarees

@login_required
def index_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    sarees = Saree.objects.all()
    trending_sarees=TrendingSarees.objects.all()
    silk_sarees =SilkSaree.objects.all()
    cotton_sarees = CottonSaree.objects.all()
    featured_sarees = FeaturedSaree.objects.all()
    return render(request, 'index.html',{'cart_items':cart_items,
                                         'sarees':sarees,
                                         'silk_sarees':silk_sarees,
                                         'cotton_sarees':cotton_sarees,
                                         'featured_sarees':featured_sarees,
                                         'trending_sarees':trending_sarees
                                         })

@login_required
def product_view(request, product_id):
    print(f"Fetching product with ID: {product_id}")  # Debugging print

    # Try fetching from Saree first
    saree = Saree.objects.filter(product_id=product_id).first()
    model_name = "Saree" if saree else None  # Store model name

    # If not found in Saree, check FeaturedSaree
    if not saree:
        print("Product not found in Saree, checking FeaturedSaree")
        saree = FeaturedSaree.objects.filter(product_id=product_id).first()
        model_name = "FeaturedSaree" if saree else None  # Update model name

    # If still not found, return 404 response
    if not saree:
        print("Product not found in any model")
        return HttpResponse("Product not found", status=404)

    print(f"Product found: {saree}")  # Debugging print
    print(f"Passing to template -> model_name: {model_name}, product_id: {product_id}")
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'product.html', {
        'cart_items':cart_items,
        'title': saree.title,
        'description': saree.description,
        'image': saree.image.url if saree.image else '',
        'saree_model': saree.saree_model,
        'about_item': saree.about_item,
        'price': saree.price,
        'color': saree.color,
        'model_name': model_name,  
        'product_id': product_id, 
    })


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html',{'cart_items':cart_items,'total_price':total_price})

def signup_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken!")
                return render(request, 'signup.html', {'form': form})

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            messages.success(request, "Account created successfully! Please sign in.")
            return redirect('signin')

    return render(request, 'signup.html', {'form': form})

def signin_view(request):
    form = SignInForm()
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data['email_or_username']
            password = form.cleaned_data['password']

            user = User.objects.filter(email=email_or_username).first()
            if user is None:
                user = User.objects.filter(username=email_or_username).first()

            if user and user.check_password(password):
                login(request, user)
                messages.success(request, "Successfully Logged in!")
                return redirect('/')
            else:
                messages.error(request, "Invalid Credentials")

    return render(request, 'signin.html', {'form': form})


@login_required
def add_to_cart(request, model_name, product_id):
    model_name = model_name.lower()  # Convert to lowercase

    # Identify which model to use
    if model_name == "saree":
        product_model = Saree
    elif model_name == "featuredsaree":
        product_model = FeaturedSaree
    else:
        messages.error(request, "Invalid product type!")
        return redirect("cart")  # Redirect to cart page if model is invalid

    product = get_object_or_404(product_model, product_id=product_id)

    quantity = int(request.POST.get('quantity',1))
    # Get or create the cart item
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        content_type=ContentType.objects.get_for_model(product),
        object_id=product.product_id,  # Ensure you're using the correct ID field
        defaults={"quantity": quantity}
        
        
    )
    
    if not created:
        cart_item.quantity += 1  # Increase quantity if already in cart
        cart_item.save()

    messages.success(request, f"{product.title} added to cart!")

    return redirect("cart")  # Redirect to the cart page

@login_required
def remove_from_cart(request,cart_id):
    cart_item = get_object_or_404(Cart,id=cart_id,user=request.user)
    cart_item.delete()
    messages.success(request,"Item removed from cart.")
    return redirect('cart')

# import razorpay
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.conf import settings
# from django.contrib.auth.decorators import login_required

# # Initialize Razorpay client
# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET))

# @login_required
# def process_payment(request):
#     if request.method == "POST":
#         total_amount = request.POST.get("total_amount")

#         # Debugging: Print the received amount
#         print(f"Received total_amount: {total_amount}")

#         # Ensure total_amount is valid
#         try:
#             total_amount = int(float(total_amount) * 100)  # Convert to paisa
#         except (ValueError, TypeError):
#             return JsonResponse({"error": "Invalid amount format"}, status=400)

#         try:
#             order = client.order.create({
#                 "amount": total_amount,  # Must be an integer in paisa
#                 "currency": "INR",
#                 "payment_capture": "1"
#             })

#             # Debugging: Print Order Details
#             print(f"Order Created: {order}")

#             return JsonResponse({"order_id": order["id"]})
#         except Exception as e:
#             print(f"Error: {e}")
#             return JsonResponse({"error": str(e)}, status=400)

#     return JsonResponse({"error": "Invalid request"}, status=400)
