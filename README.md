# Raykhan Aytmuratova — portfolio

One self-contained page: `src/index.src.html` plus the fonts and images in `assets/`.
`python3 build.py` inlines everything into `index.html`.

## Deploy

The server checks this repository every minute and publishes each new push to `main`
(nginx, `/var/www/portfolio`). One-time setup on the server:

```
curl -fsSL https://raw.githubusercontent.com/rea1706-max/potfolio/main/deploy/install.sh | sudo bash
```

Live: http://82.115.51.36/
