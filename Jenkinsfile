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
                  docker build -t tfm-devsecops-demo:latest .
                '''
            }
        }

        stage('Analisis de imagen (Trivy)') {
            steps {
                sh '''
                  mkdir -p reports/trivy
                  mkdir -p .trivy-cache
                  docker run --rm \
                    -v /var/lib/jenkins/workspace/tfm-devsecops-pipeline:/src \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    -v /var/lib/jenkins/workspace/tfm-devsecops-pipeline/.trivy-cache:/root/.cache/ \
                    aquasec/trivy:latest image \
                      --exit-code 1 \
                      --severity HIGH,CRITICAL \
                      --format json \
                      --output /src/reports/trivy/trivy-image.json \
                      tfm-devsecops-demo:latest
                      tfm-devsecops-demo:latest
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
