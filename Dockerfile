FROM nginx:alpine AS prod_serv

COPY web /usr/share/nginx/html

EXPOSE 80
