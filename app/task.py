from app import celery
from .utils import *

@celery.task(name='process_document')
def process_document(filename):
    # Simulate a long-running task
    print(f"Processing document {filename}")
    # document processing logic here
    return f"Document {filename} processed successfully"