// also don't display any greetings
function hvr(dom, action)
{
    if (action == 'in')
    {
        $(dom).find("[col=g]").css("display", "none");
        $(dom).find("[col=b]").css("display", "inline-block");
    }

    else
    {
        $(dom).find("[col=b]").css("display", "none");
        $(dom).find("[col=g]").css("display", "inline-block");
    }
}

var updateBtns = document.getElementsByClassName("update-cart")

for (var i=0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productID = this.dataset.product
        var action    = this.dataset.action
        console.log('productID:', productID, 'action:', action)

        console.log('USER:', user)
        if (user === 'AnonymousUser') {
            // console.log('Not logged in')
            addCookieItem(productID, action)
        }
        else {
            updateUserOrder(productID, action)
        }
    })
}

// action is an add or remove when changing the state of the cart
function addCookieItem(productID, action) {
    console.log('User Is Not Logged In Yet...') 

    if (action == 'add'){
        if(cart[productID] == undefined) {
            cart[productID] = {'quantity': 1}
        }
        else {
            cart[productID]['quantity'] += 1
        }
    }

    // if removing from our local storage cart
    if (action == 'remove'){
        cart[productID]['quantity'] -= 1
        if(cart[productID]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[productID]
        }
    }

    console.log('Cart:', cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    // reload cart on each page
    location.reload()
}

function updateUserOrder(productID, action){
    console.log('User is logged in, sending data...')

    // using the fetch API
    var url = '/update_item/'

    fetch(url, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productID': productID, 'action': action})
    })

    .then((response) => {
        console.log('Got Here first')
        return response.json()
        
    })

    .then((data) => {
        console.log('data:', data)
        location.reload() // to reload our page automatically everytime items gets added to our cart.
    })
}