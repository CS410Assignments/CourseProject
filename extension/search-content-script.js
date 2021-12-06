console.log("Search page content script");
let query = null;

/**
 * Function Where available robust Search
 **/
function getText(){
    return document.body.innerText;
}

/**
 * Robust search web document given text
 **/
function search(query){
	const Dom = document.querySelectorAll('h1, h2, h3, h4, h5, a, p, li, td, th')
	for(let text of Dom){
		console.log(text.innerHTML.includes(query))
		if (text.innerHTML.includes(query)){
			console.log(text)
			// while(text.children.length){
			// 	if(text.children.length != 1){
			// 		console.log(text.children.length)
			// 		break;
			// 	} else {
			// 		text = text.children
			// 	}
			// }
			text.innerHTML = text.innerHTML.replaceAll(query, "SPONGEBOB");
		}
	}
    return document.body.innerText;
}

chrome.runtime.onMessage.addListener(function(msg) {
  query = msg.message;
  search(query);
});