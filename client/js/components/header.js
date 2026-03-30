import { getCartCount } from '../store/cart.js';

// Вставляет шапку в #header-slot и обновляет счётчик корзины
export function renderHeader() {
    const slot = document.getElementById('header-slot');
    if (!slot) return;

    slot.innerHTML = `
        <header class="site-header">
            <div class="container site-header__inner">
                <a class="brand" href="/index.html">Le désir d'être</a>
                <nav class="header-nav">
                    <a class="nav-link" href="/catalog.html">Каталог</a>
                    <a class="cart-link" href="/cart.html" aria-label="Корзина">
                        🛒 <span class="cart-count" data-cart-count>0</span>
                    </a>
                </nav>
            </div>
        </header>
    `;

    updateCartBadge();
}

// Обновляет цифру на иконке корзины
export function updateCartBadge() {
    const count = getCartCount();
    document.querySelectorAll('[data-cart-count]').forEach((el) => {
        el.textContent = count;
    });
}

// Подписывается на событие изменения корзины и обновляет счётчик
export function syncCartBadge() {
    updateCartBadge();
    window.addEventListener('cart:updated', updateCartBadge);
}