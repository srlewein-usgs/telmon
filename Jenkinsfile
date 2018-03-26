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
                sh "cd %WORKSPACE/telmon"
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