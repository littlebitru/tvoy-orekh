# «Твой орех»

Интернет-магазин на Django: регистрация и вход, каталог с поиском, карточки товаров, корзина, оформление заказов, личный кабинет с историей покупок и администрирование.

## Запуск

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install django pillow
python manage.py migrate
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`. Демонстрационные товары уже загружены в `db.sqlite3`.

## Администратор

```powershell
python manage.py createsuperuser
```

После этого панель управления товарами и заказами доступна по адресу `http://127.0.0.1:8000/admin/`.
