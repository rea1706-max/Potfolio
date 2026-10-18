#!/usr/bin/env bash
# Runs on the server after the files are copied to ~/portfolio-release.
# Installs nginx if missing, publishes the site to /var/www/portfolio and reloads nginx.
set -euo pipefail
sudo_() { echo "$DEPLOY_PASS" | sudo -S -p '' "$@"; }
REL="$HOME/portfolio-release"

if ! command -v nginx >/dev/null 2>&1; then
  sudo_ apt-get update -y
  sudo_ env DEBIAN_FRONTEND=noninteractive apt-get install -y nginx
fi

sudo_ mkdir -p /var/www/portfolio
sudo_ cp "$REL/index.html" "$REL/favicon.ico" /var/www/portfolio/
sudo_ chown -R www-data:www-data /var/www/portfolio

sudo_ cp "$REL/deploy/nginx.conf" /etc/nginx/sites-available/portfolio
sudo_ ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/portfolio

if command -v ufw >/dev/null 2>&1 && sudo_ ufw status | grep -q "Status: active"; then
  sudo_ ufw allow 80/tcp
fi

sudo_ nginx -t
sudo_ systemctl enable --now nginx
sudo_ systemctl reload nginx
echo "Deployed: http://82.115.51.36/"
