from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from google.appengine.ext import blobstore
import io
import datetime
import cloudstorage as gcs

GCLOUD_BUCKET = 'nest-rhythm.appspot.com'

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        bucket_path = GCLOUD_BUCKET + '/' + request.session['user_id']
        stats = gcs.listbucket('/' + bucket_path)
        files = []
        for stat in stats:
            files.append({
                'name': stat.filename,
                'time': datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'size': stat.st_size,
            })
        upload_url = blobstore.create_upload_url(success_path='/files/', gs_bucket_name=bucket_path)
    else:
        files = None

    if request.method == 'POST':
        print request.POST.dict()
        # file_info = request.get_file_infos()[0]
        # print file_info.filename,
        # print file_info.gs_object_name

    return render(request, 'files/list_files.html', {
        'files': files,
        'upload_url': upload_url,
    })


def upload(request):
    pass
