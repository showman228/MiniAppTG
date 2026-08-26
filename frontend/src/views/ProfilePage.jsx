import AuthForms from "../components/AuthForms";
import Notice from "../components/Notice";
import { useAuth } from "../context/AuthContext";
import { useFetch } from "../hooks/useFetch";
import { getUserOrders } from "../api/orders";
import { getProducts } from "../api/products";
import { formatDate, formatPrice } from "../utils/format";

export default function ProfilePage() {
  const { user, ready, logout } = useAuth();

  const orders = useFetch(user ? () => getUserOrders(user.id) : null, [user?.id]);
  // Заказ хранит только product_id — названия подтягиваем одним запросом
  const products = useFetch(user ? getProducts : null, [user?.id]);

  if (!ready) return <Notice text="Проверяем сессию…" />;

  if (!user) {
    return (
      <div className="page">
        <div className="page-head">
          <h1>Профиль</h1>
        </div>
        <AuthForms />
      </div>
    );
  }

  const names = new Map((products.data || []).map((p) => [p.id, p.name]));
  const items = orders.data || [];

  return (
    <div className="page">
      <div className="page-head">
        <h1>Профиль</h1>
      </div>

      <div className="profile-card">
        <div className="profile-card__head">
          <div>
            <h2 className="profile-card__name">{user.firstname || user.username}</h2>
            <p className="profile-card__email">{user.email}</p>
          </div>
          <button type="button" className="btn-quiet" onClick={logout}>
            Выйти
          </button>
        </div>
      </div>

      <h2 className="section-title">История заказов</h2>

      {orders.loading && <Notice text="Загружаем заказы…" />}
      {orders.error && <Notice text="Не удалось загрузить заказы" variant="error" />}
      {!orders.loading && !orders.error && items.length === 0 && (
        <Notice text="Заказов пока нет" backLink />
      )}

      {items.length > 0 && (
        <div className="receipt">
          {items.map((order) => (
            <div key={order.id} className="receipt__row order-row">
              <span className="order-row__date">{formatDate(order.created_at)}</span>
              <span className="order-row__name">
                {names.get(order.product_id) || `Товар №${order.product_id}`} × {order.quantity}
              </span>
              <span className="order-row__sum">{formatPrice(order.total_price)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
