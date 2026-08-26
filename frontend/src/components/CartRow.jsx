import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { formatPrice } from "../utils/format";

export default function CartRow({ item }) {
  const { update, remove, busy } = useCart();

  return (
    <div className="receipt__row">
      <div className="cart-row__media media-placeholder">
        {item.image_url && <img src={item.image_url} alt={item.name} loading="lazy" />}
      </div>

      <div className="cart-row__body">
        <h3 className="cart-row__name">
          <Link to={`/product/${item.product_id}`} className="product-card__link">
            {item.name}
          </Link>
        </h3>
        <span className="cart-row__price">{formatPrice(item.price)} за штуку</span>
      </div>

      <div className="cart-row__side">
        <span className="cart-row__subtotal">{formatPrice(item.subtotal)}</span>

        <div className="qty">
          <button
            type="button"
            className="qty__btn"
            aria-label="Убрать одну штуку"
            disabled={busy || item.quantity <= 1}
            onClick={() => update(item.product_id, item.quantity - 1)}
          >
            −
          </button>
          <span className="qty__value">{item.quantity}</span>
          <button
            type="button"
            className="qty__btn"
            aria-label="Добавить одну штуку"
            disabled={busy}
            onClick={() => update(item.product_id, item.quantity + 1)}
          >
            +
          </button>
        </div>

        <button
          type="button"
          className="cart-row__remove"
          disabled={busy}
          onClick={() => remove(item.product_id)}
        >
          Убрать
        </button>
      </div>
    </div>
  );
}
