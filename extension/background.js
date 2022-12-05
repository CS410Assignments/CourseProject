let currentUser;
let threshold;
// chrome.tabs.onUpdated.addListener((tabId, changedInfo, tab) => {
//     if (changedInfo.status === 'complete') {
//         chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
//             if (tabs[0].url.includes("/twitter.com/")) {
//                 currentUser = tabs[0].url.split("/twitter.com/")[1];
//                 // chrome.tabs.sendMessage(tabs[0].id, {userId: currentUser})
//             }
//         });
//     }
// });

// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//     console.log(request)
//     if (type === "requestCurUser") {
//         chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
//             if (tabs[0].url.includes("/twitter.com/")) {
//                 currentUser = tabs[0].url.split("/twitter.com/")[1];
//                 // chrome.tabs.sendMessage(tabs[0].id, {userId: currentUser})
//             }
//         });
//         sendResponse({curUser: currentUser});
//     }
// });
// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//     const {type} = request;
//     if (type === "request") {
//         chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
//             if (tabs[0].url.includes("/twitter.com/")) {
//                 currentUser = tabs[0].url.split("/twitter.com/")[1];
//                 console.log(currentUser)
//                 // chrome.tabs.sendMessage(tabs[0].id, {userId: currentUser})
//             }
//         });
//         sendResponse({res: currentUser});
//     } else {
//         sendResponse({res: 0});
//     }
// });

  