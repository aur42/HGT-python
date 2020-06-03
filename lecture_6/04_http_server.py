#04_http_server

# That's pretty bare bones,
# which is alright if you want to create your own app from scratch.
# But what if you just want to make or visit websites?
# I already showed one example on how to use HTTP,
# but that was tedious, and that was just the client.
# Fortunately, you don't have to do it all by yourself.

# In fact, if all you want to do is create your own web pages,
# then there is a module for that, called http.server.
# You can run that directly,
# inside the folder containing your contents: python3 -m http.server.
# I have a folder called simple_contents, with HTML files,
# so we can run the server in there.
# You could add the port number if you want.
# By default, it's 8000
# So on your own computer, you can visit http://localhost:8000

# But let's say you want to do something more complicated.
# There's nothing keeping us from using the http.server module.
# The class that does the network stuff is HTTPServer,
# and you need to extend BaseHTTPRequestHandler.

from http.server import HTTPServer, BaseHTTPRequestHandler

class RealHTTPRequestHandler(BaseHTTPRequestHandler):
	# If you look at the server log, you probably noticed the GET keyword.
	# HTTP has several methods, and normally,
	# your browser uses the GET method.
	# That, by convention, means that
	# the browser only wants to get data,
	# and the data stored on the server should not change,
	# at least not visibly to the client.
	def do_GET(self):
		# How do you respond to that?
		# If you look at the log again,
		# you see that it includes the number 200.
		# That's the best case: you found what you wanted.
		# In Python, you send that number with send_response
		self.send_response(200)

		# But we also need to send content.
		# As you will see, an HTTP server can send more than just HTML.
		# How does the browser know what the content is?
		# You set a header.
		# Headers are kind of like dictionaries.
		# You have names and values.
		# For content type, the header name is "Content-Type".
		# For HTML, the value "text/html".
		self.send_header("Content-Type", "text/html")
		# You end it all with end_headers()
		self.end_headers()

		# Now, we give the content.
		# Let's have a page that gives some information
		# about your GET request.
		content_format = """<html>
<head><meta charset="UTF-8"><title>Generated By Python</title></head>
<body>
Path = %(path)s
<br>Client = %(client)s
</body>
</html>"""

		# The path field is the path part of the URL.
		# The request field is the socket to the client,
		# and it has the IP address and port.
		message = content_format % {"path": self.path,
					    "client":
					    self.request.getpeername()}
		# The handler has two file streams as fields.
		# The one for reading doesn't work for GET requests,
		# but you can use the writing one
		# to write messages to the client.
		# The field is called wfile.
		# But it has to be in binary.
		# We said that the encoding would be UTF-8
		self.wfile.write(message.encode("UTF-8"))

# That's the handler. How do we run it?
# As I said, the HTTPServer takes care of the protocol business.
# You give it the address and handler class you want to use.
# The address is just like the one for the socket.
server = HTTPServer(("", 8080), RealHTTPRequestHandler)
server.serve_forever()
