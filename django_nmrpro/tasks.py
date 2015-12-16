from models import SessionSpec
from datetime import datetime, timedelta
from celery import task

@task
def clearSessionSpec():
    SessionSpec.objects.filter(accessed__lt=datetime.now() - timedelta(days=1)).delete()