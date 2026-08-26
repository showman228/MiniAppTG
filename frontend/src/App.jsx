import { Route, Routes } from "react-router-dom";

import Header from "./components/Header";
import Notice from "./components/Notice";
import HomePage from "./views/HomePage";
import ProductPage from "./views/ProductPage";
import CartPage from "./views/CartPage";
import ProfilePage from "./views/ProfilePage";

export default function App() {
  return (
    <>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/product/:id" element={<ProductPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="*" element={<Notice text="Такой страницы нет" backLink />} />
        </Routes>
      </main>
    </>
  );
}
