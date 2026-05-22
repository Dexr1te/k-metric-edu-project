import time
import random
from app import create_app, db
from app.models import CronTask, ApiMetric
from datetime import datetime

app = create_app()

def simulate_metrics():
    with app.app_context():
        print("Worker started, generating metrics...")
        while True:
            # Simulate a Cron Task
            if random.random() < 0.3:
                task_name = random.choice(["data_cleanup", "email_sender", "report_generator", "cache_warmup"])
                status = random.choice(["success", "success", "success", "failed"])
                runtime = round(random.uniform(0.5, 5.0), 2)
                
                task = CronTask(name=task_name, status=status, runtime=runtime)
                db.session.add(task)
                print(f"Added CronTask: {task_name} - {status} ({runtime}s)")

            # Simulate an API Metric
            endpoints = ["/api/login", "/api/dashboard/summary", "/api/cron-tasks", "/api/register"]
            endpoint = random.choice(endpoints)
            response_time = random.randint(50, 500)
            status_code = random.choice([200, 200, 200, 401, 404, 500])
            
            metric = ApiMetric(endpoint=endpoint, response_time=response_time, status_code=status_code)
            db.session.add(metric)
            print(f"Added ApiMetric: {endpoint} - {status_code} ({response_time}ms)")

            db.session.commit()
            time.sleep(5)

if __name__ == "__main__":
    try:
        simulate_metrics()
    except KeyboardInterrupt:
        print("Worker stopped.")
