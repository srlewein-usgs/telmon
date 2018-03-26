pipeline {
    agent any 
    stages {
        
        stage('Build') {
            steps {
                echo 'Building...' 
                echo "WORKSPACE -- $WORKSPACE"
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