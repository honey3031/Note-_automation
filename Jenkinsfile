pipeline {

    agent any

    environment {

        VENV = 'venv'

        EXECUTION = 'remote'

        GRID_URL = 'http://localhost:4444/wd/hub'

        BROWSER = 'chrome'

        EMAIL = credentials('notes-email')

        PASSWORD = credentials('notes-password')
    }

    stages {

        stage('Clone Repository') {

            steps {

                git branch: 'main',
                url: 'https://github.com/honey3031/Note-_automation.git'
            }
        }

        stage('Create Virtual Environment') {

            steps {

                bat 'py -m venv %VENV%'
            }
        }

        stage('Install Dependencies') {

            steps {

                bat '.\\%VENV%\\Scripts\\python -m pip install --upgrade pip'

                bat '.\\%VENV%\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Start Selenium Grid') {

            steps {

                bat 'docker compose down'

                bat 'docker compose up -d --scale chrome=2'
            }
        }

        stage('Prepare Reports') {

            steps {

                bat '''
                if not exist logs mkdir logs
                if not exist reports mkdir reports
                if not exist screenshots mkdir screenshots
                if not exist reports\\allure-results mkdir reports\\allure-results
                '''
            }
        }

        stage('Run Tests') {

            steps {

                script {

                    def status = bat(
                        returnStatus: true,
                        script: '.\\%VENV%\\Scripts\\pytest tests --alluredir=reports/allure-results --html=reports/report.html --self-contained-html'
                    )

                    if (status != 0) {

                        currentBuild.result = 'UNSTABLE'

                        echo "Pytest exited with code ${status}. Continuing to publish reports."
                    }
                }
            }
        }

        stage('Publish Allure Results') {

            steps {

                allure includeProperties: false,
                    jdk: '',
                    results: [[path: 'reports/allure-results']]
            }
        }
    }

    post {

        always {

            archiveArtifacts artifacts: 'reports/**,screenshots/**,logs/**',
                allowEmptyArchive: true,
                fingerprint: true

            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Automation Test Report'
            ])

            bat 'docker compose down'
        }

        success {

            echo 'Pipeline executed successfully'
        }

        unstable {

            echo 'Pipeline completed with test failures'
        }

        failure {

            echo 'Pipeline execution failed'
        }
    }
}
