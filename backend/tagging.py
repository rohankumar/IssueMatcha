import os
import json
from backend.prompts.tagging import tagging_prompt, summary_prompt

def generate_tags(tag_input, summ_ip):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"
    client = MistralClient(api_key=api_key)
    tag_msgs = [
        ChatMessage(role="user", content=tagging_prompt.replace('{query_str}', tag_input))
    ]
    repo_msgs = [ChatMessage(role="user", content=summary_prompt.replace('{query_str}', summ_ip))]
    repo_tags = client.chat(
        model=model,
        response_format={"type": "json_object"},
        messages=tag_msgs,
    )
    repo_summary = client.chat(
        model=model,
        response_format={"type": "json_object"},
        messages=repo_msgs,
    )
    tags = repo_tags.choices[0].message.content
    summ = repo_summary.choices[0].message.content
    output = dict()
    output.update(json.loads(tags))
    output.update(json.loads(summ))
    return output

def load_domain(path):
    repo_docs = []
    issue_docs = []
    for repo in os.listdir(path):
        all_repo_tags = []
        repo_doc = json.load(open(f'{path}/{repo}/README.json', 'r'))
        issues = json.load(open(f'{path}/{repo}/issues.json', 'r'))
        for i in issues:
            i['repo'] = repo
            tag_engine_input = f'''
            REPO NAME: {repo}
            ISSUE TITLE: {i["title"]}.
            ISSUE BODY: {i["body"]}.
            COMMENTS: {i["comments"]}
            README: {repo_doc["markdown"]}
            LABELS: {i["labels"]}
            '''
            repo_tags = {"issue_title": i['title']}
            repo_tags.update(generate_tags(tag_engine_input, summ_ip=repo_doc["markdown"]))
            all_repo_tags.append(repo_tags)
        json.dump(all_repo_tags, open(f'{path}/{repo}/tags_summary.json', 'w')) 
    return repo_docs, issue_docs
    