#!/bin/sh
# Copies the current checkout into the web root. Called by /usr/local/bin/portfolio-update.
set -e
cd /opt/portfolio-src
mkdir -p /var/www/portfolio
# assets first (new hashed files), then the page that points to them
rm -rf /var/www/portfolio/a.new && cp -r a /var/www/portfolio/a.new
rm -rf /var/www/portfolio/a && mv /var/www/portfolio/a.new /var/www/portfolio/a
cp index.html favicon.ico /var/www/portfolio/
cp robots.txt sitemap.xml /var/www/portfolio/ 2>/dev/null || true
rm -rf /var/www/portfolio/yohaku
cp -r yohaku /var/www/portfolio/yohaku
cp deploy/nginx.conf /etc/nginx/sites-available/portfolio
ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/portfolio
nginx -t && systemctl reload nginx
