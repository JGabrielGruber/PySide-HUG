import	hug

from	routes		import index

api = hug.API(__name__)

@hug.extend_api('')
def index_api():
	return [index]
