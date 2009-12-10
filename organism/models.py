from django.db import models
try:
	from petridish.dish.models import Dish
except:
	pass

# Create your models here.

class Organism(models.Model):
	born = models.DateTimeField('birthdate')
	code = models.CharField(max_length=9999)
	dish = models.ForeignKey('dish.Dish')
	generation = models.IntegerField()
	def __unicode__(self):
		return self.code
