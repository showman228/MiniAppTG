import { createContext, useContext, useEffect, useState } from "react";
import * as usersApi from "../api/users";
import { getToken, setToken, clearToken } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false); // чтобы /profile не мигал формой входа

  // Восстановление сессии при загрузке
  useEffect(() => {
    if (!getToken()) {
      setReady(true);
      return;
    }
    usersApi
      .getMe()
      .then(setUser)
      .catch(() => {}) // 401 уже почистил токен в интерцепторе
      .finally(() => setReady(true));
  }, []);

  // 401 из любого запроса — разлогиниваемся
  useEffect(() => {
    const onLogout = () => setUser(null);
    window.addEventListener("auth:logout", onLogout);
    return () => window.removeEventListener("auth:logout", onLogout);
  }, []);

  // Бэкенд ищет пользователя по username, не по email (services/user_service.py).
  // btoa безопасен: формы не пропускают не-ASCII, а FastAPI декодирует Basic как ascii.
  async function login(username, password) {
    setToken(btoa(`${username}:${password}`));
    const me = await usersApi.getMe();
    setUser(me);
    return me;
  }

  async function register(form) {
    await usersApi.register(form);
    return login(form.username, form.password);
  }

  function logout() {
    clearToken();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, ready, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
