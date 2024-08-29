import json
from django.conf import settings
from django.db import models

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)  # Default $100

    def to_json(self):
        return json.dumps({'balance': str(self.balance)})

    def save_json(self):
        with open(f'wallet_{self.user.username}.json', 'w') as f:
            json.dump({'balance': str(self.balance)}, f)