//TODO Use shared repository
@Library('jenkins-shared-library@main') _

pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        TIMESTAMP = "${new Date().format('yyyyMMdd_HHmmss')}"
        REPO_URL = 'https://github.com/krotok/Check_Point_interview.git'
        PROJECT_DIR = 'project'
    }

    tools {
        python 'Python 3'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                echo 'Clean project working folder'
                dir("${PROJECT_DIR}") {
                    deleteDir()
                }
            }
        }

        stage('Clone Repo') {
            steps {
                dir("${PROJECT_DIR}") {
                    git url: "${REPO_URL}", branch: 'main'
                }
            }
        }

        stage('Setup Python & Playwright') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh '''
                        python -m venv ${VENV_DIR}
                        source ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        python -m playwright install
                    '''
                }
            }
        }

        def browsers = ['chromium', 'firefox', 'webkit'] //TODO move it to the job fields
        for (browser in browsers) {
            stage('Run Tests in Browsers "${browser}"') {
                steps {
                    script {

                            def reportFile = "report_${browser}_${env.TIMESTAMP}.html"
                            dir("${PROJECT_DIR}") {
                                sh """
                                    source ${VENV_DIR}/bin/activate
                                    pytest -n auto --browser=${browser} --html=reports/${reportFile} --self-contained-html
                                """
                            }
                    }
                }
            }
        }

        stage('Archive Reports and Screenshots') {
            steps {
                dir("${PROJECT_DIR}") {
                    archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
                    archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo "Remove the project"
            dir("${PROJECT_DIR}") {
                deleteDir()
            }
            echo "✅ Pipeline finished: ${env.TIMESTAMP}"
        }

        failure {
            echo "Test failed"
        }
    }
}
