// Ключ в localStorage
const CART_KEY = 'le-desir-cart';

function readCart() {
    try {
        return JSON.parse(localStorage.getItem(CART_KEY) || '[]');
    } catch {
        return [];
    }
}

function writeCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    // Уведомляем все части страницы об изменении корзины
    window.dispatchEvent(new CustomEvent('cart:updated', { detail: cart }));
}

export function getCart() {
    return readCart();
}

export function getCartCount() {
    return readCart().reduce((sum, item) => sum + item.quantity, 0);
}

export function getCartTotal() {
    return readCart().reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// product — объект { id, name, price, image_url }
export function addToCart(product, quantity = 1) {
    const cart = readCart();
    const existing = cart.find((i) => i.id === product.id);
    if (existing) {
        existing.quantity += quantity;
    } else {
        cart.push({
            id:        product.id,
            name:      product.name,
            price:     product.price,
            image_url: product.image_url || null,
            quantity,
        });
    }
    writeCart(cart);
}

export function removeFromCart(productId) {
    writeCart(readCart().filter((i) => i.id !== productId));
}

export function increaseQuantity(productId) {
    const cart = readCart();
    const item = cart.find((i) => i.id === productId);
    if (item) { item.quantity += 1; writeCart(cart); }
}

export function decreaseQuantity(productId) {
    const cart = readCart();
    const item = cart.find((i) => i.id === productId);
    if (!item) return;
    item.quantity -= 1;
    if (item.quantity <= 0) {
        writeCart(cart.filter((i) => i.id !== productId));
    } else {
        writeCart(cart);
    }
}

export function clearCart() {
    writeCart([]);
}