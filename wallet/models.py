import json
from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)  # Default $100

    def save_json(self):
        with open(f'wallet_{self.user.username}.json', 'w') as f:
            json.dump({'balance': str(self.balance)}, f)
