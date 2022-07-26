let updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function() {
        let productId = updateBtns[i].dataset.product
        let action = updateBtns[i].dataset.action
        let pronum = updateBtns[i].dataset.pronum

        console.log('produtId: ', productId, 'action: ', action, 'pronum: ', pronum)
        console.log('USER: ', user)
        console.log(pronum)
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        }
        else{
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action, pronum) {
    console.log('Not logged in...')
    // console.log(session_id)
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity':1}
        }
        else {
            if (cart[productId]['quantity'] < pronum) {
                cart[productId]['quantity'] += 1
            }
        }
    }
    
    if (action == 'remove') {
        if (cart[productId]['quantity'] < 1) {
            console.log('Remove Item')
            delete cart[productId]
        }
        else {
            cart[productId]['quantity'] -= 1
        }
    }

    if (action == 'del') {
        delete cart[productId]
    }
    console.log('Cart: ', cart)
    a = new Date(new Date().getTime() +1000*60*60*24*365);
    // document.cookie = 'cart=' + JSON.stringify(cart); expires='+a.toGMTString()+';'; 
    // document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    document.cookie = 'cart=' + JSON.stringify(cart) + ";expires=Thu, 18 Dec 2100 12:00:00 UTC;" + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId, action, pronum) {
    console.log('User is logged in, sending data.')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({productId:productId, action:action, pronum:pronum})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}