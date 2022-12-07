import React from 'react'
import Sentiment from 'sentiment';
import { useState } from 'react';
import data from '../data/articleKeywordData';
var sentiment = require('sentiment');
function Home() {

  const [message, setMessage] = useState('');
  const [sentimentScore, setSentimentScore] = useState(0);
  const [searchClicked, setSearchClicked] = useState(false);
  const [articleURL, setArticleURL] = useState('');

  // From 3 - 1
  const rangeResponseOne = "Love the enthusiasm! Hope this article helps you on your investment journey :) ";

  // From 1 - (-1)
  const rangeResponseTwo = "I see you're very curious! Here's an article to help you on your knowledge search! ";

  // From (-1) - (-3)
  const rangeResponseThree = "I see you're having a rough day, Hope this article helps you on your journey! ";

  const userRequestSearch = (sentence) => {
    var sentimentObj = new Sentiment();
    var sentimentDoc = sentimentObj.analyze(sentence);
    setSentimentScore(sentimentDoc['comparative']);
    setSearchClicked(true);
    findURLMatch(message)
  }

  const handleChange = event => {
    setMessage(event.target.value);
  }

  const sentimentPrompt = (score) => {
    if (score <= 3 && score > 1){
      return <div><p className='buddy-response'>{rangeResponseOne}</p> <a href={articleURL}>Click here</a> </div>
    }
    else if (score <= 1 && score > -1){
      return <div><p className='buddy-response'>{rangeResponseTwo}</p> <a href={articleURL}>Click here</a> </div>
    }
    else if (score <= -1 && score > -3){
      return <div><p className='buddy-response'>{rangeResponseThree}</p> <a href={articleURL}>Click here</a> </div>
    }

  }

  function getIntersection(setA, setB) {
    const intersection = new Set(
      [...setA].filter(element => setB.has(element))
    );
  
    return intersection;
  }

  const findURLMatch = (message) => {
    var cur_url_keyword_matches = 0;
    var message_arr = String(message).split(" ");

    // Iterate through all entries
    for (var i = 0; i < data.length; i++) {
      var keywordSet = new Set(data[i]["keywords"]);
      var messageTokenSet = new Set(message_arr);
      var intersectionSet = getIntersection(keywordSet, messageTokenSet);

      if (intersectionSet.size > cur_url_keyword_matches){
        cur_url_keyword_matches = intersectionSet.length
        console.log(data[i]["article_url"])
        setArticleURL(data[i]["article_url"])
      }
    }
    console.log(articleURL);
    sentimentPrompt(sentimentScore);
  }

  return (
    
    <div>
        <h1 className='home'>Welcome to InvestBuddy!</h1>
        <br/>
        <p className='home-secondary'>Enter the prompt below that you would like to ask our search engine!</p>

      <div className='searchbar'>
      <input className="search" type="text" placeholder='Search here...' onChange={handleChange} value={message}></input>
      <button className='button-search' onClick={() => userRequestSearch(message)}>Search</button>
      </div>

      {searchClicked ? sentimentPrompt(sentimentScore): null}
      
    </div>
  )
}

export default Home