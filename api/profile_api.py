from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_jwt_identity,jwt_required
from models import db
from models.profile import Profile
from models.user import User

class ProfileAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        student = Profile.query.filter_by(user_id=user_id).first()
        if student:
            return student.to_dict(),200
        else:
            return {'message': 'Student not found'}, 404

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        profile = Profile.query.filter_by(user_id=user_id).first()
        payload = request.get_json()
        if profile:
            if not payload:
                return {'message': 'No data provided'}, 400
            profile.updateData(payload)
            db.session.commit()
            return {'message': 'Profile updated successfully'}, 200
        else:
            user = User.query.filter_by(user_id=user_id).first()
            db.session.flush() #forces SQLite to assign user_id NOW
            profile = Profile(user_id=user.user_id,name = user.username,email = user.email)
            profile.updateData(payload)
            db.session.add(profile)
            db.session.commit()
            return {'message': 'Profile created successfully'}, 201