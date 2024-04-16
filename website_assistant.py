from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAI,OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


from dotenv import load_dotenv


load_dotenv()


chat_history=[]

def searchwith_url(url):

    search=WebBaseLoader(url)
    docs=search.load()
    return docs


def article_chat(url,que):

    article=searchwith_url(url)
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=0)
    doc_chunks=text_splitter.split_documents(article)
    article_db=FAISS.from_documents(doc_chunks,OpenAIEmbeddings())
    rel_docs=article_db.similarity_search(que,k=1)
    llm=OpenAI(temperature=0)
    template='''you are expert article analizer and understand detaily
        answer the following questions:{query}
        by searching from the article : {article}
    '''
    
    prompt_t=PromptTemplate.from_template(template)
    chain=LLMChain(llm=llm,prompt=prompt_t)

    response=chain.predict(query=que,article=rel_docs.page_content)

    return response
    








#print(article_chat("https://en.wikipedia.org/wiki/Artificial_intelligence","what is artificial intelligence"))