pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          docker.build('publichealthdomain:latest', '.')
        }
      }
    }

    stage('Run Docker Container') {
      steps {
        script {
          docker.image('publichealthdomain:latest').run('-d -p 8080:8000')
        }
      }
    }
  }

  post {
    always {
      echo "Pipeline completed."
    }
  }
}
