from .models import  Tags, TutorialSeries

def Gettags(request):
    alltags = Tags.objects.all()
    allseries = TutorialSeries.objects.all()
    return {
        'alltags': alltags,
        'allseries': allseries,
    }