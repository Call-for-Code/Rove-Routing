# Call-For-Code-Routing

### Project: Rove
Built by Bryan Chiang, Max Wu, Daniel Ciao, Lucas Xia for 2019 Call for Code Challenge  

### Purpose
Effectively gather data in the wake of natural disasters and direct responders.

##### Demo
https://www.youtube.com/watch?v=ibbUAn-4l3k&t=10s

### Rove's Routing Functionality
Routing for Rove uses HERE REST API

Given data on blocked roads gathered from image processing techniques, the routing generates a route that avoids hazardous roads while minimizing duration of the route to direct responders to people of need as quickly as possible.

### How It Works
Given road segments, which is represented as two pairs of coordinates of latitude, longitude, routing is done by avoiding these roads through an iterative process. The process first generates a route, then checks to see if it passes through unsafe roads, and reroutes while avoiding these roads. The result is a list of coordinates that specify the fastest route.

Both HERE Javascript and REST API versions are used, and the REST version is deployed to IBM Cloud with a Flask Python app at ligma@mybluemix.net

### Requests to the server
Base url: ligma@mybluemix.net/api/route/  
Parameters: start, end  
Format for each must be latitutecoordinate,longitudecoordinate with no spaces  
