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
  const rangeResponseOne = "Love the enthusiasm! Hope this article helps you on your investment journey :) {}";

  // From 1 - (-1)
  const rangeResponseTwo = "I see you're very curious! Here's an article to help you on your knowledge search! {}";

  // From (-1) - (-3)
  const rangeResponseThree = "I see you're having a rough day, Hope this article helps you on your journey! {}";

  const userRequestSearch = (sentence) => {
    var sentimentObj = new Sentiment();
    var sentimentDoc = sentimentObj.analyze(sentence);
    setSentimentScore(sentimentDoc['comparative']);
    console.log(sentimentScore);
    setSearchClicked(true);
  }

  const handleChange = event => {
    setMessage(event.target.value);
  }

  const sentimentPrompt = (score) => {
    if (score <= 3 && score > 1){
      return <p className='buddy-response'>{rangeResponseOne}</p>
    }
    else if (score <= 1 && score > -1){
      return <p className='buddy-response'>{rangeResponseTwo}</p>
    }
    else if (score <= -1 && score > -3){
      return <p className='buddy-response'>{rangeResponseThree}</p>
    }
    findURLMatch(message)
  }

  const findURLMatch = (message) => {
    var cur_url_match = "";
    var cur_url_keyword_matches = 0;
    var message_arr = message.split(" ");
    console.log("hello")
    for (var i = 0; i < data.length; i++) {
      console.log("in for loop")
      for (var j = 0; j < data[i]['keywords'].length; j++){
        var matches_found = 0;
        for (var k = 0; k < message_arr.length; k++){
          if (message_arr[k] == data[i]['keywords'][j]){
            matches_found += 1;
          }
        }
        if (matches_found > cur_url_keyword_matches){
          cur_url_keyword_matches = matches_found;
          cur_url_match = data[i]['article_url']
        }
      }
    }
    setArticleURL(cur_url_match);
    console.log(articleURL)
    
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

      {searchClicked ? 
      sentimentPrompt(sentimentScore): null}
      
    </div>
  )
}

export default Home