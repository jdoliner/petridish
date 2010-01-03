from django.db import models

class Evolver(models.Model):
	name = models.CharField(max_length = 20)
