
exports.calculateBlockedRoads = function() {
	var calculateRectangles = function(segment) {
		// return all the rectangles that correspond to the segment
		var rectangle = {
			'lat1': Math.max(segment.lat1, segment.lat2),
			'lng1': Math.min(segment.lng1, segment.lng2),
			'lat2': Math.min(segment.lat1, segment.lat2),
			'lng2': Math.max(segment.lng1, segment.lng2)
		}
		return rectangle;
	}

	var processBlockedRoads = function() {
		// get the data from Max
		// some sort of input
		var blockedRoads = [37.302391, -122.000760, 37.302184, -122.000655, 
							37.302629, -121.999748, 37.302197, -121.999346];
		var segments = [];
		// process the data
		for (var i = 0; i < blockedRoads.length; i+=4) {
			var segment = {
				'lat1': blockedRoads[i],
				'lng1': blockedRoads[i+1],
				'lat2': blockedRoads[i+2],
				'lng2': blockedRoads[i+3]
			};
			segments.push(segment);
		}
		console.log(segments)
		return segments;
	}

	var segments = processBlockedRoads();
	var rectangles = [];
	for (var i = 0; i < segments.length; i++) {
		//console.log();
		rectangles.push(calculateRectangles(segments[i]));
		//console.log();
	}
	return rectangles;
}