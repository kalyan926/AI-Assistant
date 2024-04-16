from youtube_assistant import llm_response
from wikipedia_assistant import wiki_search
from website_assistant import article_chat
from chat_with_pdf import chatpdf
from langchain.memory import ConversationBufferWindowMemory
import streamlit as st
#from streamlit_chat import message




st.title(':violet[Welcome to AI Assistance]')

option=st.sidebar.selectbox("Choose your Assistant",["Youtube","Wikipedia","Website","PDF"])

spin={"Ask Questions":"Answering...." ,"Summary":"Summarizing..."}
answer_b={"Ask Questions":"Answer" ,"Summary":"Summarize"}

if option=="Youtube":
   st.subheader("Youtube Assistant")
   y_url=st.text_input("Paste youtube URL here")
   option_y=st.selectbox("Choose the action you want",["Ask Questions","Summary"])
   query=None
   if option_y=="Ask Questions":
      query=st.text_input("Ask any question about video")

   answer=st.button(answer_b[option_y])
   if answer==True:
      with st.spinner(spin[option_y]):
         response=llm_response(query,y_url,option_y)
         st.write(response)


if option=="Wikipedia":
   st.subheader("Wikipedia Assistant")
   search=st.text_input("Search on Wikipedia")
   option_w=st.selectbox("Choose the action you want",["Ask Questions","Summary"])
   query=None
   if option_w=="Ask Questions":
      query=st.text_input("Ask any question about article")

   answer=st.button("Answer")
   if answer==True:
      with st.spinner("Searching...."):
         result=wiki_search(search)
         st.write(result)



if option=="Website":
   
   st.subheader("Website Assistant")
   web_url=st.text_input("Paste website URL here")
   option_web=st.selectbox("Choose the action you want",["Summary","Chat with Article"])
   #answer=st.button("Answer")
   if option_web=="Chat with Article" and web_url!="":
      st.subheader(":orange[Welcome to Chat Bot]")
      clear_b=st.sidebar.button(":red[Clear Chat]")
      with st.chat_message("AI"):
            st.write("Hello! how can i help you ?")
               
      user_input=st.chat_input("Type your query here")
      
      if "chat_history" not in st.session_state:
         st.session_state.chat_history=[]
      
      if clear_b==True:
         st.session_state.chat_history.clear()

      if user_input is not None and user_input != "":
      
         st.session_state.chat_history.append({"User":user_input})
         for i,d in enumerate(st.session_state.chat_history):
               
            if i%2==1:
               
               with st.chat_message("AI"):
                  st.write(d['AI'])
                     
            if i%2==0:
         
               with st.chat_message("user"):
                  st.write(d['User'])

         with st.spinner("Answering......"):
               
               response=article_chat(web_url,user_input)
               st.session_state.chat_history.append({"AI":response}) 

               with st.chat_message("AI"): 
                  st.write(response)

                  


if option=="PDF":
   st.subheader("PDF Assistant")
   file=st.file_uploader("",accept_multiple_files=True)
   col1,col2=st.columns([2,9])
   with col1:
      clear_b=st.button(":red[Remove PDF's]")
   with col2:
      mem_b=st.button(":green[Use Memory]")
      if mem_b:
         st.write("Chat is using MEMORY")
            
   
   if clear_b==True:
      file.clear()

   option_pdf=st.selectbox("Select Your Action",["Summarize","Chat With PDF"])

   if len(file)!=0 and option_pdf=="Chat With PDF":
      st.subheader(":orange[Welcome to PDF Chat]")

      query=st.chat_input("Ask Anything From PDF")

      
      button=st.sidebar.button(":red[Clear Chat]")


      with st.chat_message("AI"):
            st.write("Hello, how can i help you")


      if "pdf_history" not in st.session_state:
         
         st.session_state.pdf_history=[]

      if "memory" not in st.session_state:   
         st.session_state.memory=ConversationBufferWindowMemory(k=3,memory_key="chat_history",output_key='answer',return_messages=True)
      
      if button==True:
         st.session_state.pdf_history.clear()
         st.session_state.memory.clear()
         


      
      if query!=None and query!="":
         st.session_state.pdf_history.append({"Human":query})
         for i,d in enumerate(st.session_state.pdf_history):
               
               if i%2==0:
                  with st.chat_message("Human"):
                        st.write(d["Human"])
               if i%2==1:
                  with st.chat_message("Ai"):
                        res=d["res"]
                        st.write(res["answer"])

                        with st.expander("Show Relavant Documents Chunks"):
                           #rel_docs=st.session_state.pdf
                           for i ,docs in enumerate(res):
                                 st.write(f":blue[Chunk-{i+1}]")
                                 st.write(res["source_documents"][i].page_content)



      if query!=None and query!="": 
         with st.spinner("Loading....."):
               
               response=chatpdf(query,file,st.session_state.memory)
               
         with st.chat_message("AI"):
                     
            st.write(response['answer'])
               
            with st.expander("Show Relavant Documents Chunks"):
               for i ,docs in enumerate(response):
                  st.write(f":blue[Chunk-{i+1}]")
                  st.write(response["source_documents"][i].page_content)

            st.session_state.pdf_history.append({"res":response})                                                 
                     
               
               
         
   
