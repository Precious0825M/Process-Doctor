# PR Creation Troubleshooting Guide

## Error: Repository Not Found (404)

The error you're seeing indicates that the GitHub repository cannot be accessed. Here's how to fix it:

### 1. Verify Repository Exists

Make sure the repository exists and you have the correct name format:
- Format should be: `owner/repo` (e.g., `octocat/hello-world`)
- Check that the repository name is spelled correctly
- Verify the repository exists on GitHub

### 2. Check GitHub Token

Your GitHub token needs proper permissions:

```bash
# Check if GITHUB_TOKEN is set in backend/.env
cat backend/.env | grep GITHUB_TOKEN
```

The token must have:
- ✅ `repo` scope (full control of private repositories)
- ✅ Access to the target repository
- ✅ Not expired

### 3. Create a New GitHub Token (if needed)

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "ProcessDoctor PR Creator")
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. Copy the token immediately (you won't see it again!)
7. Update `backend/.env`:
   ```
   GITHUB_TOKEN=ghp_your_new_token_here
   ```

### 4. Test Repository Access

Create a test script to verify access:

```bash
cd backend
python -c "
from github import Github
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('GITHUB_TOKEN')
g = Github(token)

# Test with your repository
repo_name = 'owner/repo'  # Replace with your repo
try:
    repo = g.get_repo(repo_name)
    print(f'✅ Successfully accessed: {repo.full_name}')
    print(f'   Default branch: {repo.default_branch}')
    print(f'   Permissions: {repo.permissions}')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### 5. Alternative: Use a Public Test Repository

If you don't have a repository yet, create a test one:

1. Go to GitHub and create a new repository
2. Make it public (easier for testing)
3. Initialize with a README
4. Use the format: `your-username/your-repo-name`

### 6. Restart Backend Server

After updating the token:

```bash
cd backend
# Kill the existing server (Ctrl+C)
# Restart it
uvicorn app.main:app --reload --port 8000
```

## Common Issues

### Issue: "Resource not accessible by integration"
**Solution:** Your token doesn't have `repo` scope. Create a new token with proper permissions.

### Issue: "Bad credentials"
**Solution:** Your token is invalid or expired. Generate a new one.

### Issue: "Not Found" for a repository you own
**Solution:** 
- Verify the repository name format is `owner/repo`
- Check if the repository is private and your token has private repo access
- Make sure you're using the correct GitHub account

## Testing the Fix

Once you've updated your token, test the PR creation:

1. Start the backend server
2. In the frontend, enter a valid repository name (e.g., `your-username/test-repo`)
3. Click "Approve and deploy"
4. Check the backend logs for detailed error messages

## Need More Help?

Check the backend logs for detailed error messages:
```bash
# Backend logs will show:
# - Repository access attempts
# - Authentication status
# - Detailed GitHub API errors
```

The improved error handling now provides specific guidance based on the error type (404, 401, 403).