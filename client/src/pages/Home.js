import React from 'react'
import Sentiment from 'sentiment';
import { useState } from 'react';

var sentiment = require('sentiment');

function Home() {

  const [message, setMessage] = useState('');
  const [isReponseViewable, setIsResponseViewable] = useState(false);

  const get_sentiment_score = (sentence) => {
    var sentimentObj = new Sentiment();
    var sentimentDoc = sentimentObj.analyze(sentence);
    console.log(sentimentDoc);
  }

  const handleChange = event => {
    setMessage(event.target.value);
  }

  return (
    
    <div>
        <h1 className='home'>Welcome to InvestBuddy!</h1>
        <br/>
        <p className='home-secondary'>Enter the prompt below that you would like to ask our search engine!</p>

      <div className='searchbar'>
      <input className="search" type="text" placeholder='Search here...' onChange={handleChange} value={message}></input>
      <button className='button' onClick={() => get_sentiment_score(message)}>Search</button>
      </div>

      {}
      
    </div>
  )
}

export default Home