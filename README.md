# StudyAI

This project is a React web application that uses retrieval augmented generation (RAG) to pull information from uploaded PDFs. I used the sentence-transformers/all-MiniLM-L6-v2 model from Huggingface to perform the RAG procedures. This application's primary use is for students to receive study help in their classes, which is specifically tailored to the material given to them. Once they upload a PDF of their class notes or textbook, each page is loaded into the RAG function and outputs the relevant pages for whatever the student's question is. These pages are given to a Claude model as context to answer the user's question. For this project, I used the claude-3-haiku-20240307 model. I have provided a link below to view a small demo I have prepared to show what the application looks like during use.

### Demo:
https://drive.google.com/file/d/1tUgXvP7wnt1wOFopQFz5-3vChhBk4LNs/view?usp=sharing

## Backend

In order to run the backend, Go into the api directory in your terminal and run <br>
```pip install -r requirements.txt``` <br>
This will install the necessary libraries for the program. Make sure to add your ```Anthropic API Key``` in line 99 of app.py in the api directory. Then run the backend with the command<br> 
```python app.py``` <br>
This will have the backend up and running.

## Frontend

In order to run the frontend, you will first have to install the necessary libraries. Run this command in a split terminal next to where you run your backend commands: <br>
```npm install react react-dom react-router-dom react-pdf```
<br>
Once these are installed, you can run it with <br>
```npm start``` <br>
This should have your web application up and running on your machine.
