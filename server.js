var http = require('http')
var fs = require('fs')
var url = require('url')

// create a service
http.createServer(function(request, response){
	// analyse the request, and contain the file name
	var pathname = url.parse(request.url).pathname;
	
	// print the file name requested
	console.log("request for " + pathname + "received.");
	
	// read the request contant from the file system
	fs.readFile(pathname.substr(1), function(err, data){
		if(err){
			// http status code: 404: not find file
			// content Type: text/plain
			response.writeHead(404, {'content-type': 'text/plain'});
		}else{
			// http status code: 200: ok
			//content type: text/plain
			response.writeHead(200, {'Content-Type': 'text/plain'});
			
			// request content
			response.write(data.toString());
		}
		// send request data
		response.end();
	});
}).listen(8080);

// control plane print
console.log('Server runing at http://127.0.0.1:8080/')