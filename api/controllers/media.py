import	json
import	os
import	random
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_500
from	datetime	import datetime

from	controllers		import auth

def getMedias(response):
	try:
		return load("medias.json")
	except Exception:
		response.status = HTTP_500
		return { "error": "unexpected_exception" }

def getMediaById(response, id):
	try:
		for media in load("medias.json"):
			if media['id'] == id:
				return media
		response.status = HTTP_500
		return { "error": "not_found" }
	except Exception:
		response.status = HTTP_500
		return { "error": "unexpected_exception" }

def newMedia(request, response, body):
	try:
		filename	= request.headers['FILENAME']
		save({
			"id": random.randint(0, 99999),
			"filename": filename,
			"timestamp": str(datetime.now())
		}, "medias.json")
		if not os.path.exists('./uploads'):
			os.makedirs('./uploads')
		with open('./uploads/' + filename, 'wb') as file:
			file.write(body['media'] if isinstance(body['media'], (bytes, bytearray)) else str.encode(body['media']))
			file.close()
		return filename
	except Exception as e:
		print(e)
		response.status = HTTP_500
		return { "error": "unexpected_exception" }

def deleteMediaById(response, id):
	try:
		return
	except Exception:
		response.status = HTTP_500
		return { "error": "unexpected_exception" }

def save(data, fileName):
	file		= open("./.cache/" + fileName, "r+")
	file_open	= file.read()
	if (isJSON(file_open)):
		content	= json.loads(file_open)
	else:
		content	= []
	content.append(data)
	file.close()
	open("./.cache/"  + fileName, "w").close()
	file	= open("./.cache/"  + fileName, "r+")
	file.write(json.dumps(content))
	file.close()

def load(fileName):
	if not os.path.exists('./.cache'):
		os.makedirs('./.cache')
	if os.path.exists('./.cache/' + fileName):
		with open('./.cache/' + fileName, mode='rb') as read_file:
			return	json.load(read_file)
	else:
		with open('./.cache/' + fileName, mode='w') as write_file:
			write_file.write(json.dumps([]))
		load(fileName)

def isJSON(file):
	try:
		json_object = json.loads(file)
	except:
		return False
	return True