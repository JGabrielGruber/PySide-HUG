class Login():
	client_id		= ""
	client_secret	= ""
	token			= False

	@classmethod
	def setCredentials(cls, client_id, client_secret):
		cls.client_id		= client_id
		cls.client_secret	= client_secret

	@classmethod
	def setToken(cls, token):
		cls.token	= token