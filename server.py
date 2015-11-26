import json

from bottle import response
from bottle import run as bottle_run
from bottle import get, HTTPResponse


@get('/')
def home():
	api = {"School": "ENISo",
		    "University": "Soussa"}
	return HTTPResponse(api,
						content_type="application/json", status=200)

def main():
   bottle_run(host='0.0.0.0', port=1028, reloader=True)
   response.content_type = 'application/json'

if __name__ == '__main__':
    main()
