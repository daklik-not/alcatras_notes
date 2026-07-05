
## Что проверять

| Что | Куда |
|-----|------|
| **.htaccess** | `/.htaccess` |
| **.htpasswd** | `/.htpasswd` |
| **server-status** | `/server-status` |
| **Directory listing** | убрать имя файла из URL |
| **Резервные копии** | `index.html.bak`, `.htaccess.bak`, `*.swp`, `*~` |
| **Path traversal** | `../../../../etc/passwd` |

## Быстро
1. `curl -I <url>`
2. Открыть корень `/`
3. `/.htaccess`
4. `/server-status`