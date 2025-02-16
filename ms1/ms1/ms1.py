from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# Load AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

# Initialize SQS client
sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


@app.route("/message", methods=["POST"])
def send_message():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field in request body"}), 400

    try:
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=data["message"]
        )
        return jsonify({"message_id": response["MessageId"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
