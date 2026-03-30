import { getCart, getCartTotal, clearCart } from '../store/cart.js';
import { renderHeader, syncCartBadge }      from '../components/header.js';

renderHeader();
syncCartBadge();

const list  = document.getElementById('checkout-list');
const total = document.getElementById('checkout-total');
const form  = document.getElementById('checkout-form');

// Рендер состава заказа в правой колонке
function renderSummary() {
    const cart = getCart();

    if (!cart.length) {
        list.innerHTML = '<li>Корзина пуста</li>';
        total.textContent = '0 ₽';
        return;
    }

    list.innerHTML = cart
        .map((item) => `<li>${item.name} × ${item.quantity} — ${item.price * item.quantity} ₽</li>`)
        .join('');

    total.textContent = `${getCartTotal()} ₽`;
}

// Отправка заказа
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = form.querySelector('[type=submit]');
    btn.disabled    = true;
    btn.textContent = 'Оформляем...';

    // Здесь можно добавить POST /api/order/create когда будет готова авторизация
    // Пока просто очищаем корзину и редиректим
    clearCart();
    location.href = '/order-success.html';
});

renderSummary();