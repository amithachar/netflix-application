pipeline {
    agent any

    environment {
        // Docker
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred-id')
        IMAGE_NAME = "amithachar/ott-app"

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

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
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

        stage('Authenticate to GCP using OIDC') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'gcp-oidc-token', variable: 'ID_TOKEN')]) {

                        writeFile file: 'id_token.txt', text: ID_TOKEN

                        sh """
                        gcloud iam workload-identity-pools create-cred-config ${PROVIDER_PATH} \
                          --service-account=${GCP_SA_EMAIL} \
                          --output-file=gcp-credentials.json \
                          --credential-source-file=id_token.txt
                        """

                        sh "gcloud auth login --cred-file=\$(pwd)/gcp-credentials.json"
                    }
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh """
                gcloud config set project ${GCP_PROJECT_ID}
                gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${CLUSTER_ZONE}

                sed -i 's|DOCKER_IMAGE|${IMAGE_NAME}:${BUILD_NUMBER}|g' k8s/deployment.yaml

                kubectl apply -f k8s/
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
