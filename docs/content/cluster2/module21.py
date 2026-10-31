from authoring import lesson as l, module, n, s


def build():
    return module('algorithmization-flowcharts', 1,
        'Algoritmizatsiya va blok-sxemalar || Алгоритмизация и блок-схемы', ['algorithmic'], [
        l('algo-io', 'Kirish, chiqish va shartnoma || Вход, выход и контракт', [
            'Algoritm — berilgan kirishdan talab qilingan chiqishga olib boruvchi aniq qadamlar. Avval nima berilgani, nima topilishi va qaysi qiymatlar mumkinligini yozing. || Алгоритм — точные шаги от заданного входа к требуемому выходу. Сначала запишите исходные данные, результат и допустимые значения.',
            'Kirish foydalanuvchidan keladi, chiqish hisoblanadi. To‘rtburchak perimetri uchun kirish a va b tomonlar, chiqish esa P = 2 × (a + b). Musbat uzunliklar talab qilinadi. || Вход поступает от пользователя, выход вычисляется. Для периметра прямоугольника вход — стороны a и b, выход — P = 2 × (a + b). Длины должны быть положительными.',
            'Hisoblashdan oldin birliklarni moslang. Natija to‘g‘ri son bo‘lishi yetmaydi: uning nimani va qaysi birlikda bildirishini ham aniqlang. || До вычисления согласуйте единицы. Недостаточно получить правильное число: определите его смысл и единицу измерения.'
        ], 'Bir daftar 4000 so‘m, miqdor 3. Jami to‘lovni toping. || Одна тетрадь стоит 4000 сумов, количество — 3. Найдите общую стоимость.',
           'Kirish: narx va miqdor.|Jami = 4000 × 3 = 12000.|Chiqish — jami to‘lov, so‘mda. || Вход: цена и количество.|Итого = 4000 × 3 = 12000.|Выход — общая стоимость в сумах.', '12000 so‘m || 12000 сумов', [
            n('Bir chipta 6000 so‘m. 4 chipta jami necha so‘m? || Один билет стоит 6000 сумов. Сколько сумов стоят 4 билета?', 24000,
              'Narx miqdorga ko‘payadi.|6000 × 4 = 24000. || Цена умножается на количество.|6000 × 4 = 24000.',
              'Narx va miqdorni qo‘shish jami to‘lovni bermaydi. || Сложение цены и количества не даёт общую стоимость.',
              'Bir xil narx har bir chiptaga tegishli. || Одинаковая цена относится к каждому билету.'),
            s('Aylana uzunligi emas, to‘rtburchak YUZINI hisoblash kerak. Qaysi kirish/chiqish mos? || Нужно вычислить ПЛОЩАДЬ прямоугольника, а не длину окружности. Какие вход и выход подходят?', [
                ('Kirish: a, b tomonlar; chiqish: a × b || Вход: стороны a, b; выход: a × b', 'Ikki tomon yuza uchun yetarli. || Двух сторон достаточно для площади.'),
                ('Kirish: r radius; chiqish: aylana uzunligi || Вход: радиус r; выход: длина окружности', 'Bu boshqa shakl va boshqa kattalik. || Это другая фигура и другая величина.'),
                ('Kirish: a, b; chiqish: 2 × (a + b) || Вход: a, b; выход: 2 × (a + b)', 'Bu yuzani emas, perimetrni beradi. || Это даёт периметр, а не площадь.')],
              'Yuza uchun ikki tomon olinadi.|S = a × b formulasi ishlatiladi. || Для площади берутся две стороны.|Используется формула S = a × b.',
              'Kirish bir xil bo‘lsa ham chiqish maqsadini almashtirmang. || Даже при одинаковом входе не подменяйте цель результата.',
              'Yuza ichki sohani o‘lchaydi. || Площадь измеряет внутреннюю область.'),
            s('Yo‘l vaqtini topish uchun masofa va o‘zgarmas tezlik beriladi. Qaysi cheklov zarur? || Для нахождения времени пути заданы расстояние и постоянная скорость. Какое ограничение необходимо?', [
                ('Tezlik musbat, birliklar mos || Скорость положительна, единицы согласованы', 'Tezlikka bo‘linadi; nol va nomos birliklar yaramaydi. || Выполняется деление на скорость; ноль и несогласованные единицы недопустимы.'),
                ('Tezlik nol bo‘lishi shart || Скорость обязательно равна нулю', 'Nolga bo‘lib vaqt topilmaydi. || Делением на ноль время не найти.'),
                ('Masofa har doim tezlikka teng || Расстояние всегда равно скорости', 'Turli fizik kattaliklar uchun bunday talab yo‘q. || Для разных физических величин такого требования нет.')],
              'Vaqt = masofa / tezlik.|Tezlik musbat bo‘lishi, birliklar mos kelishi kerak. || Время = расстояние / скорость.|Скорость должна быть положительной, единицы — согласованными.',
              'Formula bilan birga uning qo‘llanish shartini ham yozing. || Вместе с формулой указывайте условия её применения.'),
            n('Omborda 18 quti bor, har birida 12 dona buyum. Dona sonini toping. || На складе 18 коробок, в каждой 12 предметов. Найдите количество предметов.', 216,
              'Chiqish — qutilar emas, dona soni.|18 × 12 = 216. || Выход — число предметов, а не коробок.|18 × 12 = 216.',
              'Qutilar sonini o‘zini javob deb olmang. || Не принимайте само количество коробок за ответ.')]),
        l('algo-decompose', 'Masalani bosqichlarga ajratish || Декомпозиция задачи', [
            'Dekompozitsiya katta vazifani kichik va tekshiriladigan qismlarga bo‘ladi. Har qismning kirishi, chiqishi va keyingi qismga bog‘lanishi aniqlanadi. || Декомпозиция делит большую задачу на небольшие проверяемые части. Для каждой части определяются вход, выход и связь со следующей частью.',
            'Buyurtma hisobida avval ma’lumotni tekshiring, keyin buyumlar summasini toping, chegirmani hisoblang va oxirida yetkazishni qo‘shing. Tartib masala shartidan olinadi. || При расчёте заказа сначала проверьте данные, затем найдите сумму товаров, примените скидку и в конце добавьте доставку. Порядок следует из условия задачи.',
            'Qismni alohida tekshirish xatoni toraytiradi. Har ekran yoki har satr alohida masala emas: bo‘linish mazmunli natijaga ega bo‘lsin. || Отдельная проверка части сужает поиск ошибки. Не каждый экран или строка — самостоятельная задача: часть должна иметь осмысленный результат.'
        ], '20000 so‘mlik buyumga 5000 so‘m chegirma va keyin 3000 so‘m yetkazish qo‘shiladi. Bosqichlarni bajaring. || Из стоимости товара 20000 сумов вычитают скидку 5000 сумов, затем добавляют доставку 3000 сумов. Выполните этапы.',
           'Buyum summasi 20000.|Chegirmadan keyin 20000 − 5000 = 15000.|Yetkazish bilan 15000 + 3000 = 18000. || Сумма товаров — 20000.|После скидки 20000 − 5000 = 15000.|С доставкой 15000 + 3000 = 18000.', '18000 so‘m || 18000 сумов', [
            s('O‘rtacha baho dasturini qaysi tartibda tuzish ma’qul? || В каком порядке удобно построить программу среднего балла?', [
                ('Baholarni olish → tekshirish → yig‘indi va son → o‘rtacha || Получить оценки → проверить → сумма и количество → среднее', 'Bo‘lishdan avval yig‘indi va bo‘luvchi tayyor. || До деления подготовлены сумма и делитель.'),
                ('O‘rtacha → baholarni olish → yig‘indi || Среднее → получить оценки → сумма', 'Hali olinmagan ma’lumot bilan o‘rtacha hisoblanmaydi. || Среднее нельзя вычислить по ещё не полученным данным.'),
                ('Faqat oynaning rangini tanlash || Только выбрать цвет окна', 'Bu hisoblash vazifasini qismlarga ajratmaydi. || Это не разбивает вычислительную задачу на части.')],
              'Kirish va tekshirish birinchi.|Hisoblash natijalari ketma-ket keyingi qismga uzatiladi. || Вход и проверка идут первыми.|Результаты вычислений последовательно передаются следующей части.',
              'Hisoblashni o‘z kirishidan oldin joylashtirmang. || Не ставьте вычисление раньше его входных данных.',
              'Har bosqichga avvalgi bosqich nimani beradi? || Что предыдущий этап передаёт каждому следующему?'),
            n('Buyum 80000 so‘m. Avval 10000 so‘m chegirma, so‘ng 5000 so‘m yetkazish. Jami qancha? || Товар стоит 80000 сумов. Сначала скидка 10000 сумов, затем доставка 5000 сумов. Каков итог?', 75000,
              '80000 − 10000 = 70000.|70000 + 5000 = 75000. || 80000 − 10000 = 70000.|70000 + 5000 = 75000.',
              'Yetkazishni chegirma sifatida ayirmang. || Не вычитайте доставку как скидку.',
              'Chegirma kamaytiradi, yetkazish oshiradi. || Скидка уменьшает сумму, доставка увеличивает.'),
            s('Ro‘yxat bo‘sh bo‘lishi mumkin. O‘rtachani hisoblashdan oldingi qaysi kichik vazifa zarur? || Список может быть пустым. Какая подзадача нужна до вычисления среднего?', [
                ('Elementlar soni nol emasligini tekshirish || Проверить, что количество элементов не равно нулю', 'Bu nolga bo‘lishni oldini oladi. || Это предотвращает деление на ноль.'),
                ('Natijani oldindan yaxlitlash || Заранее округлить результат', 'Hisoblanmagan qiymatni yaxlitlash bo‘sh ro‘yxatni hal qilmaydi. || Округление ещё не вычисленного значения не решает случай пустого списка.'),
                ('Barcha baholarni o‘chirib tashlash || Удалить все оценки', 'Bu kerakli ma’lumotni yo‘qotadi. || Это уничтожает нужные данные.')],
              'Bo‘luvchi — elementlar soni.|Son nol bo‘lsa o‘rtacha o‘rniga bo‘sh holat qaytariladi. || Делитель — количество элементов.|Если оно равно нулю, вместо среднего возвращается состояние пустого списка.',
              'Bo‘sh kirishni tekshirish hisoblashdan oldin turadi. || Проверка пустого входа должна предшествовать вычислению.'),
            n('Hisob: 3 ta mahsulot, har biri 20000 so‘m; umumiy summadan 15000 so‘m chegirma; keyin 7000 so‘m yetkazish. Jami? || Расчёт: 3 товара по 20000 сумов; скидка с общей суммы 15000 сумов; затем доставка 7000 сумов. Итого?', 52000,
              '3 × 20000 = 60000.|60000 − 15000 + 7000 = 52000. || 3 × 20000 = 60000.|60000 − 15000 + 7000 = 52000.',
              'Umumiy chegirmani har bir mahsulotdan ayirmang. || Не вычитайте общую скидку из цены каждого товара.')], ['algo-io']),
        l('algo-assignment', 'Ketma-ketlik va qiymat berish || Последовательность и присваивание', [
            'Psevdokodda x ← ifoda qiymat berish, x == y taqqoslashdir. O‘ng tomon avval hisoblanadi, so‘ng chap o‘zgaruvchi yangilanadi. || В псевдокоде x ← выражение означает присваивание, x == y — сравнение. Сначала вычисляется правая часть, затем обновляется левая переменная.',
            'Amallar yozilgan tartibda bajariladi. x ← x + 1 eski qiymatga qo‘shadi; tenglik tenglamasi sifatida yechilmaydi. || Действия выполняются в записанном порядке. x ← x + 1 увеличивает прежнее значение; это не уравнение для решения.',
            'Ikki qiymatni almashtirishda vaqtinchalik t kerak: t ← a; a ← b; b ← t. Aks holda bir qiymat ustidan yozilib yo‘qoladi. || При обмене двух значений нужна временная t: t ← a; a ← b; b ← t. Иначе одно значение будет перезаписано и потеряно.'
        ], 'x ← 4; y ← x + 3; x ← y × 2. Oxirgi x? || x ← 4; y ← x + 3; x ← y × 2. Чему равно конечное x?',
           'x dastlab 4.|y = 4 + 3 = 7.|x yangi qiymati 7 × 2 = 14. || Сначала x равно 4.|y = 4 + 3 = 7.|Новое значение x равно 7 × 2 = 14.', '14 || 14', [
            n('x ← 5; x ← x + 2; x ← x × 3. Oxirgi x? || x ← 5; x ← x + 2; x ← x × 3. Чему равно конечное x?', 21,
              'Yangilanishdan keyin x = 7.|Keyin x = 7 × 3 = 21. || После обновления x = 7.|Затем x = 7 × 3 = 21.',
              'Oxirgi amalda dastlabki qiymatni qayta ishlatmang. || В последнем действии не используйте снова исходное значение.',
              'Har satrdan keyin qiymat jadvalini yangilang. || Обновляйте таблицу значений после каждой строки.'),
            n('a ← 2; b ← 9; a ← b; b ← a. Oxirgi a + b? || a ← 2; b ← 9; a ← b; b ← a. Чему равно конечное a + b?', 18,
              'a ← b dan keyin a = 9.|b ← a dan keyin b = 9; yig‘indi 18. || После a ← b значение a = 9.|После b ← a значение b = 9; сумма равна 18.',
              'Bu vaqtinchalik o‘zgaruvchisiz almashtirish emas. || Это не обмен: временной переменной нет.',
              'Birinchi qiymat berishda a ning eski qiymati yo‘qoladi. || При первом присваивании прежнее значение a теряется.'),
            n('a ← 6; b ← 4; t ← a; a ← b; b ← t. Oxirgi b? || a ← 6; b ← 4; t ← a; a ← b; b ← t. Чему равно конечное b?', 6,
              't eski a qiymati 6 ni saqlaydi.|b ← t sabab b = 6. || t сохраняет прежнее a, равное 6.|Из-за b ← t получаем b = 6.',
              'Vaqtinchalik saqlangan qiymatni keyingi a bilan aralashtirmang. || Не путайте сохранённое значение с последующим a.'),
            n('x ← 3; y ← x × 2; x ← y − 1; y ← x + y. Oxirgi y? || x ← 3; y ← x × 2; x ← y − 1; y ← x + y. Чему равно конечное y?', 11,
              'y = 6, keyin x = 5.|y = 5 + 6 = 11. || y = 6, затем x = 5.|y = 5 + 6 = 11.',
              'Har bir o‘zgaruvchining eng so‘nggi qiymatini oling. || Берите последнее значение каждой переменной.')], ['algo-io']),
        l('algo-symbols', 'Blok-sxema belgilari va yo‘nalishlar || Символы и переходы блок-схемы', [
            'Ushbu kursdagi shartli belgilar: oval — boshlash/tugatish; parallelogramm — kirish/chiqish; to‘g‘ri to‘rtburchak — amal; romb — shart. Har belgi matn yorlig‘i bilan ham beriladi. || Обозначения курса: овал — начало/конец; параллелограмм — ввод/вывод; прямоугольник — действие; ромб — условие. У каждого символа также есть текстовая подпись.',
            'O‘qlar bajarish tartibini ko‘rsatadi. Rombdan TRUE va FALSE deb belgilangan yo‘llar chiqadi. Hisoblash amali bilan shartni farqlang. || Стрелки показывают порядок выполнения. Из ромба выходят ветви TRUE и FALSE. Отличайте вычисление от условия.',
            'Matnli yozuv ham sxemani ifodalaydi: START → INPUT x → DECISION x > 0; TRUE → OUTPUT musbat → END; FALSE → OUTPUT musbat emas → END. Har yo‘l tugashi yoki belgilangan takrorlashga qaytishi kerak. || Текстовая запись тоже описывает схему: START → INPUT x → DECISION x > 0; TRUE → OUTPUT положительное → END; FALSE → OUTPUT неположительное → END. Каждый путь должен завершаться или возвращаться к указанному повторению.'
        ], '“n juftmi?” tekshiruvi va “n ni chiqarish” uchun belgilarni tanlang. || Выберите символы для проверки «n чётное?» и для вывода n.',
           'Savol shart bo‘lgani uchun romb.|Chiqarish kirish/chiqish amali, parallelogramm.|Shartdan ikkita belgilangan yo‘l chiqadi. || Вопрос является условием, поэтому нужен ромб.|Вывод — операция ввода/вывода, нужен параллелограмм.|Из условия выходят две подписанные ветви.',
           'Romb; parallelogramm || Ромб; параллелограмм', [
            s('x ← x + 1 amali qaysi blokka yoziladi? || В какой блок записывается действие x ← x + 1?', [
                ('To‘g‘ri to‘rtburchak || Прямоугольник', 'Bu qiymatni yangilash amali. || Это действие обновления значения.'),
                ('Romb || Ромб', 'Bu yerda rost/yolg‘on savoli yo‘q. || Здесь нет вопроса с ответом истина/ложь.'),
                ('Oval || Овал', 'Oval boshlash yoki tugatish uchun. || Овал предназначен для начала или конца.')],
              'Qiymat hisoblanib yoziladi.|Hisoblash bloki to‘g‘ri to‘rtburchak. || Значение вычисляется и записывается.|Вычислительный блок — прямоугольник.',
              'Hisoblashni taqqoslash bilan almashtirmang. || Не заменяйте вычисление сравнением.',
              'Bu buyruq savol beradimi yoki qiymatni o‘zgartiradimi? || Эта команда задаёт вопрос или изменяет значение?'),
            s('DECISION x ≥ 10 dan x = 10 uchun qaysi yo‘l tanlanadi? || Какая ветвь выбирается из DECISION x ≥ 10 при x = 10?', [
                ('TRUE || TRUE', 'Tenglik ≥ shartiga kiradi. || Равенство входит в условие ≥.'),
                ('FALSE || FALSE', '≥ faqat qat’iy kattalik emas. || ≥ означает не только строго больше.'),
                ('Ikkala yo‘l birga || Обе ветви одновременно', 'Bitta tekshiruv natijasi bitta yo‘lni tanlaydi. || Один результат проверки выбирает одну ветвь.')],
              '10 ≥ 10 rost.|Shuning uchun TRUE yo‘li olinadi. || 10 ≥ 10 истинно.|Поэтому выбирается ветвь TRUE.',
              'Chegaradagi tenglikni unutmang. || Не забывайте равенство на границе.',
              '≥ belgisi tenglikni ham o‘z ichiga oladi. || Знак ≥ включает равенство.'),
            s('Qaysi blok kirish/chiqishga tegishli? || Какой блок относится к вводу/выводу?', [
                ('Parallelogramm || Параллелограмм', 'Kursdagi kirish/chiqish belgisi shu. || Это обозначение ввода/вывода в курсе.'),
                ('Romb || Ромб', 'Romb shartni bildiradi. || Ромб обозначает условие.'),
                ('Oval || Овал', 'Oval bajarilishning boshlanishi yoki oxiri. || Овал обозначает начало или конец выполнения.')],
              'INPUT va OUTPUT ma’lumot almashadi.|Ular parallelogramm bilan ko‘rsatiladi. || INPUT и OUTPUT обмениваются данными.|Они изображаются параллелограммом.',
              'Blok nomini uning vazifasidan ajrating. || Определяйте блок по его назначению.'),
            s('Sxema: START → INPUT x → DECISION x < 0; TRUE → OUTPUT 1 → END; FALSE → OUTPUT 0 → END. x = 0 da chiqish? || Схема: START → INPUT x → DECISION x < 0; TRUE → OUTPUT 1 → END; FALSE → OUTPUT 0 → END. Каков выход при x = 0?', [
                ('0 || 0', 'Nol manfiy emas, FALSE yo‘li olinadi. || Ноль не отрицателен, выбирается FALSE.'),
                ('1 || 1', 'Bu TRUE yo‘lining chiqishi. || Это выход ветви TRUE.'),
                ('Chiqish yo‘q || Выхода нет', 'FALSE yo‘lida ham OUTPUT bor. || В ветви FALSE тоже есть OUTPUT.')],
              '0 < 0 yolg‘on.|FALSE yo‘li 0 ni chiqarib tugaydi. || 0 < 0 ложно.|Ветвь FALSE выводит 0 и завершается.',
              'Rombdan keyingi yorliqni tekshirmay chiqishni tanlamang. || Не выбирайте выход, не проверив подпись ветви после ромба.')], ['algo-assignment']),
        l('algo-trace', 'Algoritmni qadam bilan tekshirish || Пошаговая проверка алгоритма', [
            'Kuzatish jadvalida buyruqdan keyingi o‘zgaruvchilar va chiqarilgan qiymatlar alohida yoziladi. OUTPUT qiymatni ko‘rsatadi, o‘zgaruvchini o‘zgartirmaydi. || В таблице трассировки отдельно записываются значения переменных после команды и выведенные значения. OUTPUT показывает значение, но не меняет переменную.',
            'Oddiy, chegaraviy va yaroqsiz kirishni farqlang. Musbat yosh talab qilinsa, nol yoki manfiy qiymatni hisoblashdan oldin qaytarish kerak. || Различайте обычный, граничный и недопустимый вход. Если требуется положительный возраст, ноль или отрицательное значение нужно отклонить до вычисления.',
            'Bir muvaffaqiyatli misol algoritmni barcha kirishda to‘g‘ri qilmaydi. Avval kichik kirishlar bilan qo‘lda kuzating, keyin shartni buzadigan qarshi misol qidiring. || Один успешный пример не доказывает правильность на всех входах. Сначала проследите малые примеры вручную, затем ищите контрпример.'
        ], 'x ← 2; OUTPUT x; x ← x + 5; OUTPUT x. Chiqishlar ketma-ketligi? || x ← 2; OUTPUT x; x ← x + 5; OUTPUT x. Какова последовательность выводов?',
           'Birinchi OUTPUT 2 ni chiqaradi.|Yangilanishdan keyin x = 7.|Ikkinchi OUTPUT 7 ni chiqaradi. || Первый OUTPUT выводит 2.|После обновления x = 7.|Второй OUTPUT выводит 7.', '2, 7 || 2, 7', [
            n('a ← 8; OUTPUT a; a ← a − 3; OUTPUT a. Faqat oxirgi chiqarilgan sonni yozing. || a ← 8; OUTPUT a; a ← a − 3; OUTPUT a. Запишите только последнее выведенное число.', 5,
              'Birinchi chiqish 8.|a yangilangach 5, oxirgi chiqish 5. || Первый вывод — 8.|После обновления a равно 5, последний вывод — 5.',
              'Birinchi va oxirgi chiqishni aralashtirmang. || Не путайте первый и последний вывод.',
              'OUTPUTdan keyin ham buyruqlar davom etadi. || После OUTPUT выполнение команд продолжается.'),
            s('n musbat butun bo‘lishi kerak. Qaysi to‘plam odatiy, chegara va yaroqsiz holatni qamraydi? || n должно быть положительным целым. Какой набор охватывает обычный, граничный и недопустимый случаи?', [
                ('5, 1, 0 || 5, 1, 0', '5 odatiy, 1 eng kichik yaroqli, 0 yaroqsiz. || 5 — обычное, 1 — минимальное допустимое, 0 — недопустимое.'),
                ('5, 6, 7 || 5, 6, 7', 'Barchasi yaroqli ichki qiymatlar. || Все значения допустимы и не граничны.'),
                ('0, −1, −2 || 0, −1, −2', 'Bu to‘plamda yaroqli holat yo‘q. || В этом наборе нет допустимого случая.')],
              'Talab n > 0.|Eng kichik yaroqli 1, uning ostidagi 0 ni ham tekshiring. || Требование: n > 0.|Минимальное допустимое — 1, проверьте и стоящий ниже 0.',
              'Faqat bir xil turdagi misollar bilan cheklanmang. || Не ограничивайтесь примерами одного типа.',
              'Talab bajarilishining eng chet nuqtasini toping. || Найдите крайнюю точку выполнения требования.'),
            n('x ← 7; y ← x; x ← 2; OUTPUT y. Chiqish? || x ← 7; y ← x; x ← 2; OUTPUT y. Каков выход?', 7,
              'y ga shu paytdagi 7 nusxalanadi.|x ni o‘zgartirish y ni o‘zgartirmaydi. || В y копируется текущее значение 7.|Изменение x не изменяет y.',
              'Qiymat nusxasini doimiy bog‘lanish deb tushunmang. || Не считайте копирование значения постоянной связью.'),
            s('“Har qanday a va b uchun kattasini topadi” degan algoritm faqat a > b da OUTPUT a qiladi. Qaysi kirish kamchilikni ko‘rsatadi? || Алгоритм «находит максимум для любых a и b» выполняет OUTPUT a только при a > b. Какой вход выявляет недостаток?', [
                ('a = 2, b = 5 || a = 2, b = 5', 'Shart yolg‘on, lekin 5 chiqarilishi kerak; algoritm chiqish bermaydi. || Условие ложно, но должно выводиться 5; алгоритм ничего не выводит.'),
                ('a = 5, b = 2 || a = 5, b = 2', 'Bu kirishda katta a chiqariladi, kamchilik ochilmaydi. || На этом входе выводится большее a, недостаток не выявляется.'),
                ('a = 9, b = 1 || a = 9, b = 1', 'Bu ham a katta bo‘lgan muvaffaqiyatli holat. || Это тоже успешный случай, когда a больше.')],
              'a > b bo‘lmagan holatni oling.|b katta bo‘lsa ham chiqish bo‘lishi kerak. || Возьмите случай, когда a > b не выполняется.|Даже если b больше, результат должен выводиться.',
              'Faqat ishlaydigan tarmoqni sinash boshqa yo‘lni tekshirmaydi. || Проверка только работающей ветви не проверяет другой путь.')], ['algo-assignment', 'algo-symbols'])])
