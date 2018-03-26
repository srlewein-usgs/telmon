pipeline {
    agent any 
    stages {
        
        stage('Build') {
            steps {
                echo 'Building...' 
            }
        }
    }
        
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'python3 -m unittest' 
            }
        } 
        
        stage('Deploy') {
            steps {
                echo 'Deploying...' 
            }
        }        
    }
}