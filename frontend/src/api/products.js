import api from "./client";

export const getProducts = () => api.get("/products/");
export const getProductsByCategory = (categoryId) => api.get(`/products/category/${categoryId}`);
export const getProduct = (productId) => api.get(`/products/${productId}`);
