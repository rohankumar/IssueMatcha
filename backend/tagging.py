import os
import json
from backend.prompts.tagging import tagging_prompt, summary_prompt
import os
import requests

def generate_response(prompt):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 512,
        "temperature": 0.01,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "n": 1,
        "stop": None,
        "response_format": { "type": "json_object" },
        "model": "accounts/fireworks/models/mixtral-8x7b-instruct",
        "stream": False
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {os.environ.get('FIREWORKS_API_KEY')}"
    }

    response = requests.post(url, json=payload, headers=headers)
    return json.loads(response.text)




def generate_tags(tag_input, summ_ip):
    # api_key = os.environ["MISTRAL_API_KEY"]
    # model = "mistral-large-latest"
    # client = MistralClient(api_key=api_key)
    # tag_msgs = [
    #     ChatMessage(role="user", content=tagging_prompt.replace('{query_str}', tag_input))
    # ]
    # repo_msgs = [ChatMessage(role="user", content=summary_prompt.replace('{query_str}', summ_ip))]
    # repo_tags = client.chat(
    #     model=model,
    #     response_format={"type": "json_object"},
    #     messages=tag_msgs,
    # )
    # repo_summary = client.chat(
    #     model=model,
    #     response_format={"type": "json_object"},
    #     messages=repo_msgs,
    # )
    try:
        tags = generate_response(tagging_prompt.replace('{query_str}', tag_input))['choices'][0]['message']['content']
    except:
        tags = generate_response(tagging_prompt.replace('{query_str}', tag_input[:-30000]))['choices'][0]['message']['content']
    try:
        summ = generate_response(summary_prompt.replace('{query_str}', summ_ip))['choices'][0]['message']['content']
    except:
        summ = generate_response(summary_prompt.replace('{query_str}', summ_ip[:-30000]))['choices'][0]['message']['content']

    output = dict()
    print(tags)
    try:
        output.update(json.loads(tags))
    except:
        print(tags)
        if tags[-1] == '"':
            tags = tags + ']}'
        elif tags[-1] == ",":
            tags = tags[:-1] + ']}'
        else:
            tags = tags + '"]}'
        output.update(json.loads(tags))
    output.update(json.loads(summ))
    return output

def load_domain(path):
    repo_docs = []
    issue_docs = []
    for repo in os.listdir(path):
        if 'tags_summary.json' in os.listdir(f'{path}/{repo}'):
            continue
        all_repo_tags = []
        repo_doc = json.load(open(f'{path}/{repo}/README.json', 'r'))
        issues = json.load(open(f'{path}/{repo}/issues.json', 'r'))
        for i in issues:
            i['repo'] = repo
            tag_engine_input = f'''
            REPO NAME: {repo}
            ISSUE TITLE: {i["title"]}.
            ISSUE BODY: {i["body"]}.
            
            README: {repo_doc["markdown"]}
            LABELS: {i["labels"]}
            '''
            # COMMENTS: {i["comments"]}
            repo_tags = {"issue_title": i['title']}
            repo_tags.update(generate_tags(tag_engine_input, summ_ip=repo_doc["markdown"]))
            all_repo_tags.append(repo_tags)
        json.dump(all_repo_tags, open(f'{path}/{repo}/tags_summary.json', 'w')) 
    return repo_docs, issue_docs

dirs = ['AI_REPOS', 'DATA_SCIENCE', 'SYSTEM_ADMIN', 'WEB_APP_DEV']
for d in dirs:
    load_domain(f'/Users/swarnashree/mistral_hack/IssueMatcha/data/new_files/{d}')
