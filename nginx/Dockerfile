FROM nginx:alpine

<<<<<<< HEAD
LABEL maintainer="Uallas Leles Pereira <uallasleles@hotmail.com>"

=======
>>>>>>> c5b77bfff5d8b4673439ed379f08cb420e2af38f
RUN apk --update add nginx && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log && \
    mkdir /etc/nginx/sites-enabled/ && \
    mkdir -p /run/nginx && \
    rm -rf /etc/nginx/conf.d/default.conf && \
    rm -rf /var/cache/apk/*

COPY conf.d/app.conf /etc/nginx/conf.d/app.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]

