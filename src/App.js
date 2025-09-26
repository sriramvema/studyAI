import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import "./App.css";
import QuestionPage from "./QuestionPage";

function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload-pdf", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("Response from backend:", data);

      // Navigate to QuestionPage and pass PDF URL via Router state
      navigate("/ask", { state: { pdfUrl: data.pdf_url } });
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="center-title">
          <h1 className="main-title">StudyAI</h1>
          <h2 className="subtitle">Powered by Claude</h2>
          <h4>Upload PDF</h4>
          <input type="file" accept="application/pdf" onChange={handleFileChange} />
          {selectedFile && <p>Selected file: {selectedFile.name}</p>}
          <button onClick={handleUpload} style={{ marginTop: "10px" }}>
            Upload PDF
          </button>
        </div>
      </header>
      
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ask" element={<QuestionPage />} />
      </Routes>
    </Router>
  );
}

export default App;
