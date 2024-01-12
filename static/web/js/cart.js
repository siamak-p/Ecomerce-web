/**
 * Created by siamak on 8/15/22.
 */
// var addtoCart = document.getElementsByClassName('add-to-cart');
//
// for(var i= 0; i< addtoCart.length; i++){
//     addtoCart[i].addEventListener('click', function(){
//         var productID = this.dataset.product;
//         var action = this.dataset.action;
//         console.log('productID: ', productID, 'Action: ', action);
//         console.log('user: ', user);
//
//         if(user === 'AnonymousUser'){
//             console.log('login nakardid')
//         }else{
//             addItems(productID, action)
//         }
//     })
// }
//
// function addItems(productID, action){
//     console.log('login kardid');
//     // var url = 'additems/'
//     var url = (`${window.location.protocol}//${window.location.host}`+'/cart/add-to-cart/')
//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'ContentType': 'application/json',
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({
//             'productID': productID,
//             'action': action,
//         })
//     })
//     .then((response) => {
//             return response.json()
//         })
//         .then((data) => {
//             console.log('Data: ', data);
//         })
// }




// $(document).ready(function () {
//     var btnUpdate = document.getElementsByClassName('cart-update');
//     var token = $('input[name=csrfmiddlewaretoken]').val();
//     for (var i = 0; i < btnUpdate.length; i++){
//         var button = btnUpdate[i];
//         button.addEventListener('click', function (event) {
//             var buttonClicked = event.target.value;
//             console.log(buttonClicked);
//             var qntFromSite = document.getElementById('number-'+ event.target.value);
//             // console.log('value is: ', qntFromSite.value);
//             $.ajax({
//                 method: "POST",
//                 url:(`${window.location.protocol}//${window.location.host}`+'/cart/cart-update/'),
//                 data:{
//                     'productID': buttonClicked,
//                     'qntFromSite': qntFromSite.value,
//                     csrfmiddlewaretoken: token
//                 },
//                 cache: false,
//                 dataType: 'json',
//
//                 success: function (res) {
//                     alertify.set('notifier','position', 'top-left');
//                     alertify.success(res.status);
//
//                 },
//                 error: function(){
//                     alertify.error('خطایی رخ داده است. لطفا مجددا امتحان فرمایید.');
//                 }
//
//             });
//
//         });
//         // window.location.reload()
//     }
//
// });
