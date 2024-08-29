from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Wallet

def wallet_balance(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        return JsonResponse({'error': 'Wallet does not exist for this user.'}, status=404)

    return JsonResponse({'balance': wallet.balance})


@csrf_exempt
def add_funds(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return JsonResponse({'error': 'Wallet does not exist for this user.'}, status=404)

        amount = request.POST.get('amount')

        # Validate amount
        if not amount or not amount.replace('.', '', 1).isdigit():
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({'error': 'Invalid amount format'}, status=400)

        wallet.balance += amount
        wallet.save()
        wallet.save_json()

        return JsonResponse({'message': 'Funds added successfully', 'balance': wallet.balance})

    return JsonResponse({'error': 'Invalid request method'}, status=405)
