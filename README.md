# Employee Management System - 2-Tier DevOps Project

## Project Overview
A containerized employee management web application built with Flask and MySQL. Jenkins automates testing, Docker image creation, and deployment.

## Architecture
Browser -> Flask Web Container -> MySQL Database Container

## Technologies
- Python / Flask
- HTML / CSS
- MySQL 8
- Docker
- Docker Compose
- Jenkins
- GitHub
- AWS EC2

## Features
- Add employee
- View employees
- Edit employee
- Delete employee
- Database health endpoint
- Automated tests
- Jenkins CI/CD pipeline

## Run locally
```bash
docker compose up -d --build
```

Open:
http://localhost:5000

Health check:
http://localhost:5000/health

Stop:
```bash
docker compose down
```

## Jenkins
Create a Jenkins Pipeline job connected to the GitHub repository and use the included Jenkinsfile.

The Jenkins host must have Docker, Docker Compose, Python 3 and Git installed. The Jenkins user needs permission to execute Docker commands.

## AWS EC2
Use an EC2 Linux instance, install Docker, Git, Python and Jenkins, clone the repository, and configure the Jenkins pipeline.

For a production deployment, move passwords/secrets to Jenkins credentials or AWS Secrets Manager rather than keeping them in docker-compose.yml.
