// let updateBtns = document.getElementsByClassName('update-cart')

// for (let i = 0; i < updateBtns.length; i++){
//     updateBtns[i].addEventListener('click', function() {
//         let productId = updateBtns[i].dataset.product
//         let action = updateBtns[i].dataset.action
//         let pronum = updateBtns[i].dataset.pronum

//         console.log('produtId: ', productId, 'action: ', action, 'pronum: ', pronum)
//         console.log('USER: ', user)
//         console.log(pronum)
//         if (user === 'AnonymousUser') {
//             addCookieItem(productId, action, pronum)
//         }
//         else{
//             updateUserOrder(productId, action, pronum)
//         }
//     })
// }

// function addCookieItem(productId, action, pronum) {
//     console.log('Not logged in...')
//     // console.log(session_id)
//     if (action == 'add') {
//         if (device[productId] == undefined) {
//             device[productId] = {'quantity':1}
//         }
//         else {
//             if (device[productId]['quantity'] < pronum) {
//                 device[productId]['quantity'] += 1
//             }
//         }
//     }
    
//     if (action == 'remove') {
//         if (device[productId]['quantity'] < 1) {
//             console.log('Remove Item')
//             delete device[productId]
//         }
//         else {
//             device[productId]['quantity'] -= 1
//         }
//     }

//     if (action == 'del') {
//         delete device[productId]
//     }
//     console.log('Cart: ', device)
//     location.reload()
// }

// function updateUserOrder(productId, action, pronum) {
//     console.log('User is logged in, sending data.')

//     var url = '/update_item/'

//     fetch(url, {
//         method:'POST',
//         headers:{
//             'Content-Type':'application/json',
//             'X-CSRFToken':csrftoken,
//         },
//         body:JSON.stringify({productId:productId, action:action, pronum:pronum})
//     })
//     .then((response) =>{
//         return response.json()
//     })
//     .then((data) => {
//         console.log('data:', data)
//         location.reload()
//     })
// }