# Domain Modeler

## Purpose

Формализовать домен проектирования бассейнов в структуру опросника, данных и итогового ТЗ.

## Use When

- добавляются новые поля анкеты;
- меняется структура шагов конфигуратора;
- нужно перенести пункты из `tz_bass.docx` в продуктовую модель;
- нужно определить словари значений, labels, required fields, optional fields;
- нужно отделить инженерные факты от маркетингового текста.

## Inputs

- `documents/tz_bass.docx`;
- `app/config/cost_steps.py`;
- `app/services/tz_formatter.py`;
- `app/handlers/project_configurator.py`;
- task dossier.

## Workflow

1. Прочитай релевантный раздел ТЗ.
2. Раздели все поля на логические группы.
3. Определи для каждого поля source, обязательность, тип значения, human label и влияние на расчет/ТЗ.
4. Зафиксируй mapping.
5. Подготовь handoff в `Architect` или `Backend Bot Engineer`.

## Outputs

- domain field mapping;
- предложение по шагам опросника;
- список новых/измененных полей и labels.
