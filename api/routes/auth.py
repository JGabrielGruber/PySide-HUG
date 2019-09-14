import	hug

from	controllers	import auth
from	libraries.veryx	import auth as veryx

@hug.post('/token', version=1)
def get_token(
	grant_type: hug.types.text,
	client_id: hug.types.text,
	client_secret: hug.types.text,
	response
):
	return auth.getToken(response, grant_type, client_id, client_secret)