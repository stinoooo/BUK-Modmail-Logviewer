
__version__ = "1.1.2"

import html
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic, response
from sanic.exceptions import NotFound
from jinja2 import Environment, FileSystemLoader
from core.models import LogEntry

load_dotenv()

if "URL_PREFIX" in os.environ:
    print("Using the legacy config var `URL_PREFIX`, rename it to `LOG_URL_PREFIX`")
    prefix = os.environ["URL_PREFIX"]
else:
    prefix = os.getenv("LOG_URL_PREFIX", "/logs")

if prefix == "NONE":
    prefix = ""

MONGO_URI = os.getenv("MONGO_URI") or os.getenv("CONNECTION_URI")
if not MONGO_URI:
    print("No CONNECTION_URI config var found. Please enter your MongoDB connection URI in the configuration or .env file.")
    exit(1)

app = Sanic(__name__)
app.static("/static", "./static")

# Jinja environment for rendering HTML templates
jinja_env = Environment(loader=FileSystemLoader("templates"))

def render_template(name, *args, **kwargs):
    template = jinja_env.get_template(name + ".html")
    return response.html(template.render(*args, **kwargs))

# MongoDB client setup
client = AsyncIOMotorClient(MONGO_URI)
db = client['your-database-name']  # Replace with actual database name
transcripts_collection = db['transcripts']  # Replace with actual collection name

@app.route('/')
async def home(request):
    return render_template('index')

# API Endpoint to get transcript count
@app.route('/api/transcripts_count')
async def transcripts_count(request):
    total_transcripts = await transcripts_collection.count_documents({})
    return response.json({'total_transcripts': total_transcripts})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
