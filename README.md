# kumaPublicApiV1: python library for KUMA REST API
English version below

## Описание

kumaPublicApiV1 - это библиотека для python для работы с открытым REST API KUMA.
Бибилиотека содержит большинство поддерживаемых методов API KUMA, за исключением методов по работе с ресурсами: экспорт, импорт, просмотр, скачивание.

## Использование

Скачайте kumaPublicApiV1.py и используйте модуль в своих проектах интеграции с KUMA.

## Быстрый старт
Импортируйте модуль в свой проект на Python
```
from kumaPublicApiV1 import Kuma
```
Создайте объект класса Kuma, указав адрес сервера ядра KUMA, API-порт и токен
```
kuma = Kuma(address='10.10.10.10', port='7223', token='1fe5588a65e47f40a0717d82206090b9')
```

### Примеры использования
Просмотр информации о предъявителе токена
```
token_owner = kuma.whoami()
```
Поиск тенантов
```
tenant_info = kuma.get_tenant_by_name('My Tenant')
```
Импорт записей в активный лист
```
with open('records.csv', 'r') as file:
  data = file.read()
kuma.import_active_list_records(data, correlatorID='2f743382-8313-4f45-a801-979367a0d0a3', activeListID='a0996458-8b25-42e9-a673-d800d6169703', keyField='key')
```
Бэкап
```
kuma.core_backup('backup.tar.gz')
```
Импорт активов
```
kuma.import_assets(tenantID='a0996458-8b25-42e9-a673-d800d6169703', assets=assets)
```
Поиск адертов
```
alerts_list = kuma.get_alerts()
```

## Description

kumaPublicApiV1 - python module for KUMA REST API .
Module contains most REST API KUMA methods except resource export, import, view and download.

## Usage

Download kumaPublicApiV1.py and use it in your project related to KUMA.

## Quick start
Import the module to your Python script
```
from kumaPublicApiV1 import Kuma
```
Create a Kuma object by providing the address of the KUMA core installation, API port and token
```
kuma = Kuma(address='10.10.10.10', port='7223', token='1fe5588a65e47f40a0717d82206090b9')
```

### Examples
View token bearer information
```
token_owner = kuma.whoami()
```
Search tenants
```
tenant_info = kuma.get_tenant_by_name('My Tenant')
```
Import records in active lists
```
with open('records.csv', 'r') as file:
  data = file.read()
kuma.import_active_list_records(data, correlatorID='2f743382-8313-4f45-a801-979367a0d0a3', activeListID='a0996458-8b25-42e9-a673-d800d6169703', keyField='key')
```
Backup core settings
```
kuma.core_backup('backup.tar.gz')
```
Import assets
```
kuma.import_assets(tenantID='a0996458-8b25-42e9-a673-d800d6169703', assets=assets)
```
Search alerts
```
alerts_list = kuma.get_alerts()
```
