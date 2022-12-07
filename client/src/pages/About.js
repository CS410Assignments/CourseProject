import React from 'react';
import UIUCLogo from '../assets/UIUCLogo.png';

function About() {
  return (
    <div>
        <h1 className='about'>Learn more about the purpose of InvestBuddy...</h1>
        
        <div className="row">
  <div className="column">
    <div className="card">
        <div className='about-img'>
            <img src={UIUCLogo} alt='Anthony Huerta'/>
        </div>
      <div className="container">
        <h2>Anthony Huerta</h2>
        <p className="title">Software Engineer</p>
        <p>Lead developer in creating InvestBuddy. Added the sentiment analysis feature and contributed to 
            implementing the article scoring feature.
        </p>
        <p><button className="button">Contact</button></p>
      </div>
    </div>
  </div>

  <div className="column">
    <div className="card">
    <div className='about-img'>
            <img src={UIUCLogo} alt='Anthony Huerta'/>
    </div>
      <div className="container">
        <h2>Jade Xu</h2>
        <p className="title">Software Engineer</p>
        <p> User experience improvent. Be responsible to record tutorial video and solve all problems that may occur when downloading.</p>
        <p><button className="button">Contact</button></p>
      </div>
    </div>
  </div>

  <div className="column">
    <div className="card">
    <div className='about-img'>
            <img src={UIUCLogo} alt='Anthony Huerta'/>
    </div>
      <div className="container">
        <h2>Yuhua Weng</h2>
        <p className="title">Software Engineer</p>
        <p>Some text that describes me lorem ipsum ipsum lorem.</p>
        <p>example@example.com</p>
        <p><button className="button">Contact</button></p>
      </div>
    </div>
  </div>
</div>
    </div>
  )
}

export default About
