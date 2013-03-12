from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register(method='GET')
def sayhello(request):
    return simplejson.dumps({'message':'Hello World'})
