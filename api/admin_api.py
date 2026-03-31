from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_restful import Resource
from models.user import User
from models.placement import PlacementDrive


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

class AdminStatsAPI(Resource):
    @admin_required
    def get_stats(self):
        student_count = User.query.filter_by(role='student').count()
        company_count = User.query.filter_by(role='company').count()
        placement_drive_count = PlacementDrive.query.count()
        return jsonify({
            'student_count': student_count,
            'company_count': company_count,
            'placement_drive_count': placement_drive_count
        },200)
