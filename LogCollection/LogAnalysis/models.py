# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from webpage.models import *


# Create your models here.
class PlotColor(models.Model):
    name = models.TextField()
    character = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PlotMarker(models.Model):
    name = models.TextField()
    character = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PlotLineStyle(models.Model):
    name = models.TextField()
    character = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MLModel(models.Model):
    name = models.TextField()
    plot_color = models.ForeignKey(PlotColor, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    line_style = models.ForeignKey(PlotLineStyle, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    line_width = models.IntegerField(default=1)
    marker = models.ForeignKey(PlotMarker, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class ScoreStatistic(models.Model):
    job = models.ForeignKey(Job, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    model = models.ForeignKey(MLModel, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    dataset_num = models.IntegerField(null=False)
    score = models.FloatField()
    training_time = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    duration = models.FloatField(default=0.0)

    class Meta:
        ordering = ('-job', '-model', '-training_time',)


def InitPlotColors():
    if not PlotColor.objects.all():
        PlotColor.objects.create(name='blue', character='#0000FF')
        PlotColor.objects.create(name='green', character='#008000')
        PlotColor.objects.create(name='red', character='#FF0000')
        PlotColor.objects.create(name='cyan', character='#00FFFF')
        PlotColor.objects.create(name='magenta', character='#FF00FF')
        PlotColor.objects.create(name='yellow', character='#FFFF00')
        PlotColor.objects.create(name='purple', character='#800080')
        PlotColor.objects.create(name='black', character='#000000')
        PlotColor.objects.create(name='white', character='#FFFFFF')
        PlotColor.objects.create(name='brown', character='#A52A2A')
        PlotColor.objects.create(name='gold', character='#FFD700')
        PlotColor.objects.create(name='silver', character='#C0C0C0')
        PlotColor.objects.create(name='gray', character='#808080')
        PlotColor.objects.create(name='orange', character='#FFA500')
        PlotColor.objects.create(name='pink', character='#FFC0CB')


def InitPlotMarkers():
    if not PlotMarker.objects.all():
        PlotMarker.objects.create(name='point marker', character='.')
        PlotMarker.objects.create(name='pixel marker', character=',')
        PlotMarker.objects.create(name='circle marker', character='o')
        PlotMarker.objects.create(name='triangle_down marker', character='v')
        PlotMarker.objects.create(name='triangle_up marker', character='^')
        PlotMarker.objects.create(name='triangle_left marker', character='<')
        PlotMarker.objects.create(name='triangle_right marker', character='>')
        PlotMarker.objects.create(name='tri_down marker', character='1')
        PlotMarker.objects.create(name='tri_up marker', character='2')
        PlotMarker.objects.create(name='tri_left marker', character='3')
        PlotMarker.objects.create(name='tri_right marker', character='4')
        PlotMarker.objects.create(name='square marker', character='s')
        PlotMarker.objects.create(name='pentagon marker', character='p')
        PlotMarker.objects.create(name='star marker', character='*')
        PlotMarker.objects.create(name='hexagon1 marker', character='h')
        PlotMarker.objects.create(name='hexagon2 marker', character='H')
        PlotMarker.objects.create(name='plus marker', character='+')
        PlotMarker.objects.create(name='x marker', character='x')
        PlotMarker.objects.create(name='diamond marker', character='D')
        PlotMarker.objects.create(name='vline marker', character='|')
        PlotMarker.objects.create(name='hline marker', character='_')


def InitPlotLineStyles():
    if not PlotLineStyle.objects.all():
        PlotLineStyle.objects.create(name='solid line style', character='-')
        PlotLineStyle.objects.create(name='dashed line style', character='--')
        PlotLineStyle.objects.create(name='dash-dot line style', character='-.')
        PlotLineStyle.objects.create(name='dotted line style', character=':')


def InitMLModel():
    InitPlotColors()
    InitPlotLineStyles()
    InitPlotMarkers()
    if not MLModel.objects.all():
        MLModel.objects.create(name='naive bayes', plot_color_id=2, line_width=1, line_style_id=1)
        MLModel.objects.create(name='mlp', plot_color_id=1, line_width=1, line_style_id=1)
        MLModel.objects.create(name='svm', plot_color_id=14, line_width=1, line_style_id=1)
