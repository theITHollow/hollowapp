pipeline {
    agent any

    stages {
        stage('build') {
            steps {
                sh 'chmod +x deploy/infraDeploy.py'
                sh 'python deploy/infraDeploy.py'
            }
        }
    }
}
