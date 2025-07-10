brew install pipx
pipx install poetry
pipx inject poetry poetry-plugin-shell
poetry install

POSTGRES_URL="postgresql+psycopg:///hars:ket6711@192.168.0.3:5432/app_db"
SQLITE_URL="sqlite+aiosqlite:///database.db"