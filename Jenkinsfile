pipeline {
    agent any 
    stages {
        
        stage('Build') {
            steps {
                echo 'Building...' 
            }
        }
        
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'python -m unittest' 
            }
        } 
        
        stage('Deploy') {
            steps {
                echo 'Deploying...' 
            }
        }        
    }
}