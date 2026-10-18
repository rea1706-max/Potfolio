# Raykhan Aytmuratova — portfolio

One self-contained page: `src/index.src.html` plus the fonts and images in `assets/`.
`python3 build.py` inlines everything into `index.html`.

## Deploy

Every push to `main` builds the page and publishes it to the server through
`.github/workflows/deploy.yml` (nginx, `/var/www/portfolio`).

Repository secrets the workflow needs (Settings → Secrets and variables → Actions):

| Secret | Value |
|---|---|
| `SSH_HOST` | server IP |
| `SSH_USER` | ssh user |
| `SSH_PASSWORD` | that user's password |

Live: http://82.115.51.36/
