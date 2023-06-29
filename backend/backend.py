from flask import Flask, request, jsonify, render_template
from langchain.vectorstores import FAISS
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI





app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

os.environ["OPENAI_API_KEY"] = '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'

# This is a long document we can split up.
with open('/Users/arjunkataria/PycharmProjects/pythonProject5/backend/scratch_2.txt') as f:
    state_of_the_union = f.read()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=20,
    length_function=len,
)

texts = text_splitter.create_documents([state_of_the_union])


# Get embedding model
embeddings = OpenAIEmbeddings()

# Create vector database (unhash db = FAISS & db.save_local when uplaoding new files)
db = FAISS.from_documents(texts, embeddings)

db.save_local("faiss_indexall_product")


# Load the vector store
new_db = FAISS.load_local("faiss_indexall_product", embeddings)

# Chat completion llm
llm = ChatOpenAI(model_name='gpt-3.5-turbo-0301', temperature=0, max_tokens=500)

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=6, return_messages=True)

tm = OpenAI(temperature=0)
doc_chain = load_qa_with_sources_chain(tm, chain_type="map_reduce")


qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=new_db.as_retriever(search_type="mmr", search_kwargs={"score_threshold": 0.9}),
    memory=memory,verbose=True)


from langchain.prompts import SystemMessagePromptTemplate

# PROMPT
sys_prompt = "I want you to act as a technical software consultant named Rajesh answers. Your goal is to understand user needs for their product.Do not manipulate the answer just say you don't it. You may ask follow-up questions to confirm the needs by asking for relevant details, such as employee size and tech stack. Always provide an answer in a minimum of 150 words and only give answers related to the software consultant and while answering use basics html only give the correct answer don't make up things if you don't know the answer say i do not know yet."
qa.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate.from_template(sys_prompt)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Invalid request. Missing question parameter.'}), 400

    # Generate response
    response = generate_response(question)

    return jsonify({'answer': response})


def generate_response(question):
    # Process the question and generate a response using the language model
    response = qa({'question': question})
    answer = response['answer']

    return answer


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
