pipeline {
    agent any

    environment {
        PROJECT_NAME      = "tfm-devsecops-demo"
        DEP_CHECK_OUT_DIR = "reports/dependency-check"
        TRIVY_OUT_DIR     = "reports/trivy"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build y pruebas') {
            steps {
                sh '''
                    echo "Ejecutando build y pruebas básicas..."
                '''
            }
        }

        stage('Analisis de dependencias (OWASP Dependency-Check)') {
            steps {
                sh '''
                  mkdir -p reports/dependency-check
                  mkdir -p .depcheck-data
                  docker run --rm \
                    -v "$PWD":/src \
                    -v "$PWD/.depcheck-data":/usr/share/dependency-check/data \
                    owasp/dependency-check:latest \
                    --project tfm-devsecops-demo \
                    --scan /src \
                    --format HTML \
                    --out /src/reports/dependency-check || true
                '''
            }
        }


        stage('Construccion imagen Docker') {
            steps {
                sh '''
                  echo "Construyendo imagen Docker de la aplicación..."
                  docker build -t tfm-devsecops-demo:latest backend
                '''
            }
        }

        stage('Analisis de imagen (Trivy)') {
            steps {
                sh '''
                    mkdir -p ${TRIVY_OUT_DIR}
                    mkdir -p .trivy-cache

                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v "$PWD/.trivy-cache":/root/.cache/ \
                        aquasec/trivy:latest \
                        image --exit-code 0 \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output /src/${TRIVY_OUT_DIR}/trivy-image.json \
                        ${PROJECT_NAME}:latest
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
        }
    }
}
