pipeline {
    agent any

    environment {
        ACR_NAME = "myacrterraform1234"
        RESOURCE_GROUP = "rg-aks-demo"
        AKS_CLUSTER = "aks-demo-cluster"
        TENANT_ID = "1a11d729-ee9e-44cc-a724-244076864120"
        IMAGE_NAME = "ott-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} .
                    """
                }
            }
        }

        stage('Login to Azure') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'jenkins-sp',
                                                 usernameVariable: 'AZURE_CLIENT_ID',
                                                 passwordVariable: 'AZURE_CLIENT_SECRET')]) {
                    sh """
                    az login --service-principal \
                      --username $AZURE_CLIENT_ID \
                      --password $AZURE_CLIENT_SECRET \
                      --tenant 1a11d729-ee9e-44cc-a724-244076864120
                    """
                }
            }
        }

        stage('Push to ACR') {
            steps {
                sh """
                az acr login --name $ACR_NAME
                docker push ${ACR_NAME}.azurecr.io/$IMAGE_NAME:$IMAGE_TAG
                """
            }
        }

stage('Deploy to AKS') {
    steps {
        sh """
        az aks get-credentials \
          --resource-group $RESOURCE_GROUP \
          --name $AKS_CLUSTER \
          --overwrite-existing

        kubectl apply -f deployment.yml
        kubectl apply -f service.yml

        kubectl set image deployment/ott-app \
          ott-app=${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}

        kubectl rollout status deployment/ott-app
        """
        }
    }
}
