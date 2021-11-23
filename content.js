console.log("Content script running...");

function clear() {
    const contents = document.querySelectorAll('p,li,span,h1,h2,h3,h4,h5,h6');
    for(const snippet of contents){
        snippet.style.backgroundColor = "initial";
    }
}

function findText(find, results){
    // const regex = new RegExp(find, "gi");
    clear();
    const contents = document.querySelectorAll('p,li,span,h1,h2,h3,h4,h5,h6');

    console.log("in script");

    outputArray = [];

    for(const snippet of contents){
        // snippet.textContent = snippet.textContent.replace(regex, replace);
        if(snippet.textContent.toLowerCase().includes(find.toLowerCase())){
            // outputArray.push(snippet.textContent);
            snippet.style.backgroundColor = "red";
            for (const sen of snippet.textContent.split(".")) {
                if(sen.toLowerCase().includes(find.toLowerCase())){
                    outputArray.push(sen);
                    console.log(sen);
                }
            }
        }
    }
    outputText = "";
    for(elem of outputArray){
        outputText = outputText.concat(elem);
        outputText = outputText.concat(" \n ");
        outputText = outputText.concat(" \n ");
    }
    console.log(outputText);
    // results.insertAdjacentHTML('afterbegin', outputText);

}

chrome.runtime.onMessage.addListener(function(message){
    if(message.action === 'FIND_TEXT'){
        message.results = findText(message.find, message.results);
    }
});
