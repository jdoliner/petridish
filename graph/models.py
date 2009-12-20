from django.db import models
try:
	from petridish.organism.models import Organism
except:
	pass

# Create your models here.
max_neighbors = 1000

class Vertex(models.Model):
	graph = models.ForeignKey('graph.Graph')
	def in_edges(self):
		return Edge.objects.filter(graph = self.graph, to = self.pk)
	def out_edges(self):
		return Edge.objects.filter(graph = self.graph, fr = self.pk)
	def neighbors(self):
		neighbors = []
		for e in self.out_edges():
			neighbors.append(Vertex.objects.filter(graph = self.graph, pk = e.to))
		return neighbors

class Edge(models.Model):
	graph = models.ForeignKey('graph.Graph')
	fr = models.ForeignKey('graph.Vertex', related_name = 'fr')
	to = models.ForeignKey('graph.Vertex', related_name = 'to')
	

class Graph(Organism):
	def v(self):
		return Vertex.objects.filter(graph=self.pk)
	def e(self):
		return Edge.objects.filter(graph=self.pk)
