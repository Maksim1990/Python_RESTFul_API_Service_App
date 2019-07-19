from flask_restful import reqparse, Resource, abort
from flask import request
from flask_jwt import JWT, jwt_required, current_identity
import system.responces.api_response as response
from system.model import db
from functools import wraps
from resources.user import User
from system.model import mongo
import json
from bson import ObjectId

def checkuser(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = User.query.filter_by(id=current_identity.id).first()
        if user:
            return func(*args, **kwargs)
        return response.errorView('Not authenticated',401)
    return wrapper

def encodeObjectID(doc):
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

def deleteErrorMessage():
    return response.errorView('Note with such ID and \'user_id\' does not exist',400)

def customExceptionHandler(ex):
    if type(ex).__name__== 'InvalidId':
        return response.errorView("Provided 'note_id' is invalid",400)
    else:
        return response.errorView(str(ex),400)

# Notes collection class
class NoteCollection(Resource):
    decorators = [checkuser, jwt_required()]
    def get(self,user_id):
        #notes = mongo.db.notes.find({'user_id': user_id},{'_id': 1, 'user_id': 1,'name':1})
        notes = mongo.db.notes.find({'user_id': int(user_id)})
        notes_list = []
        for doc in notes:
            encodeObjectID(doc)
            notes_list.append(doc)
        return response.view(notes_list,200)

    def post(self, user_id):
        createData={}
        try:
            createData= request.get_json()
            createData["user_id"]=user_id
            mongo.db.notes.insert(createData)
            return response.view(encodeObjectID(createData),200)
        except Exception as ex:
            return response.errorView(str(ex),400)

# Note resource class
class NoteResource(Resource):
    decorators = [checkuser, jwt_required()]
    def get(self, user_id,note_id):
        try:
            notes = mongo.db.notes.find({'user_id': int(user_id),"_id":ObjectId(note_id)})
            notes_list = []
            for doc in notes:
                encodeObjectID(doc)
                notes_list.append(doc)
            return response.view(notes_list,200)
        except:
          return response.errorView('Provided note_id is invalid',400)

    def delete(self, user_id,note_id):
        try:
            noteItem=mongo.db.notes.find_one({'user_id': int(user_id),'_id': ObjectId(note_id)}, {'_id': 1})
            if noteItem != None:
                mongo.db.notes.delete_one({'user_id': int(user_id),"_id":ObjectId(note_id)})
                return response.view('Note was successfully deleted!',200)
            else:
                return deleteErrorMessage()
        except Exception as ex:
            return customExceptionHandler(ex)

    def put(self, user_id,note_id):
        try:
            noteItem=mongo.db.notes.find_one({'_id': ObjectId(note_id)}, {'_id': 1})
            if noteItem != None:
                updateValues={ "$set": request.get_json() }
                mongo.db.notes.update_one({'user_id': int(user_id),"_id":ObjectId(note_id)},updateValues)
                return response.view("Successfully updated",200)
            else:
                return deleteErrorMessage()
        except Exception as ex:
            return customExceptionHandler(ex)
