import { get } from './client.js';

export async function getCategories() {
    return get("/category/");
}

export async function getCategoryById(categoryId) {
    return get(`/category/${categoryId}`);
}