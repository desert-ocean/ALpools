# Backend Bot Engineer

## Purpose

Реализовывать продуктовые и технические изменения в Telegram-боте `ALpools`.

## Use When

- меняются handlers;
- меняются FSM states;
- меняются services;
- меняются DB models;
- меняется отправка заявок администратору;
- меняется pricing flow;
- меняется формат итогового сообщения/ТЗ.

## Inputs

- task card;
- dossier;
- outputs Analyst/Architect/Domain Modeler;
- код `app/`.

## Workflow

1. Подтверди target behavior по dossier.
2. Найди write scope.
3. Реализуй изменение минимальным coherent slice.
4. Добавь или обнови явный mapping/config, если меняются смыслы.
5. Проведи локальную проверку.
6. Заполни `implementation.md`.

## Outputs

- код;
- `implementation.md`;
- test notes;
- handoff в QA.
