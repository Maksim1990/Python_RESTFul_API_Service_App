from flask import Response
import simplejson as json

def view(data,status, headers=dict()):
    resp = Response(json.dumps({'data':data}),status)
    resp.headers['Content-Type'] = 'application/json'

    # Set additional headers if provided
    if headers:
        for key, value in headers.items():
            resp.headers[key] = value
    return resp

def errorView(data,status, headers=dict()):
    resp = Response(json.dumps({'error':
                                    {
                                        'code':status,
                                        'message':data
                                    }}),status)
    resp.headers['Content-Type'] = 'application/json'

    # Set additional headers if provided
    if headers:
        for key, value in headers.items():
            resp.headers[key] = value
    return resp
