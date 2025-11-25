FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y curl gnupg2 unixodbc unixodbc-dev gcc g++ apt-transport-https ca-certificates

# Добавляем GPG-ключ Microsoft (новый способ — через keyring)
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
       | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg

# Добавляем репозиторий MSSQL ODBC для Debian 12
RUN echo "deb [signed-by=/etc/apt/keyrings/microsoft.gpg] \
    https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/mssql-release.list

# Устанавливаем драйвер ODBC
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . /app/

WORKDIR /app/src

COPY init.sh /init.sh
RUN chmod +x /init.sh

EXPOSE 8000

ENTRYPOINT ["/init.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]