from authoring import lesson as l, module, n, s


def build():
    return module('loops-recursion', 3, 'Takrorlash operatorlari va rekursiya || Циклы и рекурсия', ['algorithmic'], [
        l('loop-for', 'for va takrorlanish chegaralari || for и границы повторения', [
            'Kursda for i ← a TO b {amal} butun i ni a dan b gacha oshirib yuradi; ikkala chegara kiritiladi. a > b bo‘lsa tana bajarilmaydi. Bu Python range qoidasidan farq qiladi. || В курсе for i ← a TO b {действие} увеличивает целое i от a до b; обе границы включены. При a > b тело не выполняется. Это отличается от правила Python range.',
            'Hisoblagich iteratsiya qiymatini, jamlagich esa umumiy natijani saqlaydi. Yig‘indi uchun s ← 0 sikldan oldin yoziladi; tanada s ← s + i yangilanadi. || Счётчик хранит значение итерации, накопитель — общий результат. Для суммы s ← 0 записывается до цикла; в теле выполняется s ← s + i.',
            'Jamlagichni har aylanishda nol qilish avvalgi yig‘indini yo‘qotadi. Tana necha marta bajarilishini va har safar qaysi qiymat bilan ishlashini alohida kuzating. || Обнуление накопителя на каждом проходе теряет прежнюю сумму. Отдельно отслеживайте число выполнений тела и значение на каждом проходе.'
        ], 's ← 0; for i ← 1 TO 4 {s ← s + i}. s? || s ← 0; for i ← 1 TO 4 {s ← s + i}. Чему равно s?',
           'i qiymatlari 1, 2, 3, 4.|s qiymatlari 1, 3, 6, 10.|Oxirgi yig‘indi 10. || Значения i: 1, 2, 3, 4.|Значения s: 1, 3, 6, 10.|Конечная сумма — 10.', '10 || 10', [
            n('s ← 0; for i ← 2 TO 5 {s ← s + i}. s? || s ← 0; for i ← 2 TO 5 {s ← s + i}. Чему равно s?', 14,
              'Ikkala chegara kiradi.|2 + 3 + 4 + 5 = 14. || Обе границы включены.|2 + 3 + 4 + 5 = 14.',
              'Oxirgi chegarani tashlab ketmang. || Не пропускайте конечную границу.',
              'Avval barcha i qiymatlarini yozing. || Сначала выпишите все значения i.'),
            n('p ← 1; for i ← 1 TO 3 {p ← p × 2}. p? || p ← 1; for i ← 1 TO 3 {p ← p × 2}. Чему равно p?', 8,
              'Tana 3 marta bajariladi.|p: 2, 4, 8. || Тело выполняется 3 раза.|p: 2, 4, 8.',
              'Ko‘paytirish sonini i qiymatlari yig‘indisi bilan aralashtirmang. || Не путайте число умножений с суммой значений i.',
              'Har safar avvalgi p ikki baravar bo‘ladi. || Каждый раз прежнее p удваивается.'),
            n('c ← 0; for i ← 3 TO 7 {c ← c + 1}. c? || c ← 0; for i ← 3 TO 7 {c ← c + 1}. Чему равно c?', 5,
              'Qiymatlar 3, 4, 5, 6, 7.|Ular 5 ta, demak c = 5. || Значения: 3, 4, 5, 6, 7.|Их 5, значит c = 5.',
              'Takrorlar soni oxirgi i qiymatiga teng bo‘lishi shart emas. || Число повторов не обязано равняться последнему i.'),
            n('s ← 9; for i ← 5 TO 3 {s ← s + i}. Kurs qoidasi bo‘yicha s? || s ← 9; for i ← 5 TO 3 {s ← s + i}. Чему равно s по правилам курса?', 9,
              'Boshlanish tugashdan katta.|O‘suvchi for tanasi bajarilmaydi, s = 9. || Начало больше конца.|Тело возрастающего for не выполняется, s = 9.',
              'TO yashirin kamayish qadamini bildirmaydi. || TO не задаёт скрытый убывающий шаг.')], ['algo-assignment']),
        l('loop-while', 'while va tugash sharti || while и условие завершения', [
            'while shartni tanadan oldin tekshiradi. Dastlab FALSE bo‘lsa tana bir marta ham bajarilmaydi. Har aylanishdan keyin shart qayta tekshiriladi. || while проверяет условие до тела. Если оно изначально FALSE, тело не выполняется ни разу. После каждого прохода условие проверяется снова.',
            'Sikl holati shartni bir kuni FALSE qiladigan tomonga o‘zgarishi kerak. i ← i + 1 yoki qoldiqni kamaytirish kabi qadamning yo‘qligi cheksiz siklga olib kelishi mumkin. || Состояние цикла должно изменяться так, чтобы условие однажды стало FALSE. Отсутствие шага вроде i ← i + 1 или уменьшения остатка может привести к бесконечному циклу.',
            'Tugashni taxmin qilish o‘rniga nima kamayishi yoki chegaraga yaqinlashishini ayting. Shartdagi va yangilanishdagi belgilar bir-biriga mos bo‘lsin. || Вместо предположения о завершении укажите, что уменьшается или приближается к границе. Знаки в условии и обновлении должны согласовываться.'
        ], 'x ← 1; while x < 8 {x ← x × 2}. Oxirgi x? || x ← 1; while x < 8 {x ← x × 2}. Чему равно конечное x?',
           'x: 1 → 2 → 4 → 8.|8 < 8 yolg‘on.|Tana qayta bajarilmaydi, x = 8. || x: 1 → 2 → 4 → 8.|8 < 8 ложно.|Тело больше не выполняется, x = 8.', '8 || 8', [
            n('x ← 3; c ← 0; while x < 12 {x ← x + 3; c ← c + 1}. c? || x ← 3; c ← 0; while x < 12 {x ← x + 3; c ← c + 1}. Чему равно c?', 3,
              'Tana x boshlanishlari 3, 6, 9 da ishlaydi.|x = 12 da to‘xtaydi, c = 3. || Тело работает при начальных x: 3, 6, 9.|При x = 12 цикл останавливается, c = 3.',
              'To‘xtashdagi tekshiruvni yana bitta tana deb sanamang. || Не считайте проверку остановки ещё одним выполнением тела.',
              'Shart har gal tanadan oldin tekshiriladi. || Условие каждый раз проверяется до тела.'),
            s('i ← 0; while i < 4 {OUTPUT i}. Nima yetishmayapti? || i ← 0; while i < 4 {OUTPUT i}. Чего не хватает?', [
                ('Tanada i ni chegaraga yaqinlashtiruvchi yangilanish || Обновления i в теле, приближающего его к границе', 'i o‘zgarmasa shart doim rost qoladi. || Если i не меняется, условие остаётся истинным.'),
                ('Har safar i ← 0 qilish || Каждый раз делать i ← 0', 'Bu holatni boshlanishga qaytarib, tugashga yordam bermaydi. || Это возвращает состояние к началу и не помогает завершению.'),
                ('OUTPUT ni ko‘paytirish || Добавить больше OUTPUT', 'Chiqarish i ni o‘zgartirmaydi. || Вывод не меняет i.')],
              'i qiymati tanada o‘zgarmayapti.|Masalan, i ← i + 1 tugashga olib boradi. || Значение i в теле не меняется.|Например, i ← i + 1 приводит к завершению.',
              'OUTPUTni holat yangilanishi deb hisoblamang. || Не считайте OUTPUT обновлением состояния.',
              'Shartni yolg‘on qiladigan qiymatga qanday yetiladi? || Как достичь значения, делающего условие ложным?'),
            n('x ← 10; c ← 0; while x < 5 {c ← c + 1; x ← x + 1}. c? || x ← 10; c ← 0; while x < 5 {c ← c + 1; x ← x + 1}. Чему равно c?', 0,
              'Dastlab 10 < 5 yolg‘on.|Tana bajarilmaydi, c = 0. || Изначально 10 < 5 ложно.|Тело не выполняется, c = 0.',
              'while kamida bir marta ishlaydi degan taxmin noto‘g‘ri. || Предположение, что while работает хотя бы один раз, неверно.'),
            n('x ← 20; c ← 0; while x > 2 {x ← x div 2; c ← c + 1}. c? || x ← 20; c ← 0; while x > 2 {x ← x div 2; c ← c + 1}. Чему равно c?', 3,
              'Butun bo‘linish: 20 → 10 → 5 → 2.|2 > 2 yolg‘on, c = 3. || Целочисленное деление: 20 → 10 → 5 → 2.|2 > 2 ложно, c = 3.',
              'div kasr qismini tashlaydi; oddiy bo‘lish bilan almashtirmang. || div отбрасывает дробную часть; не заменяйте его обычным делением.')], ['loop-for', 'cond-if']),
        l('loop-do', 'do-while: avval tana, keyin shart || do-while: сначала тело, затем условие', [
            'do {tana} while shart tanani avval bajaradi, keyin shart TRUE bo‘lsa takrorlaydi. Shuning uchun tana kamida bir marta bajariladi. || do {тело} while условие сначала выполняет тело, затем повторяет его, если условие TRUE. Поэтому тело выполняется хотя бы один раз.',
            'Bu yozuv repeat-until emas: while sharti rost bo‘lsa DAVOM etadi. Shartning ma’nosini teskarilash xatoga olib keladi. || Это не repeat-until: при истинном условии while выполнение ПРОДОЛЖАЕТСЯ. Обращение смысла условия приводит к ошибке.',
            'Menyu yoki birinchi urinish majburiy bo‘lgan jarayonga mos. Kirishning yaroqliligini baribir tekshirish kerak; kamida bir marta bajarilishi xavfsizlik tekshiruvi o‘rnini bosmaydi. || Подходит для меню или процесса с обязательной первой попыткой. Вход всё равно нужно проверять; обязательное выполнение не заменяет проверку допустимости.'
        ], 'x ← 5; do {x ← x + 1} while x < 3. Oxirgi x? || x ← 5; do {x ← x + 1} while x < 3. Чему равно конечное x?',
           'Tana avval x ni 6 qiladi.|6 < 3 yolg‘on.|Takror yo‘q, x = 6. || Тело сначала делает x равным 6.|6 < 3 ложно.|Повторения нет, x = 6.', '6 || 6', [
            n('x ← 0; do {x ← x + 2} while x < 5. Oxirgi x? || x ← 0; do {x ← x + 2} while x < 5. Чему равно конечное x?', 6,
              'Tanadan keyingi qiymatlar 2, 4, 6.|6 < 5 yolg‘on, x = 6. || Значения после тела: 2, 4, 6.|6 < 5 ложно, x = 6.',
              'Chegaraga yetishdan oldingi qiymatda to‘xtatmang. || Не останавливайте цикл на значении до достижения границы.',
              'Shartni yangilangan qiymatda tekshiring. || Проверяйте условие по обновлённому значению.'),
            n('c ← 0; do {c ← c + 1} while FALSE. c? || c ← 0; do {c ← c + 1} while FALSE. Чему равно c?', 1,
              'Birinchi tana shartsiz bajariladi.|FALSE takrorni to‘xtatadi, c = 1. || Первое тело выполняется без проверки.|FALSE прекращает повторение, c = 1.',
              'Boshlang‘ich shartni tanadan oldin qo‘ymang. || Не ставьте начальную проверку перед телом.',
              'do-while ning birinchi qadami tana. || Первый шаг do-while — тело.'),
            n('x ← 9; do {x ← x − 4} while x > 3. Oxirgi x? || x ← 9; do {x ← x − 4} while x > 3. Чему равно конечное x?', 1,
              'Avval x = 5, shart rost.|Keyin x = 1, shart yolg‘on. || Сначала x = 5, условие истинно.|Затем x = 1, условие ложно.',
              'do-while shart rostligida tugamaydi, davom etadi. || do-while при истинном условии не завершается, а продолжается.'),
            s('Dastlab shart FALSE. while va do-while tanalari necha marta bajariladi? Shart tanada ham FALSE qoladi. || Изначально условие FALSE. Сколько раз выполняются тела while и do-while? В теле условие тоже остаётся FALSE.', [
                ('while: 0; do-while: 1 || while: 0; do-while: 1', 'Tekshirish joylari farq qiladi. || Места проверки различаются.'),
                ('Ikkalasi: 0 || Оба: 0', 'do-while dastlab tanani bajaradi. || do-while сначала выполняет тело.'),
                ('Ikkalasi: 1 || Оба: 1', 'while yolg‘on boshlang‘ich shartda kirmaydi. || while не входит при ложном начальном условии.')],
              'while oldindan tekshiradi.|do-while birinchi tanadan keyin tekshiradi. || while проверяет заранее.|do-while проверяет после первого тела.',
              'Nomiga emas, tekshirish joyiga qarang. || Смотрите на место проверки, а не на название.')], ['loop-while']),
        l('loop-nested', 'Ichma-ich sikllarni kuzatish || Трассировка вложенных циклов', [
            'Tashqi siklning har bir aylanishida ichki sikl qaytadan boshlanadi. Mustaqil chegaralarda umumiy tana soni tashqi va ichki takrorlar ko‘paytmasidir. || На каждом проходе внешнего цикла внутренний начинается заново. При независимых границах число выполнений общего тела равно произведению повторов.',
            'for i ← 1 TO 2 {for j ← 1 TO 3 {...}} juftlari qatorlab yuradi. Juftlar sonini takrorlar sonlarini qo‘shib hisoblamang. || В for i ← 1 TO 2 {for j ← 1 TO 3 {...}} пары обходятся построчно. Не находите число пар сложением количества повторов.',
            'Ichki chegara i ga bog‘liq bo‘lsa ko‘paytma yetmaydi: har tashqi qiymatdagi ichki takrorni alohida sanang. Uchburchak shakldagi ish 1 + 2 + ... bo‘lishi mumkin. || Если внутренняя граница зависит от i, произведения недостаточно: считайте повторы отдельно для каждого внешнего значения. Работа треугольной формы может быть 1 + 2 + ...'
        ], 'c ← 0; for i ← 1 TO 2 {for j ← 1 TO 3 {c ← c + 1}}. c? || c ← 0; for i ← 1 TO 2 {for j ← 1 TO 3 {c ← c + 1}}. Чему равно c?',
           'Tashqi sikl 2 marta.|Har safar ichki sikl 3 marta.|c = 2 × 3 = 6. || Внешний цикл — 2 раза.|Каждый раз внутренний — 3 раза.|c = 2 × 3 = 6.', '6 || 6', [
            n('c ← 0; for i ← 1 TO 3 {for j ← 1 TO 4 {c ← c + 1}}. c? || c ← 0; for i ← 1 TO 3 {for j ← 1 TO 4 {c ← c + 1}}. Чему равно c?', 12,
              'Har tashqi aylanishda 4 ichki aylanish.|3 × 4 = 12. || На каждом внешнем проходе 4 внутренних.|3 × 4 = 12.',
              'Takrorlar sonini qo‘shmang. || Не складывайте числа повторов.',
              'Har tashqi qiymat uchun ichki sikl yangidan yuradi. || Для каждого внешнего значения внутренний цикл идёт заново.'),
            n('c ← 0; for i ← 1 TO 3 {for j ← 1 TO i {c ← c + 1}}. c? || c ← 0; for i ← 1 TO 3 {for j ← 1 TO i {c ← c + 1}}. Чему равно c?', 6,
              'Ichki takrorlar mos ravishda 1, 2, 3.|1 + 2 + 3 = 6. || Числа внутренних повторов: 1, 2, 3.|1 + 2 + 3 = 6.',
              'Bog‘liq chegarada bir xil ichki uzunlikni olmang. || При зависимой границе не считайте внутреннюю длину постоянной.',
              'Har i uchun j chegarasini alohida yozing. || Отдельно запишите границу j для каждого i.'),
            n('s ← 0; for i ← 1 TO 2 {for j ← 1 TO 3 {s ← s + i}}. s? || s ← 0; for i ← 1 TO 2 {for j ← 1 TO 3 {s ← s + i}}. Чему равно s?', 9,
              'i = 1 da 1 uch marta, i = 2 da 2 uch marta qo‘shiladi.|3 + 6 = 9. || При i = 1 число 1 добавляется три раза, при i = 2 число 2 — три раза.|3 + 6 = 9.',
              'Tana sanog‘i bilan jamlanayotgan qiymat bir xil emas. || Число выполнений тела и накапливаемое значение — не одно и то же.'),
            n('c ← 0; for i ← 1 TO 4 {for j ← 1 TO i {c ← c + 1}}. c? || c ← 0; for i ← 1 TO 4 {for j ← 1 TO i {c ← c + 1}}. Чему равно c?', 10,
              'Ichki takrorlar 1, 2, 3, 4.|Yig‘indi 10. || Числа внутренних повторов: 1, 2, 3, 4.|Сумма — 10.',
              'Ichki chegaraning tashqi hisoblagichga bog‘liqligini saqlang. || Учитывайте зависимость внутренней границы от внешнего счётчика.')], ['loop-for']),
        l('loop-recursion', 'Rekursiya va tayanch holat || Рекурсия и базовый случай', [
            'Rekursiv funksiya o‘zini kichikroq masala bilan chaqiradi. Tayanch holat bevosita javob qaytarib, yangi chaqiruv qilmaydi. || Рекурсивная функция вызывает себя для меньшей задачи. Базовый случай сразу возвращает ответ и не создаёт нового вызова.',
            'S(n): if n == 0 {RETURN 0} else {RETURN n + S(n − 1)}, n manfiy bo‘lmagan butun. Har chaqiruv argumentni kamaytirib tayanch holatga olib boradi. || S(n): if n == 0 {RETURN 0} else {RETURN n + S(n − 1)}, n — неотрицательное целое. Каждый вызов уменьшает аргумент и ведёт к базовому случаю.',
            'Chaqiruvlar avval chuqurlashadi, javoblar esa orqaga qaytadi. Rekursiya bepul emas: tugallanmagan chaqiruvlar stekda joy oladi. Yetarli bo‘lmagan tayanch yoki noto‘g‘ri yo‘nalish tugamaslikka olib keladi. || Вызовы сначала углубляются, ответы возвращаются назад. Рекурсия не бесплатна: незавершённые вызовы занимают стек. Недостаточная база или неверное направление ведут к незавершению.'
        ], 'S(3) ni yuqoridagi qoida bilan toping. || Найдите S(3) по правилу выше.',
           'S(3) = 3 + S(2), S(2) = 2 + S(1).|S(1) = 1 + S(0), S(0) = 0.|Orqaga qaytib: 1, 3, 6. || S(3) = 3 + S(2), S(2) = 2 + S(1).|S(1) = 1 + S(0), S(0) = 0.|Возвращаясь назад: 1, 3, 6.', '6 || 6', [
            n('F(0) = 1; n > 0 da F(n) = n × F(n − 1). F(4)? || F(0) = 1; при n > 0 F(n) = n × F(n − 1). Чему равно F(4)?', 24,
              'F(4) = 4 × 3 × 2 × 1 × F(0).|F(0) = 1, natija 24. || F(4) = 4 × 3 × 2 × 1 × F(0).|F(0) = 1, результат — 24.',
              'Ko‘paytmaning tayanchini nol qilmang. || Не делайте базу произведения нулевой.',
              'Chaqiruvni tayanch holatgacha yozib chiqing. || Распишите вызов до базового случая.'),
            s('n ≥ 0 uchun G(n) faqat G(n + 1) ni chaqiradi, tayanch esa n == 0. n > 0 da muammo? || Для n ≥ 0 функция G(n) вызывает только G(n + 1), база — n == 0. В чём проблема при n > 0?', [
                ('Argument tayanchdan uzoqlashadi || Аргумент удаляется от базы', 'Musbat qiymat oshib nolga yetmaydi. || Положительное значение растёт и не достигает нуля.'),
                ('Rekursiya avtomatik kamaytiradi || Рекурсия автоматически уменьшает аргумент', 'O‘zgarish aynan yozilgan ifodaga bog‘liq. || Изменение определяется записанным выражением.'),
                ('Tayanch borligi o‘zi yetarli || Самого наличия базы достаточно', 'Unga yetish ham zarur. || Нужно ещё достичь базы.')],
              'n + 1 musbat argumentni oshiradi.|Tayanchga yetish yo‘li yo‘q, yo‘nalish tuzatilishi kerak. || n + 1 увеличивает положительный аргумент.|Пути к базе нет, направление нужно исправить.',
              'Tayanchni yozish bilan birga unga yetishni isbotlang. || Помимо записи базы обоснуйте достижение базы.',
              'Har chaqiruvda argument tayanchga yaqinlashyaptimi? || Приближается ли аргумент к базе при каждом вызове?'),
            n('H(0) = 2; n > 0 da H(n) = H(n − 1) + 3. H(3)? || H(0) = 2; при n > 0 H(n) = H(n − 1) + 3. Чему равно H(3)?', 11,
              'H(1) = 5, H(2) = 8.|H(3) = 11. || H(1) = 5, H(2) = 8.|H(3) = 11.',
              'Boshlang‘ich tayanch qiymatni yo‘qotmang. || Не теряйте исходное базовое значение.'),
            n('R(0) = 0; n > 0 da R(n) faqat R(n − 1) ni bir marta chaqiradi. R(4) hisobida tayanch bilan jami nechta funksiya chaqiruvi bor? || R(0) = 0; при n > 0 R(n) один раз вызывает только R(n − 1). Сколько всего вызовов, включая базовый, при R(4)?', 5,
              'Argumentlar 4, 3, 2, 1, 0.|Boshlang‘ich va tayanch bilan 5 chaqiruv. || Аргументы: 4, 3, 2, 1, 0.|С исходным и базовым — 5 вызовов.',
              'Faqat rekursiv o‘tishlarni sanab, dastlabki chaqiruvni unutmang. || Не забывайте исходный вызов, считая только рекурсивные переходы.')], ['loop-while'])])
