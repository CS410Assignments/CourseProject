import React from 'react'
import JobItem from './JobItem';

const Results = ({jobsData}) => {
  const jobs = jobsData.data;

  return (
    <div>
      <h3>Recommended jobs for you</h3>
      <p>Based on your Resume</p>
      {
        jobs.map((job)=>(
          <div className='resultsItem' key={job.title+job.company+Date.now()}>
            <JobItem job={job}/>
          </div>
        ))
      }
    </div>
  )
}

export default Results