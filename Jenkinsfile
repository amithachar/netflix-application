pipeline {
    agent any

     tools {
        sonarQube 'sonar-scanner'
    }

    environment {
        // Docker
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred-id')
        IMAGE_NAME = "amithachar/ott-app"
        DOCKER_BUILDKIT = "0"

        // SonarQube
        SONAR_TOKEN = credentials('sonar-token-id')

        // GCP
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
                set -e
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
                withSonarQubeEnv('sonar') {
                    sh '''
                    set -e
                    sonar-scanner \
                    -Dsonar.projectKey=sonars \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://34.133.65.101:9000 \
                    -Dsonar.login=9c9b8c09f9f2c19bbb5b915143515cf09356082c
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                set -e
                docker build --pull --no-cache -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                sh '''
                set -e
                trivy image --severity CRITICAL --exit-code 1 ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh '''
                set -e
                echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                docker push ${IMAGE_NAME}:latest
                docker logout
                '''
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh '''
                set -e
                gcloud config set project ${GCP_PROJECT_ID}
                gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${CLUSTER_ZONE}

                kubectl set image deployment/ott-app \
                ott-app=${IMAGE_NAME}:${BUILD_NUMBER}

                kubectl rollout status deployment/ott-app
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
