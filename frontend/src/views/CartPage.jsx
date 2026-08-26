import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import CartRow from "../components/CartRow";
import Notice from "../components/Notice";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import { createOrder } from "../api/orders";
import { errorText } from "../api/client";
import { formatPrice, pluralizeTovar } from "../utils/format";

export default function CartPage() {
  const { details, clear, busy } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [placing, setPlacing] = useState(false);
  const [error, setError] = useState("");

  async function placeOrder() {
    if (!user) {
      navigate("/profile");
      return;
    }

    setPlacing(true);
    setError("");
    try {
      // Заказ на бэкенде — одна строка на товар, поэтому шлём по позиции за раз
      for (const item of details.items) {
        await createOrder({
          product_id: item.product_id,
          quantity: item.quantity,
          price: item.price,
          total_price: item.subtotal,
        });
      }
      clear();
      navigate("/profile");
    } catch (err) {
      setError(errorText(err, "Не удалось оформить заказ"));
    } finally {
      setPlacing(false);
    }
  }

  if (details.items.length === 0) {
    return (
      <div className="page">
        <div className="page-head">
          <h1>Корзина</h1>
        </div>
        <Notice text="В корзине пока пусто" backLink />
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-head">
        <h1>Корзина</h1>
        <span className="products__count">
          {details.items_count} {pluralizeTovar(details.items_count)}
        </span>
      </div>

      <div className="receipt">
        {details.items.map((item) => (
          <CartRow key={item.product_id} item={item} />
        ))}

        <div className="receipt__total">
          <span className="receipt__total-label">Итого</span>
          <span className="receipt__total-value">{formatPrice(details.total)}</span>
        </div>
      </div>

      {error && <p className="auth-form__error">{error}</p>}

      <div className="cart-actions">
        <button
          type="button"
          className="btn-primary"
          disabled={busy || placing}
          onClick={placeOrder}
        >
          {placing ? "Оформляем…" : "Оформить заказ"}
        </button>
        {!user && (
          <span className="cart-actions__hint">
            Сначала <Link to="/profile">войдите в профиль</Link>
          </span>
        )}
      </div>
    </div>
  );
}
