pipeline {
    environment { 
        registry = ""
        folder = "ms1/."
        registryCredential = ""
        appname = "ms1"
        dockerImage = ""
        
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        AWS_DEFAULT_REGION = "eu-west-1"
    }    
    
agent any

stages {

stage('Building docker image') { 
    steps { 
        script { 
            dir('ms1') {
                dockerImage = docker.build(registry + ":${env.BUILD_NUMBER}", "./ms1") 
            }
        }
    } 
}


stage('Push image') { 
    steps { 
        script { 
            docker.withRegistry( '', registryCredential )  {
                dockerImage.push() 
            }
        } 
    }
} 


        stage("Create an EKS Cluster") {
            steps {
                script {
                    dir('eks') {
                    sh '''#!/bin/bash
                      terraform init
                      terraform plan
                      terraform apply -auto-approve
                      '''
                    }
                }
            }
        }
        
          stage("Create SQS") {
            steps {
                script {
                    dir('sqs') {
                    sh '''#!/bin/bash
                      terraform init
                      terraform plan
                      terraform apply -auto-approve
                      '''
                    }
                }
            }
        }
  
        
        stage("Deploy to EKS") {
            steps {
                script {
                    dir('ms1') {
                        sh '''#!/bin/bash
                        aws eks update-kubeconfig --name eks-cluster
                        kubectl apply -f ms1-deployment.yaml
                        kubectl apply -f ms1-service.yaml
                    '''
                    }
                }
            }
        }      
  }
}
