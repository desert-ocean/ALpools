from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectCatalogItem:
    id: str
    title: str
    city: str
    size: str
    type: str
    description: str
    photos: tuple[str, ...]


PROJECTS: tuple[ProjectCatalogItem, ...] = (
    ProjectCatalogItem(
        id="villa_moscow_01",
        title="Частный переливной бассейн с лаунж-зоной",
        city="Москва",
        size="12 x 4 м",
        type="Переливной, частный, внутренний",
        description="Компактный семейный бассейн с технической зоной в смежном помещении и подводным освещением.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="resort_sochi_02",
        title="Открытый бассейн для загородного отеля",
        city="Сочи",
        size="20 x 6 м",
        type="Скиммерный, общественный, наружный",
        description="Проект для курортного комплекса с акцентом на сезонную эксплуатацию и быстрый сервис оборудования.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="spa_kazan_03",
        title="SPA-бассейн с гидромассажем",
        city="Казань",
        size="8 x 3 м",
        type="Переливной, частный, внутренний",
        description="Небольшой wellness-проект с гидромассажной зоной и повышенными требованиями к акустике помещения.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="school_tver_04",
        title="Учебный бассейн при школе",
        city="Тверь",
        size="16 x 8 м",
        type="Переливной, общественный, внутренний",
        description="Учебная чаша с разделением потоков посетителей, режимом интенсивной фильтрации и безопасной логистикой.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="club_msk_05",
        title="Бассейн фитнес-клуба бизнес-класса",
        city="Москва",
        size="25 x 10 м",
        type="Переливной, общественный, внутренний",
        description="Классическая спортивно-рекреационная чаша с отдельной зоной аттракционов и инженерным резервом.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="villa_spb_06",
        title="Семейный бассейн в частном доме",
        city="Санкт-Петербург",
        size="10 x 3.5 м",
        type="Скиммерный, частный, внутренний",
        description="Минималистичный проект для частного интерьера с тёплой чашей и спокойной подсветкой.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="hotel_anapa_07",
        title="Гостиничный открытый бассейн",
        city="Анапа",
        size="18 x 7 м",
        type="Скиммерный, общественный, наружный",
        description="Открытая чаша для сезонного потока гостей с простым техобслуживанием и устойчивой инженерной схемой.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="medical_perm_08",
        title="Реабилитационный бассейн",
        city="Пермь",
        size="14 x 5 м",
        type="Переливной, общественный, внутренний",
        description="Проект с мягкими режимами водообмена, удобными закладными элементами и адаптацией под медперсонал.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="country_tula_09",
        title="Частный уличный бассейн у террасы",
        city="Тула",
        size="11 x 4 м",
        type="Скиммерный, частный, наружный",
        description="Наружный бассейн для загородного участка с роллетным покрытием и удобным обходом вокруг чаши.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="aqua_ufa_10",
        title="Детский бассейн в аква-зоне",
        city="Уфа",
        size="9 x 5 м",
        type="Переливной, общественный, внутренний",
        description="Неглубокая детская чаша с усиленным контролем качества воды и сценариями безопасной эксплуатации.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="sport_ekb_11",
        title="Тренировочный бассейн спортивного центра",
        city="Екатеринбург",
        size="25 x 8 м",
        type="Переливной, общественный, внутренний",
        description="Инженерно насыщенный объект для тренировочного процесса с акцентом на надёжность и сервисный доступ.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="villa_krasnodar_12",
        title="Бассейн с панорамным остеклением",
        city="Краснодар",
        size="13 x 4 м",
        type="Переливной, частный, внутренний",
        description="Частный проект в доме с панорамными окнами, где важны влажностный режим и визуальная чистота деталей.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="residence_samara_13",
        title="Бассейн в премиальном ЖК",
        city="Самара",
        size="15 x 6 м",
        type="Переливной, общественный, внутренний",
        description="Объект для residents-only формата с аккуратной интеграцией в общественную SPA-инфраструктуру.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="cottage_ryazan_14",
        title="Компактный бассейн для дачи",
        city="Рязань",
        size="7 x 3 м",
        type="Скиммерный, частный, наружный",
        description="Небольшой наружный проект с оптимизированным бюджетом, но без компромисса по базовой инженерии.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="wellness_vrn_15",
        title="Термальная чаша wellness-комплекса",
        city="Воронеж",
        size="10 x 4 м",
        type="Переливной, общественный, внутренний",
        description="Wellness-формат с тёплой водой, продуманной обвязкой оборудования и расширенным сценарным освещением.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="hotel_tyumen_16",
        title="Бассейн при спа-отеле",
        city="Тюмень",
        size="17 x 6 м",
        type="Переливной, общественный, внутренний",
        description="Проект для гостиницы с комбинированным режимом отдыха и спокойным архитектурным сценарием.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="private_kaluga_17",
        title="Частный бассейн с противотоком",
        city="Калуга",
        size="9 x 3 м",
        type="Скиммерный, частный, внутренний",
        description="Частный бассейн с противотоком и закладными элементами для индивидуального домашнего использования.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="club_omsk_18",
        title="Рекреационный бассейн в клубе",
        city="Омск",
        size="14 x 5 м",
        type="Скиммерный, общественный, внутренний",
        description="Рекреационная чаша с равномерной циркуляцией воды и удобным сценарием регулярного обслуживания.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="estate_pskov_19",
        title="Уличный бассейн у гостевого дома",
        city="Псков",
        size="12 x 4.5 м",
        type="Скиммерный, частный, наружный",
        description="Наружный бассейн для гостевого дома с упором на эксплуатационную устойчивость и простую консервацию.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="school_kursk_20",
        title="Малый учебный бассейн",
        city="Курск",
        size="12 x 6 м",
        type="Переливной, общественный, внутренний",
        description="Проект для детско-юношеских программ с адаптацией под учебный режим и удобную работу персонала.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="spa_belgorod_21",
        title="Релакс-бассейн для spa-центра",
        city="Белгород",
        size="11 x 4 м",
        type="Переливной, общественный, внутренний",
        description="Релакс-формат с мягким светом, тихой работой инженерии и акцентом на архитектурное восприятие.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="villa_yalta_22",
        title="Террасный бассейн с видом на участок",
        city="Ялта",
        size="15 x 4 м",
        type="Переливной, частный, наружный",
        description="Открытая чаша на террасном участке с повышенным вниманием к гидравлике и распределению оборудования.",
        photos=(),
    ),
    ProjectCatalogItem(
        id="resort_altai_23",
        title="Бассейн для загородного ретрита",
        city="Горно-Алтайск",
        size="16 x 5 м",
        type="Скиммерный, общественный, наружный",
        description="Наружный бассейн для ретрит-комплекса с лаконичной архитектурой и понятной эксплуатационной моделью.",
        photos=(),
    ),
)


def get_projects() -> tuple[ProjectCatalogItem, ...]:
    return PROJECTS


def get_project_by_id(project_id: str) -> ProjectCatalogItem | None:
    for project in PROJECTS:
        if project.id == project_id:
            return project
    return None
