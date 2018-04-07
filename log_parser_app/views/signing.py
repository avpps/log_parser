from django.views.decorators.http import require_http_methods

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from django.core.signing import Signer
from django.contrib.auth.models import User

from log_parser_app.lib.validators import validate_new_user


@require_http_methods(['GET'])
def signup_init(request):

    template = loader.get_template(
        'log_parser_app/signup.html')

    return HttpResponse(template.render({}, request))


@require_http_methods(['POST'])
def signup(request):

    user_data = validate_new_user(**request.POST.dict())
    User.objects.create_user(**user_data)

    return HttpResponseRedirect(reverse('log_parser_app:index'))


@require_http_methods(['POST'])
def signin_init(request):
    pass


@require_http_methods(['POST'])
def signin(request):
    pass


@require_http_methods(['POST'])
def signout(request):
    pass
