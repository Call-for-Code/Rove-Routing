import requests


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
	blockedRoads = [37.302391, -122.000760, 37.302184, -122.000655, 
					37.303651, -122.003879, 37.302439, -122.002040]
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
	
	print(segments)
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

	print(segments);
	print(rects);
	print(strRects);
	return strRects

strRects = processToString()
# 37.302391,-122.00076;37.302184,-122.000655!37.302629,-121.999748;37.302197,-121.999346
# 37.302391,-122.00076;37.302184,-122.000655!37.303651,-122.003879;37.302439,-122.00204
# get request
res = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json', 
	params = {'app_id':'Te1UQqIdCLzaogGN5nwS',
				'app_code':'evjL5KiQwy1TvVmY1cMJZw',
				'waypoint0':'geo!37.301750,-122.000900',
				'waypoint1':'geo!37.298050,-122.007210',
				'mode':'fastest;car;traffic:disabled',
				'avoidareas':strRects
			}
		)
if not res:
	sys.exit("Error with request")
print(res.json())
res = res.json()['response']['route'][0]['leg'][0]

route = []

for maneuver in res['maneuver']:
	route.append(maneuver['position'])

i = 0
for coords in route:
	i += 1
	print(str(coords['latitude']) + "," + str(coords['longitude']) + "," + str(i) + ",#00FF00")


