Project contains:
1. IaC code in Terraform: EKS, S3 bucket and SQS creation
2. groovy file for Jenkins CI/CD job
3. Microservice 1 and Microservice 2 files - Dockerfile, deployment YAML files, Python code

To run the full CI/CD cycle:
1. A Jenkins server is needed, configured to run on the relevant AWS account
2. Change the S3 bucket name inside the relevant Terrafrom files (For saving TF state and for the Microservice 2 usage)

For Microservice 1 - before running set environment variables relevant for the AWS account and define the SQS url (Can be fetched from the Terraform output on the Jenkins console)

AWS_ACCESS_KEY
AWS_SECRET_KEY
AWS_REGION
SQS_QUEUE_URL

