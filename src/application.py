from flask import Flask, Response, request, url_for, redirect
from datetime import datetime
import json, os
from candidate_resource import CandidateResource
from flask_cors import CORS
from flask_login import LoginManager,current_user,login_required, login_user,logout_user

from oauthlib.oauth2 import WebApplicationClient
import requests

# Create the Flask application object.
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = os.environ.get('secret_key')
CORS(app)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.get("/login_test")
def index(): 
    if current_user.is_authenticated:
        return "Welcome!"
    return "<a class='button' href='/login'>Google Login</a>"

@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "Candidate-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result

@app.route("/api/candidates/", methods=["GET"])
def get_all_students():

    result = CandidateResource.get_all()

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/candidates/<id>", methods=["GET"])
def get_student_by_uni(id):

    result = CandidateResource.get_by_key(id)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route('/login')
def login():

    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for('login_callback', _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route('/api/login/redirect')
def login_callback():

    code = request.args.get("code")

    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
   
    # user = User(
    #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    # )
    # # Doesn't exist? Add it to the database.
    # if not User.get(unique_id):
    #     User.create(unique_id, users_name, users_email, picture)

    # login_user(user)
    return redirect(url_for("get_health"))

if __name__ == "__main__":
    app.run()