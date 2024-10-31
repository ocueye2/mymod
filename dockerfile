FROM  python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install cherrypy

COPY . .

EXPOSE 90

CMD ["python", "app.py"]
