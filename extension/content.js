let arr = []

let list = $('.css-79elbk .list__09f24__ynIEd').childNodes

let len = $('.css-79elbk .list__09f24__ynIEd').childNodes.length

for(let i = 0; i < len; i++) {
    let info = list[i].querySelectorAll('.user-passport-info .css-1m051bw')
    let s = list[i].querySelectorAll('.margin-t1__09f24__w96jn .five-stars__09f24__mBKym')[0].getAttribute('aria-label').split(' ')[0]
    let dateil = list[i].querySelectorAll('.comment__09f24__gu0rG .raw__09f24__T4Ezm')[0].textContent
    let location = list[i].querySelectorAll('.user-passport-info .responsive-hidden-small__09f24__qQFtj .css-qgunke')[0].textContent
    
    let obj = {
        name: info[0].textContent,
        star: s,
        review: dateil,
        location: location
    }
    arr.push(obj)
}

console.log(arr)