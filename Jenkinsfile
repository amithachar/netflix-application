pipeline {
    agent any

    environment {
        // Docker
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred-id')
        IMAGE_NAME = "amithachar/ott-app"
        DOCKER_BUILDKIT = "0"


        // GCP Workload Identity
        GCP_PROJECT_ID     = "project-3a9d1629-f247-457c-ae4"
        GCP_PROJECT_NUMBER = "579466139442"
        GCP_POOL_ID        = "jenkins-pool"
        GCP_PROVIDER_ID    = "jenkins-provider"
        GCP_SA_EMAIL       = "jenkins-terraform-sa@project-3a9d1629-f247-457c-ae4.iam.gserviceaccount.com"

        CLUSTER_NAME = "cluster-1"
        CLUSTER_ZONE = "us-central1-a"

        PROVIDER_PATH = "projects/${GCP_PROJECT_NUMBER}/locations/global/workloadIdentityPools/${GCP_POOL_ID}/providers/${GCP_PROVIDER_ID}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest coverage
                '''
            }
        }
        stage('SonarQube Analysis') {
             steps {
        // This wrapper provides the SonarQube server details to the build tool
        withSonarQubeEnv('sonar') { 
            // Replace this with your actual build command (sh or bat)
            sh './mvnw sonar:sonar' 
            // OR if using Sonar Scanner directly:
            // sh 'sonar-scanner'
        }
    }
}

        stage('Build Docker Image') {
            steps {
                sh "docker build --pull --no-cache -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Trivy Scan') {
            steps {
                sh """
                trivy image --severity CRITICAL --exit-code 1 ${IMAGE_NAME}:${BUILD_NUMBER}
                """
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh """
                echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                docker push ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh """
                gcloud config set project ${GCP_PROJECT_ID}
                gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${CLUSTER_ZONE}

                kubectl set image deployment/ott-app \
                ott-app=${IMAGE_NAME}:${BUILD_NUMBER}

                kubectl rollout status deployment/ott-app
                """
            }
        }
    }

    post {
        always {
            sh "rm -f gcp-credentials.json id_token.txt"
        }
    }
}
