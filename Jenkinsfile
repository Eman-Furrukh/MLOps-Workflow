pipeline {
    agent any

    environment {
        IMAGE_NAME = 'wahidimahrukh/mlops-workflow-app'
        CONTAINER_NAME = 'mlops-container'
        DOCKER_REGISTRY = 'docker.io'
    }

    stages {
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
                        bat "docker login %DOCKER_REGISTRY% -u %DOCKER_USER% -p %DOCKER_PASS%"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t %IMAGE_NAME% ."
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
                    // Clean up any existing container
                    bat """
                        docker stop %CONTAINER_NAME% 2> nul || echo Container not running
                        docker rm %CONTAINER_NAME% 2> nul || echo Container not found
                    """
                    
                    // Run new container and verify it's running
                    bat """
                        docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%
                        timeout /t 30 /nobreak
                        for /l %%x in (1,1,10) do (
                          docker inspect -f \"{{.State.Running}}\" %CONTAINER_NAME% | findstr \"true\" && exit /b 0
                          timeout /t 3 /nobreak
                        )
                        exit /b 1
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