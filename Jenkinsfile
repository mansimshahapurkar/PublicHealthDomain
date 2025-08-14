pipeline {
    agent any

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
                withCredentials([usernamePassword(credentialsId: 'aws-access-key', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                        docker logs health-app > app.log
                        aws s3 cp app.log s3://jenkins-artifacts-logs/logs/app-${BUILD_NUMBER}.log
                    '''
                }
            }
        }

        stage('Upload Artifacts') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-access-key', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                        mkdir -p build
                        cp -r * build/ || true
                        aws s3 cp build/ s3://jenkins-artifacts-logs/artifacts/${BUILD_NUMBER}/ --recursive
                    '''
                }
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
