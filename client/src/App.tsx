import { useState } from 'react';
import './App.css';
import UploadFile from './components/UploadFile';
import Results from 'components/Results';

const App = () => {
  const [jobsData, setJobsData] = useState(false);

  return (
    <>
    <div className='navbar'>
        <h1 className='title'>Job Recommendation System</h1>
        <a href='https://github.com/OjasviAgarwal/JobRecommendationSystem'>Github</a>
    </div>
    <div className='container'>
      <UploadFile setJobsData={setJobsData}/>
      {jobsData?
      <div className='results'>
        <Results jobsData = {jobsData} />
      </div>
      :
      <p>No results Found</p>}
    </div>
    </>
  );
}

export default App;
