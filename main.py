import os

from flask import Flask

from settings import TEMP_FOLDER
from dotenv import load_dotenv

from src.middlewares.auth import AuthMiddleware
from src.routes.calibration import CalibrationValve

load_dotenv()


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000 * 25  # 25 megabytes
app.config['UPLOAD_FOLDER'] = TEMP_FOLDER

app.wsgi_app = AuthMiddleware(app.wsgi_app, app)

app.add_url_rule(
    "/generate/valve/pdf",
    view_func=CalibrationValve.as_view("CalibrationValve")
)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=os.getenv("PORT", 5000),
        debug=True
    )
