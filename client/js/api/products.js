import { get } from './client.js';

export async function getProducts() {
    return get("/products");
}

export async function getProductById(productId) {
    return get(`/products/${productId}`);
}

export async function getProductByCategoryId(categoryId) {
    return get(`/products/category/${categoryId}`);
}