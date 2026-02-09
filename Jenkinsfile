pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred-id')
        GCP_CREDENTIALS = credentials('gcp-service-account')
        IMAGE_NAME = "yourdockerhub/ott-app"
        PROJECT_ID = "your-gcp-project-id"
        CLUSTER_NAME = "ott-cluster"
        CLUSTER_ZONE = "us-central1"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh """
                echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                docker push $IMAGE_NAME:$BUILD_NUMBER
                docker tag $IMAGE_NAME:$BUILD_NUMBER $IMAGE_NAME:latest
                docker push $IMAGE_NAME:latest
                """
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh """
                echo $GCP_CREDENTIALS > gcp-key.json
                gcloud auth activate-service-account --key-file=gcp-key.json
                gcloud config set project $PROJECT_ID
                gcloud container clusters get-credentials $CLUSTER_NAME --zone $CLUSTER_ZONE

                sed -i 's|DOCKERHUB_USERNAME/ott-app:latest|$IMAGE_NAME:$BUILD_NUMBER|g' k8s/deployment.yaml

                kubectl apply -f k8s/
                """
            }
        }
    }
}
