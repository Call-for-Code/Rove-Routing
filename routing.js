//const getRectangles = require('./calculate_blocked_roads.js')

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
                      37.303651, -122.003879, 37.302439, -122.002040];
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
  return segments;
}

var segments = processBlockedRoads();
var rectangles = [];
for (var i = 0; i < segments.length; i++) {
  //console.log();
  rectangles.push(calculateRectangles(segments[i]));
  //console.log();
}

// Instantiate a map and platform object:
var platform = new H.service.Platform({
  'apikey': '0up0QFyBHkN_L0y1CiABHMc7VVSbX_gbf9zwrJFvSR0'
});
// Retrieve the target element for the map:
var targetElement = document.getElementById('mapContainer');

// Get the default map types from the platform object:
var defaultLayers = platform.createDefaultLayers();

// Instantiate the map:
var map = new H.Map(
  document.getElementById('mapContainer'),
  defaultLayers.vector.normal.map,
  {
  zoom: 10,
  center: { lat: 41.110759, lng: -73.719639 }
  });

// get areas to avoid
//var rects = getRectangles.calculateBlockedRoads();
var rects = rectangles;
var strRects = "";
for (var i = 0; i < rects.length; i++) {
  if (i != 0) strRects += '!';
  strRects += rects[i].lat1 + ',' + rects[i].lng1 + ";"
            + rects[i].lat2 + ',' + rects[i].lng2;
}
console.log(segments);
console.log(rects);
console.log(strRects);


// Create the parameters for the routing request:
var routingParameters = {
  // The routing mode:
  'mode': 'fastest;car',
  // The start point of the route:
  'waypoint0': 'geo!37.301750,-122.000900',
  // The end point of the route:
  'waypoint1': 'geo!37.298050,-122.007210',
  // To retrieve the shape of the route we choose the route
  // representation mode 'display'
  'avoidareas': strRects,
  'representation': 'display'
};

// Define a callback function to process the routing response:
var onResult = function(result) {
  var route,
  routeShape,
  startPoint,
  endPoint,
  linestring;
  if(result.response.route) {
  // Pick the first route from the response:
  route = result.response.route[0];
  // Pick the route's shape:
  routeShape = route.shape;

  // Create a linestring to use as a point source for the route line
  linestring = new H.geo.LineString();

  // Push all the points in the shape into the linestring:
  routeShape.forEach(function(point) {
  var parts = point.split(',');
  //console.log(parts);
  linestring.pushLatLngAlt(parts[0], parts[1]);
  });

  // Retrieve the mapped positions of the requested waypoints:
  startPoint = route.waypoint[0].mappedPosition;
  endPoint = route.waypoint[1].mappedPosition;

  // Create a polyline to display the route:
  var routeLine = new H.map.Polyline(linestring, {
  style: { strokeColor: 'blue', lineWidth: 3 }
  });

  // Create a marker for the start point:
  var startMarker = new H.map.Marker({
  lat: startPoint.latitude,
  lng: startPoint.longitude
  });

  // Create a marker for the end point:
  var endMarker = new H.map.Marker({
  lat: endPoint.latitude,
  lng: endPoint.longitude
  });

  // Add the route polyline and the two markers to the map:
  map.addObjects([routeLine, startMarker, endMarker]);

  // Set the map's viewport to make the whole route visible:
  map.getViewModel().setLookAtData({bounds: routeLine.getBoundingBox()});
  }
};

// Get an instance of the routing service:
var router = platform.getRoutingService();

// Call calculateRoute() with the routing parameters,
// the callback and an error callback function (called if a
// communication error occurs):
router.calculateRoute(routingParameters, onResult,
  function(error) {
  alert(error.message);
  });