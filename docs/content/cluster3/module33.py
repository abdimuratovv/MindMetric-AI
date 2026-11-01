from authoring import choice as c, lesson as l, module, numeric as n, q


def build():
    return module('attention-code-review', 3, 'Diqqat va aniqlik uchun code review || Внимательность и точность при ревью кода', [
        l('review-requirement', 'Talab va diffni solishtirish || Сопоставление требования и diff',
          'O‘zgarishning talabni bajarayotganini va uning ta’sir doirasini tekshirasiz. || Проверяете соответствие изменения требованию и область его влияния.', [
            'Review avval talabdan boshlanadi: nima o‘zgarishi va nima saqlanishi kerak? Diffdagi + qo‘shilgan, - olib tashlangan satrni bildiradi; bu belgilar kodning arifmetik operatori emas. Atrofdagi kodni ham o‘qing. || Ревью начинается с требования: что должно измениться и что сохраниться? В diff знак + обозначает добавленную строку, - удалённую; это не арифметические операторы кода. Читайте и окружающий код.',
            'Avval funksional talab, keyin aniqlik va o‘qiluvchanlikni tekshiring. Chiroyli format noto‘g‘ri hisobni oqlamaydi. Kichik diff ham autentifikatsiya yoki chegara xatti-harakatini o‘zgartirishi mumkin. || Сначала проверьте функциональное требование, затем точность и читаемость. Красивый формат не оправдывает неверное вычисление. Даже небольшой diff может изменить проверку доступа или граничное поведение.',
            'Review savol yoki dalilli taklif beradi. Agar kod allaqachon to‘g‘ri bo‘lsa, sun’iy xato qidirmang: tekshirilgan talab va dalilni yozib tasdiqlash ham to‘g‘ri natija. || Ревью даёт вопрос или предложение с основанием. Если код уже правильный, не выдумывайте дефект: одобрение с указанием проверенного требования и подтверждения тоже правильно.'
          ], '''Talab: 10 va undan katta qiymat qabul qilinsin. Diff:
```diff
-ok = x > 10
+ok = x >= 10
```
O‘zgarishni qanday tekshirasiz? || Требование: принимать 10 и больше. Diff:
```diff
-ok = x > 10
+ok = x >= 10
```
Как проверить изменение?''',
          'Talab tenglikni ham oladi.|9, 10 va 11 ni solishtiring.|Yangi shart ayni chegarani to‘g‘rilaydi. || Требование включает равенство.|Сравните 9, 10 и 11.|Новое условие исправляет именно границу.',
          '9 rad, 10 va 11 qabul; diff talabga mos. || 9 отклоняется, 10 и 11 принимаются; diff соответствует требованию.', [
            q('Reviewda birinchi qaysi savol foydali? || Какой вопрос полезен первым при ревью?', [
                c('Qaysi talab o‘zgaradi va kutilgan natija qanday? || Какое требование меняется и каков ожидаемый результат?', 'To‘g‘rilik uchun mezon beradi. || Даёт критерий правильности.'),
                c('Faqat o‘zgargan satrlar kammi? || Только мало ли изменённых строк?', 'Kichik diff ham talabni buzishi mumkin. || Даже маленький diff может нарушать требование.'),
                c('Kod formatlash qoidasiga mosmi, talabni keyin ko‘ramizmi? || Соответствует ли код форматированию, а требование посмотрим потом?', 'Format foydali, ammo avval xatti-harakat mezoni kerak. || Формат полезен, но сначала нужен критерий поведения.')],
              'Avval maqsadni aniqlang.|Diffni shu maqsadga nisbatan baholang. || Сначала определите цель.|Оцените diff относительно неё.',
              'Talabsiz review shaxsiy didga aylanadi. || Без требования ревью превращается в вопрос вкуса.', 'To‘g‘ri yoki noto‘g‘riligini nimaga qarab aytasiz? || По чему определить правильность?'),
            q('Diffda -print(old) va +print(new) bor. - va + nimani bildiradi? || В diff есть -print(old) и +print(new). Что означают - и +?', [
                c('Olib tashlangan va qo‘shilgan satrlar || Удалённую и добавленную строки', 'Diff o‘zgarishlarni shunday belgilaydi. || Так diff отмечает изменения.'),
                c('Sonlarni ayirish va qo‘shish || Вычитание и сложение чисел', 'Bu yerda belgilar diff metama’lumoti. || Здесь это обозначения diff.'),
                c('Har ikkisi bajariladigan yakuniy satrlar || Обе строки выполняются в итоговом коде', 'Olib tashlangan satr yangi holatda yo‘q. || Удалённой строки в новом состоянии нет.')],
              'Diffni kodning o‘zi bilan adashtirmang.|Yangi holatda faqat qo‘shilgan variant qoladi. || Не путайте diff с самим кодом.|В новом состоянии остаётся добавленный вариант.',
              'Diff belgilarini dasturga ko‘chirmang. || Не копируйте обозначения diff в программу.', 'Yangi faylda qaysi satr qoladi? || Какая строка останется в новом файле?'),
            q('Talab: faqat chegirmani tuzatish. Diff shu bilan birga kirish nazoratini olib tashlagan. Xulosa? || Требование: исправить только скидку. Diff также убрал контроль доступа. Вывод?', [
                c('Qo‘shimcha ta’sirni aniqlashtirish va kirish nazoratini tekshirish kerak || Нужно уточнить дополнительное влияние и проверить контроль доступа', 'Talabdan tashqari xatti-harakat o‘zgargan. || Изменилось поведение вне требования.'),
                c('Satrlar kamaysa har doim yaxshi || Меньше строк — всегда лучше', 'Qisqarish zarur talabni yo‘qotishi mumkin. || Сокращение может удалить нужное требование.'),
                c('Chegirma to‘g‘ri bo‘lsa boshqasini ko‘rmaymiz || Если скидка верна, остальное не смотрим', 'Review o‘zgarishning ta’sirini ham ko‘radi. || Ревью учитывает и влияние изменения.')],
              'Diffning barcha ta’sirini ko‘ring.|Aloqasiz o‘zgarishga dalil yoki ajratish so‘rang. || Проверьте все последствия diff.|Попросите обоснование или отделение несвязанной правки.',
              'Kichik vazifa keng ta’sirni yashirishi mumkin. || Маленькая задача может скрывать широкое влияние.'),
            q('Talab, oddiy va chegara testlari o‘tdi, reviewda xato topilmadi. To‘g‘ri yakun? || Требование, обычные и граничные тесты проверены, дефектов не найдено. Правильное завершение?', [
                c('Tekshirilgan qamrovni yozib tasdiqlash || Одобрить с указанием проверенной области', 'Review doim xato topishga majbur emas. || Ревью не обязано всегда находить дефект.'),
                c('Albatta biror xato o‘ylab topish || Обязательно придумать дефект', 'Asossiz fikr sifatni oshirmaydi. || Необоснованное замечание не повышает качество.'),
                c('Testlarni ko‘rmagandek baholash || Оценить, игнорируя тесты', 'Mavjud dalil e’tiborsiz qoladi. || Имеющееся подтверждение игнорируется.')],
              'Dalillarni qayd eting.|Qamrov chegarasini bildirib tasdiqlang. || Зафиксируйте подтверждения.|Одобрите, указав границы проверки.',
              'Reviewni kamchilik soni bilan baholamang. || Не оценивайте ревью по числу замечаний.')]),
        l('review-tokens', 'Nomlar, operatorlar va bloklar || Имена, операторы и блоки',
          'Bir belgi yoki chekinishdagi o‘zgarishning ma’nosini tekshirasiz. || Проверяете смысл изменения символа или отступа.', [
            'Bir-biriga o‘xshash nomlar boshqa o‘zgaruvchi bo‘lishi mumkin: total va tota1, count va counts. Nom aniqlanganmi, ayni vazifani bildiradimi? Ko‘rish bilan cheklanmay ta’rif va ishlatishni izlang. || Похожие имена могут быть разными переменными: total и tota1, count и counts. Определено ли имя и означает ли нужное? Не ограничивайтесь взглядом, найдите определение и использования.',
            'Python da = qiymat beradi, == taqqoslaydi. >= bilan > tenglik holatida farq qiladi. and/or shartni o‘zgartiradi. Python bloklari chekinish bilan ajraladi; semicolon satr oxirida majburiy emas. || В Python = присваивает, == сравнивает. >= и > различаются на равенстве. and/or меняют условие. Блоки Python определяются отступами; точка с запятой в конце строки не обязательна.',
            'Muammo turini aniq nomlang: aniqlanmagan nom bajarilish xatosi bo‘lishi mumkin, noto‘g‘ri aniqlangan nom esa jim noto‘g‘ri natija beradi. Rasmiy sintaksisni boshqa tildan taxmin qilib qo‘llamang. || Называйте вид проблемы точно: неопределённое имя может вызвать ошибку выполнения, а неверно выбранное определённое имя — тихо дать неверный результат. Не переносите синтаксис из другого языка по догадке.'
          ], '''Python 3:
```python
total = 12
tota1 = 2
print(tota1)
```
Talab total ni chiqarish. Muammo? || Python 3:
```python
total = 12
tota1 = 2
print(tota1)
```
Требуется вывести total. В чём проблема?''',
          'Ikkala nom aniqlangan.|Print oxiri 1 raqamli nomni olgan.|Natija 2, keraklisi 12. || Оба имени определены.|Print использует имя с цифрой 1 на конце.|Результат 2, нужно 12.',
          'Mantiqiy nom xatosi; print(total) kerak. || Логическая ошибка выбора имени; нужен print(total).', [
            q('Python 3 da print(5) oxirida ; yo‘q. Review xulosasi? || В Python 3 после print(5) нет ;. Вывод ревью?', [
                c('Bu o‘zi xato emas; ; majburiy emas || Само по себе это не ошибка; ; не обязательна', 'Python satr tugashini qabul qiladi. || Python допускает завершение строки без неё.'),
                c('Har doim SyntaxError || Всегда SyntaxError', 'Boshqa til qoidasi ko‘chirilgan. || Перенесено правило другого языка.'),
                c('Natija 0 bo‘ladi || Результат будет 0', 'Bu chiqish qiymatini o‘zgartirmaydi. || Это не меняет выводимое значение.')],
              'Tilni aniqlang.|Python uchun ; talab qilmang. || Определите язык.|Не требуйте ; для Python.',
              'Tilga xos qoida bilan ishlang. || Применяйте правило конкретного языка.', 'Bu misol qaysi tilda? || На каком языке пример?'),
            q('Talab: login ham, kod ham to‘g‘ri bo‘lsin. Kod login_ok or code_ok. Muammo? || Требование: верны и логин, и код. Код login_ok or code_ok. Проблема?', [
                c('or o‘rniga and kerak || Нужен and вместо or', 'Ikkala shart majburiy. || Обязательны оба условия.'),
                c('or doim ikkala shartni talab qiladi || or всегда требует оба условия', 'or kamida bittasini qabul qiladi. || or принимает хотя бы одно.'),
                c('Faqat nom uzunligini o‘zgartirish kerak || Нужно только изменить длину имён', 'Operator semantikasi qoladi. || Смысл оператора сохранится.')],
              'Bir shart yolg‘on holatni sinang.|or uni o‘tkazadi, and rad qiladi. || Проверьте случай с одним ложным условием.|or пропускает, and отклоняет.',
              'Mantiqiy operatorni ko‘rinishi bilan tanlamang. || Не выбирайте логический оператор по виду.', 'Bittasi noto‘g‘ri bo‘lsa ruxsat bo‘ladimi? || Допустим ли доступ, если одно условие неверно?'),
            q('Python 3: total=8, count=2; print(totla). totla aniqlanmagan. Muammo? || Python 3: total=8, count=2; print(totla). totla не определено. Проблема?', [
                c('Nomdagi xato NameError beradi || Опечатка в имени вызывает NameError', 'Ishlatilgan nom ta’rifi yo‘q. || У использованного имени нет определения.'),
                c('count avtomatik chiqariladi || Автоматически выводится count', 'Python eng yaqin nomni o‘zi tanlamaydi. || Python сам не выбирает ближайшее имя.'),
                c('Natija har doim 8 || Всегда получается 8', 'total boshqa nom. || total — другое имя.')],
              'Ta’rif va ishlatilgan nomni belgima-belgi solishtiring.|totla topilmaydi. || Посимвольно сравните определение и использование.|totla не найдено.',
              'O‘xshash yozuv bir xil identifikator emas. || Похожее написание не означает одинаковый идентификатор.'),
            n('''Python 3:
```python
s = 0
for x in [1, 2, 3]:
    s = s + x
    print(s)
```
print necha marta bajariladi? || Python 3:
```python
s = 0
for x in [1, 2, 3]:
    s = s + x
    print(s)
```
Сколько раз выполнится print?''', 3,
              'Print sikl ichida chekingan.|Har element uchun bir marta, jami 3. || Print находится внутри цикла по отступу.|По одному разу на элемент, всего 3.',
              'Chekinishni bezak deb olmang. || Не считайте отступ украшением.')]),
        l('review-boundaries', 'Chegaraviy holat va invariant || Граничный случай и инвариант',
          'Oddiy misoldan tashqari buzuvchi kirishni va saqlanishi kerak bo‘lgan xususiyatni topasiz. || Находите нарушающий вход и свойство, которое должно сохраняться.', [
            'Invariant — jarayon davomida saqlanishi kerak bo‘lgan xususiyat. Kutubxonada mavjud nusxalar soni manfiy bo‘lmasligi shunday mezon. Har qadamdan keyin uni tekshiring. || Инвариант — свойство, сохраняемое в процессе. Число доступных экземпляров библиотеки не должно быть отрицательным — это такой критерий. Проверяйте его после каждого шага.',
            'Chegaraviy kirishlar: bo‘sh ro‘yxat, bitta element, oxirgi indeks, limitga teng qiymat. Qarshi misol koddagi da’voni buzadi: “hamma sonlarda maksimum” funksiyasi faqat musbatlarda ishlasa, manfiy ro‘yxat uni fosh qiladi. || Граничные входы: пустой список, один элемент, последний индекс, значение на лимите. Контрпример опровергает утверждение кода: если «максимум любых чисел» работает только на положительных, отрицательный список выявит дефект.',
            'Test kutilgan natijasi koddan ko‘chirib olinmaydi. Avval talabni yozing, keyin natijani mustaqil hisoblang. Bitta testning o‘tishi umumiy isbot emas. || Ожидаемый результат теста не копируют из кода. Сначала запишите требование, затем независимо вычислите результат. Прохождение одного теста не является общим доказательством.'
          ], 'max_value boshida best=0, keyin kattaroq elementni oladi. Talab: bo‘sh bo‘lmagan butun sonlar ro‘yxatining maksimumi. [-5, -2] da nima bo‘ladi? || max_value начинает с best=0, затем берёт больший элемент. Требование: максимум непустого списка целых. Что будет для [-5, -2]?',
          'Hech bir element 0 dan katta emas.|Kod 0 ni qoldiradi.|Haqiqiy maksimum -2; best birinchi elementdan boshlanishi mumkin. || Ни один элемент не больше 0.|Код оставит 0.|Настоящий максимум -2; best можно начать с первого элемента.',
          '0 noto‘g‘ri; manfiylar qarshi misol bo‘ldi. || 0 неверно; отрицательные числа стали контрпримером.', [
            q('Nusxalar soni 0. borrow uni tekshirmasdan 1 ga kamaytiradi. Qaysi invariant buziladi? || Экземпляров 0. borrow уменьшает число на 1 без проверки. Какой инвариант нарушен?', [
                c('Mavjud nusxalar manfiy bo‘lmasligi || Число доступных экземпляров не должно быть отрицательным', '0 − 1 = -1. || 0 − 1 = -1.'),
                c('Har doim nusxalar 100 bo‘lishi || Экземпляров всегда должно быть 100', 'Bunday talab berilmagan. || Такое требование не задано.'),
                c('Har commitda rang o‘zgarishi || Цвет должен меняться с каждым коммитом', 'Bu ma’lumot invariantiga aloqasiz. || Это не относится к инварианту данных.')],
              'Berishdan keyingi sonni hisoblang.|-1 mavjudlik talabiga zid. || Вычислите число после выдачи.|-1 противоречит требованию доступности.',
              'Holatni yangilashdan oldin ruxsatni tekshiring. || Проверяйте допустимость до обновления состояния.', '0 dan yana bitta olish mumkinmi? || Можно ли взять ещё один при 0?'),
            q('Python xs[0] ni doim o‘qiydi. Qaysi kirish chegaraviy nosozlikni topadi? || Python всегда читает xs[0]. Какой вход выявит граничный сбой?', [
                c('[] || []', 'Birinchi element mavjud emas. || Первого элемента нет.'),
                c('[7] || [7]', 'Birinchi element bor. || Первый элемент есть.'),
                c('[7, 8] || [7, 8]', 'Bu ham birinchi elementga ega. || Здесь тоже есть первый элемент.')],
              'Indeks 0 mavjudligini tekshiring.|Bo‘sh ro‘yxatda u yo‘q. || Проверьте наличие индекса 0.|В пустом списке его нет.',
              'Har ro‘yxatni bo‘sh emas deb olmang. || Не считайте любой список непустым.', 'Eng kichik ro‘yxat uzunligi qanday? || Какова минимальная длина списка?'),
            q('Talab: qolgan balans manfiy bo‘lmasin. balans=50, yechish=50. Qaysi shart mos? || Требование: остаток неотрицателен. Баланс=50, снятие=50. Какое условие подходит?', [
                c('yechish <= balans || yechish <= balans', 'Tenglikda qolgan qiymat 0 bo‘ladi. || При равенстве остаток равен 0.'),
                c('yechish < balans || yechish < balans', 'Ruxsat etilgan tenglikni rad qiladi. || Отклоняет допустимое равенство.'),
                c('yechish > balans || yechish > balans', 'Manfiy balansga ruxsat beradi. || Допускает отрицательный баланс.')],
              'Tenglik holatida 50 − 50 = 0.|0 talabga mos. || При равенстве 50 − 50 = 0.|0 соответствует требованию.',
              'Nol va manfiy natijani ajrating. || Различайте ноль и отрицательный результат.'),
            q('Talab: musbat va manfiy sonlar maksimumi. best=0 boshlanishiga qaysi qarshi misol mos? || Требование: максимум положительных и отрицательных чисел. Какой контрпример выявит проблему best=0?', [
                c('[-8, -3] || [-8, -3]', 'Kod 0 qoldirishi mumkin, maksimum esa -3. || Код может оставить 0, хотя максимум -3.'),
                c('[2, 9] || [2, 9]', 'Musbat maksimum boshlang‘ich 0 dan katta. || Положительный максимум больше начального 0.'),
                c('[0, 4] || [0, 4]', 'Bu misolda 4 olinadi. || В этом примере получится 4.')],
              'Barcha element boshlang‘ich bestdan kichik bo‘lsin.|Manfiylar buni ko‘rsatadi. || Пусть все элементы меньше начального best.|Отрицательные числа это показывают.',
              'Faqat odatiy musbatlar bilan tekshirmang. || Не проверяйте только обычные положительные числа.')]),
        l('review-feedback', 'Aniq va hurmatli izoh || Точное и уважительное замечание',
          'Joy, talab, qarshi misol va taklif bilan foydali review izohini yozasiz. || Формулируете замечание с местом, требованием, контрпримером и предложением.', [
            'Yaxshi izoh koddagi joyni, talabga zid holatni va uning ta’sirini ko‘rsatadi. “Shu shartda x=0 noto‘g‘ri rad qilinadi, talab nolga ruxsat beradi” tekshiriladigan fikrdir. || Хорошее замечание указывает место в коде, случай нарушения требования и его последствие. «В этом условии x=0 ошибочно отклоняется, требование разрешает ноль» — проверяемая мысль.',
            'Majburiy tuzatishni shaxsiy diddan ajrating: nuqson, savol yoki ixtiyoriy uslub taklifi ekanini ayting. Izoh odamning qobiliyatiga emas, kod va dalilga qaratiladi. || Отличайте обязательное исправление от личного вкуса: укажите дефект, вопрос или необязательное стилевое предложение. Комментарий относится к коду и фактам, а не способностям человека.',
            'Muallif fikrni tushunmasa, kichik misol bering. O‘zingiz ham xato qilishingiz mumkin: talab aniqlashsa, izohni yangilang. Review maqsadi bahs yutish emas, tekshirilgan yaxshi o‘zgarishdir. || Если автор не понял, приведите небольшой пример. Вы тоже можете ошибиться: после уточнения требования обновите замечание. Цель ревью — проверенное хорошее изменение, а не победа в споре.'
          ], 'Kod x > 0, talab x >= 0. “Yomon kod!” o‘rniga izoh yozing. || Код x > 0, требование x >= 0. Напишите замечание вместо «Плохой код!».',
          'Muammoli shartni ko‘rsating.|x=0 qarshi misolini bering.|>= va chegara testini taklif qiling. || Укажите проблемное условие.|Приведите контрпример x=0.|Предложите >= и граничный тест.',
          '“x=0 rad bo‘lyapti; talab uni qabul qiladi. >= ni va 0 testini qo‘sha olamizmi?” || «x=0 отклоняется, хотя требование его принимает. Можем использовать >= и добавить тест 0?»', [
            q('Eng foydali review izohi qaysi? || Какое замечание полезнее?', [
                c('Shu shart 0 ni rad qiladi; talab qabul qiladi. Chegara testini qo‘shaylik || Это условие отклоняет 0, хотя требование принимает. Добавим граничный тест', 'Joy, talab va tekshiruv taklifi bor. || Есть место, требование и предложение проверки.'),
                c('Siz umuman bilmaysiz || Вы вообще не разбираетесь', 'Shaxsiy hukm kodni tuzatishga dalil bermaydi. || Личное суждение не помогает исправить код.'),
                c('Nimadir yoqmadi || Что-то не понравилось', 'Muammo aniqlanmagan. || Проблема не определена.')],
              'Fikrni aniq kirish bilan bog‘lang.|Tuzatish yoki savolni ko‘rsating. || Свяжите замечание с точным входом.|Укажите исправление или вопрос.',
              'Shaxsiy baho dalil emas. || Личная оценка не является доказательством.', 'Muallif izoh asosida test yozoladimi? || Сможет ли автор написать тест по замечанию?'),
            q('Nomlash variantlari ikkalasi ham qo‘llanmaga mos. Birini ko‘proq yoqtirasiz. Izoh turi? || Оба варианта имени соответствуют руководству. Один нравится вам больше. Тип замечания?', [
                c('Ixtiyoriy uslub taklifi || Необязательное стилевое предложение', 'Majburiy nuqson uchun asos yo‘q. || Нет основания считать это обязательным дефектом.'),
                c('Kritik bajarilish xatosi || Критическая ошибка выполнения', 'Nom yoqishi bajarilish xatosi emas. || Предпочтение имени не является ошибкой выполнения.'),
                c('Shaxs qobiliyati tashxisi || Диагноз способностей человека', 'Kod reviewsi buni o‘lchamaydi. || Ревью кода этого не измеряет.')],
              'Talab va qo‘llanma buzilmagan.|Taklifni ixtiyoriy deb belgilang. || Требование и руководство не нарушены.|Отметьте предложение как необязательное.',
              'Didni majburiy qoida deb bermang. || Не выдавайте вкус за обязательное правило.', 'Qaysi yozilgan qoida buzilgan? || Какое записанное правило нарушено?'),
            q('Talab noaniq, ammo xato bo‘lishi mumkin. Qanday yozish mos? || Требование неясно, но возможен дефект. Как написать?', [
                c('Talabni aniqlashtiruvchi savol va mumkin bo‘lgan qarshi misol || Вопрос для уточнения требования и возможный контрпример', 'Noaniqlik ochiq ko‘rsatiladi. || Неопределённость обозначена явно.'),
                c('Dalilsiz qat’iy ayblov || Категоричное обвинение без фактов', 'Noma’lum talabni isbotlangan xato deb beradi. || Неизвестное требование выдаётся за доказанный дефект.'),
                c('Har qanday savolni yashirish || Скрыть все вопросы', 'Muhim noaniqlik hal bo‘lmaydi. || Важная неопределённость не разрешится.')],
              'Nima ma’lum va nima noaniqligini ayting.|Aniq holat uchun kutilgan natijani so‘rang. || Укажите известное и неясное.|Уточните ожидаемый результат конкретного случая.',
              'Taxminni fakt sifatida yozmang. || Не записывайте предположение как факт.'),
            q('Muallif rasmiy talabni ko‘rsatdi va sizning qarshi misolingiz noto‘g‘ri ekani aniqlandi. Keyingi qadam? || Автор показал официальное требование, ваш контрпример оказался неверным. Следующий шаг?', [
                c('Izohni tuzatish va talab bo‘yicha tekshiruvni yangilash || Исправить замечание и обновить проверку по требованию', 'Review dalilga moslashadi. || Ревью следует фактам.'),
                c('Har qanday holatda oldingi fikrda qolish || При любых фактах стоять на прежнем мнении', 'Dalil e’tiborsiz qoladi. || Подтверждение игнорируется.'),
                c('Muallifdan kodni ataylab buzishni so‘rash || Попросить автора намеренно сломать код', 'Talabga zid o‘zgarish kiritadi. || Вносит изменение против требования.')],
              'Yangi dalilni qabul qiling.|Tekshiruvni haqiqiy talabga moslang. || Примите новое подтверждение.|Приведите проверку к настоящему требованию.',
              'Reviewda fikrni yangilash sifatning bir qismi. || Пересмотр мнения — часть качества ревью.')]),
        l('review-followup', 'Tuzatishni qayta tekshirish || Повторная проверка исправления',
          'Izoh yopilishidan oldin kod, test va umumiy ta’sirni tekshirasiz. || Проверяете код, тест и общее влияние до закрытия замечания.', [
            '“Tuzatildi” degan xabar tekshiruv dalili emas. Yangilangan diffni, ayni qarshi misolni va atrofdagi talablarni qayta ko‘ring. Yangi o‘zgarish eski review qamrovini oshirib yuborsa, uni ham tekshiring. || Сообщение «исправлено» не является подтверждением. Снова проверьте обновлённый diff, тот же контрпример и соседние требования. Если новая правка расширила область ревью, проверьте и её.',
            'Qisqa ro‘yxat yordam beradi: talab; nom/operator/blok; bo‘sh va chegara holat; xato holatida holat o‘zgarmasligi; test; ortiqcha o‘zgarish. Ro‘yxat fikrlashga yordamchi, satrlarni mexanik belgilash emas. || Помогает короткий список: требование; имя/оператор/блок; пустой и граничный случай; сохранение состояния при отказе; тест; лишние изменения. Список помогает думать, а не механически ставить галочки.',
            'Review yakunida qaysi holatlar tekshirilgani va qaysi cheklov qolgani aytiladi. Bir xil savolni cheksiz takrorlash o‘rniga tekshiruv dalili saqlanadi. || В конце ревью укажите проверенные случаи и оставшиеся ограничения. Вместо бесконечного повторения одного вопроса сохраняйте подтверждение проверки.'
          ], 'Izoh: 0 noto‘g‘ri rad qilingan. Tuzatishdan keyin 0 o‘tdi, lekin -1 ham o‘tdi. Reviewni yopasizmi? || Замечание: 0 ошибочно отклонён. После исправления 0 прошёл, но -1 тоже прошёл. Закрыть ревью?',
          'Talab manfiy qiymatni rad qiladi.|0 testi o‘tishi yetarli emas.|-1 uchun regressiyani tuzatishni so‘rang. || Требование отклоняет отрицательные значения.|Успех теста 0 недостаточен.|Попросите устранить регрессию для -1.',
          'Yo‘q, yangi regressiya bor. || Нет, есть новая регрессия.', [
            q('Muallif “tuzatdim” dedi. Izohni yopish uchun nima kerak? || Автор сказал «исправил». Что нужно для закрытия замечания?', [
                c('Yangilangan diff va muammoli testni qayta tekshirish || Перепроверить обновлённый diff и проблемный тест', 'Tuzatish dalil bilan tasdiqlanadi. || Исправление подтверждается проверкой.'),
                c('Faqat xabarga ishonish || Только поверить сообщению', 'Aniq tekshiruv yo‘q. || Конкретной проверки нет.'),
                c('Eski skrinshotga qarash || Посмотреть старый снимок', 'Yangi holatni ko‘rsatmaydi. || Не показывает новое состояние.')],
              'Yangi mazmunni ko‘ring.|Avval yiqilgan holatni qaytaring. || Посмотрите новое содержимое.|Повторите ранее падавший случай.',
              'Xabar bilan tekshirishni farqlang. || Различайте сообщение и проверку.', 'Qaysi dalil yangilandi? || Какое подтверждение обновилось?'),
            q('Review ro‘yxatidan foydalanishning to‘g‘ri maqsadi? || Правильная цель списка проверки ревью?', [
                c('Muhim holatlarni unutmaslik va har birini dalil bilan tekshirish || Не забыть важные случаи и проверить каждый с подтверждением', 'Ro‘yxat diqqatni qo‘llab-quvvatlaydi. || Список поддерживает внимание.'),
                c('Kodni o‘qimasdan barcha bandni belgilash || Отметить всё, не читая код', 'Tekshiruv bajarilmaydi. || Проверка не выполнена.'),
                c('Testlarni har doim almashtirish || Всегда заменять тесты', 'Ro‘yxat testning o‘rnini bosmaydi. || Список не заменяет тесты.')],
              'Har band aniq kuzatuvga bog‘lansin.|Mexanik belgi yetmaydi. || Свяжите каждый пункт с наблюдением.|Механической отметки недостаточно.',
              'Ro‘yxat sifat kafolati emas, yordamchi. || Список — помощник, а не гарантия качества.', 'Band uchun qanday dalil bor? || Какое подтверждение есть у пункта?'),
            q('Rad etilgan kitob so‘rovi available ni baribir kamaytiradi. Reviewda nima tekshiriladi? || Отклонённая заявка на книгу всё равно уменьшает available. Что проверять при ревью?', [
                c('Rad holatida oldingi va keyingi holat tengligini || Равенство состояния до и после отказа', 'Rad qilingan amal resursni sarflamasligi kerak. || Отклонённая операция не должна расходовать ресурс.'),
                c('Faqat rad javobi matnini || Только текст отказа', 'To‘g‘ri xabar bilan noto‘g‘ri holat birga kelishi mumkin. || Правильное сообщение может сопровождаться неверным состоянием.'),
                c('Faqat muvaffaqiyatli berish sonini || Только количество успешных выдач', 'Rad yo‘lidagi yon ta’sir tekshirilmaydi. || Побочный эффект отказа не проверяется.')],
              'Rad oldidagi available ni yozing.|Raddan keyin ayni qiymat qolishini talab qiling. || Запишите available до отказа.|Требуйте того же значения после отказа.',
              'Natija xabari bilan holatni birga tekshiring. || Проверяйте сообщение вместе с состоянием.'),
            q('Faqat kichik sun’iy kirishlar tekshirildi. Yakuniy reviewda qanday yoziladi? || Проверены только небольшие искусственные входы. Что написать в конце ревью?', [
                c('Tekshirilgan holatlarni va katta yuklama tekshirilmaganini aytish || Указать проверенные случаи и отсутствие проверки большой нагрузки', 'Dalilning amaliy chegarasi aniq. || Пределы подтверждения ясны.'),
                c('Barcha holatlarda mutlaq to‘g‘ri deyish || Объявить абсолютную правильность во всех случаях', 'Tekshiruv buni isbotlamagan. || Проверка этого не доказала.'),
                c('Tekshiruvni yashirish || Скрыть проверку', 'Natijani baholash qiyinlashadi. || Результат труднее оценить.')],
              'Nima tekshirilganini sanang.|Qolgan noaniqlikni qisqa yozing. || Перечислите проверенное.|Кратко запишите оставшуюся неопределённость.',
              'Cheklangan dalildan umumiy kafolat chiqarmang. || Не выводите общую гарантию из ограниченной проверки.')])
    ])
