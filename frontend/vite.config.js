import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Читается Node-процессом самого Vite, а не браузером.
// В docker это http://app:8000 (имя сервиса), локально — 127.0.0.1:8000.
const target = process.env.API_TARGET || "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // 0.0.0.0, иначе контейнер недоступен с хоста
    port: 5173,
    watch: { usePolling: true }, // Docker Desktop на macOS не пробрасывает fsevents
    proxy: {
      // Префикс /api искусственный: без него SPA-маршрут /cart ушёл бы в бэкенд.
      // rewrite срезает его обратно, поэтому бэкенд менять не нужно.
      "/api": { target, changeOrigin: true, rewrite: (p) => p.replace(/^\/api/, "") },
      // Картинки товаров: в БД лежит готовый путь /static/images/*.jpeg
      "/static": { target, changeOrigin: true },
    },
  },
});
