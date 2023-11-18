const { Client } = require('@elastic/elasticsearch')
const client = new Client({
    cloud: {
        id: '<cloud-id>'
    },
    auth: {
        username: 'elastic',
        password: 'changeme'
    }
})


const result = await client.search({
    index: 'my-index',
    query: {
        match: { hello: 'world' }
    }
})