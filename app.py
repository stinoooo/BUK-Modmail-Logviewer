
__version__ = "1.1.2"

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic, response
from jinja2 import Environment, FileSystemLoader
from pymongo import MongoClient

load_dotenv()

# MongoDB connection setup
mongo_uri = "mongodb+srv://stijnstijlai:4HrUYi0syty9Ksrq@buk-modmail.recdp.mongodb.net"
client = MongoClient(mongo_uri)

# Connect to the database and collection
db = client['modmail_db']
collection = db['transcripts']

# Count the number of transcripts
transcript_count = collection.count_documents({})

# Sanic app setup
app = Sanic(__name__)
app.static("/static", "./static")
jinja_env = Environment(loader=FileSystemLoader("templates"))

def render_template(name, *args, **kwargs):
    template = jinja_env.get_template(name + ".html")
    return response.html(template.render(*args, **kwargs))

@app.route("/")
async def index(request):
    return render_template("index", transcript_count=transcript_count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
