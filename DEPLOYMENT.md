# Step-by-Step Deployment Guide

## 1. Create GitHub repository
Create a repository named:
employee-management-2tier

Push all project files.

## 2. Local Docker test
```bash
docker compose up -d --build
docker compose ps
```

Open:
http://localhost:5000

Test:
```bash
curl http://localhost:5000/health
```

## 3. AWS EC2
Launch a Linux EC2 instance.

Allow inbound:
- SSH 22: My IP
- TCP 5000: My IP (for testing)

Connect using SSH.

Install Docker, Git, Python and Jenkins according to the official documentation for your Linux distribution.

## 4. Clone project
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd employee-management-2tier
```

Test:
```bash
docker compose up -d --build
```

Then visit:
http://<EC2-PUBLIC-IP>:5000

## 5. Jenkins
Create a Pipeline job.

Pipeline definition:
Pipeline script from SCM

SCM:
Git

Repository:
<YOUR_GITHUB_REPOSITORY_URL>

Script Path:
Jenkinsfile

Run Build Now.

## 6. Jenkins pipeline stages
1. Checkout
2. Install Test Dependencies
3. Run Tests
4. Build Docker Image
5. Deploy
6. Health Check

## 7. Resume evidence
Take screenshots of:
- GitHub repository
- Docker containers
- Running web application
- Jenkins successful pipeline
- AWS EC2 instance
- Application health endpoint

Never publish passwords, private keys, or access tokens in GitHub.
