from app import create_app, db
from app.models import User, CronTask, ApiMetric
from datetime import datetime, timedelta
import random

def seed_data():
    app = create_app()
    with app.app_context():
        # 1. Create a test user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print("User 'admin' created with password 'admin123'")
        else:
            print("User 'admin' already exists")

        # 2. Add some initial Cron Tasks
        if CronTask.query.count() == 0:
            tasks = ["data_cleanup", "email_sender", "report_generator", "cache_warmup"]
            for i in range(10):
                task = CronTask(
                    name=random.choice(tasks),
                    status=random.choice(["success", "success", "failed"]),
                    runtime=round(random.uniform(0.5, 5.0), 2),
                    executed_at=datetime.utcnow() - timedelta(minutes=random.randint(1, 60))
                )
                db.session.add(task)
            print("Initial Cron Tasks seeded")

        # 3. Add some initial API Metrics
        if ApiMetric.query.count() == 0:
            endpoints = ["/api/login", "/api/dashboard/summary", "/api/cron-tasks"]
            for i in range(50):
                metric = ApiMetric(
                    endpoint=random.choice(endpoints),
                    response_time=random.randint(50, 500),
                    status_code=random.choice([200, 200, 200, 401, 500]),
                    requested_at=datetime.utcnow() - timedelta(minutes=random.randint(1, 120))
                )
                db.session.add(metric)
            print("Initial API Metrics seeded")

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
