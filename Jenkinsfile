pipeline {

    agent any

    options {

        timeout(
            time: 30,
            unit: 'MINUTES'
        )
    }

    environment {

        VENV = 'venv'

        EXECUTION = 'remote'

        GRID_URL = 'http://localhost:4444/wd/hub'

        BROWSER = 'chrome'

        NOTES_CREDS = credentials('notes-creds')
    }

    stages {

        stage('Create Virtual Environment') {

            steps {

                bat 'py -m venv %VENV%'
            }
        }

        stage('Install Dependencies') {

            steps {

                bat '.\\%VENV%\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Start Selenium Grid') {

            steps {

                bat 'docker compose down'

                bat 'docker compose up -d --scale chrome=2'

                sleep(time: 15, unit: 'SECONDS')
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

                withEnv([
                    "EMAIL=${NOTES_CREDS_USR}",
                    "PASSWORD=${NOTES_CREDS_PSW}"
                ]) {

                    script {

                        def status = bat(
                            returnStatus: true,
                            script: """
                            .\\%VENV%\\Scripts\\pytest ^
                            -n 2 ^
                            tests ^
                            --alluredir=reports/allure-results ^
                            --html=reports/report.html ^
                            --self-contained-html
                            """
                        )

                        if (status != 0) {

                            currentBuild.result = 'UNSTABLE'

                            echo "Pytest exited with code ${status}"
                        }
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

            archiveArtifacts(
                artifacts: 'reports/**,screenshots/**,logs/**',
                allowEmptyArchive: true,
                fingerprint: true
                
            )

            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Automation Test Report'
            ])

            bat 'if exist docker-compose.yml docker compose down'
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