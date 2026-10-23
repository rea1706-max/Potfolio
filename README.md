# Raykhan Aytmuratova — portfolio

`src/index.src.html` plus the fonts and images in `assets/`.
`python3 build.py` writes a light `index.html` and `a/` — every font and image as its own
WebP/woff2 file with a content hash in its name, so the first screen opens at once and
repeat visits load from cache. Commit both `index.html` and `a/`.

## Deploy

The server checks this repository every minute and publishes each new push to `main`
(nginx, `/var/www/portfolio`). One-time setup on the server:

```
curl -fsSL https://raw.githubusercontent.com/rea1706-max/potfolio/main/deploy/install.sh | sudo bash
```

Live: https://raykhan.uz/
