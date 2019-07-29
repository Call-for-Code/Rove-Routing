#!flask/bin/python
from flask import Flask, request
from routing import routePath

app = Flask(__name__)

@app.route('/api/route/', methods = ['GET'])
def routeIt():
	args = request.args.to_dict()
	if 'start' not in args or 'end' not in args:
		abort(400)
	res = routePath(args['start'], args['end'])
	print(res)
	# if len(res['route']) < 3:
	# 	abort(400)
	return res, 200 

if __name__ == '__main__':
    app.run(debug=True)
