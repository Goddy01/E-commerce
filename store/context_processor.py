from Accounts.models import User
from django.shortcutsimport request
def website_conent(request):
    try:
        user = User.objects.get(device=request.session['device'])
    except:
        device = str(uuid.uuid4())
        request.session['device'] = device
        user = User.objects.create(
            fullname=request.session['device'],
            username=request.session['device'],
            email=request.session['device'] + '@gmail.com',
            address=request.session['device'],
            first_phone_num='1',
            device=request.session['device'],

            )
    return user