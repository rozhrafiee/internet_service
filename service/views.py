from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Service, PurchasedService
from wallet.models import Wallet
from accounts.models import User

def service_list(request):
    services = Service.objects.all()
    service_list = [{'id': service.id, 'name': service.name, 'price': service.price} for service in services]
    return JsonResponse({'services': service_list})

@csrf_exempt
def buy_service(request, service_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            service = Service.objects.get(id=service_id)
            wallet = Wallet.objects.get(user=user)

            if wallet.balance >= service.price:
                wallet.balance -= service.price
                wallet.save()
                PurchasedService.objects.create(user=user, service=service)
                wallet.save_json()
                return JsonResponse({'message': 'Service purchased successfully'})
            else:
                return JsonResponse({'error': 'Insufficient funds'})
        return JsonResponse({'error': 'User not authenticated'})

    return JsonResponse({'error': 'Invalid request method'})

def shopped_services(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        purchased_services = PurchasedService.objects.filter(user=user)
        service_list = [{'id': ps.service.id, 'name': ps.service.name, 'price': ps.service.price} for ps in purchased_services]
        return JsonResponse({'purchased_services': service_list})
    return JsonResponse({'error': 'User not authenticated'})
