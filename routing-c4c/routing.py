import requests
import sys
from flask import jsonify


def calculateRectangles(segment):
	# return all the rectangles that correspond to the segment
	rectangle = {
		'lat1': max(segment['lat1'], segment['lat2'])+0.0001,
		'lng1': min(segment['lng1'], segment['lng2'])-0.0001,
		'lat2': min(segment['lat1'], segment['lat2'])-0.0001,
		'lng2': max(segment['lng1'], segment['lng2'])+0.0001
	}
	return rectangle

def getBlockedRoads():
	file = open("roads.geojson", "r")
	roadData = file.readline()
	roads = []
	for feature in roadData['features']:
		points = feature['properties']['geometry']['coordinates']
		for i in range(len(points)):
			roads.append(points[i][0])
			roads.append(points[i][1])
			if i != 0 and i != len(points)-1:
				roads.append(points[i][0])
				roads.append(points[i][1])

	return roads

def processBlockedRoads():
	# get the data from Max
	blockedRoads = getBlockedRoads()
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


