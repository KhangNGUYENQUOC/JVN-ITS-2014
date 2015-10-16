def application(env, start_response):
	start_response('200 ', [('Content-Type','text/html')])
	return [b"Hello world"]
