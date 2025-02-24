function decreaseQuantity(index) {
    let quantityInput = document.getElementById(`quantity-${index}`);
    let currentValue = parseInt(quantityInput.value);

    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
    }
}

// Function to increase quantity
function increaseQuantity(index) {
    let quantityInput = document.getElementById(`quantity-${index}`);
    let currentValue = parseInt(quantityInput.value);

    quantityInput.value = currentValue + 1;
}

// Function to add item to cart
function addToCart(productName, price, index) {
    let quantity = parseInt(document.getElementById(`quantity-${index}`).value);
    
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_name: productName,
            price: price,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            updateCartUI(productName, price, quantity);
            toggleCart(true);  // Open the cart when an item is added
        } else {
            alert("Failed to add item.");
        }
    })
    .catch(error => console.error("Error:", error));
}

// Function to toggle cart visibility
function toggleCart(forceOpen = false) {
    let cartSidebar = document.getElementById("cartSidebar");

    if (forceOpen) {
        cartSidebar.classList.add("active");
    } else {
        cartSidebar.classList.toggle("active");
    }
}

// Function to update the cart UI dynamically
function updateCartUI(productName, price, quantity) {
    let cartItems = document.getElementById("cartItems");

    // Remove "Your cart is empty" text
    if (cartItems.innerHTML.includes("Your cart is empty")) {
        cartItems.innerHTML = "";
    }

    // Check if the item is already in the cart
    let existingItem = document.querySelector(`#cartItems .cart-item[data-name='${productName}']`);

    if (existingItem) {
        // Update the quantity
        let quantitySpan = existingItem.querySelector(".cart-item-quantity");
        let newQuantity = parseInt(quantitySpan.textContent) + quantity;
        quantitySpan.textContent = newQuantity;
    } else {
        // Create a new cart item element
        let newItem = document.createElement("div");
        newItem.classList.add("cart-item");
        newItem.setAttribute("data-name", productName);
        newItem.innerHTML = `
            <span>${productName}</span>
            <span>₹${price}</span>
            <span class="cart-item-quantity">${quantity}</span>
        `;

        cartItems.appendChild(newItem);
    }
}
function proceedToCheckout() {
    let cartItems = document.querySelectorAll("#cartItems .cart-item");
    if (cartItems.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    let cartData = [];

    cartItems.forEach(item => {
        let productName = item.querySelector("span:nth-child(1)").textContent;
        let price = parseFloat(item.querySelector("span:nth-child(2)").textContent.replace("₹", ""));
        let quantity = parseInt(item.querySelector(".cart-item-quantity").textContent);

        cartData.push({ product_name: productName, price: price, quantity: quantity });
    });

    fetch('/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cart: cartData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.href = "/checkout"; // Redirect to the checkout page
        } else {
            alert("Checkout failed. Please try again.");
        }
    })
    .catch(error => console.error("Error:", error));
}