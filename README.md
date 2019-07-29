# Call-For-Code-Routing
Routing for Call for Code using HERE JS and REST API

Focus is on avoiding certain roads (because of potential damage in natural disasters)

Given a road segment, which is represented as two pairs of coordinates of latitude, longitude, routing is done by avoiding these roads. The result is a list of coordinates that specify the fastest route.

Both Javascript and REST versions are implemented, and it is deployed to IBM Cloud with a Flask Python app at ligma@mybluemix.net

### Requests to the server
Base url: ligma@mybluemix.net/api/route/
Parameters: start, end
Format for each must be latitutecoordinate,longitudecoordinate with no spaces