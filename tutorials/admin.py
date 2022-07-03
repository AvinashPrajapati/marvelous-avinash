from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Tags, Tutorial, TutorialSeries

class TutorialAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    prepopulated_fields = {'url':('title',)}
    list_display = ('id','title', 'url', 'created', 'updated')
class TutorialSeriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url':('name',)}
    list_display = ('id','name', 'url')
class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'tagUrl':('tagName',)}
    list_display = ('id','tagName', 'tagUrl')




admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(TutorialSeries, TutorialSeriesAdmin)
admin.site.register(Tags, TagsAdmin)
