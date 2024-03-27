pipeline {
    agent any
    environment {
        // Environment variables setup
        API_MONDAY = credentials('token_monday')
        JIRA_TOKEN = credentials('token_jira')
        ANACONDA_PATH = 'C:\\ProgramData\\Anaconda3'
    }
    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment with Anaconda...'
                bat '''
                call ${ANACONDA_PATH}\\Scripts\\activate.bat
                call conda create --name myenv python=3.9 -y
                call conda activate myenv
                call pip install -r requirements.txt
                '''
            }
            post {
                success {
                    slackSend (color: 'good', message: "SUCCESS: Setup Environment stage completed successfully with Anaconda.")
                }
                failure {
                    slackSend (color: 'danger', message: "FAILURE: Setup Environment stage failed with Anaconda.")
                }
            }
        }
        stage('Setup Selenium Server HUB') {
            steps {
                echo 'Setting up Selenium server HUB...'
                bat "start /b java -jar selenium-server-4.17.0.jar hub"
                bat 'ping 127.0.0.1 -n 11 > nul'
            }
            post {
                success {
                    slackSend (color: 'good', message: "SUCCESS: Setup Selenium Server HUB stage completed successfully.")
                }
                failure {
                    slackSend (color: 'danger', message: "FAILURE: Setup Selenium Server HUB stage failed.")
                }
            }
        }
        stage('Setup Selenium Server nodes') {
            steps {
                echo 'Setting up Selenium server nodes...'
                bat "start /b java -jar selenium-server-4.17.0.jar node --port 5555 --selenium-manager true"
                bat 'ping 127.0.0.1 -n 11 > nul'
            }
            post {
                success {
                    slackSend (color: 'good', message: "SUCCESS: Setup Selenium Server nodes stage completed successfully.")
                }
                failure {
                    slackSend (color: 'danger', message: "FAILURE: Setup Selenium Server nodes stage failed.")
                }
            }
        }
        stage('Running Tests') {
            steps {
                script {
                    bat '''
                    call ${ANACONDA_PATH}\\Scripts\\activate.bat myenv
                    call python test_runner_ui_api_pytest.py
                    '''
                }
            }
            post {
                success {
                    slackSend (color: 'good', message: "SUCCESS: Running Tests stage completed successfully.")
                }
                failure {
                    slackSend (color: 'danger', message: "FAILURE: Running Tests stage failed.")
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying..'
                // Deployment steps go here
            }
            post {
                success {
                    slackSend (color: 'good', message: "SUCCESS: Deploy stage completed successfully.")
                }
                failure {
                    slackSend (color: 'danger', message: "FAILURE: Deploy stage failed.")
                }
            }
        }
        stage('Publish Report') {
             steps {
                bat 'powershell Compress-Archive -Path reports/* -DestinationPath report.zip -Force'
                archiveArtifacts artifacts: 'report.zip', onlyIfSuccessful: true
    }
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
            bat '''
            call ${ANACONDA_PATH}\\Scripts\\activate.bat myenv
            call conda deactivate
            call conda env remove -n myenv -y
            '''
            slackSend (color: 'warning', message: "NOTIFICATION: Cleaning up resources and removing Anaconda environment.")
        }
        success {
            echo 'Build succeeded.'
            slackSend (color: 'good', message: "SUCCESS: Build completed successfully.")
        }
        failure {
            echo 'Build failed.'
            slackSend (color: 'danger', message: "FAILURE: Build failed.")
        }
    }
}