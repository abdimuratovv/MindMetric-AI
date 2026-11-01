"""Bilingual open tasks. Student briefs and teacher solutions render separately."""
from authoring import b


def activity(key, title, goal, materials, contract, steps, deliverables, rubric, solution):
    return {'key': key, 'assessment': 'human_or_self_review', 'title': b(title), 'goal': b(goal),
            **{name: [b(p) for p in value] for name, value in (
                ('materials', materials), ('contract', contract), ('steps', steps),
                ('deliverables', deliverables), ('rubric', rubric), ('solution', solution))}}


def build():
    return [
        activity('debugging-challenge', 'Uch bosqichli debugging challenge || Трёхэтапная задача по отладке',
            'Xatoni tasodifiy tahrir bilan emas, kuzatuv, gipoteza va regressiya bilan tuzatish. || Исправить ошибку наблюдением, гипотезой и регрессией вместо случайных правок.', [
                'Python 3, matn muharriri; debugging-starter.py.txt dan mahalliy exercise.py nusxasi. Original o‘zgarmasin. || Python 3, текстовый редактор; локальная копия exercise.py из debugging-starter.py.txt. Оригинал не менять.',
                'Jurnal ustunlari: bosqich, kirish, kutilgan, haqiqiy, xato turi, gipoteza, bitta tahrir, qayta test, xulosa. || Столбцы журнала: этап, вход, ожидание, факт, вид ошибки, гипотеза, одна правка, повторный тест, вывод.'
            ], [
                '1-bosqich add(a, b) ikki son yig‘indisini qaytaradi. Tekshirish kirishlari: (2, 5), (-3, 3), (0, 0). || Этап 1: add(a, b) возвращает сумму двух чисел. Входы проверки: (2, 5), (-3, 3), (0, 0).',
                '2-bosqich discount(price, percent): price >= 0; 0 <= percent <= 100. Foiz chegirilgan narx. Kirishlar: (200, 15), (200, 0), (200, 100), (0, 25). Shu cheklovdan tashqari validatsiya bu vazifaga kirmaydi. || Этап 2: discount(price, percent): price >= 0; 0 <= percent <= 100. Цена после процентной скидки. Входы: (200, 15), (200, 0), (200, 100), (0, 25). Валидация за этими пределами не входит в задачу.',
                '3-bosqich can_borrow(available): available manfiy bo‘lmagan butun. Kamida bitta nusxa bo‘lsa True. Kirishlar: 0, 1, 2. || Этап 3: can_borrow(available): available — неотрицательное целое. True, если есть хотя бы один экземпляр. Входы: 0, 1, 2.'
            ], [
                'Avval starterdagi sintaksis xatosini kuzating. 1-bosqich sababini yozing, bitta tahrir qiling va uning testlarini ishga tushiring. || Сначала наблюдайте синтаксическую ошибку стартового кода. Запишите причину этапа 1, сделайте одну правку и запустите его тесты.',
                '2-bosqichda kutilgan narxni qo‘lda hisoblang. Haqiqiy natija bilan farqini yozib, amallarni izlang. || На этапе 2 вычислите ожидаемую цену вручную. Запишите расхождение с фактом и проследите операции.',
                '3-bosqichda 0, 1, 2 chegaralarini tekshiring. Har tuzatishdan keyin avvalgi bosqich testlarini ham qaytaring. || На этапе 3 проверьте границы 0, 1, 2. После каждой правки повторите и тесты прежних этапов.',
                'Birinchi mashqda 1-bosqich ishorasi: funksiya sarlavhasini ko‘ring. 2-bosqichda faqat kutilgan/haqiqiy jadval beriladi. 3-bosqichda ishora berilmaydi. || В первой попытке подсказка этапа 1: проверьте заголовок функции. На этапе 2 дана только таблица ожидания/факта. На этапе 3 подсказки нет.',
                'Test yana yiqilsa, ayni taxminni ko‘r-ko‘rona takrorlamang: yangi kuzatuv va yangi gipoteza yozing. Zarur bo‘lsa tanaffus qiling yoki aniq savol bilan yordam so‘rang. || Если тест снова не прошёл, не повторяйте слепо ту же догадку: запишите новое наблюдение и гипотезу. При необходимости сделайте перерыв или задайте конкретный вопрос.'
            ], [
                'Tuzatilgan exercise.py; to‘ldirilgan jurnal; test natijalari; qaysi tuzatish nega kerakligini tushuntiruvchi qisqa qayd. || Исправленный exercise.py; заполненный журнал; результаты тестов; краткое объяснение необходимости каждой правки.'
            ], [
                'Sabab va dalil: 0 — yo‘q; 1 — qisman; 2 — uch bosqich uchun xato turi va aniq kuzatuv bor. || Причина и факт: 0 — нет; 1 — частично; 2 — для трёх этапов есть вид ошибки и конкретное наблюдение.',
                'Tuzatish: 0 — talab buzilgan; 1 — faqat oddiy holat; 2 — barcha berilgan kirishlar va cheklovlarda mos. || Исправление: 0 — требование нарушено; 1 — только обычный случай; 2 — соответствует всем заданным входам и ограничениям.',
                'Regressiya: 0 — qayta test yo‘q; 1 — ayrim holatlar; 2 — oldingi bosqichlar ham qayta tekshirilgan. || Регрессия: 0 — нет повторных тестов; 1 — отдельные случаи; 2 — повторно проверены и прежние этапы.',
                'Jarayon qaydi: 0 — yo‘q; 1 — tahrirlar bor, sabab yo‘q; 2 — gipoteza, tahrir va natija ajratilgan. Jami 8 gacha — ish dalili, sabr yoki shaxs tashxisi emas. || Запись процесса: 0 — нет; 1 — есть правки без причины; 2 — отделены гипотеза, правка и результат. До 8 баллов — подтверждение работы, а не диагностика терпения или личности.'
            ], [
                '1-bosqich: def add(a, b): sarlavhasida : zarur. Natijalar 7, 0, 0. || Этап 1: в заголовке def add(a, b): нужно :. Результаты 7, 0, 0.',
                '2-bosqich: price - price * percent / 100. Natijalar 170, 200, 0, 0. Qo‘shish narxni oshirgan. || Этап 2: price - price * percent / 100. Результаты 170, 200, 0, 0. Сложение увеличивало цену.',
                '3-bosqich: available > 0. Natijalar False, True, True. >= bo‘sh omborga ham ruxsat bergan. || Этап 3: available > 0. Результаты False, True, True. >= разрешало выдачу и при пустом запасе.',
                'debugging_reference.py — o‘qituvchi namunasi. Uni o‘quvchi ishga kirishishidan oldin ochmang. Qayta urinishda savol turi yoki asosiy shartnomani yashirin o‘zgartirmang. || debugging_reference.py — образец преподавателя. Не открывайте его до самостоятельной попытки. При повторе не меняйте незаметно тип вопроса или основной контракт.'
            ]),
        activity('team-library', 'Kutubxona uchun jamoaviy miniloyiha || Командный мини-проект библиотеки',
            '2–3 kishilik guruhda modul shartnomasi, Git, review va integratsiyani amalda qo‘llash. || Применить контракт модулей, Git, ревью и интеграцию в группе из 2–3 человек.', [
                'Python 3, Git va alohida yangi lokal repozitoriy; haqiqiy talaba yoki kitobxon ma’lumotlari kerak emas. Remote ixtiyoriy. || Python 3, Git и отдельный новый локальный репозиторий; реальные данные учащихся и читателей не нужны. Remote необязателен.',
                'Boshlang‘ich catalog = {"b1": {"title": "Algorithms", "total": 1, "available": 1}}; loans = {}. loans kaliti (reader, book_id), qiymati musbat butun miqdor. || Начальный catalog = {"b1": {"title": "Algorithms", "total": 1, "available": 1}}; loans = {}. Ключ loans — (reader, book_id), значение — положительное целое количество.'
            ], [
                'find_book(catalog, book_id) yangi dict yoki None qaytaradi; asl catalog o‘zgarmaydi. borrow(catalog, loans, reader, book_id): ok, not_found yoki unavailable. return_book shu parametrlar bilan: ok, not_found yoki no_loan. || find_book(catalog, book_id) возвращает новый dict или None; исходный catalog не меняется. borrow(catalog, loans, reader, book_id): ok, not_found или unavailable. return_book с теми же параметрами: ok, not_found или no_loan.',
                'Old shart: reader va book_id bo‘sh bo‘lmagan matn; catalog izchil, total va available manfiy bo‘lmagan butun; available <= total; mavjud qarzlar hisobga mos. Paralellik, saqlash bazasi va autentifikatsiya bu mashqqa kirmaydi. || Предусловия: reader и book_id — непустой текст; catalog согласован, total и available — неотрицательные целые; available <= total; текущие займы согласованы с учётом. Параллельность, база хранения и аутентификация не входят в упражнение.',
                'Muvaffaqiyatli berish available ni 1 kamaytiradi va qarzni 1 oshiradi. Qaytarish faqat shu reader qarzi bo‘lsa bajariladi. Rad holatida catalog va loans o‘zgarmaydi; nol qarz kaliti o‘chiriladi. || Успешная выдача уменьшает available на 1 и увеличивает долг на 1. Возврат выполняется только при долге этого reader. При отказе catalog и loans не меняются; ключ нулевого долга удаляется.',
                'Har kitob uchun available + barcha reader qarzlari yig‘indisi = total. Shu invariant har muvaffaqiyatli amaldan keyin saqlansin. || Для каждой книги available + сумма долгов всех reader = total. Инвариант сохраняется после каждой успешной операции.'
            ], [
                'Rollar: katalog va interfeys; berish/qaytarish; integratsiya/test. 2 kishi bo‘lsa integratsiya birga. Driver/navigator rolini almashing, har a’zo boshqa modulni ham review qilsin. || Роли: каталог и интерфейс; выдача/возврат; интеграция/тесты. При 2 участниках интеграция общая. Меняйте драйвера/навигатора, каждый делает ревью другого модуля.',
                'CONTRACT.md da imzo, qaytish kodi va rad holatini yozing. Har vazifa uchun mas’ul va qabul testini belgilang. Avval shartnomaga mos kichik stub bilan bog‘lanishni tekshiring. || В CONTRACT.md запишите сигнатуры, коды ответа и отказы. Для каждой задачи назначьте ответственного и приёмочный тест. Сначала проверьте соединение небольшими заглушками по контракту.',
                'Alohida branchlar va kichik commitlarda ishlang. git status, git diff va git diff --staged ni ko‘ring. Birlashtirishdan oldin hamkor reviewsi va test bo‘lsin. || Работайте в отдельных ветках и небольших коммитах. Просматривайте git status, git diff и git diff --staged. До слияния нужны ревью коллеги и тест.',
                'Konflikt simulyatsiyasi: toza bazada POLICY.md ga display_limit=2 yozib commit qiling. review-a va review-b ayni bazadan chiqsin. Birida 3, boshqasida 5 qiling. main ga birini, keyin ikkinchisini merge qiling; konfliktni yakuniy kelishuv display_limit=4 bilan hal qiling. Bu ko‘rsatish limiti, qarz olish cheklovi emas. || Симуляция конфликта: в чистой базе запишите display_limit=2 в POLICY.md и закоммитьте. review-a и review-b создайте от одной базы. В одной замените на 3, в другой на 5. Слейте в main сначала одну, затем другую; разрешите конфликт по итоговому соглашению display_limit=4. Это лимит отображения, а не ограничение выдачи.',
                'Umumiy oqim: b1 topish → r1 ga berish → r2 ga takror berishni rad qilish → r1 qaytarishi → r2 ga berish. Yo‘q kitob va qarzsiz qaytarishni ham sinang. || Общий поток: найти b1 → выдать r1 → отклонить повторную выдачу r2 → возврат r1 → выдать r2. Проверьте также отсутствующую книгу и возврат без долга.',
                'Har a’zo o‘z modulini, boshqa modulga bog‘lanishini, bitta xato holatini va bitta review qarorini tushuntirsin. || Каждый объясняет свой модуль, связь с другим, один ошибочный случай и одно решение ревью.'
            ], [
                'Kod; CONTRACT.md; vazifalar/rollar jadvali; kichik Git log va diff dalillari; konflikt yechimi qaydi; umumiy test natijalari; qisqa himoya. Commitlar soni bo‘yicha a’zolarni reyting qilmang. || Код; CONTRACT.md; таблица задач/ролей; небольшой Git log и подтверждение diff; запись решения конфликта; результаты общих тестов; краткая защита. Не ранжируйте участников по числу коммитов.'
            ], [
                'Shartnoma: 0 — yo‘q; 1 — qisman; 2 — imzo, holat kodi va old shartlar mos. || Контракт: 0 — нет; 1 — частично; 2 — согласованы сигнатуры, коды и предусловия.',
                'Integratsiya: 0 — umumiy oqim yo‘q; 1 — faqat oddiy yo‘l; 2 — umumiy yo‘l, rad holati va invariant tekshirilgan. || Интеграция: 0 — общего потока нет; 1 — только обычный путь; 2 — проверены общий путь, отказ и инвариант.',
                'Hamkorlik dalili: 0 — yo‘q; 1 — ish bo‘lingan, review yo‘q; 2 — rol almashish va dalilli o‘zaro review bor. || Подтверждение сотрудничества: 0 — нет; 1 — задачи разделены без ревью; 2 — есть смена ролей и обоснованное взаимное ревью.',
                'Git va himoya: 0 — iz yo‘q; 1 — commit yoki tushuntirish yetishmaydi; 2 — mazmunli diff, konflikt sababi va har a’zoning tushuntirishi bor. Jami 8 gacha — loyiha rubrikasi. || Git и защита: 0 — следов нет; 1 — не хватает коммита или объяснения; 2 — есть содержательный diff, причина конфликта и объяснение каждого. До 8 баллов — рубрика проекта.'
            ], [
                'library_reference.py ishlaydigan o‘qituvchi namunasi; u real ko‘p foydalanuvchili tizim arxitekturasi sifatida berilmaydi. || library_reference.py — работающий образец преподавателя; это не архитектура реальной многопользовательской системы.',
                'b1/r1 berish: ok, available=0, loans[("r1", "b1")]=1. r2 so‘rovi unavailable va ikkala holat o‘zgarmaydi. r1 qaytarishi ok, available=1, qarz kaliti o‘chadi. So‘ng r2 berish ok. || Выдача b1/r1: ok, available=0, loans[("r1", "b1")]=1. Запрос r2 — unavailable, оба состояния неизменны. Возврат r1 — ok, available=1, ключ долга удаляется. Затем выдача r2 — ok.',
                'Yo‘q kitobda not_found; o‘z qarzi yo‘q reader qaytarsa no_loan. Ikki holatda holat aynan saqlanadi. find_book natijasini tahrirlash asl katalogni o‘zgartirmasligi tekshiriladi. || Для отсутствующей книги — not_found; возврат reader без своего долга — no_loan. В обоих случаях состояние сохраняется точно. Проверяется, что правка результата find_book не меняет исходный каталог.',
                'Konfliktning yakuni display_limit=4. Nega 3 yoki 5 emasligi kelishuvga asoslanib yoziladi. Merge muvaffaqiyati umumiy test o‘rnini bosmasligi himoyada so‘ralsin. || Итог конфликта — display_limit=4. Почему не 3 или 5, объясняется соглашением. На защите уточните, почему успех merge не заменяет общий тест.'
            ]),
        activity('documentation-lab', 'Hujjatdan yangi API ni o‘rganish || Освоение нового API по документации',
            'Berilgan kichik hujjatdan qoida topib, yangi vaziyatda mustaqil qo‘llash. || Найти правило в небольшой документации и самостоятельно применить в новом случае.', [
                'Python 3 va lab_studytools.py; internet shart emas. StudyTools 1.0 — ushbu kursning mualliflik API si; pip bilan o‘rnatilmaydi. || Python 3 и lab_studytools.py; интернет не обязателен. StudyTools 1.0 — авторский API курса; через pip не устанавливается.',
                'Import: from lab_studytools import take, find, clip. Quyidagi hujjat asosiy manba. || Импорт: from lab_studytools import take, find, clip. Основной источник — документация ниже.'
            ], [
                'take(items, limit=2): items ro‘yxat; dastlabki ko‘pi bilan limit elementdan yangi sayoz ro‘yxat qaytadi. Elementlar o‘zi chuqur nusxalanmaydi. items o‘zgarmaydi. limit >= 0 butun, bool emas; manfiyga ValueError, boshqa turga TypeError. || take(items, limit=2): items — список; возвращает новый поверхностный список первых не более limit элементов. Сами элементы глубоко не копируются. items не меняется. limit — целое >= 0, не bool; отрицательное даёт ValueError, другой тип — TypeError.',
                'find(items, target, default=None): items ro‘yxat; == bo‘yicha birinchi mos elementning noldan indeksini qaytaradi. Moslik yo‘q bo‘lsa default. Kirish o‘zgarmaydi. || find(items, target, default=None): items — список; возвращает индекс первого совпадения по == с нуля. Если совпадения нет, default. Вход не меняется.',
                'clip(x, low=0, high=10): bu laboratoriyada faqat chekli int/float sonlar beriladi; low <= high. Oraliq yopiq; pastda low, yuqorida high, ichkarida x qaytadi. low > high — ValueError. Kirish o‘zgarmaydi. || clip(x, low=0, high=10): в этой лаборатории передаются только конечные int/float; low <= high. Интервал замкнут; ниже возвращает low, выше high, внутри x. low > high — ValueError. Вход не меняется.',
                'Versiya taqqoslash kartasi: faqat simulyatsiyadagi 2.0 take(items, *, count=2) nomli count talab qiladi. Lokal kod faqat 1.0 ni bajaradi. || Карточка сравнения версий: только в симуляции 2.0 take(items, *, count=2) требует именованный count. Локальный код выполняет только 1.0.'
            ], [
                'Dastlab ishga tushirmasdan natijani taxmin qiling: take([7, 8, 9]); take([7], limit=3); find([4, 4, 9], 4); find([], 2, default=-1); clip(15, low=3, high=12). || Сначала предскажите без запуска: take([7, 8, 9]); take([7], limit=3); find([4, 4, 9], 4); find([], 2, default=-1); clip(15, low=3, high=12).',
                'Keyin bitta chaqiruvni ishga tushirib, bashorat bilan solishtiring. Qaysi hujjat jumlasi javobni berganini belgilang. || Затем выполните по одному вызову и сравните с прогнозом. Отметьте предложение документации, из которого следует ответ.',
                'Xato holatlarini oldindan nomlang va sinang: take([1], limit=-1); take([1], limit=True); clip(5, low=8, high=2). Har biri uchun sababni yozing. || Заранее назовите и проверьте ошибки: take([1], limit=-1); take([1], limit=True); clip(5, low=8, high=2). Для каждого запишите причину.',
                'Yangi vaziyat: tasks=["A", "B", "C", "D"]. Dastlabki 3 topshiriqni ko‘rsating; "A" topilganini indeks 0 bo‘lsa ham to‘g‘ri aniqlang; 14 ballni [0, 10] ga cheklang. || Новый случай: tasks=["A", "B", "C", "D"]. Покажите первые 3 задания; корректно определите наличие "A", даже при индексе 0; ограничьте 14 баллов интервалом [0, 10].',
                'Rasmiy hujjat mashqi: Python str.split bo‘limini oching. sep va maxsplit ma’nosini o‘qing. Python 3 da "a,b,c".split(",", maxsplit=1) uchun natijani avval yozib, keyin tekshiring. Internet bo‘lmasa help(str.split)dan foydalaning. || Упражнение с официальной документацией: откройте раздел Python str.split. Прочитайте смысл sep и maxsplit. В Python 3 для "a,b,c".split(",", maxsplit=1) сначала запишите прогноз, затем проверьте. Без интернета используйте help(str.split).',
                'Savol, versiya, imzo, ishlagan misol, xato/chegara va manbadan iborat bilim qaydi yozing. Vaqtni ixtiyoriy o‘zingiz uchun qayd etishingiz mumkin; aniqlik birinchi o‘rinda. || Запишите заметку: вопрос, версия, сигнатура, рабочий пример, ошибка/граница и источник. При желании запишите время для себя; точность важнее.'
            ], [
                'Bashorat/haqiqiy natija jadvali; kichik lab_solution.py; xatolar sababi; yangi vaziyat yechimi; str.split qaydi va bilim kartasi. || Таблица прогноза/факта; небольшой lab_solution.py; причины ошибок; решение нового случая; запись str.split и карточка знания.'
            ], [
                'Hujjatdan dalil: 0 — taxmin; 1 — ayrim javoblar; 2 — har javob shartnomaga bog‘langan. || Подтверждение документацией: 0 — догадка; 1 — отдельные ответы; 2 — каждый ответ связан с контрактом.',
                'Aniqlik: 0 — asosiy natijalar noto‘g‘ri; 1 — qisman; 2 — berilgan natijalar va istisnolar to‘g‘ri. || Точность: 0 — основные результаты неверны; 1 — частично; 2 — заданные результаты и исключения верны.',
                'Ko‘chirish: 0 — faqat ko‘chirilgan misol; 1 — yangi vaziyatning bir qismi; 2 — topshiriq, indeks 0 va ball chegarasi to‘g‘ri. || Перенос: 0 — лишь скопирован пример; 1 — часть нового случая; 2 — задания, индекс 0 и граница баллов верны.',
                'Qayd: 0 — yo‘q; 1 — versiya yoki cheklov yetishmaydi; 2 — qayta foydalanishga yetarli. Jami 8 gacha — ish rubrikasi, umumiy o‘rganish tezligi bahosi emas. || Заметка: 0 — нет; 1 — не хватает версии или ограничения; 2 — достаточно для повторного применения. До 8 баллов — рубрика работы, а не оценка общей скорости обучения.'
            ], [
                'Asosiy natijalar: [7, 8]; [7]; 0; -1; 12. Xatolar: ValueError, TypeError, ValueError. || Основные результаты: [7, 8]; [7]; 0; -1; 12. Ошибки: ValueError, TypeError, ValueError.',
                'Ko‘chirish: take(tasks, limit=3) → ["A", "B", "C"]; idx=find(tasks, "A"), idx is not None → True; clip(14) → 10. || Перенос: take(tasks, limit=3) → ["A", "B", "C"]; idx=find(tasks, "A"), idx is not None → True; clip(14) → 10.',
                'str.split natijasi ["a", "b,c"]. maxsplit=1 ajratishlar sonini cheklaydi, oxirgi bo‘lakda qolgan matn saqlanadi. Manba: https://docs.python.org/3/library/stdtypes.html#str.split. || Результат str.split — ["a", "b,c"]. maxsplit=1 ограничивает число разделений, в последнем фрагменте сохраняется остаток текста. Источник: https://docs.python.org/3/library/stdtypes.html#str.split.',
                'O‘quvchi xulosasida sukut qiymati, limitning ma’nosi, indeks 0 va topilmadi belgisi farqlanishini tekshiring. Lokal kod 2.0 API si deb taqdim etilmasin. || Проверьте, различает ли учащийся значение по умолчанию, смысл лимита, индекс 0 и признак отсутствия. Локальный код нельзя представлять как API 2.0.'
            ])
    ]


