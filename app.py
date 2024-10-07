import os
import zipfile
import cherrypy

class ZipApp:
    def __init__(self):
        self.zip_folder()  # Zip the folder when the application starts

    def zip_folder(self):
        folder_to_zip = 'mods'  # The folder you want to zip
        zip_filename = 'mods.zip'

        # Create a Zip file
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_to_zip):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_to_zip))

    @cherrypy.expose
    def index(self):
        return open("index.html")

    @cherrypy.expose
    def download(self):
        zip_filename = 'zipped_folder.zip'

        # Return the zip file for download
        cherrypy.response.headers['Content-Type'] = 'application/zip'
        cherrypy.response.headers['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
        return open(zip_filename, 'rb')

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',  # Bind to all available network interfaces
        'server.socket_port': 90,
        'log.screen': True,
    })
    cherrypy.quickstart(ZipApp(), '/', {'/': {'tools.sessions.on': True}})
    cherrypy.engine.socket_server.bind(('0.0.0.0', 90))
