from os import popen, path
import http.server, socketserver
from urllib.parse import urlparse, unquote

workingDir = path.dirname(path.abspath(__file__))
mimes = {
    "html": "text/html",
    "css": "text/css",
    "js": "text/javascript",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
    "svg": "image/svg+xml"
}

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = unquote(urlparse(self.path).path)
        print(url)

        mime = mimes[url.split(".")[-1]]
        print(mime)
        self.send_response(200)
        self.send_header("Content-type", mime)
        self.end_headers()

        file = open(workingDir + "/Website Code" + url, "rb").read()
        self.wfile.write(file)

port = 8080
server = socketserver.TCPServer(("", port), HttpRequestHandler)
popen("start \"\" \"http://localhost:" + str(port) + "/index.html\"")
server.serve_forever()
server.server_close()