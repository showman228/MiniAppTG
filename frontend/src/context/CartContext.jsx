import { createContext, useContext, useEffect, useState } from "react";
import * as cartApi from "../api/cart";

const CartContext = createContext(null);

const STORAGE_KEY = "cart";
const EMPTY = { items: [], total: 0, items_count: 0 };

function readStorage() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  } catch {
    return {};
  }
}

// CartResponse.items -> {product_id: quantity}
const toDict = (items) => Object.fromEntries(items.map((i) => [i.product_id, i.quantity]));

export function CartProvider({ children }) {
  // cart — то, что уходит на сервер; details — последний ответ, из него рисуется UI
  const [cart, setCart] = useState(readStorage);
  const [details, setDetails] = useState(EMPTY);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
  }, [cart]);

  // При старте спрашиваем у сервера актуальные цены и названия
  useEffect(() => {
    const saved = readStorage();
    if (!Object.keys(saved).length) return;
    cartApi
      .getDetails(saved)
      .then(apply)
      .catch(() => {});
  }, []);

  // Сервер — источник истины: словарь пересобираем из ответа, а не считаем руками.
  // Если товар удалили из БД, бэкенд его молча пропустит и корзина сама починится.
  function apply(res) {
    setDetails(res);
    setCart(toDict(res.items));
  }

  async function run(request) {
    setBusy(true);
    try {
      apply(await request());
    } catch {
      // интерцептор уже залогировал
    } finally {
      setBusy(false);
    }
  }

  const value = {
    cart,
    details,
    busy,
    add: (productId, quantity = 1) => run(() => cartApi.add(productId, quantity, cart)),
    // quantity === 0 бэкенд трактует как удаление позиции
    update: (productId, quantity) => run(() => cartApi.update(productId, quantity, cart)),
    remove: (productId) => run(() => cartApi.remove(productId, cart)),
    clear: () => {
      setCart({});
      setDetails(EMPTY);
    },
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export const useCart = () => useContext(CartContext);
