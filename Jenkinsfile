pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Clonando repositorio desde GitHub...'
                checkout scm
            }
        }

        stage('Build de prueba') {
            steps {
                echo 'Pipeline del TFM ejecutado correctamente.'
            }
        }
    }
}
