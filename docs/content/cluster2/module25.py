from authoring import lesson as l, module, n, s


def build():
    return module('real-world-problem-solving', 5,
        'Hayotiy muammolarni algoritmga aylantirish || Преобразование жизненных задач в алгоритмы', ['problem_solving', 'algorithmic'], [
        l('case-contract', 'Talabdan kirish va chiqishga || От требования к входу и выходу', [
            'Hayotiy gapni hisoblash vazifasiga aylantirish uchun maqsad, kirish, chiqish, birlik va cheklovlarni yozing. Noaniq iborani kod bilan yashirmang. || Чтобы превратить жизненное описание в вычислительную задачу, запишите цель, вход, выход, единицы и ограничения. Не скрывайте неопределённость кодом.',
            'Tarif o‘quv misoli bo‘lsa barcha narx va qoidalar shartning o‘zida beriladi. Ular haqiqiy xizmatning amaldagi narxi yoki moliyaviy tavsiya emas. || В учебном примере тарифа все цены и правила задаются в условии. Это не действующая цена реального сервиса и не финансовая рекомендация.',
            'Masalan, kutubxona kechikish haqini hisoblashda kunlar butunmi, imtiyozli davr bormi, manfiy kirish qanday qaytarilishi aniqlanadi. Talab kelishilmasdan to‘g‘ri chiqishni belgilab bo‘lmaydi. || Например, для платы за просрочку в библиотеке уточняют целочисленность дней, льготный период и обработку отрицательного входа. Без согласования требований нельзя определить правильный выход.'
        ], 'O‘quv tarifida kunlik ijara 7000 so‘m, butun kunlar soni 3. Jami to‘lov? || В учебном тарифе аренда стоит 7000 сумов за день, число полных дней — 3. Какова общая плата?',
           'Kirish: kunlik narx va kunlar.|To‘lov = 7000 × 3.|Chiqish 21000 so‘m. || Вход: дневная цена и дни.|Плата = 7000 × 3.|Выход — 21000 сумов.', '21000 so‘m || 21000 сумов', [
            s('“Eng qulay yo‘lni toping” talabi uchun avval nimani aniqlash kerak? || Что сначала нужно уточнить в требовании «найдите самый удобный маршрут»?', [
                ('Qulaylik mezoni: vaqtmi, narxmi yoki boshqa talabmi || Критерий удобства: время, цена или другое требование', 'Mezonsiz eng yaxshi chiqish noaniq. || Без критерия лучший результат неопределён.'),
                ('Tugma rangini || Цвет кнопки', 'Bu yo‘lni tanlash mezonini belgilamaydi. || Это не задаёт критерий выбора маршрута.'),
                ('Tasodifiy bitta yo‘lni eng qulay deb olish || Объявить случайный маршрут самым удобным', 'Bu foydalanuvchi talabini tekshirmaydi. || Это не проверяет требование пользователя.')],
              '“Qulay” o‘lchanadigan mezonga aylantiriladi.|Shundan keyin variantlar solishtiriladi. || «Удобно» преобразуется в измеримый критерий.|Затем сравниваются варианты.',
              'Noaniq maqsadni taxmin bilan yopmang. || Не закрывайте неясную цель догадкой.',
              'Ikki yo‘ldan qaysi birini afzal deyishga nima asos bo‘ladi? || На каком основании один из двух маршрутов предпочтительнее?'),
            n('O‘quv shartida quti narxi 9000 so‘m, miqdor 5, qo‘shimcha to‘lov yo‘q. Jami? || В учебном условии коробка стоит 9000 сумов, количество — 5, доплат нет. Итого?', 45000,
              'Narx va miqdor ko‘paytiriladi.|9000 × 5 = 45000. || Цена умножается на количество.|9000 × 5 = 45000.',
              'Shartda yo‘q komissiya yoki chegirmani qo‘shmang. || Не добавляйте комиссию или скидку, которых нет в условии.',
              'Faqat berilgan qoidalardan foydalaning. || Используйте только заданные правила.'),
            s('Masofa km, tezlik km/soat; chiqish vaqt soatda. Qaysi formula mos? Tezlik musbat. || Расстояние в км, скорость в км/час; выход — время в часах. Какая формула подходит? Скорость положительна.', [
                ('vaqt = masofa / tezlik || время = расстояние / скорость', 'Birliklar soatni beradi. || Единицы дают часы.'),
                ('vaqt = masofa × tezlik || время = расстояние × скорость', 'Birliklar vaqt emas. || Единицы не соответствуют времени.'),
                ('vaqt = masofa + tezlik || время = расстояние + скорость', 'Turli birlikdagi miqdorlar bunday qo‘shilmaydi. || Величины с разными единицами так не складываются.')],
              'Vaqt = yo‘l / tezlik.|km ni km/soat ga bo‘lish soat beradi. || Время = путь / скорость.|Деление км на км/час даёт часы.',
              'Formulani birliklari bilan tekshiring. || Проверяйте формулу по единицам.'),
            s('Buyurtma summasi uchun manfiy miqdor kiritildi, talab esa musbat butun miqdor. To‘g‘ri chiqish qanday? || Для суммы заказа введено отрицательное количество, а требуется положительное целое. Каков правильный выход?', [
                ('Hisoblamasdan, miqdorni tuzatish xabari || Без расчёта сообщить о необходимости исправить количество', 'Yaroqsiz kirish shartnomaga mos qaytariladi. || Недопустимый вход обрабатывается по контракту.'),
                ('Manfiy to‘lovni tayyor buyurtma deb ko‘rsatish || Показать отрицательную плату как готовый заказ', 'Bu yaroqsiz kirishni qabul qiladi. || Это принимает недопустимый вход.'),
                ('Miqdorni yashirincha musbatga aylantirish || Скрыто сделать количество положительным', 'Bu foydalanuvchi bergan ma’lumotni kelishilmagan tarzda o‘zgartiradi. || Это несогласованно меняет введённые данные.')],
              'Miqdor talabni buzgan.|Hisoblash o‘rniga xato holati va tuzatish yo‘li beriladi. || Количество нарушает требование.|Вместо расчёта выдаются состояние ошибки и путь исправления.',
              'Kirishni yashirin tuzatish bilan validatsiyani almashtirmang. || Не заменяйте валидацию скрытым исправлением входа.')]),
        l('case-validation', 'Cheklovlar va yaroqsiz kirish || Ограничения и недопустимый вход', [
            'Kiritilgan matnni son sifatida o‘qish mumkinligi, son diapazoni va birliklari alohida tekshiriladi. “abc” son emas; manfiy masofa esa son bo‘lsa ham vazifada yaroqsiz. || Отдельно проверяются возможность прочитать текст как число, диапазон и единицы. «abc» — не число; отрицательное расстояние — число, но недопустимое в задаче.',
            'Tekshirishni hisoblashdan oldin bajaring. Noto‘g‘ri kirishda natijani nol deb berish xato bilan haqiqiy nolni ajratishni qiyinlashtiradi. || Выполняйте проверку до вычисления. Возврат нуля при неверном входе мешает отличать ошибку от настоящего нулевого результата.',
            'Xabar qaysi maydonni va qanday tuzatishni aytsin. Shaxsiy ma’lumot yoki texnik ichki xato tafsilotlari o‘rniga foydalanuvchiga kerakli ko‘rsatma bering. || Сообщение должно указывать поле и способ исправления. Вместо персональных данных или внутренних технических деталей давайте нужную пользователю инструкцию.'
        ], 'Ishtirokchilar soni butun va 1 dan 30 gacha. 0 kiritilsa nima qilinadi? || Число участников должно быть целым от 1 до 30. Что делать при вводе 0?',
           '0 pastki chegaradan kichik.|Hisoblash boshlanmaydi.|Ruxsatli oraliqni ko‘rsatuvchi xabar beriladi. || 0 ниже нижней границы.|Вычисление не начинается.|Выдаётся сообщение с допустимым интервалом.', 'Kirish rad etiladi || Вход отклоняется', [
            s('n butun, 1 ≤ n ≤ 30. Qaysi kirish yaroqli? || n — целое, 1 ≤ n ≤ 30. Какой вход допустим?', [
                ('30 || 30', 'Yuqori chegara kiritilgan va son butun. || Верхняя граница включена, число целое.'),
                ('0 || 0', 'Pastki chegaradan kichik. || Ниже нижней границы.'),
                ('2.5 || 2.5', 'Oraliqda bo‘lsa ham butun emas. || Хотя в интервале, но не целое.')],
              'Butunlik va ikkala chegara tekshiriladi.|Faqat 30 barcha talabni bajaradi. || Проверяются целочисленность и обе границы.|Только 30 выполняет все требования.',
              'Diapazonning o‘zi tur talabini almashtirmaydi. || Один диапазон не заменяет требование типа.',
              'Talablar birgalikda bajarilishi kerak. || Требования должны выполняться совместно.'),
            s('Son maydonida “abc” kiritildi. Qaysi xabar foydali? || В числовом поле введено «abc». Какое сообщение полезно?', [
                ('Miqdor maydoniga musbat butun son kiriting || Введите положительное целое число в поле количества', 'Maydon va tuzatish usuli aniq. || Понятны поле и способ исправления.'),
                ('Xato! || Ошибка!', 'Tuzatish yo‘li aytilmagan. || Не указан путь исправления.'),
                ('Natija: 0 || Результат: 0', 'Yaroqsiz kirish to‘g‘ri natijadek ko‘rsatilgan. || Недопустимый вход показан как правильный результат.')],
              'Kirish son emas.|Xabar kerakli maydon va ruxsatli formatni aytadi. || Вход не является числом.|Сообщение указывает нужное поле и допустимый формат.',
              'Xato va hisoblangan natijani bir ko‘rinishda bermang. || Не представляйте ошибку и вычисленный результат одинаково.',
              'Talaba keyin nima qilishini bilishi kerak. || Пользователь должен понимать следующий шаг.'),
            s('Cheklov: 0 ≤ d ≤ 100. Qaysi qiymat yaroqsiz? || Ограничение: 0 ≤ d ≤ 100. Какое значение недопустимо?', [
                ('−1 || −1', 'Pastki chegaradan kichik. || Ниже нижней границы.'),
                ('0 || 0', 'Pastki chegara kiritilgan. || Нижняя граница включена.'),
                ('100 || 100', 'Yuqori chegara kiritilgan. || Верхняя граница включена.')],
              'Ikkala chegara yaroqli.|Manfiy qiymat oraliqdan tashqarida. || Обе границы допустимы.|Отрицательное значение вне интервала.',
              'Tenglik belgisi chegarani qamrashini unutmang. || Не забывайте, что равенство включает границу.'),
            s('Hisob: total = price × quantity. quantity yaroqsiz bo‘lsa qaysi tartib mos? || Расчёт: total = price × quantity. Какой порядок подходит при недопустимом quantity?', [
                ('Tekshirish → xabar → hisobni to‘xtatish || Проверка → сообщение → остановка расчёта', 'Natija yaroqsiz kirishdan hosil qilinmaydi. || Результат не формируется из недопустимого входа.'),
                ('Hisoblash → qabul qilish → tekshirish || Вычисление → принятие → проверка', 'Qabul qilishdan keyingi tekshirish juda kech. || Проверка после принятия слишком поздняя.'),
                ('Xatoni yashirish → total ni ko‘rsatish || Скрыть ошибку → показать total', 'Bu foydalanuvchini chalg‘itadi. || Это вводит пользователя в заблуждение.')],
              'Avval kirish talablari tekshiriladi.|Yaroqsiz bo‘lsa hisoblash tarmog‘iga o‘tilmaydi. || Сначала проверяются требования к входу.|При недопустимости перехода к вычислению нет.',
              'Validatsiya faqat xabar emas, jarayonni boshqarish hamdir. || Валидация — это и управление процессом, а не только сообщение.')], ['case-contract', 'cond-boolean']),
        l('case-taxi', 'Bosqichli taksi tarifi modeli || Модель ступенчатого тарифа такси', [
            'Bu o‘quv modelida bazaviy to‘lov b dastlabki k kilometrni qoplaydi. d ≤ k bo‘lsa to‘lov b, d > k bo‘lsa b + (d − k) × r. Bu yerda d manfiy bo‘lmagan butun kilometr. || В учебной модели базовая плата b покрывает первые k километров. При d ≤ k плата b, при d > k — b + (d − k) × r. Здесь d — неотрицательное целое число километров.',
            'Chegaradan oshgan qism alohida hisoblanadi. Bazaga kiritilgan masofani yana narxlash ikki marta haq hisoblashga olib keladi. || Превышение границы считается отдельно. Повторная тарификация включённого расстояния приводит к двойному начислению.',
            'Shartda kutish, vaqt yoki yaxlitlash berilmagan bo‘lsa ularni o‘zingizcha qo‘shmang. Tarifning chegarasida va uning ikki yonida tekshirish qiling. || Если ожидание, время или округление не заданы, не добавляйте их сами. Проверяйте границу тарифа и значения по обе стороны.'
        ], 'b = 10000, k = 2, r = 3000; d = 5. To‘lov? || b = 10000, k = 2, r = 3000; d = 5. Какова плата?',
           'Ortiqcha masofa 5 − 2 = 3.|Qo‘shimcha 3 × 3000 = 9000.|Jami 10000 + 9000 = 19000. || Превышение: 5 − 2 = 3.|Доплата: 3 × 3000 = 9000.|Итого: 10000 + 9000 = 19000.', '19000 || 19000', [
            n('O‘quv tarifi: b = 12000, k = 3, r = 2000. d = 7 da to‘lov? || Учебный тариф: b = 12000, k = 3, r = 2000. Какова плата при d = 7?', 20000,
              'Ortiqcha masofa 7 − 3 = 4.|12000 + 4 × 2000 = 20000. || Превышение: 7 − 3 = 4.|12000 + 4 × 2000 = 20000.',
              'Barcha masofani qo‘shimcha tarifga ko‘paytirmang. || Не умножайте всё расстояние на дополнительный тариф.',
              'Baza allaqachon dastlabki masofani qoplaydi. || База уже покрывает начальное расстояние.'),
            n('b = 12000, k = 3, r = 2000. d = 2 da to‘lov? || b = 12000, k = 3, r = 2000. Какова плата при d = 2?', 12000,
              '2 ≤ 3, qo‘shimcha masofa yo‘q.|Bazaviy to‘lov 12000 saqlanadi. || 2 ≤ 3, превышения нет.|Базовая плата остаётся 12000.',
              'Bazadan kam masofaga manfiy qo‘shimcha bermang. || Не начисляйте отрицательную доплату за расстояние меньше включённого.',
              'Avval masofa qaysi tarmoqqa tushishini toping. || Сначала определите ветвь для расстояния.'),
            n('b = 9000, k = 2, r = 2500. d = 2 da to‘lov? || b = 9000, k = 2, r = 2500. Какова плата при d = 2?', 9000,
              'Chegaraning o‘zi bazaga kiradi.|Qo‘shimcha yo‘q, to‘lov 9000. || Сама граница входит в базу.|Доплаты нет, плата 9000.',
              'Chegaradagi masofani ortiqcha deb olmang. || Не считайте расстояние на границе превышением.'),
            n('b = 15000, k = 4, r = 3000. d = 6 da bazaga qo‘shiladigan QO‘SHIMCHA to‘lovni toping. || b = 15000, k = 4, r = 3000. При d = 6 найдите ДОПЛАТУ к базе.', 6000,
              'Ortiqcha masofa 6 − 4 = 2.|Faqat qo‘shimcha 2 × 3000 = 6000. || Превышение: 6 − 4 = 2.|Только доплата: 2 × 3000 = 6000.',
              'Jami to‘lov bilan so‘ralgan qo‘shimchani aralashtirmang. || Не путайте общую плату и запрошенную доплату.')], ['case-validation', 'cond-if']),
        l('case-atm', 'Soddalashtirilgan bankomat modeli || Упрощённая модель банкомата', [
            'O‘quv modelida yechish so‘rovi musbat, balansdan oshmasligi va mavjud yagona nominalga qoldiqsiz bo‘linishi kerak. Komissiya va bank qoidalari ushbu modelga kiritilmagan. || В учебной модели запрос снятия должен быть положительным, не превышать баланс и делиться без остатка на единственный доступный номинал. Комиссии и правила банков в модель не включены.',
            'Qabul sharti: (amount > 0) AND (amount ≤ balance) AND (amount mod note == 0). Faqat barchasi bajarilgach yangi balans = balance − amount. || Условие принятия: (amount > 0) AND (amount ≤ balance) AND (amount mod note == 0). Только после выполнения всех условий новый баланс = balance − amount.',
            'Rad etilganda balans o‘zgarmaydi. Haqiqiy bankomatda kupyuralar zaxirasi va boshqa cheklovlar ham bor; bu yerda yagona nominal zaxirasi yetarli deb beriladi. || При отказе баланс не меняется. У реального банкомата есть запас купюр и другие ограничения; здесь задано достаточное количество купюр единственного номинала.'
        ], 'balance = 100000, note = 10000, amount = 30000. So‘rov va yangi balans? || balance = 100000, note = 10000, amount = 30000. Принят ли запрос и каков новый баланс?',
           'Miqdor musbat va balansdan oshmaydi.|30000 mod 10000 = 0.|Qabul qilinadi, balans 100000 − 30000 = 70000. || Сумма положительна и не превышает баланс.|30000 mod 10000 = 0.|Запрос принят, баланс 100000 − 30000 = 70000.', 'Qabul; 70000 || Принят; 70000', [
            n('balance = 80000, note = 10000, amount = 50000. Yangi balans? Nominal zaxirasi yetarli. || balance = 80000, note = 10000, amount = 50000. Каков новый баланс? Купюр достаточно.', 30000,
              'Uchala shart bajariladi.|80000 − 50000 = 30000. || Все три условия выполнены.|80000 − 50000 = 30000.',
              'Qabuldan keyin yechilgan summani ayiring. || После принятия вычтите снятую сумму.',
              'Avval qabul shartlarini, keyin balansni tekshiring. || Сначала проверьте условия принятия, затем баланс.'),
            s('balance = 100000, note = 20000, amount = 30000. Nominal zaxirasi yetarli. Qaror? || balance = 100000, note = 20000, amount = 30000. Купюр достаточно. Каково решение?', [
                ('Rad: nominalga qoldiqsiz bo‘linmaydi || Отказ: нет деления на номинал без остатка', '30000 mod 20000 = 10000, shart bajarilmagan. || 30000 mod 20000 = 10000, условие не выполнено.'),
                ('Qabul: balans yetarli || Принять: баланса достаточно', 'Balans faqat bitta shart. || Баланс — только одно условие.'),
                ('Qabul: so‘rov musbat || Принять: запрос положителен', 'Musbatlik boshqa talablarni bekor qilmaydi. || Положительность не отменяет другие требования.')],
              'So‘rov balansga sig‘adi.|Lekin yagona nominal bilan aynan chiqarib bo‘lmaydi, balans o‘zgarmaydi. || Запрос укладывается в баланс.|Но единственным номиналом точно выдать нельзя, баланс не меняется.',
              'Balans yetarli bo‘lishi o‘zi yetarli emas. || Одной достаточности баланса недостаточно.',
              'Qoldiqni hisoblab ko‘ring. || Вычислите остаток.'),
            n('balance = 40000, note = 10000, amount = 50000. Rad etilgan so‘rovdan keyingi balans? || balance = 40000, note = 10000, amount = 50000. Каков баланс после отклонённого запроса?', 40000,
              'So‘rov balansdan katta.|Rad etiladi, avvalgi 40000 qoladi. || Запрос больше баланса.|Он отклоняется, остаются прежние 40000.',
              'Tekshiruvdan oldin balansni kamaytirmang. || Не уменьшайте баланс до проверки.'),
            s('balance = 60000, note = 10000, amount = 0. Qaror? || balance = 60000, note = 10000, amount = 0. Каково решение?', [
                ('Rad: so‘rov musbat emas || Отказ: запрос не положителен', 'Nol nominalga bo‘linsa ham musbatlik talabini buzadi. || Даже делясь на номинал, ноль нарушает требование положительности.'),
                ('Qabul: qoldiq nol || Принять: остаток нулевой', 'Bitta shart yetarli emas. || Одного условия недостаточно.'),
                ('Balansni nol qilish || Обнулить баланс', 'Rad yoki nol so‘rov balansni o‘chirmaydi. || Отказ или нулевой запрос не обнуляет баланс.')],
              'amount > 0 sharti yolg‘on.|So‘rov rad, balans o‘zgarmaydi. || Условие amount > 0 ложно.|Запрос отклонён, баланс не меняется.',
              'Nolning qoldiq xossasini musbatlik bilan aralashtirmang. || Не путайте свойство остатка нуля с положительностью.')], ['case-validation', 'cond-boolean']),
        l('case-tests', 'Test holatlari va kutilgan natija || Тестовые случаи и ожидаемый результат', [
            'Test holatida kirish bilan birga kutilgan chiqish yoziladi. Faqat “tekshirildi” deyish natijaning to‘g‘riligini tekshirishga yetmaydi. || В тестовом случае вместе с входом записывается ожидаемый выход. Одного слова «проверено» недостаточно для проверки правильности результата.',
            'Shart tarmoqlari uchun har xil yo‘lga tushadigan kirishlarni oling. Tarif chegarasidan past, aynan unda va yuqorida holatlar xatolarni ochishga yordam beradi. || Для ветвей условия берите входы, ведущие по разным путям. Значения ниже границы тарифа, на ней и выше помогают выявлять ошибки.',
            'Invariant — butun jarayonda saqlanishi kerak bo‘lgan xossa. Rad etilgan yechishdan keyin balans o‘zgarmasligi yoki qabul qilinganidan keyin kamayish miqdori so‘rovga tengligi tekshiriladi. || Инвариант — свойство, которое должно сохраняться в процессе. Проверяют неизменность баланса после отказа или равенство уменьшения принятой сумме.'
        ], 'O‘quv tarifi: b = 10000, k = 2, r = 3000. d = 1, 2, 3 uchun test jadvali tuzing. || Учебный тариф: b = 10000, k = 2, r = 3000. Составьте таблицу тестов для d = 1, 2, 3.',
           'd = 1: 10000.|d = 2: 10000.|d = 3: 10000 + 3000 = 13000. || d = 1: 10000.|d = 2: 10000.|d = 3: 10000 + 3000 = 13000.', '10000; 10000; 13000 || 10000; 10000; 13000', [
            s('Chegara k = 4. Qaysi masofalar to‘plami uning ikki yoni va o‘zini tekshiradi? || Граница k = 4. Какой набор расстояний проверяет её саму и обе стороны?', [
                ('3, 4, 5 || 3, 4, 5', 'Past, teng va yuqori holatlar bor. || Есть случаи ниже, на границе и выше.'),
                ('1, 2, 3 || 1, 2, 3', 'Barchasi chegaradan past. || Все значения ниже границы.'),
                ('5, 6, 7 || 5, 6, 7', 'Barchasi chegaradan yuqori. || Все значения выше границы.')],
              'Chegaradan bir qadam past va yuqorini oling.|Chegaraning o‘zini ham qo‘shing. || Возьмите по шагу ниже и выше границы.|Добавьте саму границу.',
              'Faqat bir tarmoqni tekshiruvchi misollardan foydalanmang. || Не используйте только примеры одной ветви.',
              'Uch holat: past, teng, yuqori. || Три случая: ниже, равно, выше.'),
            n('Tarif: b = 8000, k = 1, r = 2000. d = 3 uchun testdagi kutilgan JAMI chiqish? || Тариф: b = 8000, k = 1, r = 2000. Каков ожидаемый ОБЩИЙ выход теста при d = 3?', 12000,
              'Qo‘shimcha masofa 3 − 1 = 2.|8000 + 2 × 2000 = 12000. || Превышение: 3 − 1 = 2.|8000 + 2 × 2000 = 12000.',
              'Test kutilgan natijasi ham mustaqil hisoblanishi kerak. || Ожидаемый результат теста тоже нужно вычислять независимо.',
              'Bazaga faqat ortiqcha masofa haqini qo‘shing. || Добавьте к базе только плату за превышение.'),
            s('So‘rov rad etildi. Qaysi invariant tekshiriladi? || Запрос отклонён. Какой инвариант проверяется?', [
                ('Yakuniy balans boshlang‘ich balansga teng || Конечный баланс равен исходному', 'Rad etish mablag‘ni o‘zgartirmaydi. || Отказ не изменяет средства.'),
                ('Yakuniy balans nol || Конечный баланс равен нулю', 'Rad javobi hisobni bo‘shatmaydi. || Отказ не опустошает счёт.'),
                ('Balans har safar oshadi || Баланс каждый раз увеличивается', 'Bunday qoida berilmagan. || Такое правило не задано.')],
              'Rad tarmog‘ida hisob yangilanishi yo‘q.|Oldingi balans saqlanishi kerak. || В ветви отказа нет обновления счёта.|Прежний баланс должен сохраниться.',
              'Xato tarmog‘idagi yon ta’sirlarni ham tekshiring. || Проверяйте и побочные эффекты в ветви ошибки.'),
            s('Testda faqat kirish yozilgan, kutilgan chiqish yo‘q. Nima yetishmaydi? || В тесте записан только вход, ожидаемого выхода нет. Чего не хватает?', [
                ('Natijani solishtirish uchun aniq mezon || Явного критерия для сравнения результата', 'Kutilgan chiqish to‘g‘ri va noto‘g‘rini ajratadi. || Ожидаемый выход различает правильное и неправильное.'),
                ('Faqat ekran fon rasmi || Только фоновой картинки экрана', 'Rasm hisob to‘g‘riligini baholamaydi. || Картинка не оценивает правильность вычисления.'),
                ('Ko‘proq tasodifiy tugma bosish || Больше случайных нажатий кнопок', 'Mezonsiz ko‘proq harakat muammoni hal qilmaydi. || Больше действий без критерия не решают проблему.')],
              'Test kirishi bajariladi.|Chiqqan natija oldindan belgilangan kutilgan qiymatga solishtiriladi. || Тестовый вход выполняется.|Полученный результат сравнивается с заранее определённым ожидаемым значением.',
              'Har testga tekshiriladigan natija yoki xossa yozing. || Для каждого теста записывайте проверяемый результат или свойство.')], ['case-taxi', 'case-atm'])])
