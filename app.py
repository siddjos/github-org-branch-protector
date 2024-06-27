import os
import requests
from datetime import datetime

# GitHub GraphQL API endpoint
GITHUB_API_URL = "https://api.github.com/graphql"

# GitHub Personal Access Token (store this securely in Kubernetes secrets)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Organization name
ORG_NAME = os.environ.get("GITHUB_ORG_NAME")

# GraphQL query to get repositories and their default branch protection status
query = """
query($org: String!, $cursor: String) {
  organization(login: $org) {
    repositories(first: 100, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        name
        defaultBranchRef {
          name
          branchProtectionRule {
            id
          }
        }
      }
    }
  }
}
"""

# GraphQL mutation to enable branch protection
enable_protection_mutation = """
mutation($repositoryId: ID!, $pattern: String!) {
  createBranchProtectionRule(input: {
    repositoryId: $repositoryId,
    pattern: $pattern,
    requiresApprovingReviews: true,
    requiredApprovingReviewCount: 1,
    dismissesStaleReviews: true,
    restrictsReviewDismissals: true,
    requiresStatusChecks: true,
    requiresStrictStatusChecks: true,
    requiresCodeOwnerReviews: true,
    isAdminEnforced: true
  }) {
    branchProtectionRule {
      id
    }
  }
}
"""

def run_query(query, variables):
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(GITHUB_API_URL, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code: {response.status_code}. {response.text}")

def enable_branch_protection(repo_id, branch_name):
    variables = {
        "repositoryId": repo_id,
        "pattern": branch_name
    }
    result = run_query(enable_protection_mutation, variables)
    return result["data"]["createBranchProtectionRule"]["branchProtectionRule"]["id"]

def main():
    print(f"Starting branch protection check at {datetime.now()}")
    
    has_next_page = True
    cursor = None
    
    while has_next_page:
        variables = {"org": ORG_NAME, "cursor": cursor}
        result = run_query(query, variables)
        
        repos = result["data"]["organization"]["repositories"]
        
        for repo in repos["nodes"]:
            repo_name = repo["name"]
            default_branch = repo["defaultBranchRef"]["name"]
            protection_rule = repo["defaultBranchRef"]["branchProtectionRule"]
            
            if not protection_rule:
                print(f"Enabling branch protection for {repo_name} on branch {default_branch}")
                enable_branch_protection(repo["id"], default_branch)
            else:
                print(f"Branch protection already enabled for {repo_name} on branch {default_branch}")
        
        has_next_page = repos["pageInfo"]["hasNextPage"]
        cursor = repos["pageInfo"]["endCursor"]
    
    print(f"Finished branch protection check at {datetime.now()}")

if __name__ == "__main__":
    main()