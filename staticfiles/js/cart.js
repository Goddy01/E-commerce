var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log('produtId: ', productId, 'action: ', action)
        console.log('USER: ', user)
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        }
        else{
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action) {
    console.log('Not logged in...')
    // console.log(session_id)
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity':1}
        }
        else {
            // if (cart[productId]['quantity'] < product) {
            cart[productId]['quantity'] += 1
            // }
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

function updateUserOrder(productId, action, productNum) {
    console.log('User is logged in, sending data.')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({productId:productId, action:action, productNum:productNum})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}