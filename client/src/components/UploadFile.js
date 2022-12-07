import React, { useState } from 'react'
import axios from 'axios';

const UploadFile = ({setJobsData}) => {
  const [chosenFile, setChosenFile] = useState('');
  const [fileRef, setFileRef] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    if(fileRef.files[0]){
      const data = new FormData();
      data.append('file', fileRef.files[0])

      axios.post('http://localhost:4000/upload', data)
			.then((result) => {
				console.log('Success:', result);
        setJobsData(result);
			})
			.catch((error) => {
				console.error('Error:', error);
			});
    }else{
      alert("Select a File to Upload");
    }
  }

  return (
    <div className='uploadFile'>
      <form onSubmit={(e)=>handleSubmit(e)}>
        <input type="file"  ref={(ref)=> setFileRef(ref)}/> 
        <button type='submit'>Upload</button>
      </form>
    </div>
  )
}

export default UploadFile