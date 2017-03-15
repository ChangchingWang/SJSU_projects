from flask import Flask
import sys
import requests

#https://github.com/sithu/assignment1-config-example
sysArg1 = sys.argv[1]

app = Flask(__name__)

@app.route("/v1/<fileName>")
def hello(fileName):
	global sysArg1
	urlStr = sysArg1.replace("https://", "")
	fields = urlStr.split("/")
	owner = fields[1]
	repo = fields[2]
	url="https://api.github.com/repos/" + owner + "/" + repo + "/contents/" + fileName
	headers = {'Accept' : 'application/vnd.github.v3.raw'}
	r = requests.get(url, headers=headers)
	return r.text;

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
