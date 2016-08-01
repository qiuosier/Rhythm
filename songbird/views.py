from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from google.appengine.api import urlfetch
from xml.etree import ElementTree
from songbird import xmlns
from rhythm.private import WHO_GITLAB_TOKEN
import datetime

# Create your views here.
def index(request):
    return HttpResponse("Welcome to Songbird, a messenger of Qiu's Sparrow.")


def timeline(request):
    if request.GET.get('id','') == 'davelab_who':
        token = '?private_token=' + WHO_GITLAB_TOKEN
        xml_urls = [
            'https://gitlab.oit.duke.edu/davelab/who_webform/commits/QiuFeature.atom' + token,
            'https://gitlab.oit.duke.edu/davelab/who_webform/commits/QiuTest.atom' + token,
            'https://gitlab.oit.duke.edu/davelab/who_webform/commits/master.atom' + token,
        ]
        branches = []
        commits = []
        master_branch = None
        for i, url in enumerate(xml_urls):
            r = urlfetch.fetch(url, method='GET', deadline=20)
            root = ElementTree.fromstring(r.content)
            branches.append(root.find(xmlns.Gitlab.title).text)
            if 'master' in branches[i]:
                master_branch = i
            for entry in root.findall(xmlns.Gitlab.entry):
                commit = {
                    'title': entry.find(xmlns.Gitlab.title).text,
                    'badge': entry.find(xmlns.Gitlab.badge).get('url'),
                    'time': datetime.datetime.strptime(
                        entry.find(xmlns.Gitlab.time).text.rsplit('-', 1)[0],
                        '%Y-%m-%dT%H:%M:%S'
                        ),
                    'branch': i + 1,
                    'merge': None,
                }
                # Check duplicates
                if not any(c['time'] == commit['time'] for c in commits):
                    commits.append(commit)
        commits = sorted(commits, key=lambda k: k['time'], reverse=True)
        # Check merge
        for commit in commits:
            if 'Merged branch' in commit['title']:
                l = commit['title'].replace('Merged branch ','').split(' into ')
                for i in [0,1]:
                    for j, b in enumerate(branches):
                        if l[i] in b:
                            l[i] = j
                            break
                f = l[0] + 1
                t = l[1] + 1
                commit['merge'] = {'span': abs(f - t), 'right': min(f, t), 'from': f}
        branches = ['Development', 'Testing', 'Production']
        return render(request, 'songbird/git_timeline.html', {
            'branches': branches,
            'commits': commits,
        })
    return HttpResponseBadRequest("Looks like you missed something")