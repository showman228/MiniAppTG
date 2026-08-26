import api from "./client";

export const getUserOrders = (userId) => api.get(`/order/users/${userId}`);
export const createOrder = (data) => api.post("/order/create", data);
