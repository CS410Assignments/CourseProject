//const {Client} = require('@elastic/elasticsearch')
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("searchbutton").addEventListener("click", search_wild);
});


async function search_wild() {
    const ES_URL = "https://search-cs410-project-hw5dhpc4jsg3m74vnbalajt754.aos.us-east-1.on.aws"
    const ES_USER = "elastic"
    const ES_PASSWORD = "CS410-project"

    const client = new Client({
        node: ES_URL,
        auth: {
            username: ES_USER,
            password: ES_PASSWORD
        }
    })

    console.log("Inside search_wild..")
    const query_str = document.getElementById("searchbox").textContent
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