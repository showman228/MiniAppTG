import { post, put } from "./client.js"

export async function addToCart(requestCart) {
    return post("/cart/create", { request: requestCart });
}

export async function getCartDetails(cartData) {
    return post("/cart/details", { cart_data: cartData });
}

export async function updateCart(requestCart) {
    return put("/cart/update", { request: requestCart });
}

export async function removeFromCart(requestCart) {
    return del("/cart/remove", { request: requestCart });
}

