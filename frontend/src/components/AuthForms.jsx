import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { errorText } from "../api/client";

// FastAPI декодирует заголовок Basic как ascii, а btoa не умеет не-latin1.
// Кириллица в логине или пароле сломает вход, поэтому не пускаем её на форме.
const ASCII = /^[\x20-\x7E]+$/;

export default function AuthForms() {
  const { login, register } = useAuth();

  const [tab, setTab] = useState("login");
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);

  async function onSubmit(event) {
    event.preventDefault();
    const form = Object.fromEntries(new FormData(event.target));

    if (!ASCII.test(form.username) || !ASCII.test(form.password)) {
      setError("Логин и пароль — латиница, цифры и знаки препинания");
      return;
    }

    setSending(true);
    setError("");
    try {
      if (tab === "login") {
        await login(form.username, form.password);
      } else {
        await register(form);
      }
    } catch (err) {
      const status = err?.response?.status;
      if (status === 409) setError("Такой email уже зарегистрирован");
      else if (status === 401) setError("Неверный логин или пароль");
      else setError(errorText(err, "Не удалось войти"));
    } finally {
      setSending(false);
    }
  }

  function switchTab(next) {
    setTab(next);
    setError("");
  }

  return (
    <div className="auth-card">
      <div className="auth-tabs__nav">
        <button
          type="button"
          className={tab === "login" ? "auth-tabs__btn auth-tabs__btn--active" : "auth-tabs__btn"}
          onClick={() => switchTab("login")}
        >
          Вход
        </button>
        <button
          type="button"
          className={
            tab === "register" ? "auth-tabs__btn auth-tabs__btn--active" : "auth-tabs__btn"
          }
          onClick={() => switchTab("register")}
        >
          Регистрация
        </button>
      </div>

      {/* key сбрасывает поля при переключении вкладки */}
      <form className="auth-form" onSubmit={onSubmit} key={tab}>
        {tab === "register" && (
          <label className="field">
            <span>Email</span>
            <input type="email" name="email" required autoComplete="email" />
          </label>
        )}

        <label className="field">
          <span>Имя пользователя</span>
          {/* Бэкенд ищет пользователя по username, поэтому поле обязательное */}
          <input type="text" name="username" required autoComplete="username" />
        </label>

        {tab === "register" && (
          <label className="field">
            <span>Имя</span>
            <input type="text" name="firstname" autoComplete="given-name" />
          </label>
        )}

        <label className="field">
          <span>Пароль</span>
          <input
            type="password"
            name="password"
            required
            autoComplete={tab === "login" ? "current-password" : "new-password"}
          />
          <span className="field__hint">Только латиница и цифры</span>
        </label>

        {error && <p className="auth-form__error">{error}</p>}

        <button type="submit" className="auth-form__submit" disabled={sending}>
          {sending ? "Отправляем…" : tab === "login" ? "Войти" : "Зарегистрироваться"}
        </button>
      </form>
    </div>
  );
}
