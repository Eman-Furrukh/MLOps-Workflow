pipeline {
    agent any

    environment {
        IMAGE_NAME = 'wahidimahrukh/mlops-workflow-app'
        CONTAINER_NAME = 'mlops-container'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Eman-Furrukh/MLOps-Workflow.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}")
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh "docker push ${IMAGE_NAME}"
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Stop old container if it exists
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                    // Run the new container
                    sh "docker run -d --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
    }
}
