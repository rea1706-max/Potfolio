#!/bin/sh
# Copies the current checkout into the web root. Called by /usr/local/bin/portfolio-update.
set -e
cd /opt/portfolio-src
mkdir -p /var/www/portfolio
cp index.html favicon.ico /var/www/portfolio/
rm -rf /var/www/portfolio/yohaku
cp -r yohaku /var/www/portfolio/yohaku
cp deploy/nginx.conf /etc/nginx/sites-available/portfolio
ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/portfolio
nginx -t && systemctl reload nginx
