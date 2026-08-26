import { Link, NavLink } from "react-router-dom";
import { useCart } from "../context/CartContext";

export default function Header() {
  const { details } = useCart();

  return (
    <header className="site-header">
      <div className="site-header__inner">
        <Link to="/" className="brand">
          ЛАВКА
        </Link>

        <div className="site-header__actions">
          <NavLink
            to="/profile"
            className={({ isActive }) => (isActive ? "icon-btn icon-btn--active" : "icon-btn")}
            aria-label="Профиль"
          >
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 12a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9Zm0 2c-4.4 0-8 2.24-8 5v1a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-1c0-2.76-3.6-5-8-5Z" />
            </svg>
          </NavLink>

          <NavLink
            to="/cart"
            className={({ isActive }) =>
              isActive ? "icon-btn cart-btn icon-btn--active" : "icon-btn cart-btn"
            }
            aria-label="Корзина"
          >
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path
                d="M6 6h15l-1.5 9h-12L6 6Zm0 0-1-3H2m6 18a1 1 0 1 0 0-2 1 1 0 0 0 0 2Zm10 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            {details.items_count > 0 && (
              <span className="cart-btn__count">{details.items_count}</span>
            )}
          </NavLink>
        </div>
      </div>
    </header>
  );
}
