pipeline {
    agent any

    stages {
        stage('InfraBuild') {
            steps {
              script {
                if (env.BRANCH_NAME == 'master')
                {
                  echo 'Pulling...' + env.BRANCH_NAME
                }
                else
                {
                  sh 'chmod +x deploy/infraDeploy.py'
                  sh 'python deploy/infraDeploy.py'
                }
              }
            }
        }
        stage('AppDeploy') {
            steps {
              script {
                if (env.BRANCH_NAME == 'master')
                {
                  echo 'Pulling...' + env.BRANCH_NAME
                }
                else
                {
                  sh 'chmod +x deploy/appDeploy.py'
                  sh 'python deploy/appDeploy.py'
                }
              }
            }
        }
        stage('infraTest') {
            steps {
              script {
                if (env.BRANCH_NAME != 'master')
                {
                    sh 'chmod +x tests/infraTests.py'
                    sh 'python tests/infraTests.py'
                }
              }
            }
        }
        stage('infraDestroy') {
            steps {
              script {
                if (env.BRANCH_NAME == 'master')
                {
                    sh 'chmod +x tearDown/infraDestroy.py'
                    sh 'python tearDown/infraDestroy.py'
                }
              }
            }
        }
    }
}