def render(item, language, teacher=False):
    labels = {'uz': ('Maqsad', 'Vositalar', 'Shartnoma', 'Bosqichlar', 'Topshiriladigan ish', 'Rubrika', 'O‘qituvchi yechimi'),
              'ru': ('Цель', 'Материалы', 'Контракт', 'Этапы', 'Результат работы', 'Рубрика', 'Решение преподавателя')}
    lines = ['# ' + item['title'][language], '',
             ('O‘qituvchi nusxasi — yechimlar mavjud' if language == 'uz' else 'Копия преподавателя — с решениями') if teacher else
             ('O‘quvchi ish varag‘i' if language == 'uz' else 'Рабочий лист учащегося'), '', '[README](README.md)', '']
    lines += ['## ' + labels[language][0], '', item['goal'][language], '']
    fields = ['materials', 'contract', 'steps', 'deliverables', 'rubric'] + (['solution'] if teacher else [])
    for field, title in zip(fields, labels[language][1:]):
        lines += ['## ' + title, '']
        for index, row in enumerate(item[field]):
            prefix = f'{index + 1}. ' if field == 'steps' else '- '
            lines += [prefix + row[language], '']
    if not teacher:
        lines += ['## ' + ('Ish qaydi' if language == 'uz' else 'Запись работы'), '',
                  '| ' + ('Kirish | Kutilgan | Haqiqiy | Gipoteza / qaror | Qayta test |' if language == 'uz' else
                          'Вход | Ожидание | Факт | Гипотеза / решение | Повторный тест |'),
                  '|---|---|---|---|---|', '| | | | | |', '| | | | | |', '| | | | | |', '']
    return '\n'.join(lines).rstrip() + '\n'
