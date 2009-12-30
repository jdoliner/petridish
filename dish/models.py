from django.db import models
from django import forms
from datetime import datetime

class Dish(models.Model):
	name = models.CharField(max_length=20)
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

class Dish_form(forms.Form):
	name = forms.CharField(max_length=20)

class Populate_form(forms.Form):
	type = forms.ChoiceField([('graph', 'graph')])

class Properties_form(forms.Form):
	from petridish.function.models import Fitness_Function
	name = forms.CharField(max_length=20)
	functions = Fitness_Function.objects.all()
	fitness_f = forms.ChoiceField(map(lambda f: (f.id, f.name), functions))
