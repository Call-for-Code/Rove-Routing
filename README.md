# Call-For-Code-Routing
Routing for Call for Code using HERE JS API

Focus is on avoiding certain roads (because of potential damage in natural disasters)

Given a road segment, which is represented as two pairs of coordinates of latitude, longitude, routing is done by avoiding these roads.

The API only allows for avoidance of rectangular sections that are parallel to global axes, so the road is segmented for more precision.

The result is a list of coordinates that specify the fastest route.
