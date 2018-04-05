from flask import Flask, request, make_response, jsonify
from functools import wraps
import os
import json

app = Flask(__name__)

g_data_cache={}
g_data_args_cache={}

DATA_CACHE = 1
ARGS_CACHE = 2

def _get_data(path, cachetype=DATA_CACHE):
    global g_data_cache
    global g_data_args_cache
    cache = g_data_cache if cachetype==DATA_CACHE else g_data_args_cache
    ext   = ".json" if cachetype==DATA_CACHE else ".args.json"

    try:
        if path not in cache:
            source="data/"+path+ext
            print "Loading ressource ", source
            with open(source, 'r') as fd : 
                cache[path]=json.load(fd)
        return cache[path]
    except:
        return {}

def _validate_params(args, path):
    expected = _get_data(path, ARGS_CACHE)
    result = cmp(args,expected)==0
    print "_validate_params returns ", result
    if not result:
        print "expected: ", expected
        print "received: ", args
    return result

def _check_auth(username, password):
    return username == 'admin' and password == 'secret'

def _authenticate():
    return  make_response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not _check_auth(auth.username, auth.password):
            return _authenticate()
        return f(*args, **kwargs)
    return decorated 

@app.route("/<path:path>", methods=['GET'])
@requires_auth
def endpoint_ressource(path):
    print path
    response = None
    valid = _validate_params(request.args.to_dict(), path)
    if valid:
        payload=_get_data(path)
        if payload:
            response = make_response(json.dumps(payload), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
   
    response = make_response(jsonify({"errorCode": 4001, "errorMessage": "Ressource not found" if valid else "Invalid parameters"}), 404)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)