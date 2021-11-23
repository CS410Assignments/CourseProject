// const searchTextt = document.getElementById("searchInput");
// const resultsText = document.getElementById("results");
//
// document.getElementById("searchButton").addEventListener("click", async () => {
//   let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
//
//   console.log("clicked");
//   chrome.tabs.sendMessage(tabs[0].id, {action: "REPLACE_TEXT", find: searchTextt.value, results: resultsText.value});
//   // window.close();
// });

const searchButton = document.getElementById("searchButton");
const searchText = document.getElementById("searchInput");
const resultsText = document.getElementById("results");

document.getElementById("searchButton").addEventListener("click", async () => {
    console.log("clicked");
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        console.log("clicked");
        chrome.tabs.sendMessage(tabs[0].id, {action: "FIND_TEXT", find: searchText.value, results: resultsText.value});
        // window.close();
    })
});
