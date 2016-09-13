from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os

def login(request):
    oauth_flow = flow_from_clientsecrets(
        os.path.join(settings.BASE_DIR, 'authentication' ,'client_secrets.json'),
        scope=['profile','email'],
        redirect_uri=request.build_absolute_uri().split('?')[0]
    )
    code = request.GET.get('code', '')
    if not code:
        auth_uri = oauth_flow.step1_get_authorize_url()
        return HttpResponseRedirect(auth_uri)
    try:
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return HttpResponse('Failed to upgrade the authorization code.')
    request.session['user_id'] = credentials.id_token['sub']
    request.session['email'] = credentials.id_token['email']
    request.session['credentials'] = credentials
    return HttpResponseRedirect('/songbird/')


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/songbird/')