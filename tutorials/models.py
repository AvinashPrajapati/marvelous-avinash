from unicodedata import name
from django.db import models
from django.urls import reverse

# Create your models here.
class Tags(models.Model):
    tagName = models.CharField(max_length=200, unique=True)
    tagUrl = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.tagName
    def get_absolute_url(self):
        return reverse('tutorials:tagged_post_list', args=[self.tagUrl])


class TutorialSeries(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('tutorials:series_post_list', args=[self.url])


class Tutorial(models.Model):
    STATUS_CHOICES =(
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    CATEGORY_CHOICES =(
        ('tutorial', 'Tutorial'),
        ('experiment', 'Experiment'),
        ('project', 'Project'),
    )
    title = models.CharField(max_length=240)
    Description = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    poster = models.ImageField(blank=True)
    content = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='experiment')
    series_name = models.ForeignKey(TutorialSeries, on_delete=models.CASCADE, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status =models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        # pass
        return reverse('tutorials:detailpage', args=[self.category, self.url])

