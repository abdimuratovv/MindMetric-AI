from authoring import choice as c, lesson as l, module, numeric as n, q


def build():
    return module('code-debugging', 1, 'Kod tahlili va debugging || Анализ кода и отладка', [
        l('debug-types', 'Xato turini ajratish || Различение видов ошибок',
          'Belgidan kelib chiqib sintaksis, bajarilish yoki mantiqiy xatoni ajratasiz. || По признакам различаете синтаксическую ошибку, ошибку выполнения и логическую ошибку.', [
            'Python kodni avval tahlil qiladi. Masalan, if sarlavhasidagi ikki nuqta tushsa SyntaxError yuz beradi; dastur odatdagi bajarilishga o‘tmaydi. Xabar ko‘rsatgan joy sababning o‘zi bo‘lmasligi mumkin: oldingi satrni ham tekshiring. || Python сначала разбирает код. Например, пропуск двоеточия в заголовке if вызывает SyntaxError; обычное выполнение не начинается. Место из сообщения не всегда является причиной: проверьте и предыдущую строку.',
            'Sintaktik to‘g‘ri kod bajarilayotganda ham to‘xtashi mumkin: 8 / 0 — ZeroDivisionError. Kod tugab, talabga zid javob bersa, bu mantiqiy xato bo‘lishi mumkin. To‘g‘ri ishlayotganini bilish uchun kutilgan natija zarur. || Синтаксически правильный код может остановиться во время выполнения: 8 / 0 даёт ZeroDivisionError. Если код завершился, но результат противоречит требованию, возможна логическая ошибка. Для проверки нужен ожидаемый результат.',
            'Tuzatishdan oldin xato turini, berilgan kirishni va talabni yozing. Birinchi xatoni bartaraf etish barcha keyingi xatolar yo‘qligini kafolatlamaydi. || До исправления запишите вид ошибки, вход и требование. Устранение первой ошибки не гарантирует отсутствия следующих.'
          ], '''Python 3, ataylab xato kod:
```python
if 4 > 2
    print(4)
```
Nega natija chiqmaydi? || Python 3, намеренно ошибочный код:
```python
if 4 > 2
    print(4)
```
Почему нет результата?''',
          'if sarlavhasini ko‘ring.|Oxirida : yo‘q.|Sintaksisni tuzatib, keyin qayta tekshiring. || Проверьте заголовок if.|В конце нет :.|Исправьте синтаксис и проверьте снова.',
          'SyntaxError; sarlavha if 4 > 2: bo‘ladi. || SyntaxError; заголовок должен быть if 4 > 2:.', [
            q('Python 3: print(9 / 0). Qaysi turdagi xato? || Python 3: print(9 / 0). Какой вид ошибки?', [
                c('Bajarilish xatosi || Ошибка выполнения', 'Bo‘lish bajarilganda ZeroDivisionError keladi. || При делении возникает ZeroDivisionError.'),
                c('Sintaksis xatosi || Синтаксическая ошибка', 'Bu ifoda sintaktik jihatdan yaroqli. || Это синтаксически допустимое выражение.'),
                c('To‘g‘ri natija 0 || Правильный результат 0', 'Nolga bo‘lish nol natija bermaydi. || Деление на ноль не даёт ноль.')],
              'Sintaksis yaroqli.|Bo‘luvchi nol, bajarilish to‘xtaydi. || Синтаксис допустим.|Делитель равен нулю, выполнение прерывается.',
              'Barcha xatolarni SyntaxError deb atamang. || Не называйте все ошибки SyntaxError.', 'Amalni bajarish mumkinmi? || Можно ли выполнить операцию?'),
            q('Talab: a va b yig‘indisi. Python kodi print(a - b), a=8, b=3; natija 5. Sabab? || Требование: сумма a и b. Код Python print(a - b), a=8, b=3; результат 5. Причина?', [
                c('Mantiqiy xato: noto‘g‘ri amal || Логическая ошибка: неверная операция', 'Talab 11, kod esa ayirmani hisoblaydi. || Нужно 11, а код вычисляет разность.'),
                c('Bajarilish istisnosi || Исключение при выполнении', 'Berilgan sonlarni ayirish istisno bermaydi. || Вычитание этих чисел не вызывает исключения.'),
                c('Python ayirishni bilmaydi || Python не поддерживает вычитание', 'Ayirish mavjud, ammo bu talabga mos emas. || Вычитание есть, но не соответствует требованию.')],
              'Kutilgan qiymat 8 + 3 = 11.|5 talabga mos emas. || Ожидалось 8 + 3 = 11.|5 не соответствует требованию.',
              'Dastur tugaganini to‘g‘rilik isboti demang. || Не считайте завершение программы доказательством правильности.', 'Talab bilan ishlatilgan operatorni solishtiring. || Сравните требование с оператором.'),
            q('Python 3: print(total), lekin total hech qayerda aniqlanmagan. Natija? || Python 3: print(total), но total нигде не определена. Результат?', [
                c('NameError || NameError', 'Nom bajarilish vaqtida topilmaydi. || Имя не найдено во время выполнения.'),
                c('SyntaxError || SyntaxError', 'Funksiya chaqiruvining sintaksisi to‘g‘ri. || Синтаксис вызова правильный.'),
                c('Avtomatik 0 || Автоматически 0', 'Aniqlanmagan nomga Python nol bermaydi. || Python не присваивает неопределённому имени ноль.')],
              'Nomning ta’rifini qidiring.|U yo‘q, NameError yuz beradi. || Найдите определение имени.|Его нет, возникает NameError.',
              'Aniqlanmagan o‘zgaruvchini nol deb olmang. || Не считайте неопределённую переменную нулём.'),
            q('To‘rtburchak yuzi kerak. Python kodi print(2 * (a + b)), a=3, b=5. Dastur 16 chiqaradi. Xulosa? || Нужна площадь прямоугольника. Python print(2 * (a + b)), a=3, b=5. Программа выводит 16. Вывод?', [
                c('Mantiqiy xato, perimetr hisoblangan || Логическая ошибка, вычислен периметр', 'Yuza 15, qo‘llangan formula boshqa kattalik uchun. || Площадь равна 15, формула относится к другой величине.'),
                c('Sintaksis xatosi || Синтаксическая ошибка', 'Kod bajarildi, uning sintaksisi yaroqli. || Код выполнился, синтаксис допустим.'),
                c('Natija har doim to‘g‘ri || Результат всегда правильный', 'Muvaffaqiyatli bajarilish talabni almashtirmaydi. || Успешное выполнение не заменяет требование.')],
              'Talab yuzani so‘raydi.|3 × 5 = 15, kod perimetrni bergan. || Требуется площадь.|3 × 5 = 15, код дал периметр.',
              'Formula va talabni birgalikda tekshiring. || Проверяйте формулу вместе с требованием.')]),
        l('debug-reproduce', 'Xatoni qayta hosil qilish || Воспроизведение ошибки',
          'Takrorlanadigan xato hisobotini va kichik qarshi misolni tuzasiz. || Составляете воспроизводимый отчёт и небольшой контрпример.', [
            'Yaxshi hisobotda versiya, aniq kirish, bajarish qadami, kutilgan va haqiqiy natija bo‘ladi. “Ishlamadi” sababni izlashga yetmaydi. Maxfiy ma’lumot o‘rniga sun’iy kichik kirish ishlating. || Хороший отчёт содержит версию, точный вход, шаг запуска, ожидаемый и фактический результат. «Не работает» недостаточно для поиска причины. Вместо секретных данных используйте небольшой искусственный вход.',
            'Minimal misol xatoni saqlagan holda ortiqcha qismlarni olib tashlaydi. Xato yo‘qolsa, o‘sha qisqartirishni qaytaring. Minimal degani faqat satrlar soni eng kam degani emas: sababni tekshirishga yetarli bo‘lishi kerak. || Минимальный пример сохраняет ошибку, убирая лишние части. Если ошибка исчезла, отмените это сокращение. Минимальность — не просто наименьшее число строк: данных должно хватать для проверки причины.',
            'Gipoteza tekshiriladigan taxmin: “faqat bo‘sh ro‘yxatda ishlamaydi”. Bir o‘zgarish qiling va ayni testni qaytaring; bir vaqtning o‘zida bir necha joyni almashtirish sababni chalkashtiradi. || Гипотеза — проверяемое предположение: «сбой возникает только на пустом списке». Сделайте одно изменение и повторите тот же тест; несколько одновременных правок скрывают причину.'
          ], 'mean(xs) funksiyasi sum(xs) / len(xs) qaytaradi. [2, 4] da 3, [] da ZeroDivisionError. Hisobotni qisqartiring. || Функция mean(xs) возвращает sum(xs) / len(xs). Для [2, 4] получается 3, для [] — ZeroDivisionError. Сократите отчёт.',
          'Python 3 va mean funksiyasini qoldiring.|Kirish [] bo‘lsin.|Bo‘sh ro‘yxat uchun talabni aniqlang; xato va kutilgan natijani yozing. || Оставьте Python 3 и функцию mean.|Используйте вход [].|Уточните требование для пустого списка; запишите ошибку и ожидаемый результат.',
          'Bo‘sh kirish xatoni qaytaradi; bo‘sh holat uchun shartnoma zarur. || Пустой вход воспроизводит сбой; нужен контракт для пустого случая.', [
            q('Hisobot: “Chegirma noto‘g‘ri”. Qaysi qo‘shimcha eng foydali? || Отчёт: «Скидка неверна». Какое дополнение полезнее?', [
                c('Kirish 100, stavka 10%; kutilgan 90, olingan 110; ishga tushirish qadami || Вход 100, ставка 10%; ожидалось 90, получено 110; шаг запуска', 'Aniq farq va qayta bajarish yo‘li bor. || Есть точное расхождение и способ повторения.'),
                c('“Tezroq tuzating” || «Исправьте быстрее»', 'Shoshiltirish qayta hosil qilish ma’lumoti emas. || Срочность не даёт данных для воспроизведения.'),
                c('Faqat xato xabari; kirish va kutilgan natijasiz || Только сообщение об ошибке, без входа и ожидаемого результата', 'Xabar foydali, ammo hisobni qaytarish va tekshirish uchun yetarli emas. || Сообщение полезно, но недостаточно для воспроизведения и проверки расчёта.')],
              'Kirishni qaytaring.|Kutilgan va haqiqiy natijani solishtiring. || Повторите вход.|Сравните ожидаемый и фактический результат.',
              'Hisobotga faqat baho yozmang. || Не ограничивайте отчёт оценочным суждением.', 'Boshqa odam xatoni qaytara oladimi? || Сможет ли другой человек повторить сбой?'),
            q('Ro‘yxatning birinchi elementini o‘qish [] da yiqiladi. Minimal misolda nima qoladi? || Чтение первого элемента списка падает на []. Что оставить в минимальном примере?', [
                c('Bo‘sh ro‘yxat va birinchi elementni o‘qish || Пустой список и чтение первого элемента', 'Xatoni yuzaga keltiradigan sabab saqlanadi. || Сохраняется причина сбоя.'),
                c('Bo‘sh ro‘yxatni [1]ga almashtirish || Заменить пустой список на [1]', 'Bu xatoni yashiradi, qaytarmaydi. || Это скрывает сбой, а не воспроизводит его.'),
                c('Barcha interfeys va rasmlar || Весь интерфейс и картинки', 'Indeks xatosiga aloqasiz qismlar ortiqcha. || Несвязанные с ошибкой индекса части избыточны.')],
              'Xato [] da saqlansin.|Faqat zarur amalni qoldiring. || Сбой на [] должен сохраниться.|Оставьте только необходимую операцию.',
              'Minimal misolda muammoli kirishni almashtirmang. || Не заменяйте проблемный вход в минимальном примере.', 'Qisqartirishdan keyin ham xato bo‘lishi shart. || После сокращения ошибка должна оставаться.'),
            q('Nosozlik faqat miqdor 0 bo‘lganda kuzatildi. Qaysi gipoteza tekshiriladi? || Сбой замечен только при количестве 0. Какая гипотеза проверяема?', [
                c('Miqdor 0 ga bo‘linayotgan bo‘lishi mumkin; bo‘lish satrini tekshiraman || Возможно деление на количество 0; проверю строку деления', 'Aniq holat va tekshiriladigan amal bor. || Есть конкретное условие и проверяемая операция.'),
                c('Sabab aniq Pythonning o‘zida; kirishni tekshirmayman || Причина точно в самом Python; вход проверять не буду', 'Kuzatuv bunday qat’iy xulosaga yetarli emas. || Наблюдения недостаточно для такого категоричного вывода.'),
                c('Kodni to‘liq qayta yozish kerak; avval tajriba shart emas || Нужно полностью переписать код; предварительный эксперимент не нужен', 'Qayta yozish sababni sinaydigan gipoteza emas. || Переписывание не является проверяемой гипотезой о причине.')],
              '0 bilan bog‘liq amallarni qidiring.|Bo‘lish joyini ayni kirishda tekshiring. || Найдите операции, связанные с 0.|Проверьте деление на том же входе.',
              'Gipoteza va keskin qayta yozishni adashtirmang. || Не путайте гипотезу с радикальной переписью.'),
            q('Bir vaqtning o‘zida 4 joy o‘zgartirildi, xato yo‘qoldi. Keyingi yaxshi qadam? || Одновременно изменили 4 места, ошибка исчезла. Какой следующий шаг лучше?', [
                c('Alohida nusxada o‘zgarishlarni bittalab tekshirib sabab va regressiya testini aniqlash || На отдельной копии проверить изменения по одному, установить причину и регрессионный тест', 'Natijani sabab bilan bog‘lash mumkin bo‘ladi. || Можно связать результат с причиной.'),
                c('Har bir o‘zgarish zarur deb e’lon qilish || Объявить каждую правку необходимой', 'Buning uchun dalil yo‘q. || Для этого нет доказательств.'),
                c('Testni o‘chirish || Удалить тест', 'Xatoni aniqlash vositasi yo‘qoladi. || Исчезнет средство обнаружения сбоя.')],
              'Bir xil kirishni saqlang.|Har bir tuzatish ta’sirini ajrating. || Сохраните тот же вход.|Отделите влияние каждой правки.',
              'Birga o‘zgarish sababni isbotlamaydi. || Одновременные изменения не доказывают причину.')]),
        l('debug-trace', 'Qiymatlar izi va traceback || Трассировка значений и traceback',
          'Satrlar bo‘yicha qiymat o‘zgarishini va xabar zanjirini o‘qiysiz. || Читаете изменения значений по строкам и цепочку ошибки.', [
            'Trace jadvalida bajarilgan satr va undan KEYINGI qiymatlar yoziladi. Shart tekshiruvi o‘zi qiymatni o‘zgartirmaydi. Bir xil nomning qayerda aniqlangani va yangilangani kuzatiladi. || В таблице трассировки записывают выполненную строку и значения ПОСЛЕ неё. Проверка условия сама по себе не меняет значение. Отслеживайте, где имя определено и обновлено.',
            'Tracebackning oxirgi satri istisno turi va xabarini bildiradi. Yuqoridagi kadrlar chaqiruv yo‘lini ko‘rsatadi. Eng quyi tegishli kadrdan muammoli ifodani toping; chaqiruvchi berayotgan qiymatni ham tekshiring. || Последняя строка traceback сообщает тип исключения и сообщение. Кадры выше показывают путь вызовов. Найдите проблемное выражение в нижнем относящемся к делу кадре; проверьте и значение от вызывающего кода.',
            'Tasodifiy printlar o‘rniga shubhali amal oldi va keyinini kuzating. Kuzatuv o‘zgaruvchini o‘zgartirib yubormasin; diagnostik yozuvlarga maxfiy ma’lumot chiqarmang. || Вместо случайных print наблюдайте состояние до и после подозрительной операции. Наблюдение не должно менять переменную; не выводите секретные данные в диагностические записи.'
          ], '''Python 3:
```python
x = 2
x = x + 3
y = x * 2
```
y ni iz bilan toping. || Python 3:
```python
x = 2
x = x + 3
y = x * 2
```
Найдите y трассировкой.''',
          'Birinchi satrdan keyin x=2.|Ikkinchisidan keyin x=5.|Uchinchisida y=10. || После первой строки x=2.|После второй x=5.|На третьей y=10.', '10 || 10', [
            n('Python 3: x = 4; x = x + 2; x = x * 3. Oxirgi x? || Python 3: x = 4; x = x + 2; x = x * 3. Конечное x?', 18,
              'Avval x=6.|Keyin 6 × 3 = 18. || Сначала x=6.|Затем 6 × 3 = 18.',
              'Keyingi satr eski emas, yangilangan x ni oladi. || Следующая строка берёт обновлённое x.', 'Har satrdan keyingi x ni yozing. || Запишите x после каждой строки.'),
            q('Traceback oxiri: ZeroDivisionError: division by zero. Eng foydali tekshiruv? || Конец traceback: ZeroDivisionError: division by zero. Что полезнее проверить?', [
                c('Ko‘rsatilgan bo‘lish ifodasidagi bo‘luvchi qanday 0 bo‘lganini || Как делитель указанного выражения стал 0', 'Istisno ma’nosi bilan bevosita bog‘liq. || Это прямо связано со смыслом исключения.'),
                c('Faqat fayl nomini o‘zgartirish || Только переименовать файл', 'Bo‘luvchining qiymati o‘zgarmaydi. || Значение делителя не изменится.'),
                c('Har doim oxirgi printni o‘chirish || Всегда удалять последний print', 'Xabar sababini tekshirmaydi. || Это не проверяет причину сообщения.')],
              'Xabar turini o‘qing.|Amaldagi bo‘luvchi va uning manbasini toping. || Прочитайте тип сообщения.|Найдите делитель и источник его значения.',
              'Xabar matnini tuzatish sababni tuzatmaydi. || Изменение текста сообщения не устраняет причину.', 'Qaysi operand nol bo‘lishi mumkin? || Какой операнд может быть нулём?'),
            n('Python 3: a = 3; b = a; a = 8; print(b). Nima chiqadi? || Python 3: a = 3; b = a; a = 8; print(b). Что выводится?', 3,
              'b ga o‘sha paytdagi 3 berildi.|a ni 8 qilish b ni o‘zgartirmaydi. || b получает тогдашнее значение 3.|Присваивание a значения 8 не меняет b.',
              'Butun qiymat berishni doimiy formula bog‘lanishi deb olmang. || Не считайте присваивание целого постоянной связью формулы.'),
            n('''Python 3:
```python
s = 0
for x in [2, 5, 1]:
    s = s + x
```
Sikldan keyingi s? || Python 3:
```python
s = 0
for x in [2, 5, 1]:
    s = s + x
```
Чему равно s после цикла?''', 8,
              's qiymatlari 0 → 2 → 7 → 8.|Oxirgi qiymat 8. || Значения s: 0 → 2 → 7 → 8.|Конечное значение 8.',
              's ni har aylanishda noldan boshlamang. || Не обнуляйте s на каждом проходе.')]),
        l('debug-breakpoint', 'Breakpoint va qadamli tekshiruv || Точка останова и пошаговая проверка',
          'Pauza joyini va step/next/continue amallarini maqsadga mos tanlaysiz. || Выбираете место остановки и команды step/next/continue по цели.', [
            'Breakpoint dastur holatini tekshirish uchun bajarilishni pauza qiladi; u kodni avtomatik tuzatmaydi. Bu kursdagi strelka bilan belgilangan pauza satri hali bajarilmagan deb olinadi. || Точка останова приостанавливает выполнение для проверки состояния; она не исправляет код автоматически. В этом курсе строка паузы со стрелкой считается ещё не выполненной.',
            'Python pdb da p x qiymatni ko‘rsatadi; n (next) joriy satrni bajarib, odatda shu kadrdagi keyingi satrga o‘tadi; s (step) chaqirilgan funksiyaga kirishi mumkin; c (continue) keyingi to‘xtashgacha davom etadi. || В Python pdb команда p x показывает значение; n (next) выполняет текущую строку и обычно переходит к следующей в том же кадре; s (step) может войти в вызываемую функцию; c (continue) продолжает до следующей остановки.',
            'Avval taxminingizni yozing, keyin holatni kuzating. Cheksiz sikldan shubhalansangiz, shartdagi qiymat va uning yangilanishini tekshiring. Sinov nusxasida ishlang; tuzatishni oddiy ishga tushirish bilan ham tasdiqlang. || Сначала запишите прогноз, затем наблюдайте состояние. При подозрении на бесконечный цикл проверяйте значение условия и его обновление. Работайте на учебной копии; подтвердите исправление и обычным запуском.'
          ], 'Python 3: x=4 bajarilgan. Strelka x = x + 2 satrida, satr hali bajarilmagan. p x, keyin n, keyin p x nima beradi? || Python 3: x=4 уже выполнено. Стрелка на x = x + 2, строка ещё не выполнена. Что покажут p x, затем n, затем p x?',
          'Pauzada x=4.|n qo‘shishni bajaradi.|Keyingi kuzatuvda x=6. || В паузе x=4.|n выполняет сложение.|При следующем наблюдении x=6.', '4, keyin 6 || 4, затем 6', [
            n('Python pdb: x=7. Strelka x = x * 2 satrida, u hali bajarilmagan. p x nechani ko‘rsatadi? || Python pdb: x=7. Стрелка на x = x * 2, строка ещё не выполнена. Что покажет p x?', 7,
              'Pauza amal oldida.|Ko‘paytirish hali bo‘lmagan, x=7. || Пауза перед операцией.|Умножение ещё не выполнено, x=7.',
              'Pauza qilingan satrni bajarilgan deb olmang. || Не считайте строку паузы уже выполненной.', 'Strelka keyingi bajariladigan satrda. || Стрелка на следующей выполняемой строке.'),
            q('pdb da f() ichidagi satrlarni kuzatish kerak. Chaqiruv satrida qaysi buyruq mos? || В pdb нужно проследить строки внутри f(). Какая команда подходит на строке вызова?', [
                c('s — step || s — step', 'Chaqirilgan funksiyaga kirish uchun. || Для входа в вызываемую функцию.'),
                c('p x || p x', 'Bu qiymatni ko‘radi, funksiyaga qadam qilmaydi. || Показывает значение, но не делает шаг внутрь.'),
                c('q — quit || q — quit', 'Bu debuggingdan chiqadi. || Это выход из отладки.')],
              'Maqsad funksiya ichiga kirish.|step shu maqsadga mos. || Цель — войти в функцию.|step соответствует этой цели.',
              'Kuzatish buyrug‘i bilan qadam buyrug‘ini farqlang. || Различайте просмотр и выполнение шага.', 'Funksiyaga kirish va uning ustidan o‘tish farq qiladi. || Войти в функцию и пройти поверх неё — разные действия.'),
            q('Breakpoint qo‘yildi. Qaysi da’vo to‘g‘ri? || Поставлена точка останова. Какое утверждение верно?', [
                c('U holatni kuzatishga yordam beradi; sabab va tuzatish alohida aniqlanadi || Она помогает наблюдать состояние; причину и исправление определяют отдельно', 'Pauza dalil yig‘ishga xizmat qiladi. || Остановка нужна для сбора фактов.'),
                c('Barcha xatolar avtomatik tuzatiladi || Все ошибки исправляются автоматически', 'Breakpoint tuzatish mexanizmi emas. || Точка останова не является механизмом исправления.'),
                c('Shundan keyin test kerak emas || После этого тесты не нужны', 'Kuzatuv barcha kirishlarni qamramaydi. || Наблюдение не покрывает все входы.')],
              'Breakpoint bajarilishni to‘xtatadi.|Natijaning to‘g‘riligini test tekshiradi. || Точка останова приостанавливает выполнение.|Правильность результата проверяет тест.',
              'Vosita borligi to‘g‘rilik kafolati emas. || Наличие инструмента не гарантирует правильности.'),
            q('pdb da hozirgi satrni bajarib, keyingi breakpointgacha davom etish kerak. Qaysi buyruq? || В pdb нужно продолжить выполнение от текущей строки до следующей точки останова. Какая команда?', [
                c('c — continue || c — continue', 'Davom etadi; boshqa to‘xtash sababi bo‘lsa ham pauza mumkin. || Продолжает; остановка возможна и по другой причине.'),
                c('p x || p x', 'Qiymatni ko‘rsatish bajarilishni davom ettirmaydi. || Просмотр значения не продолжает выполнение.'),
                c('s ni bir marta berish || Один раз s', 'Faqat bitta qadam maqsadga yetmasligi mumkin. || Одного шага может быть недостаточно.')],
              'Ketma-ket bitta qadam emas, davom ettirish so‘ralgan.|c mos keladi. || Нужен не одиночный шаг, а продолжение.|Подходит c.',
              'step va continue ni aralashtirmang. || Не смешивайте step и continue.')]),
        l('debug-regression', 'Chegaralar va regressiya || Границы и регрессия',
          'Xato sababiga mos minimal tuzatish va regressiya to‘plamini tanlaysiz. || Выбираете минимальное исправление причины и регрессионный набор.', [
            'Chegaraviy test talab ajraladigan joyni tekshiradi: limitdan past, teng va yuqori. Ro‘yxatlarda bo‘sh, bitta va bir nechta element muhim. Kutilgan natija koddan emas, shartnomadan olinadi. || Граничный тест проверяет место разделения требований: ниже лимита, на нём и выше. Для списков важны пустой, одиночный и множественный случаи. Ожидаемый результат берут из контракта, а не из кода.',
            'Minimal tuzatish sababni nishonga oladi. Masalan, talab “kamida 18” bo‘lsa > ni >= ga almashtirish mos; barcha foydalanuvchilarni qabul qilish bu xatoni yashiradi. || Минимальное исправление направлено на причину. Например, для «не менее 18» подходит замена > на >=; разрешение всем пользователям скрывает ошибку.',
            'Regressiya testi oldingi xato qaytmaganini tekshiradi. Tuzatishdan keyin muammoli test bilan birga ilgari o‘tgan oddiy va chegaraviy testlarni qaytaring. O‘tmagan testni yashirish o‘rniga yangi kuzatuv yozing va gipotezani yangilang. || Регрессионный тест проверяет, что старая ошибка не вернулась. После исправления повторите проблемный тест и ранее проходившие обычные и граничные случаи. Вместо скрытия неудачного теста запишите наблюдение и обновите гипотезу.'
          ], 'Talab: age >= 18 bo‘lsa ruxsat. Kod age > 18. 18 yosh rad bo‘ladi. Tuzatish va testlar? || Требование: разрешить при age >= 18. Код age > 18. Возраст 18 отклоняется. Исправление и тесты?',
          '> o‘rniga >= qo‘ying.|17 rad, 18 ruxsat, 19 ruxsatni tekshiring.|Avvalgi katta yosh holatini ham qaytaring. || Замените > на >=.|Проверьте: 17 отказ, 18 разрешение, 19 разрешение.|Повторите и прежний случай большего возраста.',
          'Sababga mos tuzatish va chegara atrofidagi sinov. || Исправление причины и тесты вокруг границы.', [
            q('Bepul yetkazish summa >= 100 bo‘lganda. Qaysi to‘plam chegarani tekshiradi? || Бесплатная доставка при сумме >= 100. Какой набор проверяет границу?', [
                c('99, 100, 101 || 99, 100, 101', 'Chegaraning ikki tomoni va o‘zi bor. || Есть обе стороны границы и сама граница.'),
                c('150, 200, 300 || 150, 200, 300', 'Barchasi bir tomonda. || Все значения по одну сторону.'),
                c('Faqat 1000 || Только 1000', 'Tenglik xatosi topilmasligi mumkin. || Ошибка равенства может не обнаружиться.')],
              'Talab 100 da ajraladi.|Atrofidagi butun qiymatlarni oling. || Требование разделяется на 100.|Возьмите соседние целые значения.',
              'Faqat katta qiymatlar chegarani tekshirmaydi. || Одни большие значения не проверяют границу.', 'Past, teng, yuqori holatlarni toping. || Найдите случаи ниже, на границе и выше.'),
            q('[] da xato tuzatildi. Regressiya uchun nima kerak? || Ошибка на [] исправлена. Что нужно для регрессии?', [
                c('[] hamda ilgari o‘tgan [4] va [2, 6] ni talab bilan solishtirish || Сравнить [] и ранее проходившие [4], [2, 6] с требованиями', 'Yangi va eski holatlar birga tekshiriladi. || Проверяются и новый, и прежние случаи.'),
                c('Faqat fayl ochilishini tekshirish || Проверить только открытие файла', 'Natijalar to‘g‘riligini isbotlamaydi. || Не проверяет правильность результатов.'),
                c('[] testini o‘chirish || Удалить тест []', 'Aynan qaytishi mumkin bo‘lgan xato nazoratsiz qoladi. || Именно возможный возврат ошибки останется без проверки.')],
              'Muammoli kirishni saqlang.|Ilgari ishlagan holatlarni qaytaring. || Сохраните проблемный вход.|Повторите ранее работавшие случаи.',
              'Tuzatish boshqa holatni buzishi mumkin. || Исправление может нарушить другой случай.', 'Yangi tuzatishdan oldin nimalar ishlagan? || Что работало до исправления?'),
            q('Talab: 0 ham yaroqli. Kod x > 0. Eng kichik mos tuzatish? || Требование: 0 тоже допустим. Код x > 0. Минимальное подходящее исправление?', [
                c('x >= 0 || x >= 0', 'Nol kiradi, manfiylar kirmaydi. || Ноль допускается, отрицательные нет.'),
                c('Har doim True || Всегда True', 'Manfiylar ham o‘tib ketadi. || Пройдут и отрицательные значения.'),
                c('x < 0 || x < 0', 'Nol yana o‘tmaydi va ma’no teskarilanadi. || Ноль снова не проходит, смысл обращается.')],
              'Faqat tenglik holati yetishmayapti.|>= talabga mos. || Не хватает только равенства.|>= соответствует требованию.',
              'Xatoni barcha kirishlarga ruxsat bilan yashirmang. || Не скрывайте ошибку разрешением всех входов.'),
            q('Tuzatishdan keyin yangi test o‘tdi, avvalgi test yiqildi. Nima qilish kerak? || После исправления новый тест прошёл, прежний упал. Что делать?', [
                c('Avvalgi talabni tekshirib, regressiya sababini aniqlash || Проверить прежнее требование и найти причину регрессии', 'Talab o‘zgarmagan bo‘lsa avvalgi ishlash ham saqlanishi kerak. || Если требование не менялось, прежнее поведение нужно сохранить.'),
                c('Yiqilgan testni izohsiz olib tashlash || Удалить упавший тест без объяснения', 'Muammoni yashiradi. || Скрывает проблему.'),
                c('Faqat yangi test yetarli deyish || Считать достаточным новый тест', 'O‘tgan holat boshqa holatdagi xatoni bekor qilmaydi. || Успех одного случая не отменяет ошибку другого.')],
              'Testning kutilgan natijasini talabdan tekshiring.|Regressiyani bartaraf etib, ikkisini qaytaring. || Проверьте ожидаемый результат по требованию.|Устраните регрессию и повторите оба теста.',
              'Bitta muvaffaqiyat barcha test o‘rnini bosmaydi. || Один успех не заменяет все тесты.')])
    ])
