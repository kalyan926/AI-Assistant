from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAI,OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferWindowMemory
from PyPDF2 import PdfReader





def chatpdf(question,file,memory):
    text=""
    for pdf in file:
        pdf_reader=PdfReader(pdf)
        for page in pdf_reader.pages:           
            text=text+page.extract_text()

    text_spliter=RecursiveCharacterTextSplitter(chunk_size=500)
    doc_chunks=text_spliter.split_text(text)
    vectorstore_docs=FAISS.from_texts(doc_chunks,OpenAIEmbeddings())    

    chain=ConversationalRetrievalChain.from_llm(llm=OpenAI(temperature=0),retriever=vectorstore_docs.as_retriever(),
                        return_source_documents=True,memory=memory)
    
    response=chain({"question":question})
    return response



