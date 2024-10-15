import http.server
import socketserver
import os
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Puerto para el servidor frontend
PORT = 8000

# URL del backend
BACKEND_URL = "http://localhost:8080"

class ProxyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Maneja solicitudes a la API redirigiendo al backend
        if self.path.startswith('/api/'):
            self.send_response(301)
            self.send_header('Location', BACKEND_URL + self.path)
            self.end_headers()
        else:
            # Sirve archivos estáticos del frontend
            return SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        # Añade headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

# Configura y inicia el servidor
handler = ProxyHandler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
