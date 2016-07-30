from django.shortcuts import render

# Create your views here.
def index(request):
    return timeline(request)


def timeline(request):
    branches = [
        {
            'name': 'Development',
        },
        {
            'name': 'Testing',
        },
        {
            'name': 'Production',
        },
    ]
    return render(request, 'songbird/git_timeline.html', {
        'branches': branches,
    })