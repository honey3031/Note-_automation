pipeline {

    agent any

    environment {

        EXECUTION = 'remote'

        GRID_URL =
        'http://localhost:4444/wd/hub'

        BROWSER = 'chrome'
    }

    stages {

        stage('Checkout Source Code') {

            steps {

                git branch: 'main',
                url: 'https://github.com/honey3031/Note-_automation.git'
            }
        }

        stage('Start Selenium Grid') {

            steps {

                bat 'docker compose down'

                bat 'docker compose up -d --scale chrome=2'
            }
        }

        stage('Install Dependencies') {

            steps {

                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Parallel Tests') {

            steps {

                bat '''
                pytest -n 2 ^
                --alluredir=allure-results ^
                --html=reports/report.html ^
                --self-contained-html
                '''
            }
        }

        stage('Generate Allure Report') {

            steps {

                bat '''
                allure generate allure-results ^
                --clean -o allure-report
                '''
            }
        }
    }

    post {

        always {

            archiveArtifacts artifacts: '''
                reports/*,
                allure-report/*,
                screenshots/*
            '''
        }
    }
}