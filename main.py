import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from settings import TEMP_FOLDER
from src.middlewares.auth import AuthMiddleware
from src.routes.calibration import Calibration
from src.routes.reports import BoilerReport

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000 * 25  # 25 megabytes
app.config['UPLOAD_FOLDER'] = TEMP_FOLDER

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

app.wsgi_app = AuthMiddleware(app.wsgi_app, app)

app.add_url_rule(
    "/generate/calibration/pdf",
    view_func=Calibration.as_view("Calibration")
)

app.add_url_rule(
    "/generate/boiler/pdf",
    view_func=BoilerReport.as_view("Calibration")
)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=os.getenv("PORT", 5000),
        debug=True
    )
