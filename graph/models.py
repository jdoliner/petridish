from django.db import models
import random
import datetime
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
	def endv(self):
		fr = Vertex.objects.get(pk = self.fr)
		to = Vertex.objects.get(pk = self.to)
		return [fr, to]

class Graph(Organism):
	def v(self):
		return Vertex.objects.filter(graph=self.pk)
	def e(self):
		return Edge.objects.filter(graph=self.pk)
	def addv(self):
		v = Vertex()
		v.graph = self
		v.save()
		return v
	def adde(self, fr, to):
		e = Edge()
		e.graph = self
		e.fr = fr
		e.to = to
		e.save()
		return e
	def sanitize(self):
		self.born = datetime.datetime.now()
		self.generation = 0
		assert(self.dish)
		if (not self.id):
			self.save()
		else:
			for v in self.v():
				v.delete()
			for e in self.e():
				e.delete()
			self.save()
	#declaring a graph using a set of vertices and edges
	def G(self, V, E):
		self.sanitize()
		old_to_new = {}
		for oldv in V:
			newv = Vertex()
			newv.graph = self
			newv.save()
			old_to_new[oldv] = newv
		for olde in E:
			newe = Edge()
			newe.graph = self
			newe.fr = old_to_new[olde.fr]
			newe.to = old_to_new[olde.to]
			newe.save()
		
	def breed_subg_swp(self, mate):
		selfv = self.v()
		matev = mate.v()
		#select a subset of the vertices to induce subgraphs
		selfsubg = random.sample(selfv, random.randrange(len(selfv))+1)
		selfcomp = list(set(selfv) - set(selfsubg))
		matesubg = random.sample(matev, random.randrange(len(matev))+1)
		matecomp = list(set(selfv) - set(selfsubg))
		#which edges are entirely internal
		selfe_internal = self.e().filter(fr__in=selfsubg, to__in=selfsubg)
		matee_internal = mate.e().filter(fr__in=selfsubg, to__in=selfsubg)
		#edges that start in the subgraph but go outside
		selfe_cross = self.e().filter(fr__in=selfsubg).filter(to__in=selfcomp) 
		matee_cross = mate.e().filter(fr__in=matesubg).filter(to__in=matecomp)
		#associations to reconnect the subgraphs; map from selfcomp->matesubg and matecomp->selfsubg
		self_to_mate = {}
		for i in range(len(selfcomp)):
			self_to_mate[selfcomp[i]] = matesubg[i%len(matesubg)]
		mate_to_self = {}
		for i in range(len(matecomp)):
			mate_to_self[matecomp[i]] = selfsubg[i%len(selfsubg)]
		for e in selfe_cross:
			e.to = self_to_mate[e.to]
		for e in matee_cross:
			e.to = mate_to_self[e.to]
		g = Graph()
		g.dish = self.dish
		g.G(list(selfsubg) + list(matesubg), list(selfe_internal) + list(matee_internal) + list(selfe_cross) + list(matee_cross))
	def random(self, size, p):
		self.sanitize()
		for i in range(size):
			self.addv()
		for fr in self.v():
			for to in list(set(self.v()) - set([fr])): #no loops
				if(random.random() < p):
					self.adde(fr,to)
