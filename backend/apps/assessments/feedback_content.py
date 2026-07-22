"""
Per-question pedagogical feedback for CognitiveQuestion, keyed by the question's
stable `key` (not id) — matches content.py's own upsert-key convention.

Shown only on the student's Results page for questions they didn't answer fully
correctly (correctness < 1.0) — never during the live test, to preserve the
adaptive test's validity (see apps.scoring.views' mistakes endpoint). A missing
key simply means that question is skipped from the "typical mistakes" list, so
partial coverage never breaks anything — content can be extended incrementally.

Feedback is written at the method/concept level ("what rule applies, what's
easy to mix up") rather than restating the specific correct answer — that's
more useful for review than a bare number, and keeps the text valid even if a
question's own answer key ever needs correcting independently of this file.
"""

QUESTION_FEEDBACK = {
    # -- math (61) --------------------------------------------------------------------
    'math-easy-1': {
        'ru': 'Процент от числа считается как (число × процент) / 100 — легко перепутать «30% от 150» с «150% от 30» или посчитать 30% как отдельное число, не связанное со 150.',
        'uz': "Sondan foiz — (son × foiz) / 100 formulasi bilan hisoblanadi; «150 ning 30%» ni «30 ning 150%» bilan chalkashtirish yoki foizni 150 bilan bog'lamasdan alohida son deb hisoblash keng tarqalgan xato.",
    },
    'math-easy-2': {
        'ru': 'Скобки выполняются первыми: сначала 65-45, затем умножение на 120 — частая ошибка нарушить этот порядок и умножить 120 на 65 и 45 по отдельности.',
        'uz': "Avval qavs ichidagi amal bajariladi: 65-45, so'ng 120 ga ko'paytiriladi — bu tartibni buzib, 120 ni 65 va 45 ga alohida ko'paytirish keng tarqalgan xato.",
    },
    'math-easy-3': {
        'ru': 'Ищите не сам ряд, а ряд разностей между соседними числами — здесь разности удваиваются, а не растут на постоянную величину, что часто упускают из виду.',
        'uz': "Qatorning o'zini emas, qo'shni sonlar orasidagi farqlar qatorini kuzating — bu yerda farqlar doimiy songa emas, balki 2 baravarga oshadi, buni ko'pincha e'tibordan chetda qoldirishadi.",
    },
    'math-easy-4': {
        'ru': 'Используйте тождество (x+1/x)²=x²+2+1/x² — типичная ошибка: забыть вычесть 2 после возведения суммы в квадрат.',
        'uz': "(x+1/x)²=x²+2+1/x² ayniyatidan foydalaning — yig'indini kvadratga ko'targandan so'ng 2 ni ayirishni unutish keng tarqalgan xato.",
    },
    'math-easy-5': {
        'ru': 'Аналогично: (a+b)²=a²+2ab+b², поэтому a²+b²=(a+b)²-2ab — ошибка возникает, если забыть удвоить произведение ab перед вычитанием.',
        'uz': "Xuddi shu tarzda: (a+b)²=a²+2ab+b², shuning uchun a²+b²=(a+b)²-2ab — ab ko'paytmasini ayirishdan oldin 2 ga ko'paytirishni unutish xatoga olib keladi.",
    },
    'math-easy-6': {
        'ru': 'Модульное уравнение |x-a|=b даёт два решения: x=a+b и x=a-b — частая ошибка забыть про отрицательный случай и указать только один корень.',
        'uz': "|x-a|=b moduli tenglamasi ikkita yechim beradi: x=a+b va x=a-b — manfiy holatni unutib, faqat bitta ildizni yozish keng tarqalgan xato.",
    },
    'math-easy-7': {
        'ru': 'Количество чисел от 1 до N, кратных k, равно целой части от деления N на k — ошибка в том, чтобы округлить в большую сторону вместо отбрасывания остатка.',
        'uz': "1 dan N gacha k ga karrali sonlar soni N ni k ga bo'lib, butun qismini olish orqali topiladi — qoldiqni tashlash o'rniga yuqoriga yaxlitlash xatoga olib keladi.",
    },
    'math-easy-8': {
        'ru': 'При делении степеней с одинаковым основанием показатели вычитаются: 4⁵/4³=4^(5-3) — ошибка в том, чтобы вычесть сами основания или разделить показатели вместо вычитания.',
        'uz': "Bir xil asosli darajalarni bo'lishda ko'rsatkichlar ayiriladi: 4⁵/4³=4^(5-3) — asoslarni ayirish yoki ko'rsatkichlarni bo'lish xato hisoblanadi.",
    },
    'math-easy-9': {
        'ru': 'Каждый следующий член получается как «предыдущее число × 2 + 1» — ошибка в том, чтобы просто удвоить предыдущее число, не добавляя единицу.',
        'uz': "Har bir keyingi son «oldingi son × 2 + 1» qoidasi bilan topiladi — birni qo'shmasdan faqat 2 ga ko'paytirish xatoga olib keladi.",
    },
    'math-easy-10': {
        'ru': 'Подставьте известное x в уравнение и решайте относительно y по шагам — ошибка в том, чтобы забыть перенести получившееся число в другую часть уравнения перед делением.',
        'uz': "Ma'lum x qiymatini tenglamaga qo'yib, y ni bosqichma-bosqich toping — hosil bo'lgan sonni bo'lishdan oldin tenglamaning boshqa tomoniga o'tkazishni unutish xatoga olib keladi.",
    },
    'math-easy-11': {
        'ru': 'Приведите дроби к общему знаменателю перед сложением — частая ошибка: сложить числители и знаменатели напрямую без приведения к общему знаменателю.',
        'uz': "Qo'shishdan oldin kasrlarni umumiy maxrajga keltiring — suratlarni umumiy maxrajsiz to'g'ridan-to'g'ri qo'shish keng tarqalgan xato.",
    },
    'math-easy-12': {
        'ru': 'Сначала вычислите каждый факториал отдельно, затем вычтите — ошибка в том, чтобы посчитать (5-4)! вместо разности двух факториалов.',
        'uz': "Avval har bir faktorialni alohida hisoblang, keyin ayiring — (5-4)! ni hisoblash ikkita faktorial farqi o'rniga xato hisoblanadi.",
    },
    'math-easy-13': {
        'ru': 'Извлеките кубический корень из обеих частей уравнения — ошибка в том, чтобы перепутать кубический корень с квадратным.',
        'uz': "Tenglamaning ikkala tomonidan kub ildiz chiqaring — kub ildizni kvadrat ildiz bilan chalkashtirish xato hisoblanadi.",
    },
    'math-easy-14': {
        'ru': 'Как и в похожем задании выше, смотрите на разности между членами ряда — они удваиваются, а не растут на постоянное число.',
        'uz': "Yuqoridagi o'xshash misolda bo'lgani kabi, qator hadlari orasidagi farqlarga e'tibor bering — ular doimiy songa emas, 2 baravarga oshadi.",
    },
    'math-easy-15': {
        'ru': 'log₃81=x означает 3^x=81 — ошибка в том, чтобы посчитать 81/3 вместо подбора степени, в которую нужно возвести 3.',
        'uz': "log₃81=x degani 3^x=81 demakdir — 3 ni qaysi darajaga ko'tarish kerakligini topish o'rniga 81 ni 3 ga bo'lish xato hisoblanadi.",
    },
    'math-easy-16': {
        'ru': 'Здесь нужно точно знать количество простых чисел до 100 — типичная ошибка: посчитать нечётные числа или числа без делителя 2, что не то же самое, что простые числа.',
        'uz': "Bu yerda 100 gacha bo'lgan tub sonlar sonini aniq bilish kerak — toq sonlarni yoki 2 ga bo'linmaydigan sonlarni sanash tub sonlar bilan bir xil emas, bu keng tarqalgan xato.",
    },
    'math-easy-17': {
        'ru': 'Не забывайте, что любое число в нулевой степени равно 1, а не 0 — это частая причина ошибки в подобных суммах степеней.',
        'uz': "Har qanday sonning nolinchi darajasi 1 ga teng, 0 ga emas — bunday darajalar yig'indisida ko'p uchraydigan xato aynan shu.",
    },
    'math-easy-18': {
        'ru': 'По теореме Виета сумма корней уравнения x²+bx+c=0 равна -b, а произведение — c; ошибка часто в том, чтобы забыть сменить знак у b.',
        'uz': "Viet teoremasiga ko'ra x²+bx+c=0 tenglamasining ildizlari yig'indisi -b ga, ko'paytmasi esa c ga teng; b ning ishorasini almashtirishni unutish keng tarqalgan xato.",
    },
    'math-easy-19': {
        'ru': 'N бит позволяют закодировать 2ⁿ различных чисел — ошибка в том, чтобы умножить N на 2 вместо возведения 2 в степень N.',
        'uz': "N bit 2ⁿ ta turli sonni kodlashga imkon beradi — 2 ni N-darajaga ko'tarish o'rniga N ni 2 ga ko'paytirish xato hisoblanadi.",
    },
    'math-easy-20': {
        'ru': 'Посчитайте оба значения отдельно и сравните итоговые числа — ошибка в том, чтобы сравнивать сами проценты, а не то, что от них получается.',
        'uz': "Ikkala qiymatni alohida hisoblang va natijaviy sonlarni solishtiring — foizlarning o'zini solishtirish, natijalarni emas, xato hisoblanadi.",
    },
    'math-medium-1': {
        'ru': 'Число перестановок n различных элементов — это n! (факториал n), а не n² или 2ⁿ, которые считают другие комбинаторные величины.',
        'uz': "n ta har xil elementning tartiblanishlari soni n! (n faktorial) ga teng, n² yoki 2ⁿ esa boshqa kombinatorik miqdorlarni ifodalaydi.",
    },
    'math-medium-2': {
        'ru': 'Представьте число как степень того же основания и сравните показатели — ошибка в том, чтобы делить число один раз вместо разложения его на степень.',
        'uz': "Sonni bir xil asosli daraja sifatida ifodalang va ko'rsatkichlarni solishtiring — sonni bir marta bo'lish darajaga yoyish o'rniga xato hisoblanadi.",
    },
    'math-medium-3': {
        'ru': 'Здесь порядок выбора не важен, поэтому нужна формула сочетаний C(n,k)=n!/(k!(n-k)!) — частая ошибка: посчитать размещения с учётом порядка, что даёт число в несколько раз больше.',
        'uz': "Bu yerda tanlash tartibi muhim emas, shuning uchun kombinatsiya formulasi C(n,k)=n!/(k!(n-k)!) kerak — tartibni hisobga oluvchi joylashtirishlarni hisoblash bir necha baravar katta son beradi.",
    },
    'math-medium-4': {
        'ru': 'Разложите оба числа на простые множители и возьмите общие множители в наименьшей степени — ошибка в том, чтобы перепутать НОД с НОК.',
        'uz': "Ikkala sonni tub ko'paytuvchilarga ajrating va umumiy ko'paytuvchilarni eng kichik darajada oling — EKUB ni EKUK bilan chalkashtirish xato hisoblanadi.",
    },
    'math-medium-5': {
        'ru': 'НОК находится через разложение на простые множители, беря каждый множитель в наибольшей степени — ошибка в том, чтобы перепутать с НОД или просто перемножить числа.',
        'uz': "EKUK har bir tub ko'paytuvchini eng katta darajada olib topiladi — buni EKUB bilan chalkashtirish yoki sonlarni shunchaki ko'paytirish xato hisoblanadi.",
    },
    'math-medium-6': {
        'ru': 'Нужно точно знать количество простых чисел в диапазоне — считать только нечётные числа или числа без делителя 2 — не то же самое, что простые числа.',
        'uz': "Diapazondagi tub sonlar sonini aniq bilish kerak — faqat toq sonlarni sanash tub sonlarni sanash bilan bir xil emas.",
    },
    'math-medium-7': {
        'ru': '4⁴ означает 4×4×4×4, а не 4×4 — частая ошибка перепутать возведение в степень с обычным умножением на показатель.',
        'uz': "4⁴ — bu 4×4×4×4 degani, 4×4 emas — darajaga ko'tarishni ko'rsatkichga oddiy ko'paytirish bilan chalkashtirish keng tarqalgan xato.",
    },
    'math-medium-8': {
        'ru': 'Вычисляйте факториал последовательным умножением всех чисел от 1 до n, не пропуская ни одного множителя.',
        'uz': "Faktorialni 1 dan n gacha bo'lgan barcha sonlarni ketma-ket ko'paytirib hisoblang, birorta ko'paytuvchini ham tashlab ketmang.",
    },
    'math-medium-9': {
        'ru': 'Сначала возведите каждое число в степень отдельно, затем сложите результаты, не путая порядок действий.',
        'uz': "Avval har bir sonni alohida darajaga ko'taring, so'ng natijalarni qo'shing, amallar tartibini aralashtirmang.",
    },
    'math-medium-10': {
        'ru': '2¹⁰=1024 — это стандартное значение, которое стоит запомнить (1 килобайт = 2¹⁰ байт); ошибка в том, чтобы посчитать 2×10.',
        'uz': "2¹⁰=1024 — yodda tutish kerak bo'lgan standart qiymat (1 kilobayt = 2¹⁰ bayt); 2×10 ni hisoblash xato hisoblanadi.",
    },
    'math-medium-11': {
        'ru': 'При умножении степеней с одинаковым основанием показатели складываются — ошибка в том, чтобы перемножить показатели вместо сложения.',
        'uz': "Bir xil asosli darajalarni ko'paytirishda ko'rsatkichlar qo'shiladi — ko'rsatkichlarni ko'paytirish qo'shish o'rniga xato hisoblanadi.",
    },
    'math-medium-12': {
        'ru': 'Если цифры не повторяются, число чисел из n различных цифр равно n! — ошибка в том, чтобы допустить повторение цифр и посчитать nⁿ.',
        'uz': "Raqamlar takrorlanmasa, n ta har xil raqamdan tuzilgan sonlar soni n! ga teng — raqamlar takrorlanishiga yo'l qo'yib nⁿ ni hisoblash xato hisoblanadi.",
    },
    'math-medium-13': {
        'ru': 'Если цифры не повторяются, для каждой следующей позиции числа остаётся на одну доступную цифру меньше — перемножьте эти убывающие количества, а не одинаковые.',
        'uz': "Raqamlar takrorlanmasa, sonning har bir keyingi o'rni uchun bir dona kam raqam qoladi — shu kamayib boruvchi sonlarni ko'paytiring, bir xillarini emas.",
    },
    'math-medium-14': {
        'ru': 'Заметьте закономерность в остатках (например, все они на одну и ту же величину меньше своего делителя) — это подсказывает более быстрый способ решения, чем перебор чисел по одному.',
        'uz': "Qoldiqlardagi qonuniyatga e'tibor bering (masalan, ularning barchasi o'z bo'luvchisidan bir xil miqdorga kam) — bu sonlarni birma-bir sanashdan tezroq yechim usulini ko'rsatadi.",
    },
    'math-medium-15': {
        'ru': 'Составьте уравнение по условию и решайте по шагам: сначала перенесите свободное число, затем разделите — ошибка в том, чтобы сразу делить, не перенеся его.',
        'uz': "Shartga ko'ra tenglama tuzing va bosqichma-bosqich yeching: avval erkin sonni o'tkazing, so'ng bo'ling — uni o'tkazmasdan to'g'ridan-to'g'ri bo'lish xato hisoblanadi.",
    },
    'math-medium-16': {
        'ru': 'Задачи на остатки от деления обычно решаются перебором чисел, удовлетворяющих всем условиям одновременно, либо через китайскую теорему об остатках — ошибка в том, чтобы проверить условия по отдельности и остановиться на первом же подходящем числе.',
        'uz': "Qoldiqlarga oid masalalar odatda barcha shartlarni bir vaqtda qanoatlantiruvchi sonlarni sanab chiqish yoki qoldiqlar haqidagi xitoy teoremasi orqali yechiladi — shartlarni alohida tekshirib, birinchi mos kelgan sonda to'xtash xato hisoblanadi.",
    },
    'math-medium-17': {
        'ru': 'Разделите каждую сторону прямоугольника на сторону квадрата отдельно, затем перемножьте результаты — ошибка в том, чтобы посчитать только по одной стороне.',
        'uz': "To'g'ri to'rtburchakning har bir tomonini kvadrat tomoniga alohida bo'ling, so'ng natijalarni ko'paytiring — faqat bitta tomon bo'yicha hisoblash xato hisoblanadi.",
    },
    'math-medium-18': {
        'ru': 'Точка пересечения диагоналей квадрата делит каждую диагональ пополам — сначала найдите длину диагонали (сторона×√2), затем разделите на 2.',
        'uz': "Kvadratning diagonallari kesishgan nuqta har bir diagonalni teng ikkiga bo'ladi — avval diagonal uzunligini (tomon×√2) toping, so'ng 2 ga bo'ling.",
    },
    'math-medium-19': {
        'ru': 'Наибольший шар, вписанный в куб, касается граней в их центрах, поэтому его радиус равен половине ребра куба — ошибка в том, чтобы взять радиус равным целому ребру.',
        'uz': "Kubga sig'adigan eng katta shar uning yoqlariga markazida tegadi, shuning uchun radiusi kub qirrasining yarmiga teng — radiusni butun qirraga teng deb olish xato hisoblanadi.",
    },
    'math-medium-20': {
        'ru': 'Складывайте не сами дни, а обратные величины — доли работы за день, а затем возьмите обратное от суммы; частая ошибка: усреднить дни напрямую.',
        'uz': "Kunlarning o'zini emas, teskari miqdorlarni — kunlik ish ulushlarini qo'shing, so'ng yig'indining teskarisini oling; kunlarni to'g'ridan-to'g'ri o'rtachalashtirish keng tarqalgan xato.",
    },
    'math-hard-1': {
        'ru': 'Заметьте, что во всех условиях остаток на одну и ту же величину меньше делителя — значит число, увеличенное на эту величину, делится на НОК всех делителей сразу.',
        'uz': "Barcha shartlarda qoldiq bo'luvchidan bir xil miqdorga kam ekanligiga e'tibor bering — demak shu miqdorga oshirilgan son barcha bo'luvchilarning EKUKiga bo'linadi.",
    },
    'math-hard-2': {
        'ru': 'Дверь остаётся открытой только если у её номера нечётное количество делителей, а это бывает только у точных квадратов — сосчитайте квадраты в нужном диапазоне.',
        'uz': "Eshik faqat raqami toq sonli bo'luvchilarga ega bo'lsagina ochiq qoladi, bu esa faqat aniq kvadrat sonlarda sodir bo'ladi — kerakli diapazondagi kvadrat sonlarni sanang.",
    },
    'math-hard-3': {
        'ru': 'Переведите условие в квадратное уравнение и разложите его на множители (найдите два числа, которые в сумме и произведении соответствуют коэффициентам) — не пытайтесь угадать ответ подбором наугад.',
        'uz': "Shartni kvadrat tenglamaga aylantiring va uni ko'paytuvchilarga ajrating (yig'indisi va ko'paytmasi koeffitsientlarga mos keladigan ikkita sonni toping) — javobni tasodifiy taxmin qilib topishga urinmang.",
    },
    'math-hard-4': {
        'ru': 'Сложите дневные доли работы обоих исполнителей, вычтите выполненную за первые дни часть от целого, а затем разделите оставшуюся работу на дневную долю оставшегося исполнителя.',
        'uz': "Ikkala ijrochining kunlik ish ulushlarini qo'shing, dastlabki kunlarda bajarilgan qismni butundan ayiring, so'ng qolgan ishni qolgan ijrochining kunlik ulushiga bo'ling.",
    },
    'math-hard-5': {
        'ru': 'Здесь чередуются два действия — определите оба и то, какое из них идёт следующим по чётности позиции в ряду.',
        'uz': "Bu yerda ikkita amal navbatlashadi — ikkalasini ham aniqlang va qatordagi pozitsiya juft yoki toqligiga qarab keyingi amalni tanlang.",
    },
    'math-hard-6': {
        'ru': 'Проверьте теорему Пифагора: если квадрат наибольшей стороны равен сумме квадратов двух других, треугольник прямоугольный.',
        'uz': "Pifagor teoremasini tekshiring: agar eng katta tomon kvadrati qolgan ikkita tomon kvadratlari yig'indisiga teng bo'lsa, uchburchak to'g'ri burchakli bo'ladi.",
    },
    'math-hard-7': {
        'ru': 'Используйте теорему Пифагора: половина хорды, радиус и расстояние от центра образуют прямоугольный треугольник — половина хорды равна √(r²-d²), а сама хорда в 2 раза больше.',
        'uz': "Pifagor teoremasidan foydalaning: vatarning yarmi, radius va markazdan masofa to'g'ri burchakli uchburchak hosil qiladi — vatarning yarmi √(r²-d²) ga teng, vatarning o'zi esa undan 2 baravar katta.",
    },
    'math-hard-8': {
        'ru': 'Обозначьте меньшее число как x, тогда большее выразится через x — составьте уравнение суммы и решите, не забыв в конце вернуться к большему числу, а не к x.',
        'uz': "Kichik sonni x deb belgilang, katta son esa x orqali ifodalanadi — yig'indi tenglamasini tuzib yeching va oxirida x emas, aynan katta sonni javob sifatida yozing.",
    },
    'math-hard-9': {
        'ru': 'Приведите дроби к общему знаменателю, сложите их в одну дробь от x, и решите полученное простое уравнение.',
        'uz': "Kasrlarni umumiy maxrajga keltirib, x ning bitta kasriga qo'shing va hosil bo'lgan oddiy tenglamani yeching.",
    },
    'math-hard-10': {
        'ru': 'Средняя скорость — это общее расстояние, делённое на общее время, а не среднее арифметическое двух скоростей — частая ошибка: просто сложить скорости и поделить на 2.',
        'uz': "O'rtacha tezlik — umumiy masofani umumiy vaqtga bo'lish, ikkita tezlikning arifmetik o'rtachasi emas — tezliklarni shunchaki qo'shib 2 ga bo'lish keng tarqalgan xato.",
    },
    'math-hard-11': {
        'ru': 'Если бы шаров нежелательного цвета было слишком много, можно было бы выбрать несколько штук без единого шара нужного цвета — значит их количество ограничено этим условием.',
        'uz': "Agar kerakmas rangdagi sharlar juda ko'p bo'lsa, kerakli rangdagi sharsiz bir nechtasini tanlash mumkin bo'lardi — demak ularning soni shu shart bilan chegaralangan.",
    },
    'math-hard-12': {
        'ru': 'Проверьте каждое число на все условия по очереди — удобно начинать с самого редкого условия (например, «не делится на 5»), чтобы быстрее исключить лишние варианты.',
        'uz': "Har bir sonni barcha shartlarga navbat bilan tekshiring — variantlarni tezroq chetlash uchun eng kam uchraydigan shartdan (masalan, «5 ga bo'linmasligi») boshlash qulay.",
    },
    'math-hard-13': {
        'ru': 'Обозначьте последовательные числа как x, x+1, x+2 и так далее, составьте уравнение суммы и решите относительно x — это и будет наименьшее число.',
        'uz': "Ketma-ket sonlarni x, x+1, x+2 va hokazo deb belgilang, yig'indi tenglamasini tuzib x ni toping — bu eng kichik son bo'ladi.",
    },
    'math-hard-14': {
        'ru': 'Используйте основное тригонометрическое тождество sin²α+cos²α=1, чтобы найти одну функцию через другую — не забудьте учесть знак, соответствующий типу угла (острый/тупой).',
        'uz': "Bir trigonometrik funksiyani ikkinchisi orqali topish uchun asosiy ayniyat sin²α+cos²α=1 dan foydalaning — burchak turiga (o'tkir/o'tmas) mos ishorani hisobga olishni unutmang.",
    },
    'math-hard-15': {
        'ru': 'Переведите угол из градусов в радианы, прежде чем использовать формулу длины дуги l=rθ — частая ошибка: подставить угол в градусах напрямую в формулу для радиан.',
        'uz': "Yoy uzunligi formulasi l=rθ dan foydalanishdan oldin burchakni gradusdan radianga o'tkazing — burchakni radian uchun mo'ljallangan formulaga gradusda to'g'ridan-to'g'ri qo'yish xato hisoblanadi.",
    },
    'math-hard-16': {
        'ru': 'Высота, проведённая к основанию равнобедренного треугольника, делит его на два прямоугольных треугольника — используйте теорему Пифагора с половиной основания и боковой стороной.',
        'uz': "Teng yonli uchburchakning asosga tushirilgan balandligi uni ikkita to'g'ri burchakli uchburchakka bo'ladi — asosning yarmi va yon tomon bilan Pifagor teoremasidan foydalaning.",
    },
    'math-hard-17': {
        'ru': 'Найдите правило перехода от числа к результату и проверьте его на всех известных парах, прежде чем применять к новому числу.',
        'uz': "Sondan natijaga o'tish qoidasini toping va uni yangi songa qo'llashdan oldin barcha ma'lum juftliklarda tekshiring.",
    },
    'math-hard-18': {
        'ru': 'Порядок выбора не важен, поэтому используйте формулу сочетаний C(n,k), а не размещений — ошибка в том, чтобы посчитать вариант с учётом порядка, что даёт число в несколько раз больше.',
        'uz': "Tanlash tartibi muhim emas, shuning uchun joylashtirish emas, kombinatsiya formulasi C(n,k) dan foydalaning — tartibni hisobga olib hisoblash bir necha baravar katta son beradi.",
    },
    'math-hard-19': {
        'ru': 'Если цифры не повторяются, а порядок имеет значение, для каждой следующей позиции числа остаётся на одну доступную цифру меньше — перемножьте эти убывающие количества.',
        'uz': "Agar raqamlar takrorlanmasa va tartib muhim bo'lsa, sonning har bir keyingi o'rni uchun bir dona kam raqam qoladi — shu kamayib boruvchi sonlarni bir-biriga ko'paytiring.",
    },
    'math-hard-20': {
        'ru': 'Вероятность двух зависимых событий подряд без возвращения — это произведение условных вероятностей на каждом шаге, а не одна дробь для обоих сразу.',
        'uz': "Ketma-ket ikkita bog'liq voqea (qaytarmasdan) ehtimoli har bir qadamdagi shartli ehtimolliklar ko'paytmasiga teng, ikkalasi uchun bitta kasr emas.",
    },
    'math-hard-21': {
        'ru': 'Упростите условие до «сколько мышей ловит одна кошка за час» — тогда легко масштабировать результат на любое число кошек за то же время.',
        'uz': "Shartni «bitta mushuk bir soatda nechta sichqon tutadi» darajasiga soddalashtiring — shunda natijani xuddi shu vaqt uchun istalgan sondagi mushukka oson moslashtirish mumkin.",
    },
    # -- logic (46) --------------------------------------------------------------------
    'logic-books-interesting-1': {
        'ru': 'В силлогизмах «Все A — B, некоторые A — C» из этого следует только «некоторые B — C» — частая ошибка выводить более сильное утверждение вроде «все B — C».',
        'uz': "«Barcha A — B, ba'zi A — C» sillogizmidan faqat «ba'zi B — C» kelib chiqadi — bundan «barcha B — C» kabi kuchliroq xulosa chiqarish keng tarqalgan xato.",
    },
    'logic-powers-of-2-1': {
        'ru': 'Определите правило перехода между соседними числами (здесь — удвоение) и примените его к последнему известному числу.',
        'uz': "Qo'shni sonlar orasidagi o'tish qoidasini (bu yerda — ikki baravar oshirish) aniqlang va uni oxirgi ma'lum songa qo'llang.",
    },
    'logic-fibonacci-1': {
        'ru': 'Проверьте, не является ли каждое число суммой двух предыдущих (как в ряду Фибоначчи) — это правило легко упустить, если искать только разности или отношения.',
        'uz': "Har bir son oldingi ikkita sonning yig'indisi emasmi (Fibonachchi qatoridagi kabi) tekshiring — faqat farq yoki nisbatlarni izlasangiz bu qoidani osongina o'tkazib yuborasiz.",
    },
    'logic-squares-1': {
        'ru': 'Сравните числа ряда с квадратами натуральных чисел (1²,2²,3²,...) — легко принять этот ряд за обычную арифметическую прогрессию с постоянной разностью.',
        'uz': "Qator sonlarini natural sonlar kvadratlari (1²,2²,3²,...) bilan solishtiring — bu qatorni doimiy farqli oddiy arifmetik progressiya deb xato tushunish oson.",
    },
    'logic-halving-1': {
        'ru': 'Определите правило перехода между соседними числами (здесь — деление пополам) и примените его к последнему известному числу.',
        'uz': "Qo'shni sonlar orasidagi o'tish qoidasini (bu yerda — ikkiga bo'lish) aniqlang va uni oxirgi ma'lum songa qo'llang.",
    },
    'logic-doubling-1': {
        'ru': 'Определите правило перехода между соседними числами (здесь — удвоение) и примените его к последнему известному числу.',
        'uz': "Qo'shni sonlar orasidagi o'tish qoidasini (bu yerda — ikki baravar oshirish) aniqlang va uni oxirgi ma'lum songa qo'llang.",
    },
    'logic-diff-pattern-1': {
        'ru': 'Смотрите не на сам ряд, а на ряд разностей между соседними числами — здесь разности удваиваются на каждом шаге.',
        'uz': "Qatorning o'ziga emas, qo'shni sonlar orasidagi farqlar qatoriga qarang — bu yerda farqlar har qadamda ikki baravar oshadi.",
    },
    'logic-books-paper-1': {
        'ru': 'Из «некоторые A — B» нельзя логически вывести ничего сильнее, чем «некоторые A могут быть B» — частая ошибка утверждать это как безусловный факт для всех.',
        'uz': "«Ba'zi A — B» dan mantiqan «ba'zi A B bo'lishi mumkin» darajasidan kuchliroq narsa chiqarib bo'lmaydi — buni barcha uchun shartsiz fakt sifatida aytish keng tarqalgan xato.",
    },
    'logic-antonym-1': {
        'ru': 'В словесных аналогиях сначала определите точный тип отношения между первой парой слов (здесь — противоположность), затем подберите слово того же типа отношения ко второму слову.',
        'uz': "So'z analogiyalarida avval birinchi juftlik o'rtasidagi aniq munosabat turini (bu yerda — qarama-qarshilik) aniqlang, so'ng ikkinchi so'zga xuddi shu munosabat turidagi so'zni tanlang.",
    },
    'logic-family-1': {
        'ru': 'Постройте семейное дерево по шагам от одного человека к другому, а не пытайтесь удержать все связи в уме сразу — так легче не перепутать поколения.',
        'uz': "Oila daraxtini bir odamdan ikkinchisiga bosqichma-bosqich quring, barcha bog'lanishlarni birdaniga xayolda saqlashga urinmang — shunda avlodlarni chalkashtirmaysiz.",
    },
    'logic-race-position-1': {
        'ru': 'Если вы обогнали бегущего на 2-м месте, вы заняли именно его место — частая ошибка думать, что вы стали первым.',
        'uz': "Agar siz ikkinchi o'rindagi sportchini quvib o'tsangiz, siz aynan uning o'rnini egallaysiz — o'zingizni birinchi o'ringa chiqdim deb o'ylash keng tarqalgan xato.",
    },
    'logic-word-relation-1': {
        'ru': 'Определите точный тип связи первой пары (материал, из которого состоит целое) и подберите аналогичный элемент для второго слова, а не просто связанное по смыслу понятие.',
        'uz': "Birinchi juftlikdagi aniq bog'liqlik turini (butun narsa tarkib topgan material) aniqlang va ikkinchi so'z uchun shunga o'xshash elementni tanlang, shunchaki mazmunan bog'liq tushunchani emas.",
    },
    'logic-siblings-1': {
        'ru': 'У всех дочерей один и тот же брат, а не у каждой свой — значит братьев всего один, и его нужно прибавить только один раз, а не четыре.',
        'uz': "Barcha qizlarning bittagina umumiy akasi bor, har birining alohidasi emas — demak aka bitta, va uni to'rt marta emas, faqat bir marta qo'shish kerak.",
    },
    'logic-contrapositive-1': {
        'ru': 'Логически верным преобразованием импликации «если A, то B» является только обратное отрицание: «если не B, то не A» — обратное утверждение «если B, то A» логически не гарантировано.',
        'uz': "«Agar A bo'lsa, B bo'ladi» mulohazasining mantiqan to'g'ri aylantirilishi faqat teskari inkor: «agar B bo'lmasa, A bo'lmaydi» — «agar B bo'lsa, A bo'ladi» degan teskari mulohaza mantiqan kafolatlanmagan.",
    },
    'logic-clock-hands-1': {
        'ru': 'Стрелки часов накладываются не 24, а 22 раза в сутки — в 12- и 24-часовом цикле есть момент, когда совпадение «пропускается», это легко упустить при простом расчёте.',
        'uz': "Soat millari sutkada 24 emas, 22 marta ustma-ust tushadi — 12 va 24 soatlik davrda mos tushish «o'tkazib yuboriladigan» lahza bor, buni oddiy hisoblashda payqamay qolish oson.",
    },
    'logic-letter-pattern-1': {
        'ru': 'Считайте не сами буквы, а шаг между их позициями в алфавите — здесь шаг увеличивается на единицу каждый раз.',
        'uz': "Harflarning o'zini emas, ularning alifbodagi o'rni orasidagi qadamni sanang — bu yerda qadam har safar bittaga oshadi.",
    },
    'logic-multi-load-balancing-1': {
        'ru': 'В вопросах с несколькими правильными ответами ищите все технически обоснованные меры сразу и отсеивайте варианты, которые явно вредят, а не решают проблему.',
        'uz': "Bir nechta to'g'ri javobli savollarda barcha texnik jihatdan asoslangan choralarni toping va muammoni yechish o'rniga unga zarar keltiradigan variantlarni chetlang.",
    },
    'logic-multi-query-optimization-1': {
        'ru': 'Проверьте каждый вариант на вопрос «действительно ли это ускоряет запрос к базе данных?» — вариант, не относящийся напрямую к производительности, стоит исключить.',
        'uz': "Har bir variantni «bu haqiqatan ham baza so'rovini tezlashtiradimi?» savoli bilan tekshiring — unumdorlikka bevosita aloqasi bo'lmagan variantni chetlang.",
    },
    'logic-multi-api-security-1': {
        'ru': 'Ищите меры, которые реально ограничивают доступ или проверяют подлинность запроса — вариант, открывающий что-либо публично без защиты, всегда противоречит цели «повысить безопасность».',
        'uz': "So'rovga kirishni haqiqatan cheklaydigan yoki uning haqiqiyligini tekshiradigan choralarni toping — biror narsani himoyasiz ochiq qilib qo'yadigan variant «xavfsizlikni oshirish» maqsadiga doim zid keladi.",
    },
    'logic-multi-code-quality-1': {
        'ru': 'Ищите практики, улучшающие структуру и понятность кода — вариант, увеличивающий беспорядок, исключайте сразу.',
        'uz': "Kod tuzilishi va tushunarliligini yaxshilaydigan amaliyotlarni toping — aksincha tartibsizlikni oshiradigan variantni darhol chetlang.",
    },
    'logic-multi-web-performance-1': {
        'ru': 'Ищите меры, реально снижающие объём или время загрузки — вариант, добавляющий лишнюю нагрузку на страницу, противоречит цели ускорения.',
        'uz': "Yuklanish hajmi yoki vaqtini haqiqatan kamaytiradigan choralarni toping — sahifaga qo'shimcha yuklama qo'shadigan variant tezlashtirish maqsadiga zid keladi.",
    },
    'logic-multi-debugging-1': {
        'ru': 'Ищите шаги систематической диагностики проблемы — вариант, полностью уничтожающий код без анализа причины, не решает, а только создаёт новую проблему.',
        'uz': "Muammoni tizimli diagnostika qilish qadamlarini toping — sababni tahlil qilmasdan kodni butunlay yo'q qiladigan variant muammoni yechmaydi, faqat yangisini yaratadi.",
    },
    'logic-multi-git-collab-1': {
        'ru': 'Ищите практики совместной работы через систему контроля версий — вариант, обходящий её, нарушает саму цель совместной разработки.',
        'uz': "Versiyalarni boshqarish tizimi orqali hamkorlikda ishlash amaliyotlarini toping — uni chetlab o'tadigan variant hamkorlikda ishlash maqsadiga zid keladi.",
    },
    'logic-multi-battery-drain-1': {
        'ru': 'Ищите технические причины повышенного расхода ресурсов (память, процессор, сеть) — визуальная настройка сама по себе не расходует батарею так, как фоновые процессы.',
        'uz': "Resurs (xotira, protsessor, tarmoq) sarfini oshiruvchi texnik sabablarni toping — vizual sozlama fon jarayonlari kabi batareyani sarflamaydi.",
    },
    'logic-multi-data-privacy-1': {
        'ru': 'Ищите принципы, защищающие пользователя (согласие, шифрование, прозрачность) — вариант, продлевающий хранение данных без ограничения, противоречит именно этим принципам.',
        'uz': "Foydalanuvchini himoya qiluvchi tamoyillarni (rozilik, shifrlash, shaffoflik) toping — ma'lumotni cheklovsiz saqlaydigan variant aynan shu tamoyillarga zid keladi.",
    },
    'logic-multi-search-scale-1': {
        'ru': 'При больших объёмах данных ищите методы, ускоряющие поиск за счёт структуры данных (индекс, хеш) — линейный перебор каждый раз — это то, от чего нужно уйти при масштабировании.',
        'uz': "Katta hajmdagi ma'lumotda qidiruvni ma'lumot tuzilmasi (indeks, xesh) orqali tezlashtiruvchi usullarni toping — har safar chiziqli qidiruv qilish esa masshtablashda aynan qochish kerak bo'lgan holat.",
    },
    'logic-order-website-slow-1': {
        'ru': 'Диагностика проблемы обычно идёт от воспроизведения и наблюдения к анализу и только затем к исправлению — применить решение, минуя эти шаги, обычно ошибочно.',
        'uz': "Muammoni diagnostika qilish odatda uni qayta hosil qilish va kuzatishdan tahlilga, so'ng yechimga o'tadi — bu qadamlarni o'tkazib yuborib, darhol yechim qo'llash odatda xato bo'ladi.",
    },
    'logic-order-crash-debug-1': {
        'ru': 'Отладка нестабильно работающей программы начинается с воспроизведения ошибки и анализа логов, а тест-кейс и исправление идут уже после понимания причины.',
        'uz': "Beqaror ishlaydigan dasturni tuzatish xatoni qayta hosil qilish va loglarni tahlil qilishdan boshlanadi, test case va tuzatish esa sababni tushungandan keyin keladi.",
    },
    'logic-order-app-dev-1': {
        'ru': 'Разработка идёт от требований к дизайну, затем к коду и только потом к тестированию — пропуск этапа требований или дизайна обычно приводит к переделкам.',
        'uz': "Ishlab chiqish talablardan dizaynga, so'ng kodga va faqat undan keyin testingga o'tadi — talablar yoki dizayn bosqichini o'tkazib yuborish odatda qayta ishlashga olib keladi.",
    },
    'logic-order-query-slow-1': {
        'ru': 'При оптимизации медленного запроса сначала анализируют сам запрос, затем оптимизируют его, и только потом добавляют индекс и проверяют производительность — порядок шагов имеет значение.',
        'uz': "Sekin so'rovni optimallashtirishda avval so'rovning o'zi tahlil qilinadi, so'ng optimallashtiriladi, indeks qo'shish va unumdorlikni tekshirish esa keyin keladi — qadamlar tartibi muhim.",
    },
    'logic-order-debate-prep-1': {
        'ru': 'Подготовка к дебатам идёт от собственной позиции и аргументов к анализу контраргументов и только потом к выводу — пропуск анализа противоположной стороны ослабляет позицию.',
        'uz': "Debatga tayyorgarlik o'z pozitsiyasi va dalillardan qarshi argumentlarni tahlil qilishga, so'ng xulosaga o'tadi — qarshi tomonni tahlil qilishni o'tkazib yuborish pozitsiyani zaiflashtiradi.",
    },
    'logic-order-security-incident-1': {
        'ru': 'Реагирование на инцидент безопасности начинается с проверки логов и определения источника угрозы, и только потом применяются меры защиты и мониторинг.',
        'uz': "Xavfsizlik hodisasiga javob berish loglarni tekshirish va xavf manbasini aniqlashdan boshlanadi, himoya choralari va monitoring esa keyin qo'llaniladi.",
    },
    'logic-order-problem-solving-1': {
        'ru': 'Решение задачи идёт от анализа данных к выбору формулы, затем к вычислению и обязательной проверке результата в конце — пропуск проверки не позволяет заметить ошибку.',
        'uz': "Masalani yechish ma'lumotlarni tahlil qilishdan formula tanlashga, so'ng hisoblashga va oxirida natijani albatta tekshirishga o'tadi — tekshirishni o'tkazib yuborish xatoni payqashga imkon bermaydi.",
    },
    'logic-order-team-project-1': {
        'ru': 'Организация командного проекта идёт от распределения ролей и назначения задач к мониторингу прогресса и только потом к итоговому обзору.',
        'uz': "Jamoaviy loyihani tashkil qilish rollarni taqsimlash va vazifalarni belgilashdan progressni kuzatishga, so'ng yakuniy reviewga o'tadi.",
    },
    'logic-order-profiling-1': {
        'ru': 'Оптимизация медленного приложения начинается с профилирования, чтобы сначала найти узкое место, а не оптимизировать наугад весь код целиком.',
        'uz': "Sekin ilovani optimallashtirish avval profiling qilib bottleneckni topishdan boshlanadi, butun kodni tasodifiy optimallashtirishdan emas.",
    },
    'logic-order-time-management-1': {
        'ru': 'Управление временем идёт от определения приоритетов к составлению расписания, затем к распределению задач и оценке результата — начинать сразу с расписания без приоритетов часто неэффективно.',
        'uz': "Vaqtni boshqarish prioritetlarni aniqlashdan jadval tuzishga, so'ng vazifalarni bo'lishga va natijani baholashga o'tadi — prioritetlarsiz to'g'ridan-to'g'ri jadvaldan boshlash ko'pincha samarasiz.",
    },
    'logic-essay-ai-jobs-1': {
        'ru': 'По рубрике оцениваются четыре части: чёткая позиция, минимум два аргумента, анализ противоположной точки зрения и итоговый вывод — низкий балл чаще всего означает нехватку именно контраргумента или явного вывода.',
        'uz': "Rubrika bo'yicha to'rtta qism baholanadi: aniq pozitsiya, kamida ikkita dalil, qarshi fikr tahlili va yakuniy xulosa — past ball ko'pincha aynan qarshi argument yoki aniq xulosa yetishmasligini bildiradi.",
    },
    'logic-essay-online-education-1': {
        'ru': 'Не забудьте все четыре обязательные части ответа: позицию, минимум два аргумента, разбор противоположного мнения и вывод — эссе без анализа контраргумента получает меньше баллов даже при сильных аргументах.',
        'uz': "Javobning barcha to'rtta majburiy qismini unutmang: pozitsiya, kamida ikkita dalil, qarshi fikr tahlili va xulosa — qarshi argument tahlili bo'lmagan esse kuchli dalillar bo'lsa ham kamroq ball oladi.",
    },
    'logic-essay-smartphones-1': {
        'ru': 'Оценка складывается из позиции, аргументов, анализа контраргумента и вывода — если баллы низкие, перечитайте, действительно ли вы явно разобрали противоположную точку зрения.',
        'uz': "Baho pozitsiya, dalillar, qarshi argument tahlili va xulosadan tashkil topadi — ball past bo'lsa, qarshi fikrni haqiqatan tahlil qilganingizni qayta o'qib chiqing.",
    },
    'logic-essay-python-vs-cpp-1': {
        'ru': 'Убедитесь, что в ответе есть все четыре части рубрики: позиция, минимум два аргумента, анализ противоположного мнения и вывод — пропуск любой из них снижает итоговый балл.',
        'uz': "Javobda rubrikaning barcha to'rtta qismi borligiga ishonch hosil qiling: pozitsiya, kamida ikkita dalil, qarshi fikr tahlili va xulosa — ulardan birortasi tushib qolsa, yakuniy ball pasayadi.",
    },
    'logic-essay-homework-1': {
        'ru': 'Низкий балл за такое эссе почти всегда означает нехватку одной из четырёх частей — чаще всего это либо второй аргумент, либо анализ противоположной точки зрения.',
        'uz': "Bunday esse uchun past ball deyarli har doim to'rtta qismdan birining yetishmasligini bildiradi — ko'pincha bu ikkinchi dalil yoki qarshi fikr tahlili bo'ladi.",
    },
    'logic-essay-future-programmers-1': {
        'ru': 'Структурируйте ответ по всем четырём пунктам явно (например, отдельными предложениями) — так проверяющему легче убедиться, что ни одна часть рубрики не пропущена.',
        'uz': "Javobni barcha to'rtta band bo'yicha aniq tuzing (masalan, alohida gaplar bilan) — shunda tekshiruvchiga rubrikaning birorta qismi tushib qolmaganini ko'rish osonroq bo'ladi.",
    },
    'logic-essay-social-media-1': {
        'ru': 'Помните, что сильная позиция без анализа контраргумента оценивается ниже, чем более скромная позиция с честным разбором противоположной точки зрения.',
        'uz': "Kuchli pozitsiya, agar qarshi argument tahlil qilinmasa, qarshi fikrni halol tahlil qilgan kamtarroq pozitsiyaga qaraganda pastroq baholanishini unutmang.",
    },
    'logic-essay-programmer-salary-1': {
        'ru': 'Проверьте, что в ответе явно присутствуют два независимых аргумента, а не два варианта одной и той же мысли — рубрика оценивает именно разнообразие обоснований.',
        'uz': "Javobda bir xil fikrning ikkita ko'rinishi emas, ikkita mustaqil dalil aniq mavjudligini tekshiring — rubrika aynan asoslarning xilma-xilligini baholaydi.",
    },
    'logic-essay-technology-life-1': {
        'ru': 'Не забудьте завершить ответ явным выводом — эссе, которое просто заканчивается последним аргументом без итога, теряет баллы по этому пункту рубрики.',
        'uz': "Javobni aniq xulosa bilan yakunlashni unutmang — oxirgi dalil bilan xulosasiz tugaydigan esse rubrikaning shu bandi bo'yicha ball yo'qotadi.",
    },
    'logic-essay-it-education-1': {
        'ru': 'Оценка складывается из четырёх равнозначных частей — сосредоточение только на аргументах в пользу своей позиции без анализа противоположной снижает итоговый балл.',
        'uz': "Baho to'rtta teng ahamiyatli qismdan tashkil topadi — faqat o'z pozitsiyasi foydasidagi dalillarga e'tibor qaratib, qarshi fikrni tahlil qilmaslik yakuniy ballni pasaytiradi.",
    },
    # -- creative (25) -----------------------------------------------------------------
    'creative-plan-b-1': {
        'ru': 'Креативный подход ищет альтернативный путь к той же цели («план Б»), а не останавливает работу или ищет виноватых — обращайте внимание на вариант, который меняет средства, но сохраняет цель.',
        'uz': "Kreativ yondashuv bir xil maqsadga muqobil yo'l («B reja») qidiradi, ishni to'xtatib yoki aybdor izlab o'tirmaydi — maqsadni saqlab, vositani o'zgartiradigan variantga e'tibor bering.",
    },
    'creative-presentation-hook-1': {
        'ru': 'Сильное начало презентации цепляет внимание неожиданностью или личной связью с аудиторией — вариант, начинающийся с сухого формального определения, обычно не креативный.',
        'uz': "Kuchli taqdimot boshlanishi kutilmaganlik yoki auditoriya bilan shaxsiy bog'liqlik orqali diqqatni tortadi — quruq rasmiy ta'rifdan boshlaydigan variant odatda kreativ emas.",
    },
    'creative-thesis-interdisciplinary-1': {
        'ru': 'Научная новизна часто рождается на стыке разных областей — ищите вариант, соединяющий тему с чем-то извне, а не просто меняющий или копирующий тему целиком.',
        'uz': "Ilmiy yangilik ko'pincha turli sohalar tutashgan joyda tug'iladi — mavzuni butunlay o'zgartirish yoki ko'chirish emas, uni tashqi soha bilan bog'laydigan variantni qidiring.",
    },
    'creative-app-marketing-1': {
        'ru': 'Креативный маркетинг вовлекает пользователя через интерес и вознаграждение (геймификацию), а не через принуждение или простую раздачу листовок.',
        'uz': "Kreativ marketing foydalanuvchini majburlash yoki oddiy flayer tarqatish orqali emas, qiziqish va mukofot (geymifikatsiya) orqali jalb qiladi.",
    },
    'creative-stairs-gamification-1': {
        'ru': 'Дешёвое креативное решение превращает существующий недостаток (например, скучный подъём по лестнице) в источник вовлечения, а не устраняет его дорогим способом.',
        'uz': "Arzon kreativ yechim mavjud kamchilikni (masalan, zinapoyaning zerikarliligini) qimmat usul bilan yo'q qilish o'rniga, uni qiziqarli tajribaga aylantiradi.",
    },
    'creative-cross-domain-1': {
        'ru': 'Креативность здесь — это перенос метода из своей области в чужую задачу, а не отказ от задачи или поиск готового решения в интернете.',
        'uz': "Bu yerdagi kreativlik — o'z sohasidagi metodni boshqa soha muammosiga ko'chirish, topshiriqdan bosh tortish yoki tayyor yechimni internetdan qidirish emas.",
    },
    'creative-brainstorm-question-1': {
        'ru': 'Вопрос, снимающий ограничения («что если бы возможности были безграничны?»), раскрывает новые идеи — вопрос, критикующий уже предложенное, наоборот, сужает мышление.',
        'uz': "Cheklovlarni olib tashlaydigan savol («agar imkoniyat cheksiz bo'lsa-chi?») yangi g'oyalarni ochadi — allaqachon aytilganni tanqid qiluvchi savol esa, aksincha, fikrlashni toraytiradi.",
    },
    'creative-criticism-1': {
        'ru': 'Профессиональная реакция на резкую критику — разобрать её по частям как бесплатную обратную связь, а не обижаться или сразу отказываться от идеи.',
        'uz': "Keskin tanqidga professional reaksiya — undan xafa bo'lish yoki g'oyadan darhol voz kechish emas, uni bepul faydbek sifatida qismlarga bo'lib tahlil qilishdir.",
    },
    'creative-dorm-project-1': {
        'ru': 'Креативная организация свободного времени создаёт новый формат общения (обмен книгами, дискуссионный клуб), а не сводится к развлечению одного вида или принуждению.',
        'uz': "Bo'sh vaqtni kreativ tashkil qilish yangi muloqot formatini (kitob almashish, munozara klubi) yaratadi, bitta ko'ngilochar tur bilan cheklanmaydi yoki majburlashga tayanmaydi.",
    },
    'creative-mind-maps-1': {
        'ru': 'Креативные визуальные методы (интеллект-карты) систематизируют смысл через связи между понятиями, а не просто повторяют текст в исходном виде.',
        'uz': "Kreativ vizual usullar (intellekt-xaritalar) tushunchalar orasidagi bog'lanishlar orqali mazmunni tizimlashtiradi, matnni asl holicha shunchaki takrorlamaydi.",
    },
    'creative-startup-no-designer-1': {
        'ru': 'При нехватке ресурса ищут доступную замену (нейросети, готовые шаблоны), чтобы двигаться дальше, а не останавливают проект или используют чужой труд без разрешения.',
        'uz': "Resurs yetishmaganda loyihani to'xtatish yoki boshqalarning mehnatini ruxsatsiz ishlatish o'rniga, ilgarilash uchun mavjud almashtiruvchi (neyrotarmoqlar, tayyor shablonlar) qidiriladi.",
    },
    'creative-inversion-1': {
        'ru': 'Метод инверсии переворачивает вопрос наоборот («как добиться худшего результата?»), чтобы через анализ ошибок найти решение — это не то же самое, что искать способ наказания или экономии.',
        'uz': "Inversiya metodi savolni teskarisiga aylantiradi («eng yomon natijaga qanday erishish mumkin?»), xatolarni tahlil qilish orqali yechim topish uchun — bu jazolash yoki tejash yo'lini izlash bilan bir xil emas.",
    },
    'creative-automate-task-1': {
        'ru': 'Креативный подход к скучной механической работе — автоматизировать её (скрипт, макросы), а не терпеть медленно или перекладывать на другого.',
        'uz': "Zerikarli mexanik ishga kreativ yondashuv — uni sekin bajarish yoki boshqaga yuklash emas, avtomatlashtirish (skript, makros)dir.",
    },
    'creative-constraint-teaching-1': {
        'ru': 'Творчество в условиях ограничений превращает нехватку ресурсов в новый формат подачи материала (ролевая игра, живая демонстрация), а не отменяет занятие.',
        'uz': "Cheklovlar ostidagi ijodkorlik resurs yetishmasligini darsni bekor qilish o'rniga materialni yetkazishning yangi formatiga (rolli o'yin, jonli namoyish) aylantiradi.",
    },
    'creative-idea-journal-1': {
        'ru': 'Формирование банка идей — это привычка фиксировать любые мысли сразу, а не полагаться на память или ограничивать себя только своей специальностью.',
        'uz': "G'oyalar bankini shakllantirish — har qanday fikrni darhol yozib borish odatidir, xotiraga tayanish yoki faqat o'z mutaxassisligi bilan cheklanish emas.",
    },
    'creative-empathy-conflict-1': {
        'ru': 'Креативная эмпатия — это смена ролей, чтобы увидеть ситуацию глазами другой стороны, а не наказание или полное невмешательство.',
        'uz': "Kreativ empatiya — tomonlarni bir-birining o'rniga qo'yib, vaziyatni boshqa tomon nigohi bilan ko'rishdir, jazolash yoki umuman aralashmaslik emas.",
    },
    'creative-systemic-test-1': {
        'ru': 'Системная проверка креативной идеи — показать её людям с совершенно другим опытом и посмотреть на реакцию, а не полагаться только на своё мнение.',
        'uz': "Kreativ g'oyani tizimli tekshirish — uni mutloq boshqa tajribaga ega insonlarga ko'rsatib, reaksiyani kuzatishdir, faqat o'z fikriga tayanish emas.",
    },
    'creative-eco-art-1': {
        'ru': 'Запоминающееся креативное мероприятие превращает тему (экологию) в интерактивный опыт (арт-объекты из отходов), а не сводится к лекции или уборке.',
        'uz': "Yodda qoladigan kreativ tadbir mavzuni (ekologiyani) ma'ruza yoki tozalash bilan cheklamay, interaktiv tajribaga (chiqindilardan san'at asarlari) aylantiradi.",
    },
    'creative-combination-game-1': {
        'ru': 'Неожиданная комбинация объединяет две области в одну целостную идею (например, сюжет игры), а не просто добавляет термины одной области в учебник другой.',
        'uz': "Kutilmagan kombinatsiya ikkita sohani bitta yaxlit g'oyaga (masalan, o'yin syujetiga) birlashtiradi, bir soha atamalarini ikkinchisining kitobiga shunchaki qo'shib qo'ymaydi.",
    },
    'creative-presentation-closing-1': {
        'ru': 'Сильное завершение презентации — это призыв к действию с наглядным образом результата, а не формальная благодарность или простое выключение слайдов.',
        'uz': "Kuchli taqdimot yakuni — natijaning vizual obrazi bilan harakatga chaqiruv, rasmiy rahmat yoki slaydlarni shunchaki o'chirish emas.",
    },
    'creative-team-motivation-1': {
        'ru': 'Внутреннюю мотивацию пробуждают, учитывая личные интересы каждого при распределении задач, а не угрозами или выполнением всей работы за других.',
        'uz': "Ichki motivatsiya vazifalarni taqsimlashda har birining shaxsiy qiziqishini hisobga olish orqali uyg'onadi, qo'rqitish yoki ishning hammasini o'zi bajarish orqali emas.",
    },
    'creative-turn-weakness-1': {
        'ru': 'Превращение недостатка в преимущество отвлекает пользователя чем-то полезным или приятным во время ожидания, а не игнорирует проблему или пользователя.',
        'uz': "Kamchilikni afzallikka aylantirish kutish vaqtida foydalanuvchini foydali yoki yoqimli narsa bilan band qiladi, muammoni yoki foydalanuvchini e'tiborsiz qoldirmaydi.",
    },
    'creative-readiness-failure-1': {
        'ru': 'Реализация креативных идей начинается с готовности к первым неудачам и скепсису окружающих, а не с ожидания немедленного успеха и поддержки от всех.',
        'uz': "Kreativ g'oyalarni amalga oshirish dastlabki muvaffaqiyatsizlik va atrofdagilarning skeptik munosabatiga tayyor bo'lishdan boshlanadi, darhol muvaffaqiyat va hammaning qo'llab-quvvatlashini kutishdan emas.",
    },
    'creative-nature-analogy-1': {
        'ru': 'Ищите природную систему, которая структурно похожа на задачу (чёткие роли, общая цель), а не просто первый попавшийся образ.',
        'uz': "Vazifaga tuzilishi jihatidan o'xshash (aniq rollar, umumiy maqsad) tabiiy tizimni qidiring, birinchi ko'zga tashlangan obrazni emas.",
    },
    'creative-soft-skill-value-1': {
        'ru': 'Креативность ценится потому, что стандартные, алгоритмизируемые задачи автоматизируются, а нестандартные решения — нет; это не про отсутствие правил или узкую сферу применения только в искусстве.',
        'uz': "Kreativlik qadrlanadi, chunki standart, algoritmlashtiriladigan vazifalar avtomatlashadi, nostandart yechimlar esa yo'q; bu qoidasizlik yoki faqat san'at sohasiga tegishlilik degani emas.",
    },
    # -- problem_solving (31) ------------------------------------------------------------
    'ps-core-1': {
        'ru': 'Первый и решающий шаг — чётко сформулировать саму проблему и её первопричину, а не сразу переходить к готовым решениям или ждать, что всё разрешится само.',
        'uz': "Birinchi va hal qiluvchi qadam — muammoning o'zini va uning tub sababini aniq ta'riflashdir, darhol tayyor yechimlarga o'tish yoki o'z-o'zidan hal bo'lishini kutish emas.",
    },
    'ps-core-2': {
        'ru': 'Правильное решение командной проблемы — перераспределить задачи и помочь, сохранив общую цель, а не исключать человека или срывать сроки.',
        'uz': "Jamoaviy muammoning to'g'ri yechimi — umumiy maqsadni saqlab, vazifalarni qayta taqsimlash va yordam berish, insonni chetlashtirish yoki muddatni buzish emas.",
    },
    'ps-core-3': {
        'ru': 'Научный подход к неверной гипотезе — проанализировать причину ошибки и выдвинуть новую, а не подделывать данные или обвинять оборудование.',
        'uz': "Noto'g'ri gipotezaga ilmiy yondashuv — xatolik sababini tahlil qilib, yangi gipoteza ilgari surish, ma'lumotlarni soxtalashtirish yoki jihozni ayblash emas.",
    },
    'ps-core-4': {
        'ru': 'Конструктивная реакция на резкую критику — отделить эмоции и выделить обоснованные пункты для доработки, а не спорить или бросать проект.',
        'uz': "Keskin tanqidga konstruktiv reaksiya — hissiyotlarni chetga surib, asosli punktlarni ajratib, ular asosida takomillashtirish, bahslashish yoki loyihadan voz kechish emas.",
    },
    'ps-core-5': {
        'ru': 'Системное решение устраняет саму причину очереди через оцифровку процесса, а не ограничивает доступ или нанимает человека следить за порядком.',
        'uz': "Tizimli yechim jarayonni raqamlashtirish orqali navbatning tub sababini bartaraf etadi, kirishni cheklash yoki tartib uchun odam yollash emas.",
    },
    'ps-core-6': {
        'ru': 'При техническом сбое во время важного события первым делом фиксируют проблему официально, а не пытаются чинить самостоятельно или устраивают скандал.',
        'uz': "Muhim voqea paytida texnik nosozlik yuz berganda birinchi navbatda muammoni rasmiy qayd ettirish kerak, o'zi tuzatishga urinish yoki janjal qilish emas.",
    },
    'ps-core-7': {
        'ru': 'Слепое следование единственному решению без критики — это ловушка группового мышления (groupthink), а не эффективная экономия времени.',
        'uz': "Tanqidsiz yagona yechimga ko'r-ko'rona ergashish — bu vaqtni tejash emas, «guruhbozlik fikrlashi» (groupthink) tuzog'idir.",
    },
    'ps-core-8': {
        'ru': 'Медиатор в конфликте объективно сравнивает аргументы обеих сторон по критериям, соответствующим цели проекта, а не встаёт на чью-то сторону.',
        'uz': "Mediator nizoda ikkala tomon dalillarini loyiha maqsadiga mos mezonlar bo'yicha xolisona solishtiradi, birortasining tarafini olmaydi.",
    },
    'ps-core-9': {
        'ru': 'Декомпозиция — это разбиение большой задачи на более мелкие и решаемые части, а не отказ от задачи или поиск готового ответа.',
        'uz': "Dekompozitsiya — katta vazifani kichikroq va yechiladigan qismlarga bo'lish, vazifadan voz kechish yoki tayyor javob qidirish emas.",
    },
    'ps-core-10': {
        'ru': 'При резком сокращении времени переходят к формату «Elevator Pitch» — доносят только суть (проблема, решение, выгода), а не пытаются быстро проговорить весь материал.',
        'uz': "Vaqt keskin qisqarganda «Elevator Pitch» formatiga o'tiladi — faqat mag'iz (muammo, yechim, foyda) yetkaziladi, butun materialni tez gapirib o'tishga urinilmaydi.",
    },
    'ps-core-11': {
        'ru': 'Метод «5 Почему?» — это последовательные вопросы «почему», ведущие к истинной первопричине, а не деление проблемы на части или простое обсуждение.',
        'uz': "«5 Nega?» metodi — muammoning tub ildiziga olib boradigan ketma-ket «nega» savollari, muammoni bo'laklarga bo'lish yoki bir necha kun muhokama qilish emas.",
    },
    'ps-core-12': {
        'ru': 'Первый технический шаг при неудачном результате — диагностика через обратную связь, чтобы понять, какой именно модуль не работает, а не обвинение пользователей.',
        'uz': "Muvaffaqiyatsiz natijada birinchi texnik qadam — aynan qaysi modul ishlamayotganini aniqlash uchun faydbek orqali diagnostika, foydalanuvchilarni ayblash emas.",
    },
    'ps-core-13': {
        'ru': 'Активное слушание — задавать уточняющие вопросы и перефразировать услышанное, чтобы точно понять проблему, а не сразу давать советы.',
        'uz': "Faol eshitish — muammoni aniq tushunish uchun aniqlashtiruvchi savollar berish va eshitilganni qayta so'zlash, darhol maslahat berish emas.",
    },
    'ps-core-14': {
        'ru': 'Отсутствие критики и слепое согласие с руководителем в группе называется синдромом «Yes-man» (конформизм), а не профессионализмом.',
        'uz': "Guruhda tanqidsiz, rahbarga ko'r-ko'rona qo'shilish «Yes-man» sindromi (konformizm) deb ataladi, professionalizm emas.",
    },
    'ps-core-15': {
        'ru': 'При внешних препятствиях, не зависящих от вас, разумно временно переключиться на альтернативные направления, а не нарушать правила или всё бросать.',
        'uz': "Sizga bog'liq bo'lmagan tashqi to'siqlarda vaqtincha muqobil yo'nalishlarga o'tish oqilona, qoidalarni buzish yoki hammasidan voz kechish emas.",
    },
    'ps-core-16': {
        'ru': 'Техника «подталкивания» (Nudge) создаёт позитивные стимулы для желаемого поведения, а не запугивает и не усложняет систему.',
        'uz': "«Nudge» texnikasi istalgan xatti-harakat uchun ijobiy rag'batlar yaratadi, qo'rqitish yoki tizimni murakkablashtirish emas.",
    },
    'ps-core-17': {
        'ru': 'Абстрактное мышление помогает увидеть общую структуру проблемы и её связь с другими системами на макроуровне, а не относится только к работе с точными цифрами.',
        'uz': "Abstrakt fikrlash muammoning umumiy tuzilishi va boshqa tizimlar bilan bog'liqligini makro-darajada ko'rishga yordam beradi, bu faqat aniq raqamlar bilan ishlashga tegishli emas.",
    },
    'ps-core-18': {
        'ru': 'При неожиданном форс-мажоре сильный руководитель сразу ищет альтернативный план действий, а не паникует и не ждёт бездействуя.',
        'uz': "Kutilmagan fors-majorda kuchli rahbar darhol muqobil harakat rejasini qidiradi, vahima qilib yoki harakatsiz kutib o'tirmaydi.",
    },
    'ps-core-19': {
        'ru': 'Логические ошибки (fallacies) приводят к неверной трактовке фактов и решениям под влиянием эмоций, а не помогают быстрее решить проблему.',
        'uz': "Mantiqiy xatolar (fallacies) faktlarni noto'g'ri talqin qilish va his-tuyg'ular ta'sirida qaror qabul qilishga olib keladi, muammoni tezroq hal qilishga yordam bermaydi.",
    },
    'ps-core-20': {
        'ru': 'Объективная проверка эффективности решения — сравнение состояния «до» и «после» через конкретные метрики (KPI), а не собственное мнение.',
        'uz': "Yechim samaradorligini xolis tekshirish — aniq metrikalar (KPI) orqali «oldin» va «keyin» holatini solishtirish, o'z fikri emas.",
    },
    'ps-core-21': {
        'ru': 'Навык решения проблем ценен потому, что готовые шаблоны быстро устаревают в меняющемся мире, а не потому, что это обязательный предмет.',
        'uz': "Muammo yechish ko'nikmasi qadrlanadi, chunki tayyor andozalar o'zgaruvchan dunyoda tezda eskiradi, bu majburiy fan bo'lgani uchun emas.",
    },
    'ps-scenario-1': {
        'ru': 'Ответственность за общую цель означает взять на себя недостающую часть работы, а не требовать от больного человека или обвинять его.',
        'uz': "Umumiy maqsad uchun mas'uliyat — kasal odamdan talab qilish yoki uni ayblash emas, yetishmayotgan qismni o'z zimmasiga olishni anglatadi.",
    },
    'ps-scenario-2': {
        'ru': 'Проблему сложного интерфейса решают мгновенной подсказкой на месте и последующим упрощением на основе отзывов, а не обвинением пользователей.',
        'uz': "Murakkab interfeys muammosi darhol yordamchi ko'rsatma va keyinchalik faydbek asosida soddalashtirish orqali yechiladi, foydalanuvchilarni ayblash emas.",
    },
    'ps-scenario-3': {
        'ru': 'При сбое системы во время экзамена важно немедленно зафиксировать проблему официально и попросить пересдать, а не гадать ответы или чинить технику самому.',
        'uz': "Imtihon paytida tizim nosozligida muammoni darhol rasmiy qayd ettirib, qayta topshirish imkonini so'rash muhim, javoblarni tavakkaliga belgilash emas.",
    },
    'ps-scenario-4': {
        'ru': 'Лидер объективно анализирует аргументы обеих сторон и предлагает гибридное решение, а не поддерживает более авторитетного или выбирает случайный вариант.',
        'uz': "Yetakchi ikkala tomon dalillarini xolis tahlil qilib, gibrid yechim taklif qiladi, obro'lirog'ini qo'llab-quvvatlamaydi.",
    },
    'ps-scenario-5': {
        'ru': 'При нехватке местных источников обращаются к международным научным базам, а не меняют тему или подделывают список литературы.',
        'uz': "Mahalliy manbalar yetishmaganda xalqaro ilmiy bazalarga murojaat qilinadi, mavzu o'zgartirilmaydi yoki adabiyotlar ro'yxati soxtalashtirilmaydi.",
    },
    'ps-scenario-6': {
        'ru': 'Эффективное решение однообразной механической работы — изучить способы автоматизации и предложить оптимизацию руководителю, а не тратить время впустую.',
        'uz': "Bir xil andozadagi mexanik ishning samarali yechimi — avtomatlashtirish yo'llarini o'rganib, rahbarga optimallashtirish taklif qilish, vaqtni behuda o'tkazish emas.",
    },
    'ps-scenario-7': {
        'ru': 'При резком сокращении времени выступления сосредотачиваются на самой сути (проблема, решение, выгода), а не пытаются быстро проговорить все слайды.',
        'uz': "Nutq vaqti keskin qisqarganda eng asosiy narsaga (muammo, yechim, foyda) e'tibor qaratiladi, barcha slaydlarni tez gapirib o'tishga urinilmaydi.",
    },
    'ps-scenario-8': {
        'ru': 'Системную ошибку устраняют через декомпозицию кода на модули и диагностику по логам, а не удаляют всю программу или обвиняют пользователей.',
        'uz': "Tizimli xatolik kodni modullarga bo'lib, loglar orqali diagnostika qilish bilan bartaraf etiladi, dasturni butunlay o'chirish emas.",
    },
    'ps-scenario-9': {
        'ru': 'При полном отключении техники семинар спасают, переведя его в живой интерактивный формат (доска, обсуждение), а не отменяют его.',
        'uz': "Texnika butunlay o'chganda seminar uni jonli interaktiv formatga (doska, munozara) o'tkazish orqali saqlab qolinadi, bekor qilish emas.",
    },
    'ps-scenario-10': {
        'ru': 'Системное решение проблемы одногруппника — лично выяснить истинную причину и организовать помощь, а не наказывать или полностью игнорировать ситуацию.',
        'uz': "Guruhdoshning muammosini tizimli yechish — jazolash yoki vaziyatga aralashmaslik emas, shaxsan tub sababni aniqlab, yordam tashkil qilishdir.",
    },
    # -- attention (5) -------------------------------------------------------------------
    'attn-exact-match-1': {
        'ru': 'Сравнивайте образец с каждым вариантом посимвольно, а не «на глаз» целиком — так легче заметить переставленную или изменённую цифру.',
        'uz': "Namunani har bir variant bilan yaxlit emas, belgi-belgi solishtiring — shunda o'rni almashgan yoki o'zgargan raqamni payqash osonroq.",
    },
    'attn-spelling-1': {
        'ru': 'Читайте каждое слово по слогам, а не бегло — ошибки часто прячутся в удвоенных или похожих по звучанию буквах.',
        'uz': "Har bir so'zni yugurib emas, bo'g'inlab o'qing — xatolar ko'pincha qo'sh yoki ovozi o'xshash harflarda yashiringan bo'ladi.",
    },
    'attn-letter-count-1': {
        'ru': 'Считайте вхождения буквы, отмечая уже посчитанные, а не полагаясь на память — легко пропустить одно вхождение или посчитать одно и то же дважды.',
        'uz': "Harf uchraganda uni belgilab sanang, xotiraga tayanmang — bitta uchrashni o'tkazib yuborish yoki bir xilini ikki marta sanash oson.",
    },
    'attn-pattern-break-1': {
        'ru': 'Сравнивайте последовательность с образцом узора блок за блоком, а не всю строку целиком — так легче найти именно ту позицию, где порядок нарушен.',
        'uz': "Ketma-ketlikni namuna naqshi bilan butunlay emas, blok-blok solishtiring — shunda tartib buzilgan aniq pozitsiyani topish osonroq.",
    },
    'attn-row-compare-1': {
        'ru': 'Сравнивайте числа блоками одинаковой длины по порядку, а не всю строку сразу — различие может прятаться в середине, если проверять только начало и конец.',
        'uz': "Sonlarni tartib bo'yicha bir xil uzunlikdagi bloklarda solishtiring, butun qatorni birdaniga emas — faqat boshi va oxirini tekshirsangiz, farq o'rtada yashiringan bo'lishi mumkin.",
    },
    # -- iq (5) ----------------------------------------------------------------------------
    'iq-series-1': {
        'ru': 'Смотрите на разности между соседними числами — здесь разность растёт на постоянную величину каждый раз, это легко упустить, если искать единый постоянный шаг ряда.',
        'uz': "Qo'shni sonlar orasidagi farqlarga qarang — bu yerda farq har safar doimiy miqdorga oshadi, yagona doimiy qadamni izlasangiz buni payqamay qolish oson.",
    },
    'iq-odd-one-out-1': {
        'ru': 'Ищите общий признак у трёх слов (например, все — геометрические фигуры) и то слово, которое явно выпадает из этой категории по смыслу.',
        'uz': "Uchta so'zning umumiy belgisini (masalan, hammasi geometrik shakl ekanligini) va ma'no jihatidan shu toifadan aniq chetga chiqadigan so'zni toping.",
    },
    'iq-analogy-1': {
        'ru': 'Определите точный тип отношения в первой паре (предмет одежды/защиты для части тела) и подберите аналогичный предмет для второй части тела.',
        'uz': "Birinchi juftlikdagi aniq munosabat turini (tana qismi uchun kiyim/himoya buyumi) aniqlang va ikkinchi tana qismi uchun shunga o'xshash buyumni tanlang.",
    },
    'iq-shape-pattern-1': {
        'ru': 'Считайте не сами фигуры, а количество сторон у каждой — оно увеличивается на единицу с каждым шагом.',
        'uz': "Shakllarning o'zini emas, har birining tomonlar sonini sanang — u har qadamda bittaga oshadi.",
    },
    'iq-combinatorics-1': {
        'ru': 'Каждое рукопожатие — это пара из общего числа людей, поэтому считайте по формуле сочетаний C(n,2), а не просто умножайте число людей на количество попыток каждого.',
        'uz': "Har bir qo'l siqish odamlar sonidan tuzilgan juftlik, shuning uchun C(n,2) kombinatsiya formulasi bilan sanang, odamlar sonini har birining urinishlar soniga shunchaki ko'paytirmang.",
    },
    # -- algorithmic (20) ------------------------------------------------------------------
    'algorithmic-boolean-1': {
        'ru': 'Логическое И (AND) истинно только тогда, когда ОБА условия истинны — если хотя бы одно ложно, результат всегда ложь.',
        'uz': "Mantiqiy VA (AND) faqat ikkala shart ham rost bo'lganda rost bo'ladi — kamida bittasi yolg'on bo'lsa, natija doim yolg'on.",
    },
    'algorithmic-flowchart-1': {
        'ru': 'В блок-схемах у каждой геометрической фигуры своё назначение: ромб — это именно проверка условия, а прямоугольник обозначает обычное действие.',
        'uz': "Blok-sxemalarda har bir geometrik shaklning o'z vazifasi bor: romb aynan shartni tekshirish, to'g'ri to'rtburchak esa oddiy amalni bildiradi.",
    },
    'algorithmic-linear-structure-1': {
        'ru': 'Линейная структура — это выполнение шагов строго последовательно без ветвлений и условий, в отличие от структур с условиями или циклами.',
        'uz': "Chiziqli tuzilma — shartlar yoki tarmoqlanishlarsiz qadamlarning qat'iy ketma-ket bajarilishi, shartli yoki siklli tuzilmalardan farqli o'laroq.",
    },
    'algorithmic-property-finiteness-1': {
        'ru': 'Конечность алгоритма означает, что он обязательно завершится за конечное число шагов — это не связано со сложностью алгоритма или тем, кто его понимает.',
        'uz': "Algoritmning cheklanganligi u cheklangan sondagi qadamlardan so'ng albatta yakunlanishini bildiradi — bu algoritmning murakkabligiga bog'liq emas.",
    },
    'algorithmic-recursion-1': {
        'ru': 'Рекурсия — это обращение функции к самой себе для решения меньшей версии той же задачи, а не сортировка, ошибка или удаление данных.',
        'uz': "Rekursiya — funksiyaning xuddi shu vazifaning kichikroq versiyasini yechish uchun o'z-o'ziga murojaat qilishi, saralash, xatolik yoki ma'lumotni o'chirish emas.",
    },
    'algorithmic-trace-1': {
        'ru': 'Трассируйте код шаг за шагом, обновляя значение переменной после каждой строки — ошибка в том, чтобы применить оба действия к исходному значению одновременно.',
        'uz': "Kodni har bir qatordan keyin o'zgaruvchi qiymatini yangilab, bosqichma-bosqich kuzating — ikkala amalni boshlang'ich qiymatga bir vaqtda qo'llash xato hisoblanadi.",
    },
    'algorithmic-loop-1': {
        'ru': 'Считайте количество раз, когда условие цикла проверяется истинным и тело цикла выполняется, а не итоговое значение переменной — цикл останавливается, как только условие становится ложным.',
        'uz': "Sikl shartining necha marta rost bo'lib, sikl tanasi bajarilganini sanang, o'zgaruvchining yakuniy qiymatini emas — shart yolg'on bo'lishi bilanoq sikl to'xtaydi.",
    },
    'algorithmic-infinite-loop-1': {
        'ru': 'Бесконечный цикл — это процесс, у которого условие выхода никогда не выполняется, а не быстрая программа или полностью бинарный код.',
        'uz': "Cheksiz sikl — chiqish sharti hech qachon bajarilmaydigan jarayon, tez ishlaydigan dastur yoki butunlay ikkilik kod emas.",
    },
    'algorithmic-robot-1': {
        'ru': 'Раскладывайте перемещение по осям отдельно (вперёд-назад и влево-вправо) и складывайте шаги на каждой оси независимо.',
        'uz': "Harakatni o'qlar bo'yicha alohida yoying (oldi-orqa va o'ng-chap) va har bir o'q bo'yicha qadamlarni mustaqil qo'shing.",
    },
    'algorithmic-property-definiteness-1': {
        'ru': 'Результативность алгоритма означает получение ожидаемого результата или явного сообщения об ошибке после конечных шагов — это не про длину алгоритма или внешний вид программы.',
        'uz': "Algoritmning natijaviyligi — cheklangan qadamlardan so'ng kutilgan natija yoki aniq xatolik xabarini olishni bildiradi, bu algoritm uzunligi yoki dastur tashqi ko'rinishiga aloqador emas.",
    },
    'algorithmic-stack-1': {
        'ru': 'Stack обрабатывает элементы по правилу LIFO (последний пришёл — первый вышел) — не путайте это с FIFO, которое использует другая структура данных (очередь).',
        'uz': "Stack elementlarni LIFO qoidasi (oxirgi kelgan — birinchi ketadi) bo'yicha qayta ishlaydi — buni boshqa ma'lumotlar tuzilmasi (navbat) ishlatadigan FIFO bilan chalkashtirmang.",
    },
    'algorithmic-sequence-1': {
        'ru': 'Сначала проверьте условие (заряд 0%), затем выполняйте шаги в их логической зависимости друг от друга — подключение к зарядке должно предшествовать ожиданию экрана.',
        'uz': "Avval shartni (quvvat 0%) tekshiring, so'ng qadamlarni bir-biriga mantiqiy bog'liqligiga ko'ra bajaring — quvvatlashga ulash ekran yonishini kutishdan oldin bo'lishi kerak.",
    },
    'algorithmic-conditional-1': {
        'ru': 'Условие «если A и B» срабатывает, только если ОБА условия верны одновременно — если хотя бы одно неверно, выполняется ветка «иначе».',
        'uz': "«Agar A va B» sharti faqat ikkalasi ham bir vaqtda rost bo'lganda ishga tushadi — kamida bittasi noto'g'ri bo'lsa, «aks holda» bo'limi bajariladi.",
    },
    'algorithmic-bubble-sort-1': {
        'ru': 'Пузырьковая сортировка на первом шаге сравнивает первые два соседних элемента слева направо и меняет их местами, если левый больше правого.',
        'uz': "Ko'pikli saralash birinchi qadamda chapdan o'ngga birinchi ikkita qo'shni elementni solishtiradi va agar chapdagisi kattaroq bo'lsa, ularni almashtiradi.",
    },
    'algorithmic-traffic-light-1': {
        'ru': 'Раскладывайте номер шага на полные циклы и остаток — остаток указывает, в какой момент внутри одного повторения цикла вы находитесь.',
        'uz': "Qadam raqamini to'liq davrlar va qoldiqqa yoying — qoldiq siklning bitta takrorlanishi ichida qaysi lahzada turganingizni ko'rsatadi.",
    },
    'algorithmic-weighing-1': {
        'ru': 'При 3 монетах достаточно положить по одной на каждую чашу весов: если они равны, фальшивая — оставшаяся, если нет — та, что легче; это всего 1 взвешивание.',
        'uz': "3 ta tangada tarozining har biriga bittadan qo'yish yetarli: agar teng bo'lsa, soxtasi qolgani, teng bo'lmasa — yengilrog'i; bu atigi 1 marta tortish.",
    },
    'algorithmic-binary-search-1': {
        'ru': 'Бинарный поиск всегда начинает с середины диапазона, а не с искомого числа или с одного из краёв.',
        'uz': "Binoriy qidiruv har doim diapazon o'rtasidan boshlanadi, izlanayotgan sondan yoki chetidan emas.",
    },
    'algorithmic-recursion-2': {
        'ru': 'Применяйте рекурсивное правило шаг за шагом от известных базовых значений, вычисляя каждое следующее F(n) только после того, как найдены оба предыдущих.',
        'uz': "Rekursiv qoidani ma'lum bazaviy qiymatlardan boshlab bosqichma-bosqich qo'llang, har bir keyingi F(n) ni faqat ikkita oldingisi topilgandan keyin hisoblang.",
    },
    'algorithmic-swap-1': {
        'ru': 'Обмен значений без третьей переменной строится на обратимых операциях (сложение/вычитание или XOR), которые позволяют восстановить оба значения по очереди.',
        'uz': "Uchinchi o'zgaruvchisiz qiymatlarni almashtirish qaytariladigan amallarga (qo'shish/ayirish yoki XOR) asoslanadi, bu ikkala qiymatni navbat bilan tiklashga imkon beradi.",
    },
    'algorithmic-code-trace-1': {
        'ru': 'Сначала проверьте, выполняется ли условие, и только потом выполняйте нужную ветку — если условие ложно, изменяется переменная из ветки «иначе».',
        'uz': "Avval shart bajarilishini tekshiring va faqat shundan keyin mos bo'limni bajaring — shart yolg'on bo'lsa, «aks holda» bo'limidagi o'zgaruvchi o'zgaradi.",
    },
}
