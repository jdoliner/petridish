from django.db import models
from django import forms
from datetime import datetime

class Dish(models.Model):
	name = models.CharField(max_length=200)
	fitness = models.ForeignKey('function.Fitness_Function', null=True)
	generation = models.IntegerField()
	born = models.DateTimeField('birthdate')
	def __unicode__(self):
		return self.name
	def init(self, name):
		self.name = name
		self.generation = 0
		self.born = datetime.now()
	def organisms(generation = -1):
		if (generation == -1):
			generation = self.generation
		from petridish.organism.models import Organism
		return Organism.objects.filter(dish = self, generation = generation)
	def eval_fitness(self):
		from petridish.function.models import Fitness_Function
		f = Fitness_Function.objects.get(self.fitness)
		for o in self.organisms():
			try:
				o.fitness = f.call([o.unabstract()])
			except:
				o.fitness = -1
			o.save()

class Dish_Form(forms.Form):
	name = forms.CharField(max_length=200)

class Populate_form(forms.Form):
	type = forms.ChoiceField([('graph', 'graph')])
