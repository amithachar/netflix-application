pipeline {
    agent any

    environment {

        // Docker Image + ACR
        IMAGE_NAME = "ott-app"
        ACR_NAME = "amithacr12345"
        ACR_LOGIN_SERVER = "amithacr12345.azurecr.io"

        DOCKER_BUILDKIT = "0"

        // Azure
        AKS_RESOURCE_GROUP = "aks-rg"
        AKS_CLUSTER_NAME = "prod-aks"
        AZURE_SUBSCRIPTION_ID = "836f3bf3-eb77-4b81-be9c-88d7e07e0da7"
        AZURE_TENANT_ID = "1a11d729-ee9e-44cc-a724-244076864120"

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

        // stage('Verify Sonar Tool') {
        //     steps {
        //         sh 'which sonar-scanner || echo "Scanner not found"'
        //         sh 'sonar-scanner --version || echo "Version check failed"'
        //     }
        // }

        // stage('SonarQube Analysis') {
        //     steps {
        //         script {
        //             withSonarQubeEnv('sonar') {

        //                 sh '''
        //                 sonar-scanner \
        //                 -Dsonar.projectKey=sonarsss \
        //                 -Dsonar.sources=. \
        //                 -Dsonar.host.url=http://34.41.234.160:9000 \
        //                 -Dsonar.login=your-sonar-token
        //                 '''
        //             }
        //         }
        //     }
        // }

        stage('Build Docker Image') {
            steps {
                sh '''
                set -e

                docker build --pull --no-cache \
                -t ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        // stage('Trivy Scan') {
        //     steps {
        //         sh '''
        //         set -e

        //         trivy image \
        //         --severity CRITICAL \
        //         --exit-code 1 \
        //         ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${BUILD_NUMBER}
        //         '''
        //     }
        // }

        stage('Push to ACR') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'azure-sp',
                        usernameVariable: 'AZ_CLIENT_ID',
                        passwordVariable: 'AZ_CLIENT_SECRET'
                    )
                ]) {

                    sh '''
                    set -e

                    az login --service-principal \
                    -u ${AZ_CLIENT_ID} \
                    -p ${AZ_CLIENT_SECRET} \
                    --tenant ${AZURE_TENANT_ID}

                    az account set \
                    --subscription ${AZURE_SUBSCRIPTION_ID}

                    az acr login \
                    --name ${ACR_NAME}

                    docker push ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${BUILD_NUMBER}

                    docker tag \
                    ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${BUILD_NUMBER} \
                    ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:latest

                    docker push \
                    ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

       stage('Deploy to AKS') {

    steps {

        withCredentials([
            usernamePassword(
                credentialsId: 'azure-sp',
                usernameVariable: 'AZ_CLIENT_ID',
                passwordVariable: 'AZ_CLIENT_SECRET'
            )
        ]) {

            sh '''
            set -e

            az login --service-principal \
            -u ${AZ_CLIENT_ID} \
            -p ${AZ_CLIENT_SECRET} \
            --tenant ${AZURE_TENANT_ID}

            az account set \
            --subscription ${AZURE_SUBSCRIPTION_ID}

            az aks get-credentials \
            --resource-group ${AKS_RESOURCE_GROUP} \
            --name ${AKS_CLUSTER_NAME} \
            --overwrite-existing

            if kubectl get deployment ott-app >/dev/null 2>&1
            then
                echo "Deployment exists. Updating image..."

                kubectl set image deployment/ott-app \
                ott-app=${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${BUILD_NUMBER}

                kubectl rollout status deployment/ott-app

            else
                echo "Deployment not found. Creating deployment..."

                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f service.yaml
            fi

            kubectl get pods
            kubectl get svc
            '''
        }
    }
}

} // closes stages

post {
    always {
        cleanWs()
    }
}

} // closes pipeline