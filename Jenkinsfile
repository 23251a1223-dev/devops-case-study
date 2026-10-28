
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m pip install selenium'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat 'python -m unittest test_appointment_cases.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t appointment-system:1.0 .'
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
