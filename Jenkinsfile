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
                sh "cd %WORKSPACE/telmon
				    python3.6 -m unittest"
            }
        } 
        
        stage('Deploy') {
            steps {
                echo 'Deploying...' 
			    ssh $ec2-user@10.12.10.69 rm -rf /home/ec2-user/telmon
            }
        }        
    }
}