terraform {
  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "sqs/sqs1.tfstate"
    region = "eu-west-1"
  }
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

data "aws_iam_policy_document" "sqs_policy" {
  statement {
    sid    = "sqsstatement"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions = [
      "sqs:SendMessage",
      "sqs:ReceiveMessage"
    ]
    resources = [
      aws_sqs_queue.queue.arn
    ]
  }
}