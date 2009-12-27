from django.db import models
import datetime
try:
	from petridish.dish.models import Dish
except:
	pass

# Create your models here.

class Organism(models.Model):
	born = models.DateTimeField('birthdate')
	dish = models.ForeignKey('dish.Dish')
	generation = models.IntegerField()
	def init(self, dish, generation):
		self.born = datetime.datetime.now()
		if (type(dish) == int):
			self.dish = Dish.objects.get(id = dish)
		else:
			self.dish = dish
		self.generation = generation
