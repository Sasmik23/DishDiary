import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const[file,setFile] = useState< File | undefined>();
  const [error, setError] = useState<string | null>(null);

  function fileSelectedHandler(e: React.FormEvent<HTMLInputElement>){
    const target = e.target as HTMLInputElement & {
      files: FileList;
    }
    const selectedFile = target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
    } else {
      setError("No file selected");
    }

  }
  async function handleOnSubmit(e: React.SyntheticEvent) {
  e.preventDefault();

    if (!file) {
      setError("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append('pic', file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: 'POST',
        body: formData
      });
      if (response.ok) {
        const data = await response.json();
        console.log('Image uploaded successfully');
        console.log('Data:', data)
        }
        else{
        console.error('Failed to upload image:', response.statusText);
      }
    } catch (error) {
      console.error('Error occurred while uploading image:', error);
    }
  }

  return (
    <div className="App">
       <form onSubmit={handleOnSubmit} className="upload-form">
       <input type="file" id="file-input" name="pic" onChange={fileSelectedHandler} className="file-input" />
       {file && <button type="submit" className="submit-button">Upload</button>}
       </form>
    </div>
  );
}

export default App;
