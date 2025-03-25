import boto3
import os
import time
import datetime
import json

# Load AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
S3_BUCKET = os.getenv("S3_BUCKET")
SQS_MSGS_FILE = os.getenv("SQS_MSGS_FILE")
WAIT_TIME_SECONDS = os.getenv("WAIT_TIME_SECONDS", 10)

print(f'SQS_QUEUE_URL: {SQS_QUEUE_URL}')
print(f'S3_BUCKET: {S3_BUCKET}')
print(f'SQS_MSGS_FILE: {SQS_MSGS_FILE}')
print(f'WAIT_TIME_SECONDS: {WAIT_TIME_SECONDS}')

# Initialize S3 client
s3_client = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION)

# Initialize SQS client
sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)
ts = time.time()
file1 = open("myfile.txt", "a")  # append mode

def get_ts():
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    return f'{timestamp}'

def pull_messages():
        messages = None
        try:
            response = (sqs_client.receive_message(QueueUrl=SQS_QUEUE_URL, AttributeNames=['All'], MaxNumberOfMessages=1, WaitTimeSeconds=int(WAIT_TIME_SECONDS)))
            messages = response['Messages']
            # print("messages: " + str(messages))
            for message in messages:
                print("Full SQS message: " + str(message))
                receipt_handle = message['ReceiptHandle']
                msg_output = {'time': get_ts(), message['MessageId'] : message['Body']}
                print(f'Message body: {msg_output}')

                dlt_response = sqs_client.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=receipt_handle
                )

                if dlt_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print(f"Message {message['MessageId']} deleted successfully from queue")
                else:
                    print(f"There was an error deleting message_id {message['MessageId']} from queue")

                file1.write(f'{msg_output},\n')

                # Send to S3 bucket
                s3_object = s3_client.get_object(Bucket=S3_BUCKET, Key=SQS_MSGS_FILE)
                data = s3_object.get('Body').read()
                if len(data) != 0:
                    json_data = json.loads(data)  # Changed
                    json_data.append(msg_output)
                    p = json_data
                else:
                    p = [msg_output]

                s3_client.put_object(Body=json.dumps(p).encode(), Bucket=S3_BUCKET, Key=SQS_MSGS_FILE)
                print(f"Message {message['MessageId']} was written successfully to {SQS_MSGS_FILE} at S3 bucket {S3_BUCKET}")
            return response
        except Exception as e:
            #file1.close()
            #return jsonify({"error": str(e)}), 500
            #if not messages:
            #    print(f'{get_ts()} No messages, continue pulling, interval is {WAIT_TIME_SECONDS} seconds...')
            #else:
            #    print(f'{get_ts()} Exception: {str(e)}')
                
            print(f'{get_ts()} Exception: {str(e)}')
            return None


if __name__ == "__main__":
    while True:
        res = pull_messages()
