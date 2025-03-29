import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from settings import TEMP_FOLDER
from src.middlewares.auth import AuthMiddleware
from src.routes.calibration import Calibration
from src.routes.reports import BoilerReport

from flasgger import Swagger

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000 * 25  # 25 megabytes
app.config['UPLOAD_FOLDER'] = TEMP_FOLDER
app.config['SWAGGER'] = {
    'title': 'Inspetor PDF Generator API',
    'uiversion': 3,
    'openapi': '3.0.3'
}

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

app.wsgi_app = AuthMiddleware(app.wsgi_app, app)

@app.route('/generate/boiler-report/pdf', methods=['GET'])
def boiler_report_doc():
    """
    Generate Boiler Inspection Report.
    ---
    tags:
      - Reports
    parameters:
      - name: report_id
        in: query
        type: string
        required: true
        description: ID of the report to be processed and generated.
    responses:
      200:
        description: Public URL of the generated PDF report.
        schema:
          type: object
          properties:
            url:
              type: string
              description: Public URL of the generated PDF.
            name:
              type: string
              description: Generated file name.
            sizeInIntegerFormat:
              type: integer
              description: File size in bytes.
            size:
              type: string
              description: File size in megabytes (formatted).
            dateInIsoFormat:
              type: string
              format: date-time
              description: Creation date in ISO format.
            dateInTimestamp:
              type: integer
              description: Timestamp of the creation date.
            createdBy:
              type: string
              description: Firebase user UID.
            createdAt:
              type: integer
              description: Timestamp when the report was generated.
      401:
        description: Token not provided.
      500:
        description: Internal server error.
    """
    return BoilerReport.as_view('BoilerReport')()


@app.route('/generate/calibration/pdf', methods=['GET'])
def calibration_doc():
    """
    Generate Calibration Report.
    ---
    tags:
      - Calibration
    parameters:
      - name: report_id
        in: query
        type: string
        required: true
        description: ID of the report to be processed and generated.
      - name: calibration_type
        in: query
        type: string
        required: true
        description: Type of calibration report.
    responses:
      200:
        description: Public URL of the generated PDF report.
        schema:
          type: object
          properties:
            url:
              type: string
              description: Public URL of the generated PDF.
            name:
              type: string
              description: Generated file name.
            sizeInIntegerFormat:
              type: integer
              description: File size in bytes.
            size:
              type: string
              description: File size in megabytes (formatted).
            dateInIsoFormat:
              type: string
              format: date-time
              description: Creation date in ISO format.
            dateInTimestamp:
              type: integer
              description: Timestamp of the creation date.
            createdBy:
              type: string
              description: Firebase user UID.
            createdAt:
              type: integer
              description: Timestamp when the report was generated.
      401:
        description: Token not provided.
      500:
        description: Internal server error.
    """
    return Calibration.as_view('Calibration')()


# app.add_url_rule(
#     "/generate/calibration/pdf",
#     view_func=Calibration.as_view("Calibration")
# )
#
# app.add_url_rule(
#     "/generate/boiler/pdf",
#     view_func=BoilerReport.as_view("BoilerReport")
# )

swagger = Swagger(app)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=os.getenv("PORT", 5000),
        debug=True
    )
