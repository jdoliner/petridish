from django.shortcuts import render_to_response
from petridish.function.models import Function

def function_id(request, f_id):
	import re
	function = Function.objects.get(id = f_id)
	parse = re.search(r'^def (\w+)(\([a-zA-Z0-9_, ]*\)):(.*)', function.code, re.DOTALL)
	return render_to_response('function/function_id.html', {'name': parse.groups(0)[0], 'args': parse.groups(0)[1], 'body': parse.groups(0)[2]})
