from authoring import choice as c, lesson as l, module, numeric as n, q


def build():
    return module('documentation-learning', 4, 'Hujjatlar asosida yangi bilimni o‘zlashtirish || Освоение нового по документации', [
        l('learn-locate', 'Savol va kerakli bo‘limni topish || Вопрос и поиск нужного раздела',
          'O‘rganish maqsadini savolga aylantirib, mos versiyadagi rasmiy bo‘limni topasiz. || Превращаете цель обучения в вопрос и находите официальный раздел нужной версии.', [
            'Avval kichik amaliy savol yozing: “ro‘yxatdan ko‘pi bilan 3 elementni qanday olaman?” Keyin vosita nomi, versiyasi va muhitini belgilang. Butun qo‘llanmani boshidan oxirigacha o‘qish har vazifa uchun shart emas. || Сначала запишите небольшой практический вопрос: «как взять не больше 3 элементов списка?» Затем определите средство, версию и окружение. Не для каждой задачи нужно читать руководство целиком.',
            'Rasmiy hujjatning qidiruvi yoki mundarijasidan imzo va misolni toping. Natija turi, cheklovlar va versiya eslatmasini ham o‘qing. Tasodifiy forum parchasi ayni versiyaga tegishli bo‘lmasligi mumkin. || Найдите сигнатуру и пример через поиск или оглавление официальной документации. Прочитайте также тип результата, ограничения и сведения о версии. Случайный фрагмент форума может относиться к другой версии.',
            'Bu moduldagi StudyTools 1.0 — mualliflik o‘quv API, o‘rnatiladigan ommaviy paket emas. Uning hujjati topshiriqlarda beriladi; kodni mahalliy laboratoriya faylidan import qilish mumkin. O‘qish tezligi shaxsiy qobiliyat tashxisi sifatida baholanmaydi. || StudyTools 1.0 в этом модуле — авторский учебный API, а не публичный устанавливаемый пакет. Документация дана в заданиях; код можно импортировать из локального лабораторного файла. Скорость чтения не оценивается как диагноз способностей.'
          ], 'Vazifa: take funksiyasining limit parametrini topish. O‘quvchi StudyTools 1.0 ishlatyapti; qidiruv StudyTools 2.0 sahifasini ochdi. Nima qilinadi? || Задача: найти параметр limit функции take. Учащийся использует StudyTools 1.0; поиск открыл страницу StudyTools 2.0. Что делать?',
          'Ishlatilayotgan versiyani qayd eting.|1.0 hujjatiga o‘ting.|Imzo, cheklov va misolni shu versiyadan oling. || Зафиксируйте используемую версию.|Перейдите к документации 1.0.|Возьмите сигнатуру, ограничения и пример из этой версии.',
          'Versiya mosligini tekshirib o‘qish. || Читать с проверкой соответствия версии.', [
            q('StudyTools 1.0 da take limitini bilish kerak. Eng yaxshi boshlang‘ich manba? || Нужно узнать limit функции take в StudyTools 1.0. Лучший исходный источник?', [
                c('1.0 uchun berilgan API ma’lumotnomasi || Предоставленный справочник API 1.0', 'Ayni versiya shartnomasi mavjud. || Есть контракт нужной версии.'),
                c('Versiyasiz tasodifiy kod rasmi || Случайная картинка кода без версии', 'Moslik va cheklovlar noma’lum. || Совместимость и ограничения неизвестны.'),
                c('Funksiya nomidan javobni taxmin qilish || Угадать ответ по имени функции', 'Nom parametr semantikasini to‘liq bermaydi. || Имя не задаёт всю семантику параметра.')],
              'Versiyani moslang.|Imzoni rasmiy o‘quv ma’lumotnomasidan oling. || Сопоставьте версию.|Возьмите сигнатуру из официального учебного справочника.',
              'Qidiruvdagi birinchi natija doim mos emas. || Первый результат поиска не всегда подходит.', 'Qaysi versiya ishlatyapsiz? || Какую версию используете?'),
            q('“Kutubxonani o‘rganaman” maqsadini qaysi savol aniqlashtiradi? || Какой вопрос уточняет цель «изучу библиотеку»?', [
                c('take yordamida ro‘yxatdan ko‘pi bilan 3 elementni qanday olaman? || Как с помощью take получить не более 3 элементов списка?', 'Amal va tekshiriladigan natija aniq. || Есть конкретное действие и проверяемый результат.'),
                c('Hammasini yodlab olamanmi? || Выучу ли я всё наизусть?', 'Amaliy vazifa va natija yo‘q. || Нет практической задачи и результата.'),
                c('Barcha funksiyalar nomini bir yo‘la yodlash mumkinmi? || Можно ли сразу запомнить имена всех функций?', 'Bu aniq vazifada qo‘llash natijasini belgilamaydi. || Это не задаёт результат применения в конкретной задаче.')],
              'Vazifa kirishi va natijasini aniqlang.|Savolni bitta kichik amalga qisqartiring. || Уточните вход и результат.|Сведите вопрос к одному небольшому действию.',
              'Yodlashni qo‘llay olish bilan tenglashtirmang. || Не приравнивайте запоминание к применению.', 'Nimani ishlatib ko‘rmoqchisiz? || Что вы хотите применить?'),
            q('Misol topildi, ammo xato holatlari yozilmagan parchada. Keyin nimani qidirasiz? || Пример найден, но в отрывке нет ошибочных случаев. Что искать дальше?', [
                c('To‘liq ma’lumotnomadagi cheklov, istisno va versiya qaydi || Ограничения, исключения и сведения о версии в полном справочнике', 'Bitta misol barcha kirishni qamramaydi. || Один пример не покрывает все входы.'),
                c('Xato hech qachon bo‘lmaydi deb qabul qilish || Считать, что ошибок никогда нет', 'Parchada yo‘qlik kafolat emas. || Отсутствие в отрывке не является гарантией.'),
                c('Faqat yana bitta muvaffaqiyatli misolni || Только ещё один успешный пример', 'U foydali, lekin cheklov va xato holatlarini bermasligi mumkin. || Он полезен, но может не раскрыть ограничения и ошибки.')],
              'Misolni to‘liq shartnoma bilan to‘ldiring.|Cheklovni yozib oling. || Дополните пример полным контрактом.|Запишите ограничение.',
              'Misolni to‘liq spetsifikatsiya deb olmang. || Не считайте пример полной спецификацией.'),
            q('Lokal hujjat 1.0, internet parchasi 2.0. Natijalar zid. To‘g‘ri yo‘l? || Локальная документация 1.0, интернет-фрагмент 2.0. Результаты расходятся. Правильный путь?', [
                c('Amaldagi versiyani aniqlab, ayni versiya shartnomasini tekshirish || Определить используемую версию и проверить её контракт', 'Ziddiyatning versiya sababi tekshiriladi. || Проверяется версия как причина расхождения.'),
                c('Ikki versiya imzosini aralashtirish || Смешать сигнатуры двух версий', 'Bunday API mavjud bo‘lmasligi mumkin. || Такого API может не существовать.'),
                c('Eng yangi sana har doim mos deyish || Считать самую новую дату всегда подходящей', 'Muhit eski versiyada qolishi mumkin. || Среда может использовать старую версию.')],
              'Versiyani taxmin qilmang.|Muhit va hujjatni moslang. || Не угадывайте версию.|Согласуйте среду и документацию.',
              'Yangiroq hujjat eski kodga avtomatik mos emas. || Более новая документация не подходит старому коду автоматически.')]),
        l('learn-signature', 'Imzo, parametr va natija || Сигнатура, параметр и результат',
          'Hujjatdan sukut qiymati, parametr va qaytish turini ajratasiz. || Выделяете значение по умолчанию, параметр и тип результата.', [
            'StudyTools 1.0 hujjati: take(items, limit=2) ro‘yxatning dastlabki ko‘pi bilan limit elementidan yangi ro‘yxat qaytaradi. limit manfiy bo‘lmagan butun son; items o‘zgarmaydi. Sukut qiymati parametr berilmaganda olinadi. || Документация StudyTools 1.0: take(items, limit=2) возвращает новый список из первых не более limit элементов. limit — неотрицательное целое; items не меняется. Значение по умолчанию применяется, если параметр не передан.',
            'Natija turi va soni boshqa tushunchalar. take ro‘yxat qaytaradi; len(take(...)) uning uzunligi. Kirish qisqa bo‘lsa mavjud elementlar qaytadi; take bo‘sh joylarni sun’iy to‘ldirmaydi. || Тип результата и количество — разные понятия. take возвращает список; len(take(...)) — его длину. Если вход короче, возвращаются имеющиеся элементы; take не дополняет список искусственно.',
            'Nomli parametr limit=3 ma’noni ochiq qiladi. Imzoda bo‘lmagan nomni o‘ylab topmang. Alohida ko‘rsatilmagan yon ta’sirni taxmin qilish o‘rniga “items o‘zgarmaydi” kabi aniq shartni tekshiring. || Именованный параметр limit=3 делает смысл явным. Не придумывайте имена, которых нет в сигнатуре. Вместо догадки о побочном эффекте проверяйте явное условие вроде «items не меняется».'
          ], 'StudyTools 1.0: take(items, limit=2) dastlabki elementlardan yangi ro‘yxat qaytaradi. take([8, 4, 9]) natijasi? || StudyTools 1.0: take(items, limit=2) возвращает новый список первых элементов. Результат take([8, 4, 9])?',
          'limit berilmagan, 2 olinadi.|Birinchi ikki element 8 va 4.|Natija yangi [8, 4]. || limit не передан, берётся 2.|Первые два элемента — 8 и 4.|Результат — новый [8, 4].', '[8, 4] || [8, 4]', [
            n('StudyTools 1.0: take(items, limit=2) dastlabki ko‘pi bilan limit elementni oladi. len(take([5, 6, 7, 8])) nechaga teng? || StudyTools 1.0: take(items, limit=2) берёт первые не более limit элементов. Чему равно len(take([5, 6, 7, 8]))?', 2,
              'Sukut limit 2.|Natija uzunligi 2. || limit по умолчанию 2.|Длина результата 2.',
              'Kirish uzunligini natija uzunligi deb olmang. || Не считайте длину входа длиной результата.', 'Parametr berilmaganda imzodagi qiymat olinadi. || Если параметр не передан, используется значение из сигнатуры.'),
            q('Hujjat: take(items, limit=2), kirish o‘zgarmaydi. xs=[3, 8, 1]; take(xs, limit=1)dan keyin xs? || Документация: take(items, limit=2), вход не меняется. xs=[3, 8, 1]; чему равно xs после take(xs, limit=1)?', [
                c('[3, 8, 1] || [3, 8, 1]', 'Yangi ro‘yxat qaytadi, kirish saqlanadi. || Возвращается новый список, вход сохраняется.'),
                c('[3] || [3]', 'Bu qaytgan natija, xsning o‘zi emas. || Это возвращённый результат, а не сам xs.'),
                c('[] || []', 'Hujjat elementlarni o‘chirishni aytmagan. || Документация не говорит об удалении элементов.')],
              'Qaytgan natija va kirishni ajrating.|xs o‘zgarmaydi. || Разделите возвращённый результат и вход.|xs не меняется.',
              'Natija olish doim kirishni o‘zgartirish emas. || Получение результата не всегда означает изменение входа.', 'Hujjat yon ta’sir haqida nima deydi? || Что документация говорит о побочном эффекте?'),
            n('StudyTools 1.0: take(items, limit=2) mavjud dastlabki elementlarni qaytaradi, to‘ldirmaydi. len(take([9], limit=4))? || StudyTools 1.0: take(items, limit=2) возвращает имеющиеся первые элементы, не дополняя. len(take([9], limit=4))?', 1,
              'Kirishda bitta element bor.|Ko‘pi bilan 4, lekin mavjud 1 qaytadi. || Во входе один элемент.|Допускается до 4, но возвращается имеющийся 1.',
              'Limitni majburiy natija uzunligi deb bilmang. || Не считайте лимит обязательной длиной результата.'),
            q('Hujjat: take(items, limit=2) yangi ro‘yxat qaytaradi. Qaysi chaqiruv 3 tagacha oladi? || Документация: take(items, limit=2) возвращает новый список. Какой вызов берёт до 3 элементов?', [
                c('take(xs, limit=3) || take(xs, limit=3)', 'Imzodagi haqiqiy parametr berildi. || Передан настоящий параметр сигнатуры.'),
                c('take(xs, size=3) || take(xs, size=3)', 'size bu imzoda yo‘q. || size отсутствует в этой сигнатуре.'),
                c('take(xs) || take(xs)', 'Sukut qiymati 2. || Значение по умолчанию 2.')],
              'Imzodagi limit nomini oling.|Unga 3 bering. || Возьмите имя limit из сигнатуры.|Передайте ему 3.',
              'Parametr nomini taxmin qilmang. || Не угадывайте имя параметра.')]),
        l('learn-minimal', 'Minimal ishlaydigan misol || Минимальный работающий пример',
          'Bitta API xatti-harakatini kichik test bilan tekshirasiz. || Проверяете одно поведение API небольшим тестом.', [
            'Eng kichik tajriba bitta savolni tekshiradi: aniq kirish, oldindan yozilgan kutilgan natija, bitta chaqiruv va taqqoslash. Butun ilovaga qo‘shishdan oldin shu tajriba tushunmovchilikni kamaytiradi. || Минимальный эксперимент проверяет один вопрос: точный вход, заранее записанный ожидаемый результат, один вызов и сравнение. До включения в целое приложение он уменьшает непонимание.',
            'StudyTools 1.0: find(items, target, default=None) birinchi mos elementning noldan boshlanuvchi indeksini qaytaradi; topilmasa default. find([6, 9], 6) natijasi 0. Indeksning 0 bo‘lishi topilmadi degani emas. || StudyTools 1.0: find(items, target, default=None) возвращает индекс первого совпадения с нуля; при отсутствии — default. find([6, 9], 6) возвращает 0. Индекс 0 не означает отсутствие.',
            'Mahalliy lab_studytools.py yonida from lab_studytools import find yozib tajriba qiling. Olingan javobni talab bilan solishtiring; xato bo‘lsa birdan butun loyihani qayta yozmang. || Рядом с lab_studytools.py используйте from lab_studytools import find для эксперимента. Сравните ответ с требованием; при ошибке не переписывайте сразу весь проект.'
          ], 'Hujjat: find birinchi moslikning noldan indeksini, topilmasa None qaytaradi. find([4, 7, 4], 4) uchun kutilgan natija? || Документация: find возвращает индекс первого совпадения с нуля, при отсутствии None. Что ожидать для find([4, 7, 4], 4)?',
          'Birinchi 4 ro‘yxat boshida.|Bosh indeks 0.|Ikkinchi moslik emas, birinchi olinadi. || Первая 4 в начале списка.|Начальный индекс 0.|Берётся первое, а не второе совпадение.', '0 || 0', [
            n('StudyTools 1.0: find birinchi moslik indeksini noldan qaytaradi. find([2, 5, 8], 8) natijasi? || StudyTools 1.0: find возвращает индекс первого совпадения с нуля. Результат find([2, 5, 8], 8)?', 2,
              'Indekslar 0, 1, 2.|8 indeks 2 da. || Индексы 0, 1, 2.|8 находится по индексу 2.',
              'Indeks bilan qiymatni almashtirmang. || Не путайте индекс со значением.', 'Birinchi element indeksi 0. || Индекс первого элемента 0.'),
            q('find topilmasa None, topsa indeks qaytaradi. idx=0 bo‘lsa “topildi”ni qanday tekshiramiz? || find возвращает None при отсутствии и индекс при наличии. Как проверить «найдено», если idx=0?', [
                c('idx is not None || idx is not None', '0 ham mavjud indeks sifatida qabul qilinadi. || 0 тоже принимается как существующий индекс.'),
                c('bool(idx) || bool(idx)', 'bool(0) False, mavjud element yo‘q deb olinadi. || bool(0) равно False, найденный элемент будет отвергнут.'),
                c('idx > 0 || idx > 0', 'Birinchi element chiqarib tashlanadi. || Первый элемент исключается.')],
              'Topilmadi belgisi None.|0 ni undan ajrating. || Признак отсутствия — None.|Отличайте от него 0.',
              'Yolg‘on qiymat va topilmadi holati bir xil emas. || Ложное значение и отсутствие — не одно и то же.', 'Shartnomada topilmadi qanday ifodalangan? || Как контракт обозначает отсутствие?'),
            q('Yangi API ni birinchi marta sinashda eng foydali tajriba? || Самый полезный первый эксперимент с новым API?', [
                c('Kichik kirish, bitta chaqiruv, oldindan hisoblangan natija bilan tekshiruv || Маленький вход, один вызов и проверка заранее вычисленного результата', 'Qaysi xatti-harakat tekshirilgani aniq. || Ясно, какое поведение проверяется.'),
                c('Darhol barcha modullarni almashtirish || Сразу заменить все модули', 'Nomoslik sababini ajratish qiyin. || Трудно выделить причину несовместимости.'),
                c('Hech natijani ko‘rmaslik || Не смотреть результат', 'O‘rganish taxmini tekshirilmaydi. || Предположение об API не проверяется.')],
              'Bitta savolni ajrating.|Natijani mustaqil taxmin bilan solishtiring. || Выделите один вопрос.|Сравните результат с независимым прогнозом.',
              'Katta integratsiya birinchi tajriba uchun ortiqcha. || Большая интеграция избыточна для первого опыта.'),
            n('Hujjat: find(items, target, default=None) birinchi indeksni, topilmasa defaultni beradi. find([1, 3], 9, default=-1) natijasi? || Документация: find(items, target, default=None) даёт первый индекс, при отсутствии default. Результат find([1, 3], 9, default=-1)?', -1,
              '9 ro‘yxatda yo‘q.|Aniq default -1 qaytadi. || 9 отсутствует в списке.|Возвращается явное default=-1.',
              'Aniq berilgan default sukut None ni almashtiradi. || Явный default заменяет значение None по умолчанию.')]),
        l('learn-limits', 'Cheklov, xato va versiya || Ограничение, ошибка и версия',
          'Hujjatdagi cheklov va versiya farqiga mos chaqiruvni tanlaysiz. || Выбираете вызов с учётом ограничений и различий версий.', [
            'StudyTools 1.0: clip(x, low=0, high=10) sonni yopiq [low, high] oraliqda ushlab qaytaradi: past bo‘lsa low, yuqori bo‘lsa high, ichida bo‘lsa x. low > high bo‘lsa ValueError. Bu x ni joyida o‘zgartirmaydi. || StudyTools 1.0: clip(x, low=0, high=10) возвращает число в замкнутом [low, high]: ниже — low, выше — high, внутри — x. При low > high возникает ValueError. Функция не меняет x на месте.',
            'take uchun manfiy limit ValueError, butun bo‘lmagan yoki bool limit TypeError beradi. Bunday cheklovlar nomdan bilinmaydi, hujjatdan o‘qiladi. Xatoni tutish uni sababini tuzatish bilan bir xil emas. || Для take отрицательный limit даёт ValueError, нецелый или bool — TypeError. Эти ограничения нельзя узнать из имени, их читают в документации. Перехват ошибки не равен исправлению её причины.',
            'Faqat versiya taqqoslash mashqi uchun StudyTools 2.0 imzosi take(items, *, count=2) deb belgilangan: count faqat nom bilan beriladi. Bu simulyatsiya, 1.0 lokal faylda mavjud emas. Eski limit nomini yangi imzoga aralashtirmang. || Только для упражнения по сравнению версий сигнатура StudyTools 2.0 задана как take(items, *, count=2): count передаётся только по имени. Это симуляция, её нет в локальном файле 1.0. Не смешивайте старое имя limit с новой сигнатурой.'
          ], 'StudyTools 1.0: clip(x, low, high), low > high bo‘lsa ValueError. clip(5, low=9, high=2) ni ko‘rib chiqing. || StudyTools 1.0: clip(x, low, high), при low > high возникает ValueError. Разберите clip(5, low=9, high=2).',
          'Chegaralarni solishtiring: 9 > 2.|Oraliq shartnomaga zid.|Natija son emas, ValueError. || Сравните границы: 9 > 2.|Интервал нарушает контракт.|Результат — не число, а ValueError.',
          'Avval noto‘g‘ri chegaralar sababini tuzating. || Сначала исправьте причину неверных границ.', [
            n('StudyTools 1.0: clip past qiymatni low, yuqorini high, ichidagini o‘zini qaytaradi. clip(14, low=2, high=9)? || StudyTools 1.0: clip возвращает low для значения ниже, high для выше, иначе само значение. clip(14, low=2, high=9)?', 9,
              '14 yuqori chegara 9 dan katta.|Natija 9. || 14 больше верхней границы 9.|Результат 9.',
              'clip oraliqdan tashqari sonni o‘zgartirmay qaytarmaydi. || clip не возвращает выходящее за интервал число без ограничения.', 'Yuqori chegara qaysi? || Какова верхняя граница?'),
            q('Hujjat: take limit < 0 bo‘lsa ValueError. take([1, 2], limit=-2) natijasi? || Документация: при limit < 0 функция take даёт ValueError. Результат take([1, 2], limit=-2)?', [
                c('ValueError || ValueError', 'Berilgan limit shartnomaga zid. || Переданный limit нарушает контракт.'),
                c('Oxirgi 2 element || Последние 2 элемента', 'Python slice taxminini bu APIga ko‘chirmang. || Не переносите догадку о срезах Python в этот API.'),
                c('Har doim [] || Всегда []', 'Hujjat aynan istisno deydi. || Документация явно задаёт исключение.')],
              'Cheklovni tekshiring.|-2 manfiy, ValueError. || Проверьте ограничение.|-2 отрицателен, ValueError.',
              'O‘xshash API semantikasini taxmin qilmang. || Не угадывайте семантику по похожему API.', 'Istisno bo‘limini o‘qing. || Прочитайте раздел исключений.'),
            q('Versiya taqqoslash simulyatsiyasi: 2.0 imzosi take(items, *, count=2). Qaysi chaqiruv mos? || Симуляция сравнения версий: сигнатура 2.0 — take(items, *, count=2). Какой вызов подходит?', [
                c('take(xs, count=3) || take(xs, count=3)', 'count nomi bilan berilgan. || count передан по имени.'),
                c('take(xs, limit=3) || take(xs, limit=3)', 'Bu eski 1.0 parametr nomi. || Это имя параметра старой версии 1.0.'),
                c('take(xs, 3) || take(xs, 3)', '* dan keyingi count faqat nomli. || count после * передаётся только по имени.')],
              'Imzodagi * countni nomli qiladi.|count=3 dan foydalaning. || * в сигнатуре делает count именованным.|Используйте count=3.',
              'Versiyalarni bir chaqiruvda aralashtirmang. || Не смешивайте версии в одном вызове.'),
            q('Hujjat: clip low > high bo‘lsa ValueError. low=8, high=3. Eng to‘g‘ri keyingi qadam? || Документация: clip даёт ValueError при low > high. low=8, high=3. Лучший следующий шаг?', [
                c('Talabga ko‘ra chegaralarni tekshirib, noto‘g‘ri tartib manbasini tuzatish || Проверить границы по требованию и исправить источник неверного порядка', 'Sabab bartaraf etiladi. || Устраняется причина.'),
                c('Barcha istisnoni yutib 0 qaytarish || Подавить все исключения и вернуть 0', 'Noto‘g‘ri kirishni yashiradi. || Скрывает неверный вход.'),
                c('Hujjatni tekshirmasdan xatoni tasodifiy deb olish || Объявить ошибку случайной без проверки документации', 'Cheklov aniq buzilgan. || Ограничение явно нарушено.')],
              '8 > 3 shartnomani buzadi.|Talabga mos chegaralarni manbada belgilang. || 8 > 3 нарушает контракт.|Задайте границы по требованию в источнике.',
              'Istisnoni yashirish o‘rganish xatosini tuzatmaydi. || Подавление исключения не исправляет непонимание.')]),
        l('learn-transfer', 'Yangi vaziyatga ko‘chirish va bilim qaydi || Перенос в новую задачу и заметка',
          'O‘qigan qoidani yangi kirishga qo‘llab, qayta foydalanish uchun dalilli qayd yozasiz. || Применяете прочитанное правило к новому входу и записываете проверяемую заметку.', [
            'Ko‘chirish — misoldagi raqamlarni yodlash emas, qoida saqlangan yangi vaziyatni yechish. take uchun “ko‘pi bilan” degani ro‘yxat qisqa bo‘lsa uning bor elementlarini olishdir. Yangi uzunlik va limitda tekshiring. || Перенос — не запоминание чисел примера, а решение нового случая по правилу. Для take «не более» означает, что из короткого списка берут имеющиеся элементы. Проверьте другую длину и другой limit.',
            'Bilim qaydi qisqa bo‘lsin: savol, vosita/versiya, imzo, bitta ishlagan misol, bitta chegara yoki xato va manba. “Hammasi tushunarli” degani qayta foydalanishga yetmaydi. || Заметка должна быть краткой: вопрос, средство/версия, сигнатура, рабочий пример, граница или ошибка и источник. «Всё понятно» недостаточно для повторного использования.',
            'Avval javobning aniqligini tekshiring, keyin vaqtni ixtiyoriy qayd eting. Qiyin bo‘lsa savolni kichraytiring, misol va cheklovni qayta o‘qing. Bir mashg‘ulot vaqtidan odamning umumiy o‘rganish tezligi haqida hukm chiqarmang. || Сначала проверьте точность, затем по желанию запишите время. При затруднении уменьшите вопрос, перечитайте пример и ограничение. Не судите об общей скорости обучения человека по времени одного занятия.'
          ], 'Hujjat: take(items, limit) dastlabki ko‘pi bilan limit elementni yangi ro‘yxatga oladi. 2 kitobli katalogdan 5 tavsiya so‘raldi. Yechim va qayd? || Документация: take(items, limit) берёт первые не более limit элементов в новый список. Из каталога из 2 книг запросили 5 рекомендаций. Решение и заметка?',
          '5 limit, majburiy uzunlik emas.|Mavjud 2 kitob qaytadi.|Qaydga versiya, chaqiruv va qisqa kirish chegarasini yozing. || 5 — лимит, а не обязательная длина.|Вернутся имеющиеся 2 книги.|Запишите версию, вызов и границу короткого входа.',
          '2 tavsiya; qoida yangi vaziyatga qo‘llandi. || 2 рекомендации; правило перенесено в новый случай.', [
            q('Qayta ishlatishga eng foydali bilim qaydi? || Какая заметка полезнее для повторного применения?', [
                c('StudyTools 1.0; take(items, limit=2); qisqa kirish to‘ldirilmaydi; misol va manba || StudyTools 1.0; take(items, limit=2); короткий вход не дополняется; пример и источник', 'Versiya, qoida va tekshirish yo‘li bor. || Есть версия, правило и способ проверки.'),
                c('“Zo‘r kutubxona” || «Отличная библиотека»', 'Qanday ishlatilishi noma’lum. || Неизвестно, как применять.'),
                c('Faqat o‘rganishga ketgan soniyalar || Только потраченные секунды', 'API ma’nosi yozilmagan. || Смысл API не записан.')],
              'Qayta ochganda nima kerakligini o‘ylang.|Imzo va chegarani saqlang. || Подумайте, что нужно при повторном обращении.|Сохраните сигнатуру и границу.',
              'Mamnunlik qaydi foydalanish yo‘riqnomasi emas. || Запись впечатления не является инструкцией.', 'Bir haftadan keyin chaqiruvni tiklay olasizmi? || Сможете восстановить вызов через неделю?'),
            n('Hujjat: take dastlabki ko‘pi bilan limit elementni oladi. 5 topshiriq bor, limit=3. Natijada nechta topshiriq? || Документация: take берёт первые не более limit элементов. Есть 5 заданий, limit=3. Сколько заданий в результате?', 3,
              '5 ta mavjud, limit 3.|Ko‘pi bilan 3, natija 3. || Доступно 5, limit равен 3.|Не более 3, результат 3.',
              'Qoida o‘zgarmaydi, vaziyat nomi almashgan. || Правило не изменилось, изменился контекст.', 'Mavjud son va limitdan kichigini oling. || Возьмите меньшее из доступного количества и лимита.'),
            q('Hujjat o‘qildi, lekin yangi kirishda javob chiqmayapti. Eng foydali qadam? || Документация прочитана, но новый вход не получается разобрать. Лучший шаг?', [
                c('Savolni kichraytirib, bitta minimal misol va cheklovni qayta tekshirish || Уменьшить вопрос и перепроверить один минимальный пример и ограничение', 'Tushunilmagan qoida ajratiladi. || Выделяется непонятое правило.'),
                c('O‘zimni qobiliyatsiz deb e’lon qilish || Объявить себя неспособным', 'Bitta vaziyat bunday xulosani isbotlamaydi. || Один случай не доказывает такой вывод.'),
                c('Tasodifiy parametr nomlarini sinash || Пробовать случайные имена параметров', 'Hujjatga asoslangan o‘rganish o‘rnini taxmin egallaydi. || Догадки заменяют обучение по документации.')],
              'Aniq tushunmovchilikni toping.|Kichik tajriba bilan tekshiring. || Найдите конкретное непонимание.|Проверьте небольшим экспериментом.',
              'Qiyinchilikni shaxsiy hukmga aylantirmang. || Не превращайте затруднение в суждение о личности.'),
            n('Hujjat: clip(x, low, high) oraliq ichida x ni qaytaradi, chegaralar ham kiradi. clip(6, low=2, high=8) natijasi? || Документация: clip(x, low, high) возвращает x внутри интервала, границы включены. Результат clip(6, low=2, high=8)?', 6,
              '2 <= 6 <= 8.|Qiymat oraliqda, 6 saqlanadi. || 2 <= 6 <= 8.|Значение внутри интервала, сохраняется 6.',
              'Har chaqiruv sonni chegara qiymatiga almashtirmaydi. || Не каждый вызов заменяет число на границу.')])
    ])
