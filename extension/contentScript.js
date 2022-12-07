chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    // code...
    console.log('Get messgae', request)
    const color = request.isTroll ? 'red' : 'green'
    const doc = document.querySelector('.css-1dbjc4n.r-6gpygo.r-14gqq1x');
    doc.style.position = "realtive";
    var div = document.createElement('div');
    div.style.position = "absolute";
    div.style.right = "20px";
    div.style.height = "20px";
    div.style.width = "20px";
    div.style.background = color;
    div.style.borderRadius = "50%"
    doc.appendChild(div)

    // sendResponse('I've receieve the msg：' + JSON.stringify(request));//make response
});
// let currentUser;
// var HttpClient = function() {
//     this.get = function(aUrl, data, aCallback) {
//         var anHttpRequest = new XMLHttpRequest();
//         anHttpRequest.onreadystatechange = function() {
//             if (anHttpRequest.readyState === 4)
//                 aCallback(anHttpRequest);
//         }
//         anHttpRequest.open("GET", aUrl, true);
//         anHttpRequest.send(data);
//     }
// }
// const client = new HttpClient();
//
// chrome.tabs.onUpdated.addListener((tabId, changedInfo, tab) => {
//     if (changedInfo.status === 'complete' && tab.url.includes("/twitter.com/")) {
//         chrome.tabs.query({ active: true, currentWindow: true },
//             function(tabs){
//                 if (tabs[0].url.includes("/twitter.com/")) {
//                     currentUser = tabs[0].url.split("/twitter.com/")[1]
//                     console.log("current user is:" + currentUser)
//                 }
//             }
//         );
//     }
// });
//
// loginForm = document.getElementById('login')
// if (loginForm != null) {
//     console.log("loginForm")
//     loginForm.addEventListener('submit', (event) => {
//         event.preventDefault();
//         var data = new FormData(loginForm);
//         console.log(data)
//         data.append("userId", currentUser)
//         console.log(data)
//         get_url = "http://django-env.eba-c9dmngec.us-west-2.elasticbeanstalk.com/"
//     });
// }

