import api from "./client";

// Trailing slash обязателен — без него бэкенд отвечает 307
export const getCategories = () => api.get("/category/");
