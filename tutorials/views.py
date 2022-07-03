from unicodedata import category
from django.db.models import Q
from django.shortcuts import redirect, render
from .models import Tags, Tutorial, TutorialSeries
from django.core.paginator import Paginator
from chat.models import Message, CustomUser

# Create your views here.
def redirectPage(request):
    return redirect('tutorials:listpage', list_url='tutorials')


def listView(request, list_url): 
    checkList = ['tutorial', 'experiment', 'project']
    tutQuery = None
    
    path = request.path
    path_list = path.split('/')
    url = path_list[1]
    
    if list_url not in checkList:
        return redirect('tutorials:listpage', list_url='tutorial')

    if list_url == 'experiment':
        tutQuery = Tutorial.objects.filter(category=list_url, status='published')
    if list_url == 'project':
        tutQuery = Tutorial.objects.filter(category=list_url, status='published')
    if list_url == 'tutorial':
        tutQuery = Tutorial.objects.filter(category=list_url, status='published')

    paginator = Paginator(tutQuery, 15)
    page_number = request.GET.get('page')
    tutQuery = paginator.get_page(page_number)

    data = {'tutList':tutQuery, 'url':url}
    return render(request, 'tutorials/tutorials.html',data) 



def detailView(request, category, url): 
    tutQuery = None
    messages = Message.objects.filter(room__url = url).order_by('-date_added')
    checkList = ['tutorial', 'experiment', 'project']
    if category not in checkList:
        return redirect('tutorials:listpage', list_url='tutorial')

    if category == 'experiment':
        try:
            tutQuery = Tutorial.objects.get(category=category, url=url, status='published')
        except Exception as error:
            return redirect('tutorials:listpage', list_url=category)

    if category == 'project':
        try:
            tutQuery = Tutorial.objects.get(category=category, url=url, status='published')
        except Exception as error:
            return redirect('tutorials:listpage', list_url=category)

    if category == 'tutorial':
        try:
            tutQuery = Tutorial.objects.get(category=category, url=url, status='published')
        except Exception as error:
            return redirect('tutorials:listpage', list_url=category)

    return render(request, 'tutorials/detail.html',{'tut':tutQuery,'message_list':messages})



def searchView(request):
    query = request.GET.get('q')
    if len(query) > 70 or len(query) == 0:
        allposts = Tutorial.objects.none()
        print(allposts)
    else:
        allposts = Tutorial.objects.filter(Q(title__icontains=query) | Q(Description__icontains=query) | Q(tags__tagName__icontains=query) | Q(series_name__name__icontains=query))
        print(allposts)
    data = {
        'allposts':allposts,
        'query':query,
    }
    return render(request, 'tutorials/search.html', data)



def tagged_post_list(request, tag_url):
    tagName = None
    try:
        tagName = Tags.objects.get(tagUrl = tag_url)
    except Exception as error:
        return redirect('tutorials:pageredirect')
    tutByTag = Tutorial.objects.filter(tags__tagUrl = tag_url)
    return render(request, 'tutorials/tagged-post-list.html', {'tagName':tagName, 'tutByTag':tutByTag})



def series_post_list(request, series_url):
    seriesName = None
    try:
        seriesName = TutorialSeries.objects.get(url = series_url)
    except Exception as error:
        return redirect('tutorials:pageredirect')
    tutBySeriesName = Tutorial.objects.filter(series_name__url = series_url)
    print(tutBySeriesName)
    return render(request, 'tutorials/series-post-list.html', {'tutBySeriesName':tutBySeriesName, 'seriesName':seriesName})
    

def touch(request):
    return render(request, 'tutorials/touch.html')

def portfolio(request):
    return render(request, 'portfolio.html')
    