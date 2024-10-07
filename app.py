import os
import zipfile
import cherrypy

# Function to zip the folder
def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, relative_path)

class StaticServer:
    @cherrypy.expose
    def index(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(script_dir, 'static', 'index.html')
        with open(index_path, 'r') as f:
            return f.read()

if __name__ == '__main__':
    # Paths
    folder_to_zip = 'mods'
    output_zip = 'static/mods.zip'

    # Ensure the static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    # Zip the folder
    zip_folder(folder_to_zip, output_zip)

    # Configure CherryPy static directory
    config = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('static')
        }
    }

    # Update CherryPy server configuration
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 90,
    })

    # Start the CherryPy server
    cherrypy.quickstart(StaticServer(), '/', config)
