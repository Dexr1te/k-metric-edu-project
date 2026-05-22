from . import db
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class CronTask(db.Model):
    __tablename__ = 'cron_tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # success/failed
    runtime = db.Column(db.Float)  # in seconds
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)

class ApiMetric(db.Model):
    __tablename__ = 'api_metrics'
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(200), nullable=False)
    response_time = db.Column(db.Integer)  # in ms
    status_code = db.Column(db.Integer)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)

class ApiMetricSummary(db.Model):
    __tablename__ = 'api_metrics_summary'
    __table_args__ = {'info': dict(is_view=True), 'extend_existing': True}
    # Since it's a view, we don't have a primary key, but SQLAlchemy needs one
    endpoint = db.Column(db.String, primary_key=True)
    avg_response_time = db.Column(db.Float)
    request_count = db.Column(db.Integer)
    hour = db.Column(db.DateTime, primary_key=True)

