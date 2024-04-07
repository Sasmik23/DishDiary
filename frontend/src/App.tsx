import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [file, setFile] = useState<File | undefined>();
  const [error, setError] = useState<string | null>(null);
  const [description, setDescription] = useState<string | null>();
  const [fileName, setFileName] = useState<string | null>(null);
  const [gallery, setGallery] = useState<{ id: number; url: string; description: string }[]>([]);


  useEffect(() => {
    async function fetchImages() {
      try {
        const response = await fetch("http://localhost:5000/images");
        if (response.ok) {
          const data = await response.json();
          setGallery(data.map((item: { id: number; image: string; mimetype: string; description: string }) => ({
            id: item.id,
            url: `data:${item.mimetype};base64,${item.image}`,
            description: item.description
          })));
        } else {
          console.error('Failed to fetch images:', response.statusText);
        }
      } catch (error) {
        console.error('Error occurred while fetching images:', error);
      }
    }
    fetchImages();
  }, []); // Empty dependency array ensures the effect runs only once on mount



  function fileSelectedHandler(e: React.FormEvent<HTMLInputElement>) {
    const target = e.target as HTMLInputElement & {
      files: FileList;
    }
    const selectedFile = target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
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
        if (data && data.description) {
          console.log(data.description);
          setDescription(data.description);
          setFile(undefined);
          setFileName(null);
          setError(null);
        }
      }
      else {
        console.error('Failed to upload image:', response.statusText);
      }
    } catch (error) {
      console.error('Error occurred while uploading image:', error);
    }
  }


  return (
    <div className="App">
      <div className="form-container">
        <h2>Upload Image</h2>
        <form onSubmit={handleOnSubmit} className="upload-form">
          <label htmlFor="file-input" className="file-label">
            Choose an image
            <input type="file" id="file-input" name="pic" onChange={fileSelectedHandler} className="file-input" />
          </label>
          {fileName && <p>{fileName}</p>}
          {error && <p className="error">{error}</p>}
          {file && <button type="submit" className="submit-button">Upload</button>}
        </form>
        {description && <p className="description">{description}</p>}
      </div>
      <div className="gallery-container">
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {gallery.map((item) => (
              <tr key={item.id}>
                <td><img src={item.url} alt={`Uploaded ${item.id}`} className="gallery-image" /></td>
                <td>{item.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}


export default App;
