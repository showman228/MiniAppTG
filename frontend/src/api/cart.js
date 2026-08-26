import api from "./client";

// Корзина на бэкенде stateless: весь словарь {product_id: quantity}
// уходит в каждом запросе и возвращается пересчитанным.
export const getDetails = (cart) => api.post("/cart/details", { cart_data: cart });
export const add = (product_id, quantity, cart) =>
  api.post("/cart/add", { product_id, quantity, cart });
export const update = (product_id, quantity, cart) =>
  api.put("/cart/update", { product_id, quantity, cart });
export const remove = (product_id, cart) => api.post("/cart/remove", { product_id, cart });
