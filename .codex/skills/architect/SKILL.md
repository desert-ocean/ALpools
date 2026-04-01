# Architect

## Purpose

Фиксировать архитектурные решения для Telegram-бота и доменной модели.

## Use When

- меняется структура FSM;
- меняется модель хранения `Project`;
- добавляются новые кросс-секционные flow;
- меняется mapping между ответами пользователя и итоговым ТЗ;
- нужно вынести устойчивый контракт или границу между слоями.

## Inputs

- код `app/`;
- текущие handlers, services, models;
- документы ТЗ;
- dossier;
- role `Analyst` outputs.

## Workflow

1. Определи boundary между UI, domain logic и persistence.
2. Выдели invariants, которые нельзя сломать.
3. Определи целевую структуру модулей и данных.
4. Зафиксируй решение и компромиссы.
5. Подготовь handoff в implementation.

## Outputs

- `architect.md`;
- decision log;
- список структурных требований к реализации.
