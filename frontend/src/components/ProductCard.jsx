import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { formatPrice } from "../utils/format";

export default function ProductCard({ product }) {
  const { add, busy } = useCart();

  return (
    <article className="product-card">
      <Link to={`/product/${product.id}`} className="product-card__link">
        <div className="product-card__media media-placeholder">
          {product.image_url && (
            <img src={product.image_url} alt={product.name} loading="lazy" />
          )}
        </div>
      </Link>

      <div className="product-card__body">
        <h3 className="product-card__name">
          <Link to={`/product/${product.id}`} className="product-card__link">
            {product.name}
          </Link>
        </h3>

        <div className="product-card__row">
          <span className="product-card__price">{formatPrice(product.price)}</span>
          <button
            type="button"
            className="product-card__add"
            disabled={busy}
            onClick={() => add(product.id)}
          >
            В корзину
          </button>
        </div>
      </div>
    </article>
  );
}
