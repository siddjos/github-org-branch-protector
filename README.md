# GitHub Organization Branch Protector

This project provides an automated solution to enforce branch protection rules across all repositories in a GitHub organization. It runs as a Kubernetes CronJob, periodically checking and enabling branch protection on default branches if not already configured.

## Features

- Automatically enables branch protection on default branches for all repositories in a GitHub organization
- Uses GitHub's GraphQL API for efficient querying and updating
- Runs as a Kubernetes CronJob for easy scheduling and management
- Configurable branch protection rules

## Requirements

- Python 3.11+
- Docker
- Kubernetes cluster
- GitHub Personal Access Token with appropriate permissions

## Installation

1. Clone the repository:

git clone https://github.com/your-username/github-org-branch-protector.git
cd github-org-branch-protector

2. Build the Docker image:

docker build -t github-org-branch-protector:latest .

3. Push the image to your container registry.

4. Create a Kubernetes Secret for your GitHub token:

kubectl create secret generic github-token --from-literal=GITHUB_TOKEN=your-github-token-here

5. Apply the Kubernetes CronJob:

kubectl apply -f k8s-cronjob.yaml

## Configuration

Edit the `k8s-cronjob.yaml` file to configure:

- Schedule: Modify the `schedule` field to change the frequency of runs.
- Organization: Set the `GITHUB_ORG_NAME` environment variable to your organization's name.

To modify branch protection rules, edit the `enable_protection_mutation` in `github_branch_protection.py`.

## Usage

Once deployed, the CronJob will automatically run according to the specified schedule. You can manually trigger a job run with: