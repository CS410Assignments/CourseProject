const search_btn = document.getElementById("button");

search_btn.addEventListener('click', function () {
    search_api()
});

async function search_wild() {
    console.log("Inside search_wild..")
    //import {Client} from '@elastic'

    const ES_URL = "https://search-cs410-project-hw5dhpc4jsg3m74vnbalajt754.aos.us-east-1.on.aws"
    const ES_USER = "elastic"
    const ES_PASSWORD = "replace me"

    const client = new Client({
        node: ES_URL,
        auth: {
            username: ES_USER,
            password: ES_PASSWORD
        }
    })


    const query_str = document.getElementById("searchbox").textContent
    console.log("query_str ", query_str)
    const result = await client.search({
        index: 'subtitles',
        size: 1,
        from: 0,
        query: {
            "query_string": {
                "query": query_str,
                "default_field": "search_for"
            }
        }
    })
    const timestam_obj = result.hits.hits[0]._source
    return timestam_obj;
}


async function search_api() {
    console.log("Inside search_api..")

    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", "Basic ZWxhc3RpYzpwY2lXY2xwTE5kWHVpY1VoWFY4YmhnazI=");

    const query_txt = document.getElementById("searchbox").value
    console.log("query_txt ", query_txt)
    const query_payload = {
        size: 5,
        from: 0,
        query: {
            "query_string": {
                "query": query_txt
            }
        }
    }
    console.log("query_payload ", query_payload)
    var requestOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(query_payload)
    };

    const response = await fetch("https://ac55987c83844faa90726d4e5efe92b9.us-central1.gcp.cloud.es.io/subtitles_4/_search", requestOptions)
    const record = await response.json()
    console.log("record ", record)
    if(record.hits.total.value > 0) {
        for (let i = 0; i < 5; i++)  {
            const result = record.hits.hits[i]._source
            console.log(result)
            const response_str = '<strong>'+ result.week + ' </br> </strong>'
                + '<strong> Title :: </strong>' + result.lecture_title + '</br>' +
                '<a href="' + result.url + '">  timestamp </a>:: ' + result.time + '<br/>'
                 + '<strong> Subtitles </strong> : '+result.text
                 + '</br>'
            console.log("Resoponse :: ", response_str)
            await display_result(response_str)
        }
    } else {
        await display_result("We could not find a related topic")
    }

}

async function display_result(response_str) {
    const modal_body = document.querySelector('#modal_buttons_body')
    modal_body.style.fontSize = 14;
    modal_body.style.fontWeight = 400;
    modal_body.style.fontFamily = 'Courier New';
    modal_body.style.color = 'black';
    modal_body.style.textAlign = 'left'
    modal_body.style.backgroundColor = 'gray'
    modal_body.innerHTML += response_str

}