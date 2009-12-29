from django.db import models
from django import forms

class Dish(models.Model):
	name = models.CharField(max_length=200)
	fitness = models.ForeignKey('function.Function')
	generation = models.IntegerField()
	born = models.DateTimeField('birthdate')
	def __unicode__(self):
		return self.name

class Populate_form(forms.Form):
	type = forms.ChoiceField([('graph', 'graph')])
