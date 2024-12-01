
Необходимо создать .env файл и внести туда параметры DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME

Также:
```bash
pip install -m requirements.txt
```
И:
``` bash
sudo -E python3 db_service.py & sudo -E python3 app.py
```

\
\
Для клонирования конкретной папки из репозитория:

``` bash
mkdir <имя_папки>
cd <имя_папки>
git init

git remote add -f origin <URL_репозитория>
git config core.sparseCheckout true

echo "путь/к/директории/" >> .git/info/sparse-checkout

git pull origin master
```