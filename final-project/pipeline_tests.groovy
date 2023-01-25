pipeline {

    agent any
    stages {
        stage('Clone repo') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/alfomin11/VK-final-project.git']]
                ])
            }
        }

        stage('Run docker-compose') {
            steps {
                step([
                    $class: 'DockerComposeBuilder',
                    dockerComposeFile: 'final-project/docker-compose.yml',
                    option: [$class: 'StartAllServices'],
                    useCustomDockerComposeFile: true
                ])
            }
        }


        stage('Stop myapp') {
            steps {
                step([
                    $class: 'DockerComposeBuilder',
                    dockerComposeFile: 'final-project/docker-compose.yml',
                    option: [$class: 'StopAllServices'],
                    useCustomDockerComposeFile: true
                ])
            }
        }
    }


    post {
        always {
            allure([
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'alluredir']]
            ])
        }
    }
}
