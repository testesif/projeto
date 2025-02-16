FROM nginx:alpine

# Remove o arquivo de configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia o arquivo de configuração personalizado
COPY nginx.conf /etc/nginx/nginx.conf

# Expõe a porta 80
EXPOSE 80

# Inicia o Nginx
CMD ["nginx", "-g", "daemon off;"]