import json
from flask import g, Response
from firebase_admin import auth
from src.firebase import firebase


class AuthMiddleware:
    def __init__(self, wsgi_app, app):
        self.wsgi_app = wsgi_app
        self.app = app

    def __call__(self, environ, start_response):
        if environ["REQUEST_METHOD"] == "OPTIONS":
            res = Response(
                status=200,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization"
                }
            )
            return res(environ, start_response)

        auth_header = environ.get("HTTP_AUTHORIZATION", None)
        if auth_header and auth_header.startswith("Bearer "):
            id_token = auth_header.split(" ")[1]
            try:
                decoded_token = auth.verify_id_token(id_token, app=firebase.application)

                with self.app.app_context():
                    g.user_uid = decoded_token["uid"]
                    return self.wsgi_app(environ, start_response)
            except Exception as e:
                res = Response(
                    response=json.dumps({"error": "Token error", "details": str(e)}),
                    status=401,
                    mimetype='application/json',
                    headers={"Access-Control-Allow-Origin": "*"}
                )
                return res(environ, start_response)

        res = Response(
            response=json.dumps({"error": "Token error", "details": "No token Provided"}),
            status=401,
            mimetype='application/json',
            headers={"Access-Control-Allow-Origin": "*"}
        )
        return res(environ, start_response)
