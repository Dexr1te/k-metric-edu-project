from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
import os
from ..models import CronTask, ApiMetric, ApiMetricSummary
from .. import db

bp = Blueprint('dashboard', __name__, url_prefix='/api')

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, os.getenv('JWT_SECRET_KEY', 'super-secret-key'), algorithms=['HS256'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated

@bp.route('/dashboard/summary', methods=['GET'])
@jwt_required
def get_summary():
    summaries = ApiMetricSummary.query.order_by(ApiMetricSummary.hour.desc()).limit(20).all()
    return jsonify([{
        'endpoint': s.endpoint,
        'avg_response_time': round(s.avg_response_time, 2),
        'request_count': s.request_count,
        'hour': s.hour.isoformat()
    } for s in summaries])

@bp.route('/cron-tasks', methods=['GET'])
@jwt_required
def get_cron_tasks():
    tasks = CronTask.query.all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'status': t.status,
        'runtime': t.runtime,
        'executed_at': t.executed_at.isoformat()
    } for t in tasks])
