from django.template import Context, loader
from django.http import HttpResponse
from petridish.organism.models import Organism

def organism_id(request, organism_id):
	organism = Organism.objects.filter(pk = organism_id)[0]
	template = loader.get_template('organism/organism_id.html')
	context = Context({'organism': organism})
	return HttpResponse(template.render(context))
