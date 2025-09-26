from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import fitz
import os
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

app = Flask(__name__)
CORS(app)

# Globals
pages = []
vector_store = None
# Where PDFs will be saved
UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Flask backend is running!"

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    global pages, vector_store, last_uploaded_pdf

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    saved_filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, saved_filename)
    file.save(filepath)  # Save the file to static folder
    last_uploaded_pdf = saved_filename  # Save last uploaded

    # Read PDF for embeddings
    doc = fitz.open(filepath)
    pages = [page.get_text() for page in doc]

    docs = [
        Document(page_content=page_text, metadata={"source": file.filename, "page": i+1})
        for i, page_text in enumerate(pages)
    ]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})
    vector_store = InMemoryVectorStore.from_documents(docs, embeddings)

    return jsonify({
        "num_pages": len(pages),
        "message": f"PDF '{file.filename}' uploaded and indexed",
        "pdf_url": f"http://127.0.0.1:5000/static/{saved_filename}"  # ✅ Correct URL
    })


@app.route('/ask-question', methods=['POST'])
def question():
    global vector_store

    if vector_store is None:
        return jsonify({"error": "No PDF uploaded yet"}), 400

    data = request.get_json()
    user_question = data.get("question", "")

    print(f"User asked: {user_question}")

    # Search similar docs without a hard limit
    docs_with_scores = vector_store.similarity_search_with_score(user_question)
    context = ""
    retrieved_pages = []

    # Collect all retrieved pages
    for doc, score in docs_with_scores:
        page_num = doc.metadata['page']
        retrieved_pages.append(page_num)
        context += doc.page_content + "\n"
        print(f"Page {page_num}, score: {score}...\n")

    # Sort pages in ascending order
    sorted_retrieved = sorted(set(retrieved_pages))

    response = answer(user_question, context)
    print(response)
    print(sorted_retrieved)

    return jsonify({
        "message": "Question processed successfully",
        "user_question": user_question,
        "context": context,
        "response": response,
        "retrieved_pages": sorted_retrieved
    })

import anthropic
def answer(question, context):
    client = anthropic.Anthropic(api_key="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")

    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Or use "claude-3-haiku-20240307" for faster results
        max_tokens=500,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": f"You are a professor. Given the following context: {context}, Answer the following question:\n\n{question}. Only use the information in the context to answer the question. Provide the explanation in a bulleted format."
            }
        ]
    )

    return response.content[0].text.strip()

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
