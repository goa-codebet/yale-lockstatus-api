from flask import Flask
from yalexs.api import Api 
from yalexs.authenticator import Authenticator, AuthenticationState
from yalexs.lock import LockStatus
from dotenv import load_dotenv
import os

load_dotenv()

print(os.environ)

api = Api(timeout=20)
authenticator = Authenticator(api, "email", os.environ["YALE_EMAIL"], os.environ["YALE_PASSWORD"], access_token_cache_file="./test")
authentication = authenticator.authenticate()
state = authentication.state
print(state)

if (state == AuthenticationState.REQUIRES_VALIDATION):
    authenticator.send_verification_code()
    code = input("Enter your validataion code sent on email/sms: ")
    validation_result = authenticator.validate_verification_code(code)

authentication = authenticator.authenticate()
locks = api.get_locks(authentication.access_token)
print(locks)


app = Flask(__name__)
@app.route("/")
def index():
    return ""

@app.route("/lock-status")
def lock_status():
    lock_details = api.get_lock_detail(authentication.access_token, locks[0].device_id)
    return "LOCKED" if lock_details.lock_status == LockStatus.LOCKED else "UNLOCKED"

if __name__ == '__main__':
	app.run(host=os.environ["FLASK_HOST"], port=os.environ["FLASK_PORT"])
