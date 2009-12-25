from django.db import models
try:
	from petridish.dish.models import Dish
	from petridish.graph.models import Graph
except:
	pass

# Create your models here.

class Organism(models.Model):
	born = models.DateTimeField('birthdate')
	dish = models.ForeignKey('dish.Dish')
	generation = models.IntegerField()
