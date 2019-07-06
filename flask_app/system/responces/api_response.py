
def view(data,status, headers=dict()):
    resp = {'data':data},status
    return resp

def errorView(message,status):
    resp = {'error':{
        "code":status,
        "message":message
    }},status
    return resp
