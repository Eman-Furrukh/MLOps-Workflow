pipeline {
    agent any

    environment {
        IMAGE_NAME = 'wahidimahrukh/mlops-workflow-app'
        CONTAINER_NAME = 'mlops-container'
        DOCKER_REGISTRY = 'docker.io'
    }

    stages {
        stage('Clean Docker Environment') {
            steps {
                script {
                    bat """
                        docker builder prune -af || echo "Builder prune failed"
                        docker system prune -af || echo "System prune failed"
                    """
                }
            }
        }

        stage('Clone Repository') {
            steps {
                git branch: 'main', 
                     url: 'https://github.com/Eman-Furrukh/MLOps-Workflow.git'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    script {
                        bat "echo %DOCKER_PASS% | docker login %DOCKER_REGISTRY% -u %DOCKER_USER% --password-stdin"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build --no-cache -t %IMAGE_NAME% ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    retry(3) {
                        bat "docker push %IMAGE_NAME%"
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    bat """
                        docker stop %CONTAINER_NAME% 2> nul || echo Container not running
                        docker rm %CONTAINER_NAME% 2> nul || echo Container not found
                        docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed. Cleaning up...'
            script {
                bat "docker system prune -f 2> nul || echo Docker cleanup failed"
            }
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}