import { get, post, del, put } from './client.js';

export async function getOrders() {
    return get("/order");
}

export async function getOrder(orderId) {
    return get(`/order/${orderId}`);
}

export async function getUserOrders(userId) {
    return get(`/order/users/${userId}`);
}

export async function createOrder(orderData) {
    return post("/order/create", orderData);
}

export async function updateOrder(orderId, orderData) {
    return put(`/order/update/${orderId}`, orderData);
}

export async function deleteOrder(orderId) {
    return del(`/order/delete/${orderId}`);
}