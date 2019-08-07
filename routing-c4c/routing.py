import requests
import sys
from flask import jsonify
import json

def checkIntersectionSeg(seg1, seg2):
	slope1 = (seg1['lng2']-seg1['lng1'])*(seg2['lat2']-seg2['lat1'])
	slope2 = (seg2['lng2']-seg2['lng1'])*(seg1['lat2']-seg1['lat1'])
	interm = slope1*seg1['lat1']-slope2*seg2['lat1']
	latInt = interm/(slope2-slope1)
	seg1Diff = (latInt-seg1['lat1'])*(latInt-seg1['lat2'])
	seg2Diff = (latInt-seg2['lat1'])*(latInt-seg2['lat2'])
	return (seg1Diff <= 0 and seg2Diff <= 0)

def checkIntersectionRect(seg1, seg2):
	return

def calculateRectangles(segment):
	# return all the rectangles that correspond to the segment
	# print("hi")
	# print(segment['lat1'])
	rectangle = {
		'lat1': max(segment['lat1'], segment['lat2'])+0.0001,
		'lng1': min(segment['lng1'], segment['lng2'])-0.0001,
		'lat2': min(segment['lat1'], segment['lat2'])-0.0001,
		'lng2': max(segment['lng1'], segment['lng2'])+0.0001
	}
	return rectangle

def getBlockedRoads():
	file = open("roads.geojson", "r")
	roadData = json.loads(file.readline())
	roads = []
	for feature in roadData['features']:
		points = feature['geometry']['coordinates']
		if feature['geometry']['type'] == "LineString":
			for i in range(len(points)):
				roads.append(points[i][1])
				roads.append(points[i][0])
				if i != 0 and i != len(points)-1:
					roads.append(points[i][1])
					roads.append(points[i][0])
		else:
			for coords in points:
				for i in range(len(coords)):
					roads.append(coords[i][1])
					roads.append(coords[i][0])
					if i != 0 and i != len(coords)-1:
						roads.append(coords[i][1])
						roads.append(coords[i][0])

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
		rects.append(calculateRectangles(seg))
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
	blockedRoads = processBlockedRoads()
	strRects = ""
	# print(strRects)
	# print(strRects.count('!'))
	# 29.700232,-95.401736 start
	# 29.841133,-95.377595 end
	# get request
	for i in range(21): # max 20 rectangles allowed by the API
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
			print(res.json())
			sys.exit("Error with request")
		# print(res.json())
		route = res.json()['response']['route'][0]['shape']
		routeSegs = []
		for i in range(len(route)-1):
			point1 = route[i].split(',')
			point2 = route[i+1].split(',')
			seg = {
				'lat1': float(point1[0]),
				'lng1': float(point1[1]),
				'lat2': float(point2[0]),
				'lng2': float(point2[1])
			}
			anyBlockage = False
			for bRoad in blockedRoads:
				if checkIntersectionSeg(seg, bRoad):
					anyBlockage = True
					break
			if not anyBlockage: # no blocking!!!
				print("Path is not blocked!")
				break
		if not anyBlockage:
			break
	if anyBlockage:
		print("Cannot avoid blocked roads")
	# i = 0
	# for coords in route:
	# 	i += 1
	# 	#print(coords + "," + str(i) + ",#00FF00")
	return jsonify({'route': route})

if __name__ == '__main__':
	print("What are starting coordinates: ")
	start = input()
	print("What are ending coordinates: ")
	end = input()
	routePath(start, end)

