1. **Description**
This chatbot allows users to:

Engage in conversations with an AI assistant.
Upload multiple .txt and .pdf files.
Ask questions about uploaded documents and receive real-time answers.
If no document is uploaded, the chatbot functions as a general AI assistant.

It efficiently processes and combines multiple documents to provide relevant responses. The chatbot ensures a smooth user experience with real-time streaming answers, chat history retention, and support for large file uploads

**Features**
Supports *multiple `.txt` and `.pdf` uploads 
Processes large documents efficiently  
Maintains chat history 
Real-time streaming responses 
Works in Docker & DevContainer

2.For set up: please change the api key in docker-compose.yml---OPENAI_API_KEY: <insert right key> and make sure docker is running at the same time. Then rebuild the container.
type: streamlit run Chatbot.py in termeinal to run 

**It should look like this**: https://vimeo.com/1061419906

3. I only change api key and the model setting form gpt-4o to openai.gpt-4o. for setting. another description write on the chatbot.py