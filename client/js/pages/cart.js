import {
    getCart,
    getCartTotal,
    removeFromCart,
    increaseQuantity,
    decreaseQuantity,
} from '../store/cart.js';
import { renderHeader, syncCartBadge } from '../components/header.js';

renderHeader();
syncCartBadge();

const list  = document.getElementById('cart-list');
const total = document.getElementById('cart-total');

function renderCart() {
    const cart = getCart();

    if (!cart.length) {
        list.innerHTML = '<p class="card" style="padding:16px;">Корзина пуста.</p>';
        total.textContent = '0 ₽';
        return;
    }

    list.innerHTML = cart.map((item) => `
        <article class="card cart-item">
            <img src="${item.image_url || '/assets/images/placeholder.jpg'}" alt="${item.name}">
            <div>
                <h3 style="margin:0 0 6px;">${item.name}</h3>
                <p style="margin:0;color:#5b6474;">${item.price} ₽</p>
                <div class="qty-controls" style="margin-top:8px;">
                    <button class="qty-btn" data-dec="${item.id}">−</button>
                    <span>${item.quantity}</span>
                    <button class="qty-btn" data-inc="${item.id}">+</button>
                    <button class="btn btn-outline" data-remove="${item.id}" style="margin-left:8px;">Удалить</button>
                </div>
            </div>
        </article>
    `).join('');

    total.textContent = `${getCartTotal()} ₽`;
}

// Все клики на список корзины обрабатываем здесь
list.addEventListener('click', (e) => {
    const inc    = e.target.closest('[data-inc]');
    const dec    = e.target.closest('[data-dec]');
    const remove = e.target.closest('[data-remove]');

    if (inc)    increaseQuantity(Number(inc.dataset.inc));
    if (dec)    decreaseQuantity(Number(dec.dataset.dec));
    if (remove) removeFromCart(Number(remove.dataset.remove));

    renderCart();
});

renderCart();