FROM php:8.2-apache

# Set working directory
WORKDIR /var/www/html

# Install dependencies & PHP extensions
RUN apt-get update && apt-get install -y libpng-dev libzip-dev zip git unzip && \
    docker-php-ext-install pdo pdo_mysql mysqli gd && \
    pecl install redis && docker-php-ext-enable redis

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Izinkan akses folder
RUN echo '<Directory /var/www/html>\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>' > /etc/apache2/conf-available/docker-allow.conf \
    && a2enconf docker-allow

EXPOSE 80
CMD ["apache2-foreground"]
