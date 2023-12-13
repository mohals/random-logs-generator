import base64
import json
import gzip
import requests
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Extract log data from the CloudWatch Logs event payload
    logs_data = event['awslogs']['data']
    
    # Decode and decompress the logs data
    decoded_data = base64.b64decode(logs_data)
    decompressed_data = gzip.decompress(decoded_data)

    # Convert the data to a JSON object
    logs_json = json.loads(decompressed_data)

    # Access log events from the JSON object
    log_events = logs_json['logEvents']

    # Process the log information (you may need to customize this part based on your log format)
    processed_logs = process_logs(log_events)

    # Upload the processed logs to S3
    upload_to_s3(processed_logs, 'your-s3-bucket', 'path/in/s3/logs.txt')

#Bedrock code here

# replace with bedrock API response below 
response = requests.get('your_api_url')

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse JSON data from the response
    json_data = response.json()

    # Specify your AWS credentials and S3 bucket details
    aws_access_key = 'your_access_key'
    aws_secret_key = 'your_secret_key'
    bucket_name = 'your_s3_bucket'

    # Generate a unique file key with a timestamp
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    file_key = f'output_{timestamp}.json'

    # Write JSON data to the S3 bucket
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    s3.put_object(Body=json.dumps(json_data), Bucket=bucket_name, Key=file_key)

    # Send an email using SES
    ses = boto3.client('ses', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    
    # Replace 'sender@example.com' and 'recipient@example.com' with your verified SES email addresses
    sender = 'sender@example.com'
    recipient = 'recipient@example.com'
    
    subject = f"JSON Response - {timestamp}"
    body = f"The JSON response is available in S3: s3://{bucket_name}/{file_key}"

    ses.send_email(
        Source=sender,
        Destination={'ToAddresses': [recipient]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}},
        }
    )

    print(f"JSON data written to S3 bucket: s3://{bucket_name}/{file_key}")
    print(f"Email sent to: {recipient}")
else:
    print(f"Error: Unable to fetch data. Status code: {response.status_code}")

