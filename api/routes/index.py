import	hug

from 	routes	import auth, media

@hug.extend_api('/media')
def cliente_api():
	return [media]

@hug.extend_api('/oauth')
def auth_api():
	return [auth]