'use strict';

import './popup.css';
var Sentiment = require('sentiment');
const openai_api_url = 'https://api.openai.com/v1/engines/text-davinci-003/completions';

async function queryGPT3(promptText) {
  const response = await fetch(openai_api_url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer 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`
    },
    body: JSON.stringify({
      //model: "text-davinci-003",
      prompt: promptText,
      max_tokens: 1500,
      temperature: 0.5
    })
  });
  console.log(response.status);
  const data = await response.json();
  return data.choices[0].text.trim();
}

function getText() {
  var inputText = document.getElementById('inputText').value;
  window.documentText = inputText.toLowerCase().match(/\b(\w+)\b/g);
  document.getElementById('result').textContent = "Text Successfully Retrieved";
}
function calculateTF(words) {
  const wordCount = words.length;
  const wordFreq = {};
  words.forEach(word => {
      wordFreq[word] = (wordFreq[word] || 0) + 1;
  });
  for (let word in wordFreq) {
      wordFreq[word] = wordFreq[word] / wordCount;
      //console.log(word + wordFreq[word]);
  }
  return wordFreq;
}

async function calculateIDF() {
  try {
      const response = await fetch(chrome.runtime.getURL('IDF.json'));
      const idfData = await response.json();
      window.idf = idfData; // Now it's safe to assign to a global variable
      // You can also return 'idfData' here
      return idfData;
  } catch (error) {
      console.error('Error fetching the JSON file:', error);
  }
}
// clean
function calculateTFIDF(TF, IDF) {
  let tfIdfScores = [];
  const defaultIdf = 4; // Or calculate a dynamic default IDF value

  // Calculate TF-IDF score for each term and push to array
  for (const term in TF) {
      const idf = term in IDF ? IDF[term] : defaultIdf;
      tfIdfScores.push({ term: term, score: TF[term] * idf });
  }
  // Sort the array by TF-IDF score in descending order
  tfIdfScores.sort((a, b) => b.score - a.score);
  return tfIdfScores;
}
// clean
async function summarizeText(action) {
  const tf = calculateTF(window.documentText);
  //IDF part
  const idf = await calculateIDF();
  window.TFIDF = calculateTFIDF(tf, idf);
  let keyword_size = 7;
  if (documentText.length<50) keyword_size = 3;
  if (documentText.length>1000) keyword_size=15;
  const topTfIdfScores = TFIDF.slice(0, keyword_size);
  let textContent = '';
  for (const item of topTfIdfScores) {
      // Assuming each item has 'term' and 'score' properties
      textContent += `${item.term}\n`
      //textContent += `Term: ${item.term}, Score: ${item.score}\n`;
  }
  document.getElementById('result').textContent = textContent;
  //document.getElementById('result').textContent = window.tf;
}

function sentimentAnalysis() {
  var sentiment = new Sentiment();
  var result = sentiment.analyze(documentText.toString());
  console.dir(result);
  document.getElementById('result').textContent = result.score + " " + result.comparative;
}

function topicSummary() {
  console.log("here");
  var promptText = "Give me a very less than 30 word SUMMARY of : " + window.documentText.toString();
  console.log(promptText);
  queryGPT3("promptText").then(response => {
    console.log(response);
    document.getElementById('topicsummary').textContent = response;
  }).catch(error => {
    console.error('Error:', error);
  });
}

document.getElementById('getTextButton').addEventListener('click', getText);
document.getElementById('summarizeBtn').addEventListener('click', () => summarizeText('summarize'));
document.getElementById('sentimentBtn').addEventListener('click', () => sentimentAnalysis('sentiment'));
document.getElementById('topicBtn').addEventListener('click', topicSummary);