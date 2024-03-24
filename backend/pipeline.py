from llama_index.llms.mistralai import MistralAI
import weaviate
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from IPython.display import Markdown, display
# from llama_index.core.vector_stores import WeaviateVectorStore
from llama_index.core.storage import StorageContext
from llama_index.core import ServiceContext
from llama_index.core.indices.prompt_helper import PromptHelper
from llama_index.core.node_parser import NodeParser, MetadataAwareTextSplitter, SentenceSplitter
from llama_index.embeddings.mistralai import MistralAIEmbedding
import os
from typing import List
from llama_index.readers.json import JSONReader
import json 
from llama_index.core.schema import Document
import re
import logging
import sys
from backend.prompts.tagging import tagging_prompt, summary_prompt
from backend.prompts.recommendation import recommendation_prompt
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
logger = logging.getLogger()

repo_metadata_keys = ['repo']
issue_metadata_keys = ['repo', 'labels']
tags = []

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
    # logger.info(f'\n\n---\n{repo}: {output}\n---')
    # json.dump(output, open(f'{domain_path}/{repo}/summary_tags.json', 'w'))
    return output

def load_domain(path):
    repo_docs = []
    issue_docs = []
    for repo in os.listdir(path):
        all_repo_tags = []
        repo_doc = json.load(open(f'{path}/{repo}/README.json', 'r'))
        repo_doc['repo'] = repo
        li_repo_doc = Document(text=repo_doc['markdown'])
        li_repo_doc.metadata = {x: repo_doc[x] for x in repo_metadata_keys}
        repo_docs.append(li_repo_doc)
        
        issues = json.load(open(f'{path}/{repo}/issues.json', 'r'))
        issues_li_docs = []
        for i in issues:
            i['repo'] = repo
            doc_text = f'''
            ISSUE TITLE: {i["title"]}.
            ISSUE BODY: {i["body"]}.
            COMMENTS: {i["comments"]}
            README: {li_repo_doc.text}'''
            
            li_doc = Document(text=doc_text)
            li_doc.metadata = {x: i[x] for x in issue_metadata_keys}
            issues_li_docs.append(li_doc)
            tag_engine_input = doc_text + \
            f'''
            LABELS: {i["labels"]}
            '''
            repo_tags = {"issue_title": i['title']}
            repo_tags.update(generate_tags(tag_engine_input, summ_ip=li_repo_doc.text))
            all_repo_tags.append(repo_tags)
        json.dump(all_repo_tags, open(f'{path}/{repo}/tags_summary.json', 'w')) 
        issue_docs.extend(issues_li_docs)
    return repo_docs, issue_docs
    
llm = MistralAI(model='mistral-large', additional_kwargs={'response_format': {"type": "json_object"}})
embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=os.environ.get("MISTRAL_API_KEY"))

embeddings = embed_model.get_text_embedding("La Plateforme - The Platform")
# resp = llm.complete("Paul Graham is ")
# print(resp)

service_context = ServiceContext.from_defaults(
    llm=llm,
    prompt_helper=PromptHelper.from_llm_metadata(llm_metadata=llm.metadata),
    text_splitter=SentenceSplitter(), 
    embed_model=embed_model)

# def generate_issue_tags(issue_docs: List[Document]):
#     api_key = os.environ["MISTRAL_API_KEY"]
#     model = "mistral-large-latest"
#     client = MistralClient(api_key=api_key)
#     outputs = []
#     for i in issue_docs:
#         content = i.text
#         readme = content[re.compile(r"\bREADME: ").search(content).start():]
#         content += f'{str(issue_docs.get_metadata_str())}'

#         tag_msgs = [
#         ChatMessage(role="user", content=tagging_prompt.replace('{query_str}', content))
#     ]
#         summ_msgs = [ChatMessage(role="user", content=summary_prompt.replace('{query_str}', readme))]
#         repo_tags = client.chat(
#             model=model,
#             response_format={"type": "json_object"},
#             messages=tag_msgs,
#         )
#         repo_summary = client.chat(
#             model=model,
#             response_format={"type": "json_object"},
#             messages=summ_msgs,
#         )
#         tags = repo_tags.choices[0].message.content
#         summ = repo_summary.choices[0].message.content
#         output = dict()
#         output.update(json.loads(tags))
#         output.update(json.loads(summ))
#         outputs.append(output)
#         logger.info(f'\n\n---\n{repo}: {output}\n---')
#         json.dump(output, open(f'{domain_path}/{repo}/summary_tags.json', 'w'))
#     return True


