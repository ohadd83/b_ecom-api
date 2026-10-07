pipeline {

    agent any

    environment {

        // Docker Hub repository
        IMAGE_NAME = "ohadd306/python-ecommerce-api"

        // Docker container name
        CONTAINER_NAME = "python-ecommerce-api"

        // Application port on EC2
        APP_PORT = "8000"
        // app STG port on EC2
        STG_APP_PORT = '8002'
        // Jenkins build number becomes the image version
        IMAGE_TAG = "${BUILD_NUMBER}"
        // save the last successful build version
        ROLLBACK_FILE = "/var/lib/jenkins/last_successful_tag"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test') {

            steps {

                echo "Running Python tests..."

                sh '''
                    python3 -m pytest -v
                '''
            }
        }


// build docker image

        stage('Build Docker Image') {

            steps {

                echo "Building Docker image..."

                sh '''
                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        .
                '''
            }
        }


//test docker image

        stage('Test Docker Image') {

            steps {

                echo "Starting temporary test container..."

                sh '''
                    docker run -d \
                        --name ${CONTAINER_NAME}-test \
                        -p 8001:8000 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''

                echo "Waiting for application..."

                sleep 5

                echo "Running health check..."
                
                
//                docker ps 
//                docker inspect python-ecommerce-api --format='{{.State.Status}}' | grep running
               

                sh '''
                    curl -f http://localhost:8001/health
               
                    curl -f  -X POST  -H "Content-Type: application/json" -d '{"product_id":1,"quantity":3}' http://localhost:8001/orders/

                    curl -f http://localhost:8001/products/2
                '''
            }

            post {

                always {

                    echo "Removing test container..."

                    sh '''
                        docker rm -f ${CONTAINER_NAME}-test || true
                    '''
                }
            }
        }


// push docker image

        stage('Push to Docker Hub') {

            steps {

                echo "Logging into Docker Hub..."

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    sh '''
                        echo "$DOCKER_PASSWORD" | \
                        docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin

                        docker push \
                            ${IMAGE_NAME}:${IMAGE_TAG}

                        docker logout
                    '''
                }
            }
        }

// deploy STG application 
        stage('Deploy stg') {
            steps {
                echo "deploy app in STG"
                sh '''
                    docker stop ${CONTAINER_NAME}-stg  ||  true 
                    docker rm ${CONTAINER_NAME}-stg  || true 
                    docker pull ${IMAGE_NAME}:${IMAGE_TAG}
                    docker run -d --name ${CONTAINER_NAME}-stg -p ${STG_APP_PORT}:8000  ${IMAGE_NAME}:${IMAGE_TAG}
          '''
                  }
         }

// Manual approve production deploy 

//stage('Approve Production Deployment') {
  //  steps {
    //    input message: 'Deploy this version to PRODUCTION?',
      //        ok: 'Deploy to Production'
 //   }
//}

// Manual approve 

stage('Approve Production Deploy') {

    steps { 
        input(
            message: """
                Production Deployment Approval

                Application: ${IMAGE_NAME}
                Version: ${IMAGE_TAG}
                Build: ${BUILD_NUMBER}

                Deploy this version to PRODUCTION?
            """,
            ok: "Deploy ${IMAGE_TAG}",
            submitter: "ohad"
             )
    }
}

        
//  deploy application

        stage('Deploy') {

            steps {

                echo "Deploying application..."

                sh '''
                    docker stop ${CONTAINER_NAME} || true  

                    docker rm ${CONTAINER_NAME} || true

                    docker pull \
                        ${IMAGE_NAME}:${IMAGE_TAG}

                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:8000 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Record Successful Deployment') {
            steps {
               writeFile(
                  file: env.ROLLBACK_FILE,
                  text: "${BUILD_NUMBER}"
             )

                  echo "Recorded successful deployment: ${BUILD_NUMBER}"
                  }
       }



// production healthcheck 

        stage('Health Check') {

            steps {

                echo "Checking production application..."

                sleep 5

                sh '''
                    curl -f    http://localhost:${APP_PORT}/health
                    curl -f  http://localhost:${APP_PORT}/products/ 
                '''
            }
        }
    }




// pipeline result 

    post {

        success {

            echo """
            ==========================================
              DEPLOYMENT SUCCESSFUL
            ==========================================

            Application:
            ${IMAGE_NAME}:${IMAGE_TAG}

            Container:
            ${CONTAINER_NAME}

            Port:
            ${APP_PORT}

            ==========================================
            """
        }

        failure {

            echo """
            ==========================================
              PIPELINE FAILED
            ==========================================
            """

        echo "Production deployment failed!"
        echo "Starting rollback..."

        sh '''
            ROLLBACK_TAG=$(cat /var/lib/jenkins/last_successful_tag)
            docker pull ${IMAGE_NAME}:${ROLLBACK_TAG}

            docker stop ${CONTAINER_NAME} || true
            docker rm ${CONTAINER_NAME} || true

            docker run -d \
                --name ${CONTAINER_NAME} \
                -p ${APP_PORT}:8000 \
                ${IMAGE_NAME}:${ROLLBACK_TAG}
        '''

            echo """
            ==========================================
              ROLLBACK FINISHED 
            ==========================================
            """
        }
    }
}
