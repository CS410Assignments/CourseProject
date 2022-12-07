URL = "http://django-env.eba-c9dmngec.us-west-2.elasticbeanstalk.com/"

var HttpClient = function() {
    this.get = function(aUrl, data, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() {
            if (anHttpRequest.readyState == 4)// && anHttpRequest.status == 200) {
                aCallback(anHttpRequest); //aHttpRequest.responseText
        }
        anHttpRequest.open( "GET", aUrl, true );
        anHttpRequest.setRequestHeader("threshold", data.get("threshold"))
        anHttpRequest.send( null );
    }
}
var client = new HttpClient();

submitForm = document.getElementById('submitForm')
submitForm.addEventListener('submit', (event) => {
    event.preventDefault();
    var data = new FormData(submitForm);
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        if (tabs[0].url.includes("/twitter.com/")) {
            currentUser = tabs[0].url.split("/twitter.com/")[1];
            let aUrl = URL + currentUser + "/"
            // console.log(aUrl)
            client.get(aUrl, data, function (response) {
                //backend return value parsed_response.get("isTroll");
                var parsed_response = JSON.parse(response.responseText);
                console.log(parsed_response)
                chrome.tabs.sendMessage(tabs[0].id, { isTroll: parsed_response.get("isTroll")}, function (data) {
                    console.log("📌: bj.js  send");
                    console.log("📌: bj.js  sendBack", data);
                    console.log('.....................');
                });
            })
        } else {
            alert("Please Use in Twitter")
        }
    });

    // data.append("userid", currentUser)
});




