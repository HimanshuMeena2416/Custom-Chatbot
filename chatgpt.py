import os
import sys

import requests
from bs4 import BeautifulSoup

from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from PyPDF2 import PdfReader

import pyttsx3  
import speech_recognition as sr 
import datetime


OPENAI_API_KEY = "API Key here"
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id) #female voice
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("Hello sir. I am your chatbot. What can I do for you?")       

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        
    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query
wishMe()


# query = takeCommand().lower()# if using voice as input
# print(query)

print('Enter your Question:')
query = input()

vectorstore = None
conversation_chain = None
chat_history = []


# If using any website

def website():
    news_str=''
    URL= 'https://www.bbc.com/news'
    response=requests.get(URL)
    soup=BeautifulSoup(response.content,'html.parser')
    headlines=soup.find_all('h2')
    
    for headline in headlines:
        news_str=' '+news_str+headline.text+'.'
    return news_str
    


#using txt file
def read_file_to_string(filename):
    try:
        with open(filename, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        return f"The file {filename} does not exist."
    except Exception as e:
        return f"An error occurred: {e}"


#using pdf
def get_pdf_text(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def process_documents():
    global vectorstore, conversation_chain
   
    print('select source: 1 for txt file ,2 for pdf and 3 for website')
    source = input()
    if(source== '1'):
        raw_text = read_file_to_string('data.txt')
    elif(source=='2'):
        raw_text=get_pdf_text('data.pdf')
    elif(source=='3'):
        raw_text=website()
    else:
        print("Select from 1/2/3")


    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    conversation_chain = get_conversation_chain(vectorstore)
    return "Documents processed successfully"

def chat():
    global vectorstore, conversation_chain, chat_history
    user_question = query
    response = conversation_chain.invoke({'question': user_question})
    chat_history = response['chat_history']

    return chat_history


process_result = process_documents()
if process_result == "Documents processed successfully":
    chat_response = chat()
    print("Question : " +chat_response[0].content)
    print("Answer   : " +chat_response[1].content)
    while(takeCommand().lower()!='stop'):
        speak(chat_response[1].content)
else:
    print(process_result)
    
    
