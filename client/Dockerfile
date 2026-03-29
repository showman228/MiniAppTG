FROM nginx:alpine

# Копируем JS-файлы фронтенда
COPY client/ /usr/share/nginx/html/

# Копируем конфиг nginx
COPY nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


