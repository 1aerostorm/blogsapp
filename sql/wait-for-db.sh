#!/bin/bash
until /opt/mssql-tools/bin/sqlcmd -S "$DB_HOST" -U "$DB_USER" -P "$DB_PASSWORD" -Q "SELECT 1" > /dev/null 2>&1
do
  echo "Waiting for MSSQL..."
  sleep 2
done

echo "MSSQL is ready, running init script..."
/opt/mssql-tools/bin/sqlcmd -S "$DB_HOST" -U "$DB_USER" -P "$DB_PASSWORD" -i /sql/init-db.sql