import React, { useState } from 'react'

const JobItem = ({job}) => {
  const [isReadMore, setReadMore] = useState(false);

  const toggleReadMore = () =>{
    setReadMore((prevState) => !prevState);
  }

  return (
    <div>
        <h3>{job.company}</h3>
        <h4>{job.title}</h4>
        <span>{job.location}</span>
        <br/>
        <a href={job.link}> Apply Now</a>
        <p>
          {isReadMore?job.desc: job.desc.slice(0,150)}
          <span className='description' onClick={toggleReadMore}>
          {isReadMore?"...see less.":"...read more."}
          </span>
        </p>
    </div>
  )
}

export default JobItem