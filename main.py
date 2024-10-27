import requests
import pandas as pd
import json

# Set the city and minimum followers
city = "Chennai"
min_followers = 100
token = ""

# Set headers for authentication
headers = {"Authorization": f"token {token}"}

# GitHub Search API URL for users
base_url = "https://api.github.com/search/users"
query = f"location:{city} followers:>{min_followers}"
params = {"q": query, "per_page": 10}

# Initialize lists to store user and repository data
users_data = []
repositories_data = []
page = 1

while True:
    response = requests.get(base_url, headers=headers, params={**params, "page": page})
    data = response.json()
    users = data.get("items", [])
    
    if not users:
        break  # Stop if no users are found or we reach the end
    
    for user in users:
        # Fetch detailed user profile information
        user_profile_response = requests.get(f"https://api.github.com/users/{user['login']}", headers=headers)
        user_profile = user_profile_response.json()
        
        # Clean the company field
        company = user_profile.get("company", "")
        if company:
            company = company.strip().lstrip('@').upper()
        
        # Collect user data with the requested fields
        user_data = {
            "login": user_profile.get("login"),
            "name": user_profile.get("name"),
            "company": company,
            "location": user_profile.get("location"),
            "email": user_profile.get("email"),
            "hireable": user_profile.get("hireable"),
            "bio": user_profile.get("bio"),
            "public_repos": user_profile.get("public_repos"),
            "followers": user_profile.get("followers"),
            "following": user_profile.get("following"),
            "created_at": user_profile.get("created_at")
        }
        
        users_data.append(user_data)
        
        # Fetch up to 500 of the user's most recently pushed repositories
        repos_url = user["repos_url"]
        repo_page = 1
        while True:
            repo_response = requests.get(repos_url, headers=headers, params={"page": repo_page, "per_page": 100})
            repos = repo_response.json()
            
            if not repos or repo_page * 100 >= 500:
                break  # Stop if no more repos or we've fetched 500 repos
            
            for repo in repos:
                repo_data = {
                    "login": user_profile.get("login"),
                    "full_name": repo.get("full_name"),
                    "created_at": repo.get("created_at"),
                    "stargazers_count": repo.get("stargazers_count"),
                    "watchers_count": repo.get("watchers_count"),
                    "language": repo.get("language"),
                    "has_projects": repo.get("has_projects"),
                    "has_wiki": repo.get("has_wiki"),
                    "license_name": repo.get("license", {}).get("name") if repo.get("license") else None
                }
                repositories_data.append(repo_data)
            
            repo_page += 1

    page += 1

# Save users data to CSV
df_users = pd.DataFrame(users_data)
df_users.to_csv("users.csv", index=False)

# Save repositories data to CSV
df_repositories = pd.DataFrame(repositories_data)
df_repositories.to_csv("repositories.csv", index=False)

# Optional: Save JSON files for reference
with open("github_users.json", "w") as f:
    json.dump(users_data, f, indent=4)

with open("github_repositories.json", "w") as f:
    json.dump(repositories_data, f, indent=4)

print("Data saved to users.csv, repositories.csv, github_users.json, and github_repositories.json")
