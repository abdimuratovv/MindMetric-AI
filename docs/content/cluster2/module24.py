from authoring import lesson as l, module, n, s


def build():
    return module('solutions-optimization', 4,
        'Ko‘p variantli yechimlar va optimizatsiya || Варианты решений и оптимизация', ['algorithmic', 'problem_solving'], [
        l('opt-equivalence', 'Bir masalaga bir nechta yechim || Несколько решений одной задачи', [
            'Yechimlarni taqqoslashdan oldin bir xil vazifani bajarishini tekshiring: kirish sohasi, chiqish va chekka holatlar teng bo‘lsin. Tez, lekin noto‘g‘ri algoritm mos yechim emas. || До сравнения решений проверьте, что они решают одну задачу: одинаковы область входа, выход и крайние случаи. Быстрый, но неверный алгоритм не подходит.',
            'Musbat n uchun yig‘indini siklda jamlash yoki n × (n + 1) / 2 orqali hisoblash mumkin. Kursda bu misoldagi arifmetika aniq, katta butun sonlarni ko‘tara oladi deb olinadi; real tilda tur chegarasi tekshiriladi. || Для положительного n сумму можно накопить в цикле или вычислить как n × (n + 1) / 2. В этом примере арифметика курса считается точной и поддерживающей большие целые; в реальном языке проверяют границы типа.',
            'Yangi yechimni odatiy, eng kichik va chegara holatlarida tekshiring. Bir nechta bir xil javob moslikka dalil bo‘ladi, barcha holat uchun isbot o‘rnini bosmaydi. || Проверяйте новое решение на обычном, минимальном и граничном случаях. Несколько одинаковых ответов дают свидетельство совпадения, но не заменяют доказательство для всех случаев.'
        ], 'n = 5. Siklli yig‘indi va formula natijalarini solishtiring. || n = 5. Сравните сумму в цикле и результат формулы.',
           'Sikl: 1 + 2 + 3 + 4 + 5 = 15.|Formula: 5 × 6 / 2 = 15.|Bu kirishda natijalar teng. || Цикл: 1 + 2 + 3 + 4 + 5 = 15.|Формула: 5 × 6 / 2 = 15.|На этом входе результаты равны.', '15; 15 || 15; 15', [
            n('1 dan 8 gacha yig‘indini n × (n + 1) / 2 formulasi bilan toping. || Найдите сумму от 1 до 8 по формуле n × (n + 1) / 2.', 36,
              'n = 8 ni qo‘yamiz.|8 × 9 / 2 = 36. || Подставляем n = 8.|8 × 9 / 2 = 36.',
              'n + 1 ko‘paytuvchisini n − 1 bilan almashtirmang. || Не заменяйте множитель n + 1 на n − 1.',
              'Yig‘indining ikki uchini juftlash formulasini ishlating. || Используйте формулу попарного сложения концов суммы.'),
            s('A ro‘yxatdagi birinchi juft sonni, B esa eng katta juft sonni qaytaradi. Ularni bir masalaning yechimlari deb tezlikda solishtirish mumkinmi? || A возвращает первое чётное число списка, B — наибольшее чётное. Можно ли сравнивать их по скорости как решения одной задачи?', [
                ('Avval chiqish talabi tenglashtiriladi || Сначала нужно согласовать требуемый выход', 'Ular turli savollarga javob beradi. || Они отвечают на разные вопросы.'),
                ('Ha, ikkalasida juft son bor || Да, в обоих есть чётное число', 'Umumiy xususiyat bir xil natija shartini bermaydi. || Общее свойство не означает одинакового требования к результату.'),
                ('Har doim B tezroq || B всегда быстрее', 'Vazifalar farqi bunday xulosaga asos bermaydi. || Различие задач не даёт основания для такого вывода.')],
              'Birinchi va eng katta — turli mezon.|Bir xil spetsifikatsiya bo‘lmaguncha tezlik taqqoslanmaydi. || Первый и наибольший — разные критерии.|Без одинаковой спецификации скорость не сравнивается.',
              'Nomlari o‘xshash algoritmlarning maqsadini tekshiring. || Проверяйте цель алгоритмов с похожими названиями.',
              'Ro‘yxatdagi eng katta juft qiymat har doim birinchimi? || Всегда ли наибольшее чётное значение в списке стоит первым?'),
            s('Ikki algoritm bitta kirishda teng javob berdi. Qaysi xulosa asosli? || Два алгоритма дали одинаковый ответ на одном входе. Какой вывод обоснован?', [
                ('Faqat tekshirilgan kirishda moslik ko‘rildi || Совпадение наблюдалось только на проверенном входе', 'Boshqa kirishlar hali tekshirilmagan. || Другие входы ещё не проверены.'),
                ('Barcha kirishda tengligi isbotlandi || Доказано равенство на всех входах', 'Bitta misol umumiy isbot emas. || Один пример не является общим доказательством.'),
                ('Ikkalasi barcha kirishda xato || Оба ошибочны на всех входах', 'Moslik bunday inkorni ham ko‘rsatmaydi. || Совпадение не доказывает и такое отрицание.')],
              'Misol faqat o‘z kirishi haqida dalil.|Umumiy moslik uchun qo‘shimcha tahlil kerak. || Пример свидетельствует только о своём входе.|Для общего совпадения нужен дополнительный анализ.',
              'Test natijasi bilan isbotni bir xil deb olmang. || Не отождествляйте результат теста и доказательство.'),
            n('Formula 1 dan n gacha yig‘indini hisoblaydi. n = 1 uchun eng kichik musbat holatdagi natija? || Формула вычисляет сумму от 1 до n. Каков результат при минимальном положительном n = 1?', 1,
              'Yig‘indi faqat 1 dan iborat.|1 × (1 + 1) / 2 = 1. || Сумма состоит только из 1.|1 × (1 + 1) / 2 = 1.',
              'Minimal kirishni bo‘sh yig‘indi bilan almashtirmang. || Не заменяйте минимальный вход пустой суммой.')]),
        l('opt-time', 'Amallar soni va o‘sish || Число операций и рост', [
            'Bir xil oddiy amalni sanash vaqt xarajatini taxminiy taqqoslaydi. T(n) = n bilan T(n) = n² katta n da turlicha o‘sadi. Bu devordagi sekundning aniq bashorati emas. || Подсчёт одинаковых простых операций приближённо сравнивает временные затраты. T(n) = n и T(n) = n² по-разному растут при большом n. Это не точный прогноз секунд.',
            'Ketma-ket ikki siklning ishlari qo‘shiladi; ichma-ich mustaqil sikllarda ko‘payadi. Bir xil chegara bilan ketma-ketlik va ichma-ichlikni ajrating. || Работа двух последовательных циклов складывается; у независимых вложенных — умножается. Различайте последовательность и вложенность при одинаковой границе.',
            'O(n) o‘sish uchun yuqori chegara yozuvi. Ushbu darsdagi aniq chiziqli va kvadratik misollarni amallar soni bilan tushuntiramiz; doimiy omillar va kirish xususiyatlari ham amaliy natijaga ta’sir qiladi. || O(n) обозначает верхнюю границу роста. Точные линейные и квадратичные примеры этого урока объясняются подсчётом операций; постоянные множители и свойства входа также влияют на практический результат.'
        ], 'A n ta, B n × n ta bir xil ish qiladi. n = 10 da ishlar soni? || A выполняет n, B — n × n одинаковых действий. Каковы количества при n = 10?',
           'A: 10 ta.|B: 10 × 10 = 100 ta.|Faqat shu hisob modeli bo‘yicha A kamroq ish qiladi. || A: 10 действий.|B: 10 × 10 = 100 действий.|Только в этой модели A делает меньше работы.', '10; 100 || 10; 100', [
            n('Ketma-ket ikki sikl bor: birinchisi 7, ikkinchisi 5 marta bir xil amal qiladi. Jami amal? || Два последовательных цикла: первый выполняет одинаковое действие 7 раз, второй — 5 раз. Сколько действий всего?', 12,
              'Ketma-ket ishlar qo‘shiladi.|7 + 5 = 12. || Последовательные работы складываются.|7 + 5 = 12.',
              'Ketma-ket sikllarni ko‘paytirmang. || Не перемножайте последовательные циклы.',
              'Ikkinchi sikl birinchining ichida emas. || Второй цикл не находится внутри первого.'),
            n('Tashqi sikl 5 marta, har safar ichki sikl 6 marta bir xil amal qiladi. Jami amal? || Внешний цикл выполняется 5 раз, каждый раз внутренний делает одинаковое действие 6 раз. Сколько действий всего?', 30,
              'Har tashqi aylanishda 6 ish.|5 × 6 = 30. || На каждом внешнем проходе 6 действий.|5 × 6 = 30.',
              'Ichma-ich ishni ketma-ket ish kabi qo‘shmang. || Не складывайте вложенную работу как последовательную.',
              'Ichki ish har tashqi aylanishda takrorlanadi. || Внутренняя работа повторяется на каждом внешнем проходе.'),
            n('T(n) = n². n qiymati 4 dan 8 ga oshsa, amallar soni necha baravar oshadi? || T(n) = n². Во сколько раз растёт число операций при увеличении n с 4 до 8?', 4,
              'T(4) = 16, T(8) = 64.|64 / 16 = 4. || T(4) = 16, T(8) = 64.|64 / 16 = 4.',
              'Kirish ikki baravar bo‘lishi kvadratik ishni ikki baravar qilmaydi. || Удвоение входа не удваивает квадратичную работу.'),
            s('A uchun T(n) = 3n + 2, B uchun T(n) = n²; bir amal narxi teng. n = 10 da qaysi kamroq ish qiladi? || Для A: T(n) = 3n + 2, для B: T(n) = n²; цена действия одинакова. Кто делает меньше работы при n = 10?', [
                ('A: 32 amal || A: 32 действия', '32 kvadratik variantning 100 amalidan kam. || 32 меньше 100 действий квадратичного варианта.'),
                ('B: 100 amal || B: 100 действий', 'Bu ko‘proq, kamroq emas. || Это больше, а не меньше.'),
                ('Ikkalasi teng || Оба равны', '32 va 100 teng emas. || 32 и 100 не равны.')],
              'A = 3 × 10 + 2 = 32.|B = 10² = 100; shu modelda A tanlanadi. || A = 3 × 10 + 2 = 32.|B = 10² = 100; в этой модели выбирается A.',
              'O‘sish nomidan oldin berilgan kirishdagi hisobni tekshiring. || До вывода по названию роста проверьте расчёт на заданном входе.')], ['opt-equivalence', 'loop-nested']),
        l('opt-memory', 'Qo‘shimcha xotirani baholash || Оценка дополнительной памяти', [
            'Bu kursda qo‘shimcha xotira kirish ro‘yxatidan tashqari ajratilgan joydir. Bir necha jamlagich o‘zgarmas hajm, n ta nusxa esa n ga bog‘liq hajm oladi. || В курсе дополнительная память — место сверх входного списка. Несколько накопителей занимают постоянный объём, копия из n элементов — объём, зависящий от n.',
            'Bir o‘tishda yig‘indi topish barcha oraliq yig‘indilarni ro‘yxatga saqlashni talab qilmaydi. Agar keyin barcha oraliq natijalar so‘ralsa, vazifa o‘zgaradi. || Для суммы за один проход не требуется сохранять все промежуточные суммы в списке. Если затем нужны все промежуточные результаты, задача меняется.',
            'Rekursiyada chaqiruv steki ham xotira hisoblanadi. Nusxadan voz kechish kirishni buzsa, ruxsat etilganlikni tekshiring: xotira yutug‘i ma’lumotni yashirin o‘zgartirishga ruxsat bermaydi. || Стек рекурсивных вызовов тоже считается памятью. Если отказ от копии меняет вход, проверьте допустимость: экономия памяти не разрешает скрыто изменять данные.'
        ], 'Kirishda 100 son. A faqat sum saqlaydi, B 100 elementli nusxa ham saqlaydi. Qaysi kamroq qo‘shimcha xotira ishlatadi? || На входе 100 чисел. A хранит только sum, B также хранит копию из 100 элементов. Кто использует меньше дополнительной памяти?',
           'Kirish joyi hisobdan chiqariladi.|A bitta jamlagich ishlatadi.|B nusxa sabab ko‘proq qo‘shimcha joy oladi. || Входное место исключается из расчёта.|A использует один накопитель.|B занимает больше дополнительного места из-за копии.', 'A || A', [
            s('Faqat yig‘indi kerak. Qaysi saqlash tuzilishi yetarli? || Нужна только сумма. Какого хранения достаточно?', [
                ('Bitta jamlagich va joriy element || Один накопитель и текущий элемент', 'Barcha oldingi elementlarni qayta saqlash shart emas. || Повторно хранить все прежние элементы не требуется.'),
                ('Har bir oraliq yig‘indining to‘liq nusxalari || Полные копии каждой промежуточной суммы', 'Bular yakuniy yig‘indi uchun talab qilinmagan. || Они не требуются для конечной суммы.'),
                ('Faqat oxirgi element || Только последний элемент', 'Oldingi hissalar yo‘qoladi. || Вклад предыдущих элементов теряется.')],
              'sum har bir elementni qo‘shib yangilanadi.|Bitta jamlagich barcha oldingi hissani saqlaydi. || sum обновляется прибавлением каждого элемента.|Один накопитель хранит весь прежний вклад.',
              'Kam xotira natija uchun zarur ma’lumotni yo‘qotmasin. || Экономия памяти не должна терять необходимые для результата данные.',
              'Qaysi bitta qiymat oldingi hisobni jamlaydi? || Какое одно значение объединяет прежнее вычисление?'),
            n('A qo‘shimcha 3 ta son saqlaydi. B qo‘shimcha 20 elementli ro‘yxat va 2 ta son saqlaydi. Har bir katak hajmi bir xil. B nechta qo‘shimcha katak oladi? || A дополнительно хранит 3 числа. B — список из 20 элементов и 2 числа. Размер каждой ячейки одинаков. Сколько дополнительных ячеек занимает B?', 22,
              'Ro‘yxat va alohida sonlar birga sanaladi.|20 + 2 = 22. || Считаются список и отдельные числа.|20 + 2 = 22.',
              'Yordamchi o‘zgaruvchilarni hisobdan tushirmang. || Не исключайте вспомогательные переменные из подсчёта.',
              'B uchun ajratilgan barcha kataklarni qo‘shing. || Сложите все ячейки, выделенные для B.'),
            s('A kirishni o‘zgartirmasdan ishlaydi. B kirishni saralab yuboradi. Vazifa asl tartibni saqlashni talab qiladi. Qaysi xulosa to‘g‘ri? || A не меняет вход. B сортирует его на месте. Задача требует сохранить исходный порядок. Какой вывод верен?', [
                ('B ni qo‘shimcha chorasisiz mos yechim deb bo‘lmaydi || B нельзя считать подходящим без дополнительных мер', 'Saqlash talabi buzilyapti. || Нарушается требование сохранения.'),
                ('Kamroq xotira har qanday o‘zgarishga ruxsat beradi || Меньшая память разрешает любое изменение', 'Resurs yutug‘i shartnomani bekor qilmaydi. || Экономия ресурса не отменяет контракт.'),
                ('Tartib talabi faqat rangga tegishli || Требование порядка относится только к цвету', 'Bu ma’lumot tartibi haqida. || Речь о порядке данных.')],
              'Asl tartib — majburiy chiqishdan tashqari shart.|B shu shartni buzsa rad etiladi yoki nusxa bilan moslashtiriladi. || Исходный порядок — обязательное дополнительное условие.|Если B его нарушает, он отклоняется или адаптируется с копией.',
              'Optimizatsiya to‘g‘rilik talablarini bekor qilmaydi. || Оптимизация не отменяет требования правильности.'),
            n('Algoritm n elementli yangi nusxa va 4 yordamchi katak ishlatadi. n = 12 da kirishni hisoblamasdan qo‘shimcha kataklar soni? || Алгоритм использует новую копию из n элементов и 4 вспомогательные ячейки. При n = 12 сколько дополнительных ячеек без учёта входа?', 16,
              'Nusxa uchun 12 katak.|12 + 4 = 16 qo‘shimcha katak. || Для копии нужно 12 ячеек.|12 + 4 = 16 дополнительных ячеек.',
              'Kirish ro‘yxatini yana qo‘shib, ikki marta sanamang. || Не добавляйте входной список ещё раз, считая его дважды.')], ['opt-time']),
        l('opt-reuse', 'Takroriy hisobni kamaytirish || Уменьшение повторных вычислений', [
            'Bir xil o‘zgarmaydigan hisobni qayta-qayta bajarish o‘rniga natijasini bir marta saqlash mumkin. Bu faqat hisobning kirishlari o‘zgarmaganda mos. || Вместо повторения одного неизменного вычисления можно один раз сохранить результат. Это подходит только при неизменных входах вычисления.',
            'Masalan, o‘zgarmaydigan ro‘yxat yig‘indisini har so‘rovda qayta yurish o‘rniga saqlang. Ro‘yxat yangilansa saqlangan natija ham qayta hisoblanishi yoki mos yangilanishi kerak. || Например, вместо обхода неизменного списка при каждом запросе сохраните сумму. При изменении списка сохранённый результат тоже нужно пересчитать или обновить.',
            'Bir o‘tishda yig‘indi va maksimumni birga hisoblash ikki to‘liq o‘tishni kamaytirishi mumkin. Lekin maksimum uchun ro‘yxat bo‘sh holatini alohida qayta ishlang. || Вычисление суммы и максимума за один проход может сократить два полных обхода. Но для максимума отдельно обработайте пустой список.'
        ], 'O‘zgarmaydigan 10 elementli ro‘yxat yig‘indisi 3 marta kerak. Har safar 10 ta qo‘shish o‘rniga bir marta hisoblasak nechta qo‘shish tejaymiz? || Сумма неизменного списка из 10 элементов нужна 3 раза. Сколько сложений сэкономим, вычислив её один раз вместо 10 сложений каждый раз?',
           'Takroriy variant 3 × 10 = 30.|Saqlangan variant 10 qo‘shish.|30 − 10 = 20 qo‘shish tejaladi. || Повторный вариант: 3 × 10 = 30.|Вариант с сохранением: 10 сложений.|Экономия: 30 − 10 = 20 сложений.', '20 || 20', [
            n('O‘zgarmas hisob 6 amal oladi va 5 marta so‘raladi. Bir marta hisoblab saqlasak, saqlash/o‘qish xarajatini hisoblamay nechta amal tejaladi? || Неизменное вычисление занимает 6 операций и нужно 5 раз. Сколько операций сэкономим, вычислив его один раз, без учёта хранения и чтения?', 24,
              'Qayta hisoblash 6 × 5 = 30.|Bir marta 6, tejash 30 − 6 = 24. || Повторное вычисление: 6 × 5 = 30.|Один раз — 6, экономия: 30 − 6 = 24.',
              'Tejash umumiy eski ish emas, eski va yangi ish farqi. || Экономия — не вся прежняя работа, а разность прежней и новой.',
              'Eski va yangi hisob sonlarini alohida toping. || Отдельно найдите прежнее и новое количества вычислений.'),
            s('Ro‘yxat yig‘indisi saqlangan, keyin ro‘yxatga yangi element qo‘shildi. Nima qilish kerak? || Сумма списка сохранена, затем добавлен новый элемент. Что нужно сделать?', [
                ('Saqlangan yig‘indini yangilash yoki qayta hisoblash || Обновить или пересчитать сохранённую сумму', 'Kirish o‘zgardi, eski natija endi to‘liq emas. || Вход изменился, прежний результат больше не полон.'),
                ('Eski natijani doim qaytarish || Всегда возвращать старый результат', 'Yangi element hissasi tushib qoladi. || Вклад нового элемента пропадёт.'),
                ('Yangi elementni yashirish || Скрыть новый элемент', 'Bu vazifa ma’lumotini o‘zgartiradi. || Это меняет данные задачи.')],
              'Saqlangan natija oldingi kirishga tegishli.|Yangi kirish uchun uni yangilash zarur. || Сохранённый результат относится к прежнему входу.|Для нового входа его нужно обновить.',
              'Saqlangan natijani kirish bilan birga kuzating. || Отслеживайте сохранённый результат вместе с входом.',
              'Oldingi natija qaysi ma’lumot uchun hisoblangan edi? || Для каких данных был вычислен прежний результат?'),
            n('Bir o‘tish n elementni ko‘radi. Alohida yig‘indi va maksimum uchun ikki o‘tish o‘rniga birlashtirilgan bir o‘tish qilinadi. n = 15 da element ko‘rishlaridan nechta tejaladi? || Один проход просматривает n элементов. Вместо отдельных проходов для суммы и максимума делается один общий. При n = 15 сколько просмотров элементов экономится?', 15,
              'Oldin 2 × 15 = 30 ko‘rish.|Keyin 15, farq 15. || Раньше 2 × 15 = 30 просмотров.|Теперь 15, разность — 15.',
              'Bu faqat element ko‘rishlar soni; barcha boshqa amallar yo‘qolmaydi. || Это только число просмотров элементов; остальные действия не исчезают.'),
            s('F(x) ni sikldan tashqarida bir marta hisoblash qachon xavfsiz? F tashqi ta’sirsiz. || Когда безопасно один раз вычислить F(x) вне цикла? F не имеет внешних эффектов.', [
                ('x barcha aylanishlarda o‘zgarmasa || Если x не меняется во всех итерациях', 'Bir xil kirish bir xil natijani saqlaydi. || Одинаковый вход сохраняет одинаковый результат.'),
                ('x har aylanishda yangilansa || Если x обновляется на каждой итерации', 'Natija ham o‘zgarishi mumkin. || Результат тоже может измениться.'),
                ('F nomi qisqa bo‘lsa || Если имя F короткое', 'Nom hisob semantikasini belgilamaydi. || Имя не определяет семантику вычисления.')],
              'Sikldan chiqarilgan hisob barcha aylanishlar o‘rnini bosadi.|Shuning uchun uning kirishi o‘zgarmas bo‘lishi kerak. || Вынесенное вычисление заменяет все итерации.|Поэтому его вход должен быть неизменным.',
              'Faqat tashqi ko‘rinishga qarab hisobni ko‘chirmang. || Не переносите вычисление только по внешнему виду.')], ['opt-memory']),
        l('opt-choice', 'Cheklovlarga mos yechim tanlash || Выбор решения по ограничениям', [
            'Tanlashda avval to‘g‘rilik va majburiy cheklovlar, keyin vaqt va xotira, so‘ng tushunarlilik tekshiriladi. Mezonsiz “eng yaxshi” degan xulosa noaniq. || При выборе сначала проверяют правильность и обязательные ограничения, затем время и память, после — понятность. Вывод «лучший» без критериев неопределён.',
            'A tezroq, lekin ko‘proq xotira olishi mumkin. Qaysi cheklov muhimligi ma’lum bo‘lmasa, murosani tushuntiring; bitta universal g‘olib uydirmang. || A может быть быстрее, но занимать больше памяти. Если неизвестно, какое ограничение важнее, объясните компромисс; не придумывайте универсального победителя.',
            'Tanlangan algoritmni bir xil kirishlar va hisob modeli bilan tekshiring. Katta tezlik da’vosi kichik bir misol yoki faqat kod satrlari sonidan kelib chiqmaydi. || Проверяйте выбранный алгоритм на одинаковых входах и в одной модели расчёта. Большое преимущество скорости не следует из одного малого примера или числа строк кода.'
        ], 'Xotira chegarasi 8 katak. A: 5 katak, 30 amal; B: 12 katak, 10 amal. Qaysi mos? || Предел памяти — 8 ячеек. A: 5 ячеек, 30 операций; B: 12 ячеек, 10 операций. Кто подходит?',
           'A xotira talabiga mos.|B tezroq, lekin chegaradan oshadi.|Ushbu talabda A tanlanadi. || A удовлетворяет памяти.|B быстрее, но превышает предел.|При этом требовании выбирается A.', 'A || A', [
            s('Limit: 10 xotira katagi va 50 amal. A: 8 katak/40 amal; B: 12 katak/20 amal; C: 6 katak/60 amal. Qaysi ikkala limitga mos? || Лимиты: 10 ячеек памяти и 50 операций. A: 8 ячеек/40 операций; B: 12 ячеек/20 операций; C: 6 ячеек/60 операций. Кто удовлетворяет обоим?', [
                ('A || A', 'Ikkala miqdor ham limitdan oshmaydi. || Оба значения не превышают лимиты.'),
                ('B || B', 'Xotira limiti buziladi. || Нарушается лимит памяти.'),
                ('C || C', 'Amallar limiti buziladi. || Нарушается лимит операций.')],
              'Har nomzodda ikkala talabni tekshiring.|Faqat A ikkalasini bajaradi. || Проверьте оба требования у каждого кандидата.|Только A выполняет оба.',
              'Bitta yaxshi ko‘rsatkich boshqa limit buzilishini oqlamaydi. || Один хороший показатель не оправдывает нарушение другого лимита.',
              'Talablar OR emas, AND bilan bog‘langan. || Требования связаны через AND, а не OR.'),
            s('Barcha variant to‘g‘ri. A kam vaqt/ko‘p xotira, B ko‘p vaqt/kam xotira ishlatadi. Limitlar berilmagan. Xulosa? || Все варианты правильны. A требует мало времени/много памяти, B — много времени/мало памяти. Лимиты не заданы. Каков вывод?', [
                ('Ustuvor mezon aniqlanmaguncha yagona g‘olib yo‘q || Без приоритетного критерия единственного победителя нет', 'Bu vaqt-xotira murosasi. || Это компромисс времени и памяти.'),
                ('A har qanday vazifada eng yaxshi || A лучший в любой задаче', 'Xotira chegarasi bunga qarshi bo‘lishi mumkin. || Ограничение памяти может этому противоречить.'),
                ('B har qanday vazifada eng yaxshi || B лучший в любой задаче', 'Vaqt chegarasi bunga qarshi bo‘lishi mumkin. || Ограничение времени может этому противоречить.')],
              'Variantlar turli resursda ustun.|Mezonni aniqlab, keyin tanlang. || Варианты выигрывают по разным ресурсам.|Уточните критерий, затем выбирайте.',
              'Universal eng yaxshi degan da’vodan saqlaning. || Избегайте утверждения об универсально лучшем варианте.',
              'Qaysi resurs cheklanganini bilish kerak. || Нужно знать, какой ресурс ограничен.'),
            s('A qisqaroq kod, B uzunroq kod. Boshqa ma’lumot yo‘q. Qaysi tezroq? || Код A короче, код B длиннее. Других данных нет. Кто быстрее?', [
                ('Faqat satrlar sonidan aniqlab bo‘lmaydi || По одному числу строк определить нельзя', 'Bir satr ichida ham katta ish bo‘lishi mumkin. || Даже одна строка может выполнять большую работу.'),
                ('A albatta tezroq || A обязательно быстрее', 'Qisqalik bajariladigan ishni ko‘rsatmaydi. || Краткость не показывает объём выполняемой работы.'),
                ('B albatta tezroq || B обязательно быстрее', 'Uzunlik ham tezlik dalili emas. || Длина тоже не является доказательством скорости.')],
              'Ish hajmi va kirishlar tahlil qilinadi.|Satr soni o‘zi yetarli mezon emas. || Анализируются объём работы и входы.|Само число строк недостаточно.',
              'Kod ko‘rinishi va bajarilish xarajatini farqlang. || Различайте внешний вид кода и стоимость выполнения.'),
            s('Faqat bitta so‘rov bo‘ladi. A: tayyorlash 100 amal + so‘rov 1 amal. B: tayyorlashsiz so‘rov 20 amal. Bir xil amal narxida qaysi kamroq jami ish qiladi? || Будет только один запрос. A: подготовка 100 операций + запрос 1 операция. B: без подготовки, запрос 20 операций. При одинаковой цене операции кто делает меньше общей работы?', [
                ('B: jami 20 || B: всего 20', 'A tayyorlash bilan 101 amal oladi. || A вместе с подготовкой требует 101 операцию.'),
                ('A: faqat 1 amal || A: только 1 операция', 'Bu tayyorlash xarajatini tashlab ketadi. || Это пропускает стоимость подготовки.'),
                ('Ikkalasi: 100 amal || Оба: 100 операций', 'Berilgan xarajatlar bunday emas. || Заданные затраты не дают такого результата.')],
              'A jami 100 + 1 = 101.|B jami 20, bir so‘rovda B afzal. || A всего: 100 + 1 = 101.|B всего: 20, при одном запросе B предпочтительнее.',
              'Oldindan tayyorlashni umumiy xarajatga kiriting. || Включайте предварительную подготовку в общую стоимость.')], ['opt-reuse'])])
