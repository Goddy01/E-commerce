from django.conf import settings
import requests, json

class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    url = 'https://api.paystack.co/transaction/initialize'

    def verify_payment(self, ref, *args, **kwargs):
        # path = f'/transaction/verify/{ref}'
        # url = 'https://api.paystack.co/transaction/initialize'

        headers = {
            "Authorization": "Bearer {}".format(self.PAYSTACK_SECRET_KEY),
            "Content-Type": "application/json",
            }
        
        r = requests.get(self.url, headers=headers)
        if r.status_code == 200:
            response = r.json()
            return response['status'], response['data']
        response = response.json()
        return response['status'], response['message']