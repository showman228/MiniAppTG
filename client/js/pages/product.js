import { getProductById }   from '../api/products.js';
import { addToCart }        from '../store/cart.js';
import { renderHeader, syncCartBadge } from '../components/header.js';

console.log('[product] script loaded');

const PLACEHOLDER = '/assets/images/placeholder.jpg';

function escapeHtml(s) {
    return String(s ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function init() {
    renderHeader();
    syncCartBadge();

    const wrap = document.getElementById('product-content');
    if (!wrap) {
        console.error('[product] #product-content не найден');
        return;
    }

    const params = new URLSearchParams(location.search);
    const productId = params.get('id');

    if (!productId) {
        wrap.innerHTML = '<p>Товар не найден.</p>';
        return;
    }

    wrap.innerHTML = '<p style="padding:20px;">Загрузка...</p>';

    getProductById(productId)
        .then((p) => {
            const img = p.image_url || PLACEHOLDER;
            const cat = p.category && p.category.name ? p.category.name : '';
            wrap.innerHTML = `
                <div>
                    <img class="product-image"
                         src="${escapeHtml(img)}"
                         alt="${escapeHtml(p.name)}"
                         onerror="this.onerror=null;this.src='${PLACEHOLDER}'">
                </div>
                <div>
                    <span class="badge">${escapeHtml(cat)}</span>
                    <h1 class="page-title">${escapeHtml(p.name)}</h1>
                    <p class="product-price">${Number(p.price).toLocaleString('ru-RU')} ₽</p>
                    <p>${escapeHtml(p.description || '')}</p>
                    <button class="btn btn-primary" id="add-btn">Добавить в корзину</button>
                    <p class="success-msg" id="success-msg">✓ Товар добавлен в корзину</p>
                </div>
            `;

            document.getElementById('add-btn').addEventListener('click', () => {
                addToCart(p);
                const msg = document.getElementById('success-msg');
                msg.classList.add('show');
                setTimeout(() => msg.classList.remove('show'), 1600);
            });
        })
        .catch((err) => {
            console.error('[product] load failed:', err);
            wrap.innerHTML = `<p style="color:red;">Товар не найден.<br><small>${escapeHtml(err.message)}</small></p>`;
        });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
