import api from "./client";

export const register = (data) => api.post("/users/register", data);
export const getMe = () => api.get("/users/me");
