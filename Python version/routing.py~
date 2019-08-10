import requests
from flask import jsonify


def calculateRectangles(segment):
	# return all the rectangles that correspond to the segment
	rectangle = {
		'lat1': max(segment['lat1'], segment['lat2']),
		'lng1': min(segment['lng1'], segment['lng2']),
		'lat2': min(segment['lat1'], segment['lat2']),
		'lng2': max(segment['lng1'], segment['lng2'])
	}
	return rectangle


def processBlockedRoads():
	# get the data from Max
	# some sort of input
	blockedRoads = [37.582865, -122.361762, 37.302184, -122.000655, 
	                  37.295249, -122.009205, 37.089788, -121.620156,
	                  38.215460, -122.521367, 37.587075, -122.086155,
	                  37.297136, -121.319828, 36.525200, -120.546358,
	                  36.240705, -120.439267, 35.971323, -119.676628,
	                  35.884530, -120.375320, 35.190967, -119.338141,
	                  34.983357, -119.371975, 34.711253, -118.219843]
	segments = []
	# process the data
	i = 0
	while i < len(blockedRoads):
		segment = {
			'lat1': blockedRoads[i],
			'lng1': blockedRoads[i+1],
			'lat2': blockedRoads[i+2],
			'lng2': blockedRoads[i+3]
		}
		segments.append(segment)
		i+=4
	
	#print(segments)
	return segments
def processToString():
	segments = processBlockedRoads()
	rects = []
	for seg in segments:
		#console.log();
		rects.append(calculateRectangles(seg))
		#console.log();
	strRects = ""
	i = 0
	for rect in rects:
	  if i != 0:
	  	strRects += '!'
	  i+=1
	  strRects += str(rect['lat1']) + ',' + str(rect['lng1']) + ";" + str(rect['lat2']) + ',' + str(rect['lng2'])

	# print(segments);
	# print(rects);
	# print(strRects);
	return strRects
def routePath(start, end):
	strRects = processToString()

	# 37.301750,-122.000900 start
	# 37.298050,-122.007210 end
	# get request
	res = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json', 
		params = {'app_id':'Te1UQqIdCLzaogGN5nwS',
					'app_code':'evjL5KiQwy1TvVmY1cMJZw',
					'waypoint0':'geo!'+start,
					'waypoint1':'geo!'+end,
					'mode':'fastest;car;traffic:disabled',
					'routeAttributes':'shape',
					'avoidareas':strRects
				}
			)
	if not res:
		sys.exit("Error with request")
	#print(res.json())
	route = res.json()['response']['route'][0]['shape']

	i = 0
	for coords in route:
		i += 1
		#print(coords + "," + str(i) + ",#00FF00")
	return jsonify({'route': route})


