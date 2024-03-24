from flask import Flask, request, jsonify
from backend.pipeline import recommend
from llama_index.llms.mistralai import MistralAI
import weaviate
from llama_index.core.indices.prompt_helper import PromptHelper
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core.node_parser import NodeParser, MetadataAwareTextSplitter, SentenceSplitter
from llama_index.core import ServiceContext
import os 

app = Flask(__name__)
llm = MistralAI(model='mistral-large')
embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=os.environ.get("MISTRAL_API_KEY"))
service_context = ServiceContext.from_defaults(
    llm=llm,
    prompt_helper=PromptHelper.from_llm_metadata(llm_metadata=llm.metadata),
    text_splitter=SentenceSplitter(), 
    embed_model=embed_model)
#setup all vector indices?
all_indices = {}

@app.before_first_request
def startup():
    domain_vdb_map = {'AI/ML': 'AI_REPOS', 'Systems': 'SYSTEM_ADMIN', 'Web dev': 'WEB_APP_DEV', 'Data Science': 'DATA_SCIENCE',
                      'Game Dev': 'GAME_DEV', 'Mobile App Dev': 'MOBILE_APP'
                      }
    for dom, dom_vdb in domain_vdb_map.items():
        client = weaviate.Client(embedded_options=weaviate.embedded.EmbeddedOptions(persistence_data_path='/Users/swarnashree/mistral_hack/IssueMatcha/weaviate', binary_path='/Users/swarnashree/mistral_hack/IssueMatcha/weaviate'))
        vs_store = WeaviateVectorStore(weaviate_client=client, index_name=dom_vdb+'__WITHCOMMS', text_key="text")
        issue_index = VectorStoreIndex.from_vector_store(service_context=service_context, vector_store=vs_store, show_progress=True)
        all_indices[dom] = issue_index
    
@app.route('/issue_matcha/recommend', methods=['POST'])
def get_recommendations():
    if request.is_json:
        content = request.json
        user_pref = content['user_pref']
        past_contribs = content['past_contributions']
        domain = content['domain']
        response = recommend(all_indices[domain], user_pref, past_contribs)
        return jsonify({'results': response})
    else:
        return jsonify({'message': 'failed'})

    
if __name__=='__main__':
    app.run(debug=True, port=8989)