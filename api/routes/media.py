import	hug

from	lib.veryx	import auth
from	controllers	import media as controllerMedia

@hug.get('/', requires=auth.basicAccess())
def get_index(
	response
):
	return controllerMedia.getMedias(response)

@hug.get('/{id}', requires=auth.basicAccess())
def get_byId(
	id: hug.types.number,
	response
):
	return controllerMedia.getMediaById(response, id)

@hug.post('/', requires=auth.basicAccess())
def post_data(
	request,
	response
):
	return controllerMedia.newMedia(request, response)

@hug.delete('/{id}', requires=auth.basicAccess())
def delete_data(
	id: hug.types.number,
	response
):
	return controllerMedia.deleteMediaById(response, id)
