pipeline {
    agent any

    environment {
        // Docker configuration
        IMAGE_NAME = 'wahidimahrukh/mlops-workflow-app'
        CONTAINER_NAME = 'mlops-container'
        DOCKER_REGISTRY = 'docker.io'
        
        // Port configuration - CHANGED TO 5001
        HOST_PORT = '5001'  
        CONTAINER_PORT = '5000'
        
        // Timeout settings
        CONTAINER_STOP_TIMEOUT = '10'
    }

    stages {
        stage('Clean Docker Environment') {
            steps {
                script {
                    bat """
                        echo "Cleaning up Docker environment..."
                        docker builder prune -af || echo "Builder prune failed"
                        docker system prune -af || echo "System prune failed"
                        echo "Cleanup completed"
                    """
                }
            }
        }

        stage('Clone Repository') {
            steps {
                git branch: 'main', 
                     url: 'https://github.com/Eman-Furrukh/MLOps-Workflow.git',
                     poll: true
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
                        bat """
                            echo "Logging into Docker Hub..."
                            echo %DOCKER_PASS% | docker login %DOCKER_REGISTRY% -u %DOCKER_USER% --password-stdin
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat """
                        echo "Building Docker image..."
                        docker build --no-cache -t %IMAGE_NAME% .
                        echo "Image built successfully"
                    """
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    retry(3) {
                        bat """
                            echo "Pushing image to Docker Hub..."
                            docker push %IMAGE_NAME%
                            echo "Image pushed successfully"
                        """
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    bat """
                        echo "Starting container on port %HOST_PORT%..."
                        docker stop %CONTAINER_NAME% --time %CONTAINER_STOP_TIMEOUT% 2> nul || echo "No running container to stop"
                        docker rm %CONTAINER_NAME% 2> nul || echo "No container to remove"
                        docker run -d --name %CONTAINER_NAME% -p %HOST_PORT%:%CONTAINER_PORT% %IMAGE_NAME%
                        echo "Container started successfully on port %HOST_PORT%"
                        echo "Application should be available at: http://localhost:%HOST_PORT%"
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed. Cleaning up...'
            script {
                bat """
                    echo "Performing final cleanup..."
                    docker system prune -f 2> nul || echo "Cleanup failed"
                """
            }
        }
        success {
            echo 'Pipeline succeeded!'
            script {
                echo "Application is running at: http://localhost:${env.HOST_PORT}"
            }
        }
        failure {
            echo 'Pipeline failed!'
            script {
                bat "docker logs %CONTAINER_NAME% 2> nul || echo 'No container logs available'"
            }
        }
    }
}