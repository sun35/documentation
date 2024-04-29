from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
#from langchain.vectorstores import chroma
from langchain.vectorstores import Chroma

OPEN_API_KEY = "sk-proj-Cg7dOq3JFCcOP3NouH2oT3BlbkFJtmKvA6zZEjbzGHYMfM5T"
MODEL = "gpt-4-turbo"
template: str = """/
    You are a support specialist for developers using documentation provided /
    question: {question}. You assist users with questions based on {context} /
    and any technical issues. /
    """
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_message_prompt = HumanMessagePromptTemplate.from_template(
    input_variables = ["question", "context"],
    template = "{question}",
)
chat_prompt_template = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)
model = ChatOpenAI(openai_api_key=OPEN_API_KEY)

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

def load_documents():
    raw_docs = TextLoader("./docs/dataset.txt").load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    return text_splitter.split_documents(raw_docs)

def load_embeddings(docs, user_query):
    db = Chroma.from_documents(docs, OpenAIEmbeddings(openai_api_key=OPEN_API_KEY))
    docs = db.similarity_search(user_query)
    print(docs)
    return db.as_retriever()

def generate_response(retriever, query):
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | chat_prompt_template
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)

def query(query):
    documents = load_documents()
    retriever = load_embeddings(documents, query)
    response = generate_response(retriever, query)
    return response



