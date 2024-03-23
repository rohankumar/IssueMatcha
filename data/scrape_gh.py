import pandas as pd
import os
import json

from github import Github
from github import Auth

from dotenv import load_dotenv
from repos import REPOS
from tqdm import tqdm

load_dotenv()

# login
auth_token = os.environ["AUTH_TOKEN"]

auth = Auth.Token(auth_token)
g = Github(auth=auth)

# Get the repository
for domain, repository_names in REPOS.items():
    for repo in repository_names:
        print(f"Parsing {repo}")

        repository = g.get_repo(repo)
        issues = repository.get_issues()
        
        try:
            readme = repository.get_contents("README.md")
            if not readme:
                readme = repository.get_contents("README.rst")
        except:
            print("Readme file not found!")

        readme_content = {"markdown": str(readme.decoded_content.decode())}

        titles = []
        body = []
        labels = []
        comments = []

        # Store issues along with their labels
        for issue in tqdm(issues):
            if len(issue.labels):
                all_comments = issue.get_comments()
                comments.append([c.body for c in all_comments])
                titles.append(issue.title)
                body.append(issue.body)
                labels.append([label.name for label in issue.labels])

        d = {'title': titles, 'body': body, 'comments': comments, 'labels': labels}
        df = pd.DataFrame(data=d)

        # make result folder
        folder_name = repo.split("/")[1]
        path = f"files/{domain}/{folder_name}"
        if not os.path.exists(path):
            os.makedirs(f"files/{domain}/{folder_name}")
        
        df.to_json(f'files/{domain}/{folder_name}/issues.json', orient='records')
        
        with open(f'files/{domain}/{folder_name}/README.json', 'w') as json_file:
            json.dump(readme_content, json_file)
    
