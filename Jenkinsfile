
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat '"C:\\Users\\gnits\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"C:\\Users\\gnits\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install -r requirements.txt'
                bat '"C:\\Users\\gnits\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install selenium'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat '"C:\\Users\\gnits\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m unittest test_appointment_cases.py'
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
