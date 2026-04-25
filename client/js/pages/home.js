import { getProducts } from '../api/products.js';

console.log('[home] script loaded');

const PLACEHOLDER = 'assets/images/placeholder.jpg';
const FEATURED_LIMIT = 4;

function escapeHtml(s) {
    return String(s ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function productTile(p) {
    const img = p.image_url || PLACEHOLDER;
    return `
        <a class="product" href="product.html?id=${p.id}">
            <img src="${escapeHtml(img)}"
                 alt="${escapeHtml(p.name)}"
                 onerror="this.onerror=null;this.src='${PLACEHOLDER}'">
            <h3>${escapeHtml(p.name)}</h3>
            <p>${Number(p.price).toLocaleString('ru-RU')} ₽</p>
        </a>
    `;
}

function init() {
    const container = document.getElementById('featured-products');
    if (!container) {
        console.error('[home] #featured-products не найден');
        return;
    }

    getProducts()
        .then((data) => {
            const list = Array.isArray(data) ? data : (data?.products ?? []);
            const featured = list.slice(0, FEATURED_LIMIT);
            console.log('[home] loaded %d products (showing %d)', list.length, featured.length);

            if (!featured.length) {
                container.innerHTML = '<p style="padding:20px;color:#888;">Товаров пока нет.</p>';
                return;
            }
            container.innerHTML = featured.map(productTile).join('');
        })
        .catch((err) => {
            console.error('[home] load failed:', err);
            container.innerHTML = `<p style="padding:20px;color:red;">Не удалось загрузить товары.<br><small>${escapeHtml(err.message)}</small></p>`;
        });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
