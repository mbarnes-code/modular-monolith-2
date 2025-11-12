FROM php:8.1-apache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    zip \
    unzip \
    curl \
    libzip-dev \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libxml2-dev \
    libmcrypt-dev \
    mariadb-client \
    python3 \
    python3-pip \
    libfuzzy-dev \
    ssdeep \
    && rm -rf /var/lib/apt/lists/*

# Install PHP extensions
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        gd \
        zip \
        pdo_mysql \
        opcache \
        xml \
        mbstring \
        intl

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Enable Apache modules
RUN a2enmod rewrite headers ssl

# Set working directory
WORKDIR /var/www/html

# Copy MISP application
COPY . /var/www/html/

# Install Python dependencies
RUN pip3 install -r config/requirements.txt

# Set up Apache configuration
COPY infrastructure/docker/apache-misp.conf /etc/apache2/sites-available/misp.conf
RUN a2dissite 000-default && a2ensite misp

# Create necessary directories and set permissions
RUN mkdir -p /var/www/html/src/app/tmp/logs \
    && mkdir -p /var/www/html/src/app/tmp/cache \
    && mkdir -p /var/www/html/src/app/files \
    && chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html/src/app/tmp \
    && chmod +x /var/www/html/scripts/build-deb.sh

# Initialize git submodules (if not already done)
RUN if [ -f .gitmodules ]; then \
        git submodule update --init --recursive || true; \
    fi

# Expose port
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start Apache
CMD ["apache2-foreground"]