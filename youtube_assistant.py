
from langchain_openai import OpenAI ,OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

def load_transcripts_and_create_database(url:str):
    t=YoutubeLoader.from_youtube_url(url)
    transcripts=t.load()
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    documents=text_splitter.split_documents(transcripts)   
    embeddings=OpenAIEmbeddings()
    db=FAISS.from_documents(documents,embeddings)
    return db,transcripts



def llm_response(query,url,option):

    db_transcripts,transcripts=load_transcripts_and_create_database(url)       
    

    template_q="""
            You are a helpful assistant that can answer questions about youtube videos 
            based on the video's transcript.
            
            Answer the following question: {question}
            By searching the following video transcript: {document}
            
            Only use the factual information from the transcript to answer the question.
            
            If you feel like you don't have enough information to answer the question, say "I don't know".
            
            Your answers should be verbose and detailed.
            """
    template_s="""   
    Provide a abstractive summary of the video transcripts:{document} 
    
    summarize without lossing any information.    
    """

    if option=="Ask Questions" and query!=None :
        similar_docs=db_transcripts.similarity_search(query,k=1)
        doc=" ".join([d.page_content for d in similar_docs])
        prompt_q=PromptTemplate.from_template(template_q)
        llm=OpenAI(model="gpt-3.5-turbo-instruct")
        chain=LLMChain(llm=llm,prompt=prompt_q)
        llm_out=chain.run(question=query,document=doc)
        #response=llm_out.replace("\n"," ")


    if option=="Summary":
        transcript=" ".join([t.page_content for t in transcripts])
        prompt_s=PromptTemplate.from_template(template_s)
        llm=OpenAI(model="gpt-3.5-turbo-instruct",temperature=0)
        chain=LLMChain(llm=llm,prompt=prompt_s)
        llm_out=chain.run(document=transcript)
        #response=llm_out.replace("\n"," ")

    return llm_out


