
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
oauth = OAuth(app)

# Configure OAuth providers
oauth.register(
    name='github',
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    client_kwargs={'scope': 'user:email'},
    userinfo_endpoint='https://api.github.com/user'
)

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    client_kwargs={'scope': 'openid profile email'},
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo'
)

oauth.register(
    name='apple',
    client_id=os.getenv("APPLE_CLIENT_ID"),
    client_secret=os.getenv("APPLE_CLIENT_SECRET"),
    authorize_url='https://appleid.apple.com/auth/authorize',
    authorize_params=None,
    access_token_url='https://appleid.apple.com/auth/token',
    access_token_params=None,
    client_kwargs={'scope': 'name email'},
    userinfo_endpoint='https://appleid.apple.com/auth/userinfo'
)

@app.route('/login/<provider>')
def login(provider):
    redirect_uri = url_for('authorize', provider=provider, _external=True)
    return oauth.create_client(provider).authorize_redirect(redirect_uri)

@app.route('/authorize/<provider>')
def authorize(provider):
    token = oauth.create_client(provider).authorize_access_token()
    user_info = oauth.create_client(provider).userinfo()
    session['user'] = user_info
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
