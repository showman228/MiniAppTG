import { Link, useParams } from "react-router-dom";

import Notice from "../components/Notice";
import { useFetch } from "../hooks/useFetch";
import { getProduct } from "../api/products";
import { useCart } from "../context/CartContext";
import { formatPrice } from "../utils/format";

export default function ProductPage() {
  const { id } = useParams();
  const { add, busy } = useCart();
  const { data: product, loading, error } = useFetch(() => getProduct(id), [id]);

  if (loading) return <Notice text="Загружаем товар…" />;
  if (error) return <Notice text="Товар не найден" variant="error" backLink />;

  return (
    <div className="page">
      <Link to="/" className="back-link">
        ← Все товары
      </Link>

      <div className="product-page">
        <div className="product-page__media media-placeholder">
          {product.image_url && <img src={product.image_url} alt={product.name} />}
        </div>

        <div>
          <span className="chip chip--static">{product.category.name}</span>
          <h1 className="product-page__title">{product.name}</h1>
          <p className="product-page__description">{product.description}</p>

          <div className="product-page__price">{formatPrice(product.price)}</div>

          <div className="product-page__actions">
            <button type="button" className="btn-dark" disabled={busy} onClick={() => add(product.id)}>
              В корзину
            </button>
            <Link to="/cart" className="btn-quiet">
              Перейти в корзину
            </Link>
          </div>

          <p className="product-page__meta">Артикул {String(product.id).padStart(5, "0")}</p>
        </div>
      </div>
    </div>
  );
}
