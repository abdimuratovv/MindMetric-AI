from authoring import lesson as l, module, n, s


def build():
    return module('conditions-comparisons', 2,
        'Shart va taqqoslash operatorlari || Условия и операторы сравнения', ['algorithmic'], [
        l('cond-compare', 'Taqqoslash va chegaralar || Сравнения и границы', [
            '== tenglikni, != teng emaslikni, < va > qat’iy taqqoslashni bildiradi. ≤ va ≥ tenglikni ham qamraydi. Natija TRUE yoki FALSE bo‘ladi. || == означает равенство, != — неравенство, < и > — строгое сравнение. ≤ и ≥ включают равенство. Результат — TRUE или FALSE.',
            'x ← 5 buyruq, x == 5 esa savol. Shart o‘zgaruvchini yangilamasligi kerak. Belgining yo‘nalishini emas, butun gapning ma’nosini o‘qing. || x ← 5 — команда, а x == 5 — вопрос. Условие не должно обновлять переменную. Читайте смысл всего выражения, а не только направление знака.',
            '“Kamida”, “ko‘pi bilan” va “dan katta” turli shartlar. Chegaraning o‘zini tekshirish > bilan ≥ xatosini aniqlaydi. || «Не меньше», «не больше» и «больше» задают разные условия. Проверка самой границы выявляет путаницу между > и ≥.'
        ], '“Ball kamida 60” talabi ball = 60 da bajariladimi? || Выполняется ли требование «балл не меньше 60» при ball = 60?',
           'Talab ball ≥ 60.|60 ≥ 60 rost.|Natija TRUE. || Требование: ball ≥ 60.|60 ≥ 60 истинно.|Результат — TRUE.', 'TRUE || TRUE', [
            s('x = 8. Qaysi shart TRUE? || x = 8. Какое условие равно TRUE?', [
                ('x ≥ 8 || x ≥ 8', 'Tenglik ≥ ga kiradi. || Равенство входит в ≥.'),
                ('x > 8 || x > 8', '8 o‘zidan katta emas. || 8 не больше самого себя.'),
                ('x != 8 || x != 8', 'Qiymatlar teng. || Значения равны.')],
              'x o‘rniga 8 qo‘ying.|8 ≥ 8 rost, qolgan shartlar yolg‘on. || Подставьте 8 вместо x.|8 ≥ 8 истинно, остальные условия ложны.',
              'Qat’iy va tenglikli chegarani farqlang. || Различайте строгую границу и границу с равенством.',
              'Qiymat aynan chegaraga teng. || Значение в точности равно границе.'),
            s('“Yosh ko‘pi bilan 17” uchun to‘g‘ri shart? || Каково правильное условие для «возраст не больше 17»?', [
                ('age ≤ 17 || age ≤ 17', 'Kichik va teng qiymatlar qabul qilinadi. || Допускаются меньшие и равные значения.'),
                ('age < 17 || age < 17', 'Bu chegara yoshni chiqarib tashlaydi. || Это исключает граничный возраст.'),
                ('age ≥ 17 || age ≥ 17', 'Bu talabni teskari qiladi. || Это обращает требование.')],
              'Ko‘pi bilan — oshmasin degani.|Shuning uchun age ≤ 17. || Не больше означает не превышать.|Поэтому age ≤ 17.',
              '“Ko‘pi bilan”ni “kamida” bilan almashtirmang. || Не путайте «не больше» и «не меньше».',
              'Chegaraning o‘zi ham ruxsat etilgan. || Сама граница тоже разрешена.'),
            s('Harorat noldan qat’iy past bo‘lsa ogohlantirish kerak. Qaysi shart mos? || Предупреждение нужно, если температура строго ниже нуля. Какое условие подходит?', [
                ('t < 0 || t < 0', 'Nol kiritilmaydi, manfiylar kiritiladi. || Ноль исключён, отрицательные значения включены.'),
                ('t ≤ 0 || t ≤ 0', 'Nolni ham qamrab, talabni kengaytiradi. || Включает и ноль, расширяя требование.'),
                ('t > 0 || t > 0', 'Musbat qiymatlarni tanlaydi. || Выбирает положительные значения.')],
              '“Qat’iy past” tengliksiz taqqoslash.|Mos yozuv t < 0. || «Строго ниже» означает сравнение без равенства.|Подходит t < 0.',
              'Matndagi qat’iylikni saqlang. || Сохраняйте строгость условия из текста.'),
            s('x = 12. x != 12 ifodasining qiymati? || x = 12. Чему равно выражение x != 12?', [
                ('FALSE || FALSE', 'Bir xil qiymatlar teng emas degan gap yolg‘on. || Утверждение о неравенстве одинаковых значений ложно.'),
                ('TRUE || TRUE', '!= tenglikni emas, teng emaslikni so‘raydi. || != проверяет не равенство, а неравенство.'),
                ('x yangi qiymat oladi || x получает новое значение', 'Taqqoslash qiymat bermaydi. || Сравнение не выполняет присваивание.')],
              '12 != 12 ni tekshiring.|Qiymatlar teng, natija FALSE. || Проверьте 12 != 12.|Значения равны, результат FALSE.',
              'Taqqoslash bilan qiymat berishni farqlang. || Различайте сравнение и присваивание.')]),
        l('cond-boolean', 'Murakkab mantiqiy shartlar || Составные логические условия', [
            'AND ikkala shart rost bo‘lsa, OR kamida biri rost bo‘lsa TRUE bo‘ladi. OR ikkisi ham rost bo‘lishiga ham ruxsat beradi. NOT qiymatni teskarilaydi. || AND равно TRUE, когда истинны оба условия; OR — когда истинно хотя бы одно. OR допускает и одновременную истинность обоих. NOT обращает значение.',
            'Oraliqni ikkita taqqoslash bilan yozing: (x ≥ 1) AND (x ≤ 10). Tashqarida bo‘lish: (x < 1) OR (x > 10). Qavslar shart chegarasini aniq qiladi. || Интервал задаётся двумя сравнениями: (x ≥ 1) AND (x ≤ 10). Вне интервала: (x < 1) OR (x > 10). Скобки уточняют границы условий.',
            'NOT butun shartga taalluqli bo‘lishi mumkin. NOT (a AND b) ifodasi (NOT a) OR (NOT b) ga teng. Inkor qilganda taqqoslashning tenglik chegarasi ham o‘zgaradi. || NOT может относиться ко всему условию. NOT (a AND b) равно (NOT a) OR (NOT b). При отрицании сравнения меняется и включение равенства.'
        ], 'x = 4 uchun (x ≥ 2) AND (x < 5) ni tekshiring. || Проверьте (x ≥ 2) AND (x < 5) при x = 4.',
           '4 ≥ 2 — TRUE.|4 < 5 — TRUE.|TRUE AND TRUE = TRUE. || 4 ≥ 2 — TRUE.|4 < 5 — TRUE.|TRUE AND TRUE = TRUE.', 'TRUE || TRUE', [
            s('x = 0. (x > 0) OR (x == 0) natijasi? || x = 0. Каков результат (x > 0) OR (x == 0)?', [
                ('TRUE || TRUE', 'Ikkinchi qism rost, OR uchun yetarli. || Вторая часть истинна, для OR этого достаточно.'),
                ('FALSE || FALSE', 'OR ikkala qismni rost bo‘lishini talab qilmaydi. || OR не требует истинности обеих частей.'),
                ('Aniqlanmagan || Не определён', 'Ikkala taqqoslash ham aniq qiymatga ega. || Оба сравнения имеют определённое значение.')],
              'Birinchi qism FALSE, ikkinchisi TRUE.|FALSE OR TRUE = TRUE. || Первая часть FALSE, вторая TRUE.|FALSE OR TRUE = TRUE.',
              'OR ni AND kabi baholamang. || Не вычисляйте OR как AND.',
              'OR uchun kamida bitta rost qism yetadi. || Для OR достаточно одной истинной части.'),
            s('Qaysi shart 10 dan 20 gacha, ikkala chekkasi bilan, qiymatni qabul qiladi? || Какое условие принимает значения от 10 до 20 включительно?', [
                ('(x ≥ 10) AND (x ≤ 20) || (x ≥ 10) AND (x ≤ 20)', 'Ikkala chegara bir vaqtda bajariladi. || Обе границы выполняются одновременно.'),
                ('(x ≥ 10) OR (x ≤ 20) || (x ≥ 10) OR (x ≤ 20)', 'Bu oraliq tashqarisidagi qiymatlarni ham qabul qiladi. || Это принимает и значения вне интервала.'),
                ('(x > 10) AND (x < 20) || (x > 10) AND (x < 20)', 'Chegaralar chiqarib tashlangan. || Границы исключены.')],
              'Pastdan va yuqoridan cheklov birga kerak.|Chegaralar kiritilgani uchun ≥ va ≤ olinadi. || Нужны одновременно нижнее и верхнее ограничения.|Поскольку границы включены, используются ≥ и ≤.',
              'Oraliq ichida bo‘lish uchun AND kerak. || Для принадлежности интервалу нужен AND.',
              'Qiymat ikkala talabni ham bajarishi kerak. || Значение должно выполнить оба требования.'),
            s('a = TRUE, b = FALSE. NOT (a AND b) qiymati? || a = TRUE, b = FALSE. Чему равно NOT (a AND b)?', [
                ('TRUE || TRUE', 'AND yolg‘on, inkori rost. || AND ложно, его отрицание истинно.'),
                ('FALSE || FALSE', 'Bu AND natijasini inkorsiz qoldiradi. || Это оставляет результат AND без отрицания.'),
                ('a yangi qiymat oladi || a получает новое значение', 'Ifoda a ni o‘zgartirmaydi. || Выражение не изменяет a.')],
              'TRUE AND FALSE = FALSE.|NOT FALSE = TRUE. || TRUE AND FALSE = FALSE.|NOT FALSE = TRUE.',
              'NOT qavs ichidagi butun ifodaga qo‘llanadi. || NOT применяется ко всему выражению в скобках.'),
            s('Ruxsat: talaba yoki xodim, lekin bloklanmagan. Qaysi shart mos? || Доступ: студент или сотрудник, но без блокировки. Какое условие подходит?', [
                ('(student OR staff) AND NOT blocked || (student OR staff) AND NOT blocked', 'Rol va bloklanmaganlik birga bajariladi. || Роль и отсутствие блокировки выполняются вместе.'),
                ('student OR (staff AND NOT blocked) || student OR (staff AND NOT blocked)', 'Bu bloklangan talabaga ham ruxsat beradi. || Это разрешает доступ даже заблокированному студенту.'),
                ('student AND staff AND NOT blocked || student AND staff AND NOT blocked', 'Bir vaqtning o‘zida ikkala rolni talab qiladi. || Это требует одновременно обе роли.')],
              'Avval ruxsatli rollarni OR bilan birlashtiring.|Butun guruhga bloklanmaganlik talabini AND bilan qo‘shing. || Сначала объедините разрешённые роли через OR.|Ко всей группе добавьте требование отсутствия блокировки через AND.',
              'Qavs olib tashlansa ruxsat ma’nosi o‘zgarishi mumkin. || Удаление скобок может изменить смысл допуска.')], ['cond-compare']),
        l('cond-if', 'if-else va bitta tarmoq || if-else и одна ветвь', [
            'if sharti TRUE bo‘lsa birinchi blok, aks holda else bajariladi. Shu konstruksiyaning faqat bitta tarmog‘i ishlaydi. || Если условие if равно TRUE, выполняется первый блок, иначе — else. В этой конструкции выполняется только одна ветвь.',
            'Mustaqil ikkita if boshqa xulq beradi: ikkinchi shart birinchi blokdan keyingi qiymatni tekshiradi. if-else ikkinchi tarmog‘ida shart qayta tekshirilmaydi. || Два независимых if ведут себя иначе: второе условие проверяет значение после первого блока. В ветви else условие повторно не проверяется.',
            'Kursda bloklar { } bilan ajratiladi. Chekinish o‘qishni osonlashtiradi, ammo bajariladigan amallarni qavslar belgilaydi. || В курсе блоки выделяются { }. Отступы облегчают чтение, но выполняемые действия определяют скобки.'
        ], 'x ← −2; if x < 0 {x ← −x} else {x ← x + 1}. Oxirgi x? || x ← −2; if x < 0 {x ← −x} else {x ← x + 1}. Чему равно конечное x?',
           '−2 < 0 rost.|Birinchi blok x ni 2 qiladi.|else bajarilmaydi. || −2 < 0 истинно.|Первый блок делает x равным 2.|else не выполняется.', '2 || 2', [
            n('x ← 7; if x ≥ 5 {x ← x − 2} else {x ← x + 2}. Oxirgi x? || x ← 7; if x ≥ 5 {x ← x − 2} else {x ← x + 2}. Чему равно конечное x?', 5,
              '7 ≥ 5 rost.|x = 7 − 2 = 5; else tashlanadi. || 7 ≥ 5 истинно.|x = 7 − 2 = 5; else пропускается.',
              'Ikkala tarmoqni ketma-ket bajarmang. || Не выполняйте обе ветви последовательно.',
              'Shartni blokka kirishdan oldingi qiymatda tekshiring. || Проверьте условие по значению до входа в блок.'),
            n('x ← 1; if x < 3 {x ← x + 2}; if x == 3 {x ← x × 4}. Oxirgi x? || x ← 1; if x < 3 {x ← x + 2}; if x == 3 {x ← x × 4}. Чему равно конечное x?', 12,
              'Birinchi mustaqil if x ni 3 qiladi.|Ikkinchi if ham rost, x = 12. || Первый независимый if делает x равным 3.|Второй if тоже истинен, x = 12.',
              'Ikki mustaqil if ni if-else deb o‘qimang. || Не читайте два независимых if как if-else.',
              'Ikkinchi if yangi qiymatni ko‘radi. || Второй if видит новое значение.'),
            n('x ← 0; if x > 0 {y ← 10} else {y ← 20}. y qiymati? || x ← 0; if x > 0 {y ← 10} else {y ← 20}. Чему равно y?', 20,
              '0 > 0 yolg‘on.|else y ga 20 beradi. || 0 > 0 ложно.|else присваивает y значение 20.',
              'Nolni musbat deb hisoblamang. || Не считайте ноль положительным.'),
            n('x ← 4; if x < 5 {x ← x + 3} else {x ← x − 3}; OUTPUT x. Chiqish? || x ← 4; if x < 5 {x ← x + 3} else {x ← x − 3}; OUTPUT x. Каков выход?', 7,
              'Boshlang‘ich 4 shartni bajaradi, x = 7.|Yangi qiymat else ni ishga tushirmaydi, chiqish 7. || Исходное 4 выполняет условие, x = 7.|Новое значение не запускает else, вывод равен 7.',
              'Blokdan keyingi qiymat sabab else ga o‘tib ketmang. || Не переходите в else из-за значения после первого блока.')], ['cond-compare']),
        l('cond-multiple', 'Ichma-ich va ko‘p tarmoqli shart || Вложенные и многоветвевые условия', [
            'if ... else if ... else zanjirida birinchi rost tarmoq bajarilib, qolganlari tashlanadi. Umumiy shart avval tursa, torroq shartga navbat kelmasligi mumkin. || В цепочке if ... else if ... else выполняется первая истинная ветвь, остальные пропускаются. Если общее условие стоит первым, до более узкого можно не дойти.',
            'Ball bo‘yicha yuqori toifani avval tekshirish qulay: ball ≥ 90, keyin ball ≥ 60, oxirida qolgan holat. Chegaralarni jadval qilib tekshiring. || Для категорий балла удобно сначала проверить верхнюю: ball ≥ 90, затем ball ≥ 60, в конце остальные случаи. Проверяйте границы по таблице.',
            'Ichma-ich shartda ichki if faqat tashqi blok ochilsa bajariladi. Tashqi shart yolg‘on bo‘lsa ichki tekshiruvga umuman kirilmaydi. || Во вложенном условии внутренний if выполняется только после входа во внешний блок. Если внешнее условие ложно, внутренней проверки вообще не будет.'
        ], 'ball = 95; if ball ≥ 90 {r ← 3} else if ball ≥ 60 {r ← 2} else {r ← 1}. r? || ball = 95; if ball ≥ 90 {r ← 3} else if ball ≥ 60 {r ← 2} else {r ← 1}. Чему равно r?',
           'Birinchi shart rost.|r = 3.|Keyingi shartlar bajarilmaydi. || Первое условие истинно.|r = 3.|Следующие условия не выполняются.', '3 || 3', [
            n('ball = 75; if ball ≥ 90 {r ← 3} else if ball ≥ 60 {r ← 2} else {r ← 1}. r? || ball = 75; if ball ≥ 90 {r ← 3} else if ball ≥ 60 {r ← 2} else {r ← 1}. Чему равно r?', 2,
              '75 ≥ 90 yolg‘on.|75 ≥ 60 rost, r = 2. || 75 ≥ 90 ложно.|75 ≥ 60 истинно, r = 2.',
              'Shartlarni tartib bilan baholang. || Вычисляйте условия по порядку.',
              'Birinchi rost shartda zanjir to‘xtaydi. || Цепочка останавливается на первом истинном условии.'),
            n('a = 5, b = −1; r ← 0; if a > 0 {if b > 0 {r ← 1} else {r ← 2}} else {r ← 3}. r? || a = 5, b = −1; r ← 0; if a > 0 {if b > 0 {r ← 1} else {r ← 2}} else {r ← 3}. Чему равно r?', 2,
              'Tashqi shart rost, ichki blok ochiladi.|b > 0 yolg‘on, ichki else r = 2 qiladi. || Внешнее условие истинно, открывается внутренний блок.|b > 0 ложно, внутренний else делает r = 2.',
              'Ichki va tashqi else ni aralashtirmang. || Не путайте внутренний и внешний else.',
              'Har else qaysi if ga tegishli ekanini qavsdan toping. || По скобкам определите, к какому if относится каждый else.'),
            n('ball = 90; if ball ≥ 90 {r ← 3} else if ball ≥ 60 {r ← 2} else {r ← 1}. r? || ball = 90; if ball ≥ 90 {r ← 3} else if ball ≥ 60 {r ← 2} else {r ← 1}. Чему равно r?', 3,
              '90 yuqori chegaraga kiradi.|Birinchi tarmoq r = 3 beradi. || 90 входит в верхнюю категорию.|Первая ветвь даёт r = 3.',
              'Chegarani pastki toifaga tushirmang. || Не относите границу к нижней категории.'),
            s('Yuqori toifa ball ≥ 90. Kod avval if ball ≥ 60, keyin else if ball ≥ 90 ni tekshiradi. Muammo nima? || Верхняя категория: ball ≥ 90. Код сначала проверяет if ball ≥ 60, затем else if ball ≥ 90. В чём проблема?', [
                ('Yuqori ball birinchi tarmoqqa kirib, yuqori toifa ochilmaydi || Высокий балл попадает в первую ветвь, верхняя категория недостижима', 'Tor shart umumiy shartdan keyin qolib ketgan. || Узкое условие оказалось после общего.'),
                ('Barcha shartlar doim yolg‘on || Все условия всегда ложны', 'Yuqori ball birinchi shartni bajaradi. || Высокий балл выполняет первое условие.'),
                ('Har ikkala tarmoq bajariladi || Выполняются обе ветви', 'else if zanjiri faqat birini bajaradi. || Цепочка else if выполняет только одну ветвь.')],
              'Yuqori ball quyi chegaradan ham katta.|Birinchi tarmoq tanlangach zanjir qolganini tashlaydi. || Высокий балл также превышает нижнюю границу.|После выбора первой ветви цепочка пропускает остальные.',
              'Tor va umumiy shartlarning tartibini tekshiring. || Проверяйте порядок узких и общих условий.')], ['cond-if', 'cond-boolean']),
        l('cond-switch', 'switch-case va to‘liq qamrov || switch-case и полнота обработки', [
            'Kursdagi switch mode {case ...; default ...} bir qiymatni aniq variantlar bilan taqqoslaydi. Faqat mos case ishlaydi; avtomatik keyingi case ga o‘tish yo‘q. || В курсе switch mode {case ...; default ...} сравнивает одно значение с точными вариантами. Выполняется только совпавший case; автоматического перехода к следующему case нет.',
            'default hech bir case mos kelmaganda ishlaydi. Bu psevdokod qoidasi; haqiqiy tilda, masalan C uslubidagi switch da, break va boshqa qoidalarni alohida tekshirish zarur. || default выполняется, когда ни один case не подошёл. Это правило псевдокода; в реальном языке, например в switch стиля C, отдельно проверяют break и другие правила.',
            'Oraliq, bir nechta o‘zgaruvchi yoki murakkab mantiq uchun if ko‘pincha ravshanroq. Menyu kodi kabi aniq diskret qiymatlar switch uchun mos. || Для интервала, нескольких переменных или сложной логики if часто понятнее. Точные дискретные значения, например коды меню, подходят для switch.'
        ], 'mode = 2; switch mode {case 1: r ← 10; case 2: r ← 20; default: r ← 0}. r? || mode = 2; switch mode {case 1: r ← 10; case 2: r ← 20; default: r ← 0}. Чему равно r?',
           'mode ikkinchi case ga teng.|Faqat r ← 20 bajariladi.|default bajarilmaydi. || mode совпадает со вторым case.|Выполняется только r ← 20.|default не выполняется.', '20 || 20', [
            n('mode = 9; switch mode {case 1: r ← 10; case 2: r ← 20; default: r ← −1}. r? || mode = 9; switch mode {case 1: r ← 10; case 2: r ← 20; default: r ← −1}. Чему равно r?', -1,
              '9 berilgan case lardan biriga ham teng emas.|default r = −1 beradi. || 9 не равно ни одному из заданных case.|default даёт r = −1.',
              'Noma’lum qiymatga mavjud case ni taxminan moslamang. || Не подбирайте приблизительно существующий case для неизвестного значения.',
              'Aniq moslik bo‘lmasa default olinadi. || При отсутствии точного совпадения берётся default.'),
            s('“x musbat VA y manfiy” kabi shart uchun qaysi usul aniqroq? || Какой способ понятнее для условия «x положительно И y отрицательно»?', [
                ('if (x > 0) AND (y < 0) || if (x > 0) AND (y < 0)', 'Ikki o‘zgaruvchi bo‘yicha mantiq bevosita yozilgan. || Логика по двум переменным записана непосредственно.'),
                ('switch x da faqat case 1 || В switch x только case 1', 'Bu barcha musbat qiymatlarni va y ni qamramaydi. || Это не охватывает все положительные значения и y.'),
                ('Har qanday kirishda default || default для любого входа', 'Bu kerakli shartni tekshirmaydi. || Это не проверяет нужное условие.')],
              'Shart aniq bitta qiymatga tenglik emas.|if ikki taqqoslashni AND bilan bog‘laydi. || Условие не является равенством одному точному значению.|if объединяет два сравнения через AND.',
              'switch ni har qanday shartning o‘rniga ishlatmang. || Не подставляйте switch вместо любого условия.',
              'Bu yerda bitta kod emas, ikki belgi tekshiriladi. || Здесь проверяется не один код, а два признака.'),
            n('code = 1; switch code {case 1: r ← 4; case 2: r ← 8; default: r ← 0}. Kurs qoidasi bo‘yicha r? || code = 1; switch code {case 1: r ← 4; case 2: r ← 8; default: r ← 0}. Чему равно r по правилам курса?', 4,
              'Birinchi case mos.|Keyingi case ga o‘tish yo‘q, r = 4. || Совпадает первый case.|Перехода к следующему case нет, r = 4.',
              'Boshqa tilning fall-through qoidasini bu psevdokodga ko‘chirmang. || Не переносите правило fall-through другого языка в этот псевдокод.'),
            s('Menyu faqat OPEN va SAVE kodlarini qabul qiladi. Boshqa kod uchun xabar ham kerak. Nima qo‘shiladi? || Меню принимает только коды OPEN и SAVE. Для другого кода тоже нужно сообщение. Что добавить?', [
                ('default da noma’lum kod xabari || Сообщение о неизвестном коде в default', 'Mos kelmagan qiymatlar aniq qayta ishlanadi. || Несовпавшие значения обрабатываются явно.'),
                ('Noma’lum kodni SAVE deb olish || Считать неизвестный код SAVE', 'Bu noto‘g‘ri amalni boshlashi mumkin. || Это может запустить неверное действие.'),
                ('OPEN ni yana takrorlash || Ещё раз повторить OPEN', 'Takroriy case noma’lum qiymatni qamramaydi. || Повтор case не охватывает неизвестное значение.')],
              'Ma’lum variantlar alohida case.|Qolgan kirishlar default orqali tushunarli xabar oladi. || Известные варианты — отдельные case.|Остальные входы получают понятное сообщение через default.',
              'Noma’lum kirishni jim qoldirmang yoki boshqa amalga aylantirmang. || Не игнорируйте неизвестный вход и не превращайте его в другое действие.')], ['cond-multiple'])])
