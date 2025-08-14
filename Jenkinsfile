pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/mansimshahapurkar/PublicHealthDomain.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("public-health-app:${BUILD_NUMBER}")
                }
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 8080:8080 --name health-app public-health-app:${BUILD_NUMBER}'
            }
        }

        stage('Collect Logs') {
            steps {
                sh 'docker logs health-app > app.log'
                sh 'aws s3 cp app.log s3://my-ci-cd-artifacts/logs/app-${BUILD_NUMBER}.log'
            }
        }

        stage('Upload Artifacts') {
            steps {
                sh 'mkdir -p build'
                sh 'cp -r * build/ || true'
                sh 'aws s3 cp build/ s3://my-ci-cd-artifacts/artifacts/${BUILD_NUMBER}/ --recursive'
            }
        }
    }

    post {
        always {
            sh 'docker stop health-app || true'
            sh 'docker rm health-app || true'
        }
    }
}
