#!/usr/bin/env bash
# One-time server setup. Run on the server as:
#   curl -fsSL https://raw.githubusercontent.com/rea1706-max/potfolio/main/deploy/install.sh | sudo bash
# Installs nginx and git, serves the portfolio at http://<server-ip>/,
# and checks GitHub every minute: each push to main goes live by itself.
set -euo pipefail
REPO=https://github.com/rea1706-max/potfolio.git
SRC=/opt/portfolio-src

export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y nginx git

if [ ! -d "$SRC/.git" ]; then
  git clone -q --depth 1 "$REPO" "$SRC"
fi

cat > /usr/local/bin/portfolio-update <<'UPD'
#!/bin/sh
# Pull the latest main from GitHub and publish it if anything changed.
set -e
cd /opt/portfolio-src
git fetch -q --depth 1 origin main
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ] || [ ! -f /var/www/portfolio/index.html ]; then
  git reset -q --hard origin/main
  sh deploy/publish.sh
  echo "$(date -Is) published $(git rev-parse --short HEAD)"
fi
UPD
chmod +x /usr/local/bin/portfolio-update

echo '* * * * * root /usr/local/bin/portfolio-update >>/var/log/portfolio-update.log 2>&1' > /etc/cron.d/portfolio
chmod 644 /etc/cron.d/portfolio

if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active"; then
  ufw allow 80/tcp
fi

systemctl enable --now nginx
rm -f /var/www/portfolio/index.html
/usr/local/bin/portfolio-update
echo
echo "Done: http://82.115.51.36/"
