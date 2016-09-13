from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from gcloud import storage
import io

GCLOUD_BUCKET = 'nest-rhythm.appspot.com'

# Create your views here.
def index(request):

    if 'user_id' in request.session:
        client = storage.Client()
        bucket = client.get_bucket(GCLOUD_BUCKET)
        files = list(bucket.list_blobs(prefix=request.session['user_id']))
    else:
        files = None
    return render(request, 'files/list_files.html', {
        'files': files,
    })


def upload(request):
    pass