# def generate_and_save_tags(domain_path):
#     api_key = os.environ["MISTRAL_API_KEY"]
#     model = "mistral-large-latest"
#     client = MistralClient(api_key=api_key)
#     for repo in os.listdir(domain_path):
#         readme = json.load(open(f'{domain_path}/{repo}/README.json','r'))['markdown']
#         tag_msgs = [
#         ChatMessage(role="user", content=tagging_prompt.replace('{query_str}', readme))
#     ]
#         repo_msgs = [ChatMessage(role="user", content=summary_prompt.replace('{query_str}', readme))]
#         repo_tags = client.chat(
#             model=model,
#             response_format={"type": "json_object"},
#             messages=tag_msgs,
#         )
#         repo_summary = client.chat(
#             model=model,
#             response_format={"type": "json_object"},
#             messages=repo_msgs,
#         )
#         tags = repo_tags.choices[0].message.content
#         summ = repo_summary.choices[0].message.content
#         output = dict()
#         output.update(json.loads(tags))
#         output.update(json.loads(summ))
#         logger.info(f'\n\n---\n{repo}: {output}\n---')
#         json.dump(output, open(f'{domain_path}/{repo}/summary_tags.json', 'w'))
#     return True


def data_loader(path=None):    
    client = weaviate.Client(embedded_options=weaviate.embedded.EmbeddedOptions(persistence_data_path='/Users/swarnashree/mistral_hack/IssueMatcha/weaviate', binary_path='/Users/swarnashree/mistral_hack/IssueMatcha/weaviate'))
    domain_repo_indices = {}
    domain_issue_indices = {}
    for domain in os.listdir(path):
        logger.info(f'Loading domain: {domain}')
        domain_info = load_domain(f'{path}/{domain}')
        # repo
        # repo_vs = WeaviateVectorStore(weaviate_client=client, index_name=domain.upper()+'_repos', text_key="text")
        # repo_storage_context = StorageContext.from_defaults(vector_store=repo_vs)
        # repos = domain_info[0]
        # repo_index = VectorStoreIndex.from_documents(repos, service_context=service_context, storage_context=repo_storage_context, show_progress=True)
        # repo_index = VectorStoreIndex.from_vector_store(service_context=service_context, vector_store=repo_vs, show_progress=True)

        #generate tags for first time loading
        # generate_and_save_tags(f'{path}/{domain}')
        
        
        #issues 
        # issue_vs = WeaviateVectorStore(weaviate_client=client, index_name=domain.upper()+'_issues', text_key="text")
        # issue_storage_context = StorageContext.from_defaults(vector_store=issue_vs)
        # issue_index = VectorStoreIndex.from_documents(issues, service_context=service_context, storage_context=issue_storage_context, show_progress=True)
        # issue_index = VectorStoreIndex.from_vector_store(service_context=service_context, vector_store=issue_vs, show_progress=True)

        
        
        # index_query_engine = issue_index.as_query_engine(similarity_top_k=10, text_qa_template=recommendation_prompt)
        # # print(index_query_engine.query("Which of these issues would be suitable for me if I want to spend around 0-10 hours of my time on it? Use a chain-of-thought processing and populate the 'reason' field in the output.  Output in JSON format with following attributes: issue_repo, issue_title, reason, time_needed"))
        # issue_response = index_query_engine.query(prompt)
        # print(f'\n\nresponse metadata: {issue_response.metadata}')

        # domain_repo_indices[domain] = repo_index
        # domain_issue_indices[domain] = issue_index
        # logger.info(f'Loaded domain')
    
    
if __name__ == '__main__':
    data_loader('/Users/swarnashree/mistral_hack/IssueMatcha/data/files')
    # chat_engine = index.as_query_engine(retriever_mode='embedding', similarity_top_k=4, streaming=True)
    # response_gen = chat_engine.query('what are the risk factors of AAPL?'+' Please cite your sources from the given sources only.')
# def get_query_engine():
#     import os
#     from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
#     from llama_index.llms.mistralai import MistralAI
#     from llama_index.embeddings.mistralai import MistralAIEmbedding

#     # Load data
#     reader = SimpleDirectoryReader(input_files=["essay.txt"])
#     documents = reader.load_data()
#     # Define LLM and embedding model
#     Settings.llm = MistralAI(model="mistral-medium")
#     Settings.embed_model = MistralAIEmbedding(model_name='mistral-embed')
#     # Create vector store index 
#     index = VectorStoreIndex.from_documents(documents)
#     # Create query engine
#     query_engine = index.as_query_engine(similarity_top_k=2)
#     response = query_engine.query(
#         "What were the two main things the author worked on before college?"
#     )
#     print(str(response))