pipeline {
    agent any

    environment {
        IMAGE_NAME = 'wahidimahrukh/mlops-workflow-app'
        CONTAINER_NAME = 'mlops-container'
        DOCKER_REGISTRY = 'docker.io' // Explicitly specify Docker registry
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
                        // Login to Docker Hub with credential security
                        sh '''
                            docker login ${DOCKER_REGISTRY} \
                                -u "$DOCKER_USER" \
                                -p "$DOCKER_PASS"
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build with proper tagging and cache handling
                    docker.build("${IMAGE_NAME}", "--no-cache .")
                    
                    // Alternative if docker.build doesn't work:
                    // sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Push with retry logic
                    retry(3) {
                        sh "docker push ${IMAGE_NAME}"
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Clean up any existing container
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                    
                    // Run new container with proper port mapping if needed
                    sh """
                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            -p 5000:5000 \  # Add port mapping if your app exposes ports
                            ${IMAGE_NAME}
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed. Cleaning up...'
            script {
                // Optional: Clean up unused Docker resources
                sh 'docker system prune -f || true'
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