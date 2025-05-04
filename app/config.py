import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")
aws_endpoint = os.getenv("AWS_ENDPOINT")
aws_bucket_name = os.getenv("AWS_BUCKET_NAME")
database_url = os.getenv("DATABASE_URL")

print("AWS Access Key:", aws_access_key)
