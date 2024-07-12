# Conversational AI Chatbot with Document Retrieval

This project is a Conversational AI chatbot that uses various data sources such as text files, PDFs, and websites to retrieve and respond to user queries. The chatbot leverages LangChain, FAISS, and OpenAI's language model for conversational retrieval and processing.

## Dependencies

Make sure you have the following Python packages installed:

- `requests`
- `beautifulsoup4`
- `langchain`
- `PyPDF2`
- `pyttsx3`
- `speech_recognition`

You can install these dependencies using pip:

```bash
pip install requests beautifulsoup4 langchain PyPDF2 pyttsx3 SpeechRecognition
```
## Features
Voice Interaction: Uses pyttsx3 for text-to-speech and speech_recognition for speech-to-text interaction.
Data Ingestion: Supports ingestion from text files (txt), PDF documents, and websites (requests, beautifulsoup4).
Document Processing: Extracts text from files and websites, splits text into chunks, and creates embeddings using OpenAI's language model via LangChain.
Conversation Management: Utilizes LangChain for managing conversation history and FAISS for efficient document retrieval.
User Interaction: Enables users to ask questions via voice or text input and receive responses based on processed documents.
## Usage
1.Setting Up Environment Variables:

Replace OPENAI_API_KEY with your OpenAI API key in the script.

2.Running the Script:
Run the script in your terminal or command prompt:
```bash
python your_script_name.py
```
The script will greet you based on the time of day and wait for your command either through voice input or text input.

3.Interaction:

The chatbot listens for your query.
You can input your question through voice or text.
It processes documents based on your selection (text file, PDF, or website).
It then uses OpenAI's language model to generate responses based on the processed documents.
The chatbot will read out the response aloud (if using voice) and continue the conversation until you say "stop".
## Note
Ensure all source files (data.txt, data.pdf) exist in the project directory or update the paths accordingly in the script.
Adjust voice settings (pyttsx3) based on your preference.
Feel free to extend or modify the functionality as per your requirements.

```css
This should provide a comprehensive overview of your project's functionality and features.
```
