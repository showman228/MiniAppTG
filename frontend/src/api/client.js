import axios from "axios";

// baseURL '/api' — Vite проксирует на бэкенд и срезает префикс (см. vite.config.js)
const api = axios.create({ baseURL: "/api" });

const AUTH_KEY = "auth"; // base64(username:password) для HTTP Basic

export const getToken = () => localStorage.getItem(AUTH_KEY);
export const setToken = (token) => localStorage.setItem(AUTH_KEY, token);
export const clearToken = () => localStorage.removeItem(AUTH_KEY);

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) config.headers.Authorization = `Basic ${token}`;
  return config;
});

// Разворачиваем res.data сразу — доменные обёртки становятся однострочными
api.interceptors.response.use(
  (res) => res.data,
  (error) => {
    const status = error.response?.status;
    if (status === 401) {
      clearToken();
      // событие вместо прямого вызова setUser — иначе циклический импорт с AuthContext
      window.dispatchEvent(new Event("auth:logout"));
    }
    console.error("API:", status, error.response?.data?.detail || error.message);
    return Promise.reject(error);
  },
);

// Читаемый текст ошибки для показа пользователю
export function errorText(error, fallback = "Что-то пошло не так") {
  const detail = error?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map((d) => d.msg).join(", ");
  return fallback;
}

export default api;
