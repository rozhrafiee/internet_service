from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from wallet.models import Wallet

@csrf_exempt
def provider_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            return JsonResponse({'error': 'Passwords do not match'})

        user = User.objects.create(
            username=username,
            email=email,
            password=password,
            is_provider=True,
            is_active=False
        )
        return JsonResponse({'message': 'Provider account created, pending admin approval'})

@csrf_exempt
def customer_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            return JsonResponse({'error': 'Passwords do not match'})

        user = User.objects.create(
            username=username,
            email=email,
            password=password,
            is_customer=True
        )

        Wallet.objects.create(user=user, balance=100.00)

        request.session['user_id'] = user.id
        return JsonResponse({'message': 'Customer account created and logged in'})

