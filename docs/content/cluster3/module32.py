from authoring import choice as c, lesson as l, module, q


def build():
    return module('teamwork-git', 2, 'Kichik guruh loyihasi va Git || Командный мини-проект и Git', [
        l('team-contract', 'Vazifalar va modul shartnomasi || Задачи и контракты модулей',
          'Ishni mas’ul, kirish, chiqish va qabul mezoni bilan taqsimlaysiz. || Распределяете работу с ответственным, входом, выходом и критерием приёмки.', [
            'Modul foydali alohida natija beradi: katalog kitob ma’lumotini topadi, berish moduli mavjud nusxani qarzga beradi. Vazifa nomi bilan birga mas’ul, bog‘liqlik va tugallanish mezoni yoziladi. || Модуль даёт отдельный полезный результат: каталог находит сведения о книге, модуль выдачи выдаёт доступный экземпляр. Вместе с названием задачи записывают ответственного, зависимости и критерий завершения.',
            'Shartnomada parametrlar, natija va xato holati kelishiladi. Masalan, find_book(book_id) topilmasa None qaytaradi. Biri None, boshqasi {} kutsa, kodlar alohida ishlasa ham birgalikda buziladi. || В контракте согласуют параметры, результат и ошибочные случаи. Например, find_book(book_id) возвращает None, если книга не найдена. Если один возвращает None, а другой ждёт {}, совместная работа нарушится даже при отдельных успехах.',
            '“Tugadi” degani kod yozildi emas: shartnoma testlari o‘tgan, kerakli izoh va hamkor reviewsi bor. To‘siqni erta aytish va yangi kelishuvni yozish jamoaning vaqtini tejaydi. || «Готово» означает не только написанный код: прошли тесты контракта, есть пояснение и ревью коллеги. Раннее сообщение о препятствии и запись нового соглашения экономят время команды.'
          ], 'Katalogchi find_book(id) topilmaganda None qaytaradi. Berish moduli natijadan title o‘qiydi. Integratsiyadan oldingi kelishuv? || Автор каталога возвращает None из find_book(id), если книга не найдена. Модуль выдачи читает title из результата. Что согласовать до интеграции?',
          'Topildi va topilmadi holatlarini yozing.|None bo‘lsa berishni rad etish kelishilsin.|Ikkala holat uchun umumiy test tuzing. || Запишите случаи найдено и не найдено.|Договоритесь отклонять выдачу при None.|Составьте общие тесты обоих случаев.',
          'Bir xil shartnoma va integratsiya testi. || Единый контракт и интеграционный тест.', [
            q('“Katalogni qil” vazifasini nima aniqlashtiradi? || Что уточнит задачу «Сделай каталог»?', [
                c('Mas’ul, find_book kirish/chiqishi va topilmadi testi || Ответственный, вход/выход find_book и тест отсутствия', 'Mas’uliyat va qabul mezoni tekshiriladi. || Ответственность и приёмка проверяемы.'),
                c('Faqat “tezroq” deb yozish || Только написать «быстрее»', 'Natija va shartnoma noaniq qoladi. || Результат и контракт остаются неопределёнными.'),
                c('Har kim barcha faylni bir vaqtda yozishi || Всем одновременно писать все файлы', 'Vazifalar va bog‘lanishlar aniqlanmaydi. || Не уточняет задачи и зависимости.')],
              'Kim va nima qilishi aniq bo‘lsin.|Natijani test bilan qabul qiling. || Уточните, кто и что делает.|Принимайте результат по тесту.',
              'Topshiriq sarlavhasini shartnoma deb olmang. || Не считайте заголовок задачи контрактом.', 'Bajarilganini qanday tekshirasiz? || Как проверить готовность?'),
            q('A modul narxni so‘mda, B modul tiyin deb qabul qiladi. Oldindan nima kelishiladi? || Модуль A выдаёт цену в сумах, B принимает её за тийины. Что согласовать заранее?', [
                c('Birlik va zarur o‘zgartirish qoidasi || Единицу и нужное правило преобразования', 'Bir xil son boshqa miqdor bo‘lib talqin qilinmaydi. || Одно число не будет трактоваться как разные суммы.'),
                c('Ikkalasida ham int ishlatish; birlikni yozmaslik || Использовать int с обеих сторон, не записывая единицу', 'Bir xil tur turli birlikni ajratmaydi. || Один тип не различает разные единицы.'),
                c('Ikkala o‘zgaruvchini price deb nomlashning o‘zi || Только назвать обе переменные price', 'Bir xil nom birlik kelishuvini almashtirmaydi. || Одинаковое имя не заменяет соглашения о единицах.')],
              'Kirish/chiqishning ma’nosi ham shartnomaga kiradi.|Pul birligini bitta qilib belgilang. || Смысл входа/выхода тоже входит в контракт.|Зафиксируйте одну денежную единицу.',
              'Faqat tur mosligi yetarli emas. || Совпадения типов недостаточно.', '100 soni qaysi birlikda? || В какой единице число 100?'),
            q('Funksiya ba’zan ro‘yxat, ba’zan matn qaytaradi; chaqiruvchi faqat ro‘yxat kutadi. Birinchi qadam? || Функция возвращает то список, то текст; вызывающий код ждёт только список. Первый шаг?', [
                c('Natija va xato formatini kelishib, ikkala tomonni moslashtirish || Согласовать формат результата и ошибки, привести обе стороны к нему', 'Mos interfeys yaratiladi. || Появляется согласованный интерфейс.'),
                c('Xato chiqqan satrni yashirish || Скрыть строку ошибки', 'Format nomosligi qoladi. || Несоответствие форматов останется.'),
                c('Faqat bitta muvaffaqiyatli demo qilish || Показать только один успешный пример', 'Xato holati tekshirilmaydi. || Ошибочный случай не проверяется.')],
              'Nomoslikni shartnomada hal qiling.|Oddiy va xato holatlarni tekshiring. || Устраните несоответствие в контракте.|Проверьте обычные и ошибочные случаи.',
              'Alohida ishlash integratsiya isboti emas. || Отдельная работа не доказывает совместимость.'),
            q('Hamkor moduliga bog‘liq ish to‘xtadi. Jamoaga nima yetkazish foydali? || Работа остановилась из-за зависимого модуля коллеги. Что полезно сообщить команде?', [
                c('Qaysi shartnoma kutilayotgani, ta’siri va vaqtinchalik test varianti || Какого контракта ждём, влияние и временный вариант теста', 'To‘siq bo‘yicha qaror qilish mumkin. || Можно принять решение по препятствию.'),
                c('Indamay oxirgi kungacha kutish || Молча ждать до последнего дня', 'Bog‘liqlik xavfi kech ochiladi. || Риск зависимости обнаружится поздно.'),
                c('Hamkorni dalilsiz ayblash || Обвинить коллегу без фактов', 'Vazifa yoki yechim aniqlashmaydi. || Задача и решение не уточняются.')],
              'To‘siqni aniq yozing.|Shartnoma asosidagi vaqtinchalik stubni kelishing. || Опишите препятствие точно.|Согласуйте временную заглушку по контракту.',
              'To‘siqni yashirish hamkorlik emas. || Скрывать препятствие — не сотрудничество.')]),
        l('team-pair', 'Juftlikda dasturlash || Парное программирование',
          'Driver va navigator vazifalarini hamda foydali rol almashishni tushuntirasiz. || Объясняете роли драйвера и навигатора и полезную смену ролей.', [
            'Driver klaviaturada kod yozadi va niyatini ovoz chiqarib tushuntiradi. Navigator talab, keyingi qadam, test va xavflarni kuzatadi. Ikkalasi ham faol fikrlaydi; navigator tomoshabin emas. || Драйвер пишет код за клавиатурой и объясняет намерение. Навигатор следит за требованием, следующим шагом, тестами и рисками. Оба думают активно; навигатор не зритель.',
            'Rolni kichik vazifa tugaganda yoki kelishilgan qisqa davrda almashtiring. Almashishdan oldin joriy holat, keyingi test va ochiq savol aytiladi. Tez yozuvchi doim driver bo‘lib qolmasin. || Меняйте роли после небольшой задачи или через согласованный короткий интервал. Перед сменой передайте состояние, следующий тест и открытый вопрос. Быстро печатающий участник не должен всегда оставаться драйвером.',
            'Fikrlar farq qilsa, talab va kichik testga qayting. “Sen noto‘g‘ri” o‘rniga “bo‘sh kirishda nima bo‘ladi?” deyish muammoni tekshirishga yordam beradi. || При разногласии вернитесь к требованию и небольшому тесту. Вместо «ты неправ» спросите «что будет при пустом входе?» — это помогает проверить проблему.'
          ], 'Driver kitob berish funksiyasini yozmoqda. Navigator qaytgan kitobni yana berish mumkinligini so‘raydi. Bu rolga mosmi? || Драйвер пишет функцию выдачи. Навигатор спрашивает, можно ли снова выдать возвращённую книгу. Соответствует ли это роли?',
          'Navigator talab va holatlarni tekshiradi.|Qaytarishdan keyingi holat uchun test yoziladi.|Natija bilan qaror qilinadi. || Навигатор проверяет требования и состояния.|Добавляется тест состояния после возврата.|Решение принимается по результату.',
          'Ha, bu foydali talab/test savoli. || Да, это полезный вопрос по требованию и тесту.', [
            q('Navigator uchun eng mos ish? || Самая подходящая работа навигатора?', [
                c('Talab, chegaralar va keyingi testni tekshirish || Проверять требования, границы и следующий тест', 'Bu kod yozishni mazmunli kuzatadi. || Это содержательное сопровождение написания кода.'),
                c('Faqat xabarlarni ko‘rish || Только читать сообщения', 'Juftlikdagi faol vazifa bajarilmaydi. || Активная роль в паре не выполняется.'),
                c('Driver izohini eshitmay boshqa modul yozish || Не слушая драйвера, писать другой модуль', 'Bu juftlikdagi umumiy diqqatni bo‘ladi. || Разделяет общее внимание пары.')],
              'Bitta vazifa birgalikda bajariladi.|Navigator talab va testga e’tibor beradi. || Одна задача выполняется совместно.|Навигатор следит за требованиями и тестами.',
              'Navigator passiv kuzatuvchi emas. || Навигатор не пассивный наблюдатель.', 'Klaviaturadan tashqari qaysi fikrlash ishi kerak? || Какая мыслительная работа нужна помимо клавиатуры?'),
            q('Rol almashishda nimani topshirish kerak? || Что передать при смене ролей?', [
                c('Joriy holat, keyingi qadam va hali yechilmagan savol || Текущее состояние, следующий шаг и открытый вопрос', 'Yangi driver ishni tushunib davom ettiradi. || Новый драйвер продолжит с пониманием.'),
                c('Faqat klaviaturani || Только клавиатуру', 'Kontekst yo‘qolishi mumkin. || Контекст может потеряться.'),
                c('Faqat oxirgi satr raqamini || Только номер последней строки', 'Maqsad va tekshiruv rejasi noma’lum qoladi. || Цель и план проверки останутся неизвестны.')],
              'Holatni qisqa tushuntiring.|Keyingi testni ayting. || Кратко объясните состояние.|Назовите следующий тест.',
              'Jismoniy almashish bilim almashishning o‘zi emas. || Физическая смена не равна передаче понимания.', 'Hamkor darhol nimani bilishi kerak? || Что коллега должен сразу знать?'),
            q('Juftlik yechim bo‘yicha kelisha olmayapti. Foydali qadam? || Пара не согласна по решению. Полезный шаг?', [
                c('Talabga oid kichik test bilan variantlarni solishtirish || Сравнить варианты небольшим тестом по требованию', 'Qaror dalilga tayanadi. || Решение опирается на факты.'),
                c('Balandroq gapirgan variantni olish || Принять вариант того, кто громче говорит', 'To‘g‘rilik ovozga bog‘liq emas. || Правильность не зависит от громкости.'),
                c('Testlarni taqiqlash || Запретить тесты', 'Tekshirish imkoniyati kamayadi. || Снижается возможность проверки.')],
              'Kelishmovchilikni aniq shartga aylantiring.|Test natijasini talab bilan solishtiring. || Превратите разногласие в конкретное условие.|Сравните результат теста с требованием.',
              'Obro‘ dalil o‘rnini bosmaydi. || Авторитет не заменяет доказательства.'),
            q('Faqat bitta a’zo kod va sababni tushunadi. Qaysi yakunlash qadami mos? || Только один участник понимает код и причину решения. Какой завершающий шаг подходит?', [
                c('Rolni almashtirib, hamkor asosiy oqimni test bilan tushuntirsin || Сменить роли, пусть коллега объяснит основной поток с тестом', 'Bilimni bo‘lishish kuzatiladigan bo‘ladi. || Передачу понимания можно наблюдать.'),
                c('Faqat bitta a’zo nomidan topshirish || Сдать от имени одного участника', 'Jamoaviy o‘rganish tekshirilmaydi. || Совместное обучение не проверяется.'),
                c('Kodga tasodifiy izoh qo‘shish || Добавить случайный комментарий', 'Hamkor tushunishini ko‘rsatmaydi. || Не показывает понимание коллеги.')],
              'Hamkor izoh va test bilan qayta ko‘rsatsin.|Savol tug‘ilsa shartnomaga qayting. || Пусть коллега повторно покажет объяснение и тест.|При вопросах вернитесь к контракту.',
              'Commitlar soni bilim almashishni o‘zi isbotlamaydi. || Число коммитов само по себе не доказывает обмен знаниями.')]),
        l('git-staging', 'Fayl holati va commit || Состояния файлов и коммит',
          'Working tree, staging va commit mazmunini farqlaysiz. || Различаете рабочее дерево, индекс и коммит.', [
            'Working tree — fayllarning joriy nusxasi. git add tanlangan mazmunni staging (indeks)ga oladi. git commit indeksdagi holatni mahalliy tarixga yozadi. Commitni masofaviy serverga uzatish uchun alohida push kerak. || Рабочее дерево — текущие файлы. git add помещает выбранное содержимое в индекс. git commit записывает состояние индекса в локальную историю. Для передачи коммита на удалённый сервер нужен отдельный push.',
            'git status holatni ko‘rsatadi. git diff odatda working tree bilan indeks farqini, git diff --staged esa indeks bilan HEAD farqini ko‘rsatadi. Adddan keyingi yangi tahrir avtomatik stagingga kirmaydi. || git status показывает состояние. git diff обычно сравнивает рабочее дерево с индексом, git diff --staged — индекс с HEAD. Новая правка после add не попадает в индекс автоматически.',
            'Kichik mazmunli commit bir vazifa yoki tuzatishni tushuntiradi. Commitdan oldin diff va testni ko‘ring. O‘quv mashqlarida ham parol va tokenlarni commitga qo‘shmang. || Небольшой осмысленный коммит объясняет одну задачу или исправление. Перед коммитом проверьте diff и тесты. Даже в учебных упражнениях не включайте пароли и токены.'
          ], 'Tracked note.txt avval v1. Uni v2 qildingiz, git add note.txt; keyin v3 qildingiz. Commit nima saqlaydi? || Отслеживаемый note.txt был v1. Вы изменили на v2, выполнили git add note.txt, затем изменили на v3. Что сохранит коммит?',
          'Add paytida indeksga v2 olindi.|Keyingi v3 faqat working treeda.|Oddiy git commit indeksdagi v2 ni saqlaydi. || При add в индекс попало v2.|Позднее v3 осталось в рабочем дереве.|Обычный git commit сохранит v2 из индекса.',
          'Commit v2; ishchi faylda v3 qoladi. || В коммите v2; в рабочем файле остаётся v3.', [
            q('git add file.py dan keyin oddiy git commit nimani oladi? || Что берёт обычный git commit после git add file.py?', [
                c('Indeksdagi tanlangan mazmunni || Выбранное содержимое индекса', 'Commit staging holatini yozadi. || Коммит записывает состояние индекса.'),
                c('Har doim barcha disklardagi fayllarni || Всегда все файлы на всех дисках', 'Git repozitoriy va indeks doirasida ishlaydi. || Git работает в рамках репозитория и индекса.'),
                c('Faqat serverdagi fayllarni || Только файлы на сервере', 'Mahalliy commit server nusxasidan olinmaydi. || Локальный коммит не берётся с сервера.')],
              'Add indeksni tayyorlaydi.|Commit shu holatni yozadi. || Add готовит индекс.|Commit записывает это состояние.',
              'Working tree va indeks doim bir xil emas. || Рабочее дерево и индекс не всегда совпадают.', 'Add nima tayyorlaydi? || Что подготавливает add?'),
            q('Keyingi commitda nima bo‘lishini ko‘rish uchun qaysi diff? || Какой diff покажет содержимое будущего коммита?', [
                c('git diff --staged || git diff --staged', 'Indeksni HEAD bilan taqqoslaydi. || Сравнивает индекс с HEAD.'),
                c('Faqat git diff || Только git diff', 'Odatda stagingga olinmagan farqni ko‘rsatadi. || Обычно показывает неиндексированные изменения.'),
                c('git log --oneline || git log --oneline', 'Bu oldingi tarixni ko‘rsatadi. || Показывает прежнюю историю.')],
              'Commitning manbasi indeks.|Shuning diffini ko‘ring. || Источник коммита — индекс.|Посмотрите его diff.',
              'Tarix bilan tayyorlanayotgan o‘zgarishni farqlang. || Различайте историю и готовящиеся изменения.', 'Indeksni qaysi parametr ko‘rsatadi? || Какой параметр показывает индекс?'),
            q('Mahalliy commit yaratildi, push qilinmadi. Hamkor remote orqali uni oladimi? || Создан локальный коммит, push не выполнен. Получит ли коллега его через remote?', [
                c('Yo‘q, commit hali remote ga uzatilmagan || Нет, коммит ещё не передан на remote', 'Commit va push alohida amallar. || Commit и push — разные операции.'),
                c('Ha, commit har doim avtomatik push qiladi || Да, commit всегда автоматически делает push', 'Oddiy Git commit bunday qilmaydi. || Обычный Git commit этого не делает.'),
                c('Ha, git status uzatadi || Да, git status передаёт', 'Status kuzatuv buyrug‘i. || Status — команда просмотра.')],
              'Commit mahalliy tarixga yozildi.|Remote hali yangilanmagan. || Коммит записан локально.|Remote ещё не обновлён.',
              'Mahalliy saqlash va uzatishni aralashtirmang. || Не смешивайте локальную запись и передачу.'),
            q('Tracked a.txt v1 edi. v2 qilib add, keyin v3 qilib qayta add qilindi. Oddiy commitdagi mazmun? || Отслеживаемый a.txt был v1. Изменили на v2 и add, затем на v3 и снова add. Содержимое обычного коммита?', [
                c('v3 || v3', 'Ikkinchi add indeksni yangiladi. || Второй add обновил индекс.'),
                c('v1 || v1', 'Indeks ikki marta yangilandi. || Индекс дважды обновлён.'),
                c('v2 || v2', 'Bu birinchi add holati, ikkinchisi uni almashtirdi. || Это состояние первого add, второй его заменил.')],
              'Oxirgi add paytidagi mazmunni toping.|U v3. || Найдите содержимое на момент последнего add.|Это v3.',
              'Indeks eng birinchi addda muzlab qolmaydi. || Индекс не замораживается на первом add.')]),
        l('git-review-merge', 'Branch, review va birlashtirish || Ветка, ревью и слияние',
          'Kichik o‘zgarishni alohida branchda ko‘rib chiqib birlashtirish oqimini tanlaysiz. || Выбираете процесс проверки и слияния небольшого изменения из отдельной ветки.', [
            'Branch alohida ish yo‘lini beradi. O‘quv oqimi: kelishilgan bazadan branch, kichik o‘zgarish, test, commit, review, so‘ng maqsad branchga merge. Pull request hosting xizmatidagi review vositasi; mahalliy Gitning o‘zi emas. || Ветка даёт отдельную линию работы. Учебный процесс: ветка от согласованной базы, небольшая правка, тест, коммит, ревью, затем merge в целевую ветку. Pull request — средство ревью на хостинге, а не сама локальная система Git.',
            'git merge feature joriy branchga feature tarixini birlashtiradi. Avval joriy branchni tekshiring. Konfliktsiz merge mazmuniy to‘g‘rilikni kafolatlamaydi: natija test va shartnoma bilan tekshiriladi. || git merge feature объединяет историю feature с текущей веткой. Сначала проверьте текущую ветку. Слияние без конфликтов не гарантирует смысловую правильность: результат проверяют тестами и контрактом.',
            'Review uchun nima o‘zgargani, nima sababdan va qanday tekshirilgani yoziladi. Hamkor fikri qayta tekshiriladi; tasdiqdan keyingi yangi tuzatish ham tegishli review/testdan o‘tadi. || Для ревью описывают, что изменилось, почему и как проверено. Замечания коллеги перепроверяют; новая правка после одобрения тоже проходит нужное ревью и тест.'
          ], 'Joriy branch main, toza holat. feature da katalog testi o‘tgan. git merge feature qaysi branchni yangilaydi? || Текущая ветка main, рабочее дерево чистое. В feature прошёл тест каталога. Какую ветку обновляет git merge feature?',
          'Joriy branch main ekanini tekshiring.|Merge feature ni main ga oladi.|Birlashtirilgan holatda testni qaytaring. || Убедитесь, что текущая ветка main.|Merge включает feature в main.|Повторите тест объединённого состояния.',
          'main yangilanadi; integratsiya testi baribir kerak. || Обновляется main; интеграционный тест всё равно нужен.', [
            q('Merge oldidan eng foydali tekshiruv? || Самая полезная проверка перед merge?', [
                c('Joriy branch, diff va test natijasi || Текущая ветка, diff и результат тестов', 'Qayerga va nimani qo‘shish ma’lum. || Известно, куда и что добавляется.'),
                c('Faqat commit xabarini o‘qish, diff va testni ko‘rmaslik || Только прочитать сообщение коммита без diff и тестов', 'Tavsif haqiqiy o‘zgarish va to‘g‘rilikni kafolatlamaydi. || Описание не гарантирует фактическое изменение и правильность.'),
                c('Faqat branch testini ko‘rish, joriy branchni tekshirmaslik || Проверить только тест ветки, не проверяя текущую ветку', 'To‘g‘ri kod ham noto‘g‘ri branchga qo‘shilishi mumkin. || Даже правильный код можно слить не в ту ветку.')],
              'Maqsad branchni aniqlang.|O‘zgarish va tekshiruvni ko‘ring. || Определите целевую ветку.|Проверьте изменение и его проверку.',
              'Merge buyrug‘ini kontekstsiz bermang. || Не выполняйте merge без контекста.', 'Merge qaysi branchga ta’sir qiladi? || На какую ветку влияет merge?'),
            q('Review tavsifida nima foydali? || Что полезно в описании для ревью?', [
                c('Muammo, yangi xatti-harakat va bajarilgan test || Проблема, новое поведение и выполненный тест', 'Reviewer maqsad va dalilni baholay oladi. || Ревьюер может оценить цель и подтверждение.'),
                c('Faqat “tayyor” || Только «готово»', 'Maqsad va tekshiruv noma’lum. || Цель и проверка неизвестны.'),
                c('Barcha eski commitlarni izohsiz ko‘chirish || Скопировать все старые коммиты без пояснений', 'Joriy o‘zgarishning mazmunini yashiradi. || Скрывает смысл текущего изменения.')],
              'Nima va nima uchun o‘zgarganini yozing.|Tekshiruv dalilini qo‘shing. || Опишите что и почему изменилось.|Добавьте подтверждение проверки.',
              'Tavsif kodni ko‘rish uchun kontekst beradi. || Описание даёт контекст для просмотра кода.', 'Hamkor nimani tekshirishini biladimi? || Знает ли коллега, что проверять?'),
            q('Joriy branch review. git merge main bajarildi. Qaysi branch yangilanishi mumkin? || Текущая ветка review. Выполнили git merge main. Какая ветка может обновиться?', [
                c('review || review', 'Merge joriy branchga boshqa tarixni oladi. || Merge включает другую историю в текущую ветку.'),
                c('main har doim || Всегда main', 'Argument maqsad branchni bildirmaydi. || Аргумент не обозначает целевую ветку.'),
                c('Barcha branchlar || Все ветки', 'Merge barcha ko‘rsatkichlarni yangilamaydi. || Merge не обновляет все указатели.')],
              'Joriy branch review.|main uning ichiga birlashtiriladi. || Текущая ветка review.|main сливается в неё.',
              'Merge argumenti bilan maqsadni adashtirmang. || Не путайте аргумент merge с целью.'),
            q('Merge konfliktsiz o‘tdi. Ikki modul turli birlik kutmoqda. Xulosa? || Merge прошёл без конфликта. Два модуля ожидают разные единицы. Вывод?', [
                c('Matn birlashdi, lekin semantik integratsiya testi kerak || Текст объединился, но нужна проверка смысловой интеграции', 'Git biznes shartnomasini isbotlamaydi. || Git не доказывает бизнес-контракт.'),
                c('Konflikt yo‘qligi barcha talab bajarilganini bildiradi || Отсутствие конфликта означает выполнение всех требований', 'Birlik nomosligi qolishi mumkin. || Несовместимость единиц может остаться.'),
                c('Faqat branchni qayta nomlash yetarli || Достаточно переименовать ветку', 'Birliklar o‘zgarmaydi. || Единицы не изменятся.')],
              'Matn va ma’no mosligini ajrating.|Umumiy oqimni tekshiring. || Разделите совместимость текста и смысла.|Проверьте общий поток.',
              'Git muvaffaqiyati dastur to‘g‘riligi emas. || Успех Git не равен правильности программы.')]),
        l('git-conflict', 'Konflikt va umumiy natija || Конфликт и общий результат',
          'Konfliktni talab bilan hal qilib, integratsiya va himoya dalilini tayyorlaysiz. || Решаете конфликт по требованию и готовите доказательства интеграции и защиты.', [
            'Bir joydagi mos kelmaydigan o‘zgarishlarda Git konfliktni ko‘rsatishi mumkin. <<<<<<<, ======= va >>>>>>> markerlari yakuniy kod emas. Har ikki tomondagi niyatni o‘qib, talabga mos yakuniy variant yoziladi. || При несовместимых изменениях одного места Git может показать конфликт. Маркеры <<<<<<<, ======= и >>>>>>> не являются итоговым кодом. Прочитайте намерения обеих сторон и запишите итог по требованию.',
            'Faqat bir tomonni ko‘r-ko‘rona olish boshqa talabni yo‘qotadi. Markerlarni olib tashlagach sintaksis, shartnoma va umumiy oqim test qilinadi; hal qilingan fayl add qilinadi va merge yakunlanadi. || Слепой выбор одной стороны может потерять другое требование. После удаления маркеров проверяют синтаксис, контракт и общий поток; разрешённый файл добавляют в индекс и завершают merge.',
            'Loyiha himoyasida har ishtirokchi o‘z moduli, interfeysi, bitta xato holati va umumiy natijadagi rolini tushuntiradi. Demo bilan birga test dalillari ko‘rsatiladi; commitlar soni shaxsning hamkorlik qobiliyati bahosi emas. || На защите каждый объясняет свой модуль, интерфейс, один ошибочный случай и роль в общем результате. Вместе с демо показывают тесты; число коммитов не является оценкой способности человека к сотрудничеству.'
          ], 'Bir branch limitni 3, ikkinchisi 5 qildi. Kelishilgan talab: bir o‘quvchiga ko‘pi bilan 4 kitob. Konflikt yechimi? || Одна ветка изменила лимит на 3, другая на 5. Согласованное требование: не более 4 книг на читателя. Решение конфликта?',
          'Ikkala variant talabga mos emas.|Limitni 4 qilib, markerlarni tozalang.|3, 4 va 5 kitob holatlarida talabni tekshiring. || Оба варианта не соответствуют требованию.|Установите лимит 4 и удалите маркеры.|Проверьте случаи 3, 4 и 5 книг по требованию.',
          'Uchinchi, kelishuvga mos variant zarur. || Нужен третий вариант, соответствующий соглашению.', [
            q('Konfliktda birinchi nima qilinadi? || Что делают первым при конфликте?', [
                c('Ikkala o‘zgarish va talabni tushunish || Понять оба изменения и требование', 'Yakuniy kod mazmun bilan tanlanadi. || Итоговый код выбирается по смыслу.'),
                c('Har doim yuqoridagi bo‘lakni olish || Всегда брать верхний фрагмент', 'U boshqa talabni yo‘qotishi mumkin. || Он может потерять другое требование.'),
                c('Faqat marker satrlarini o‘chirib, ikkala kodni qoldirish || Удалить только маркеры, оставив оба фрагмента', 'Takror yoki zid kod qolishi mumkin. || Могут остаться повторы или противоречия.')],
              'Har tomonning niyatini aniqlang.|Yagona mos yechim yozing. || Определите намерение каждой стороны.|Запишите единое подходящее решение.',
              'Konflikt tanlovini joylashuvga bog‘lamang. || Не связывайте выбор с расположением фрагмента.', 'Qaysi talab saqlanishi kerak? || Какое требование нужно сохранить?'),
            q('Markerlar olib tashlandi. Merge tugatishdan oldin nima kerak? || Маркеры удалены. Что нужно до завершения merge?', [
                c('Sintaksis va umumiy test, keyin hal qilingan faylni add qilish || Синтаксис и общие тесты, затем add разрешённого файла', 'Yakuniy fayl tekshiriladi va indeksga olinadi. || Итоговый файл проверяется и добавляется в индекс.'),
                c('Faqat faylni saqlash || Только сохранить файл', 'Test va indeks holati tekshirilmaydi. || Тесты и состояние индекса не проверены.'),
                c('Talabni o‘chirish || Удалить требование', 'To‘g‘rilik mezoni yo‘qoladi. || Исчезает критерий правильности.')],
              'Marker yo‘qligi yetmaydi.|Kod va integratsiyani tekshirib indeksga oling. || Отсутствия маркеров недостаточно.|Проверьте код и интеграцию, добавьте в индекс.',
              'Matn tozaligi mazmun to‘g‘riligini kafolatlamaydi. || Чистый текст не гарантирует правильного смысла.', 'Gitga hal qilingan mazmun qanday beriladi? || Как передать Git разрешённое содержимое?'),
            q('Bir modul testdan o‘tdi, umumiy kitob berish oqimi yiqildi. Nima tekshiriladi? || Один модуль прошёл тест, общий поток выдачи упал. Что проверить?', [
                c('Modullar chegarasidagi kirish/chiqish va holat almashuvi || Вход/выход и переход состояния на границе модулей', 'Integratsiya muammosi shu yerda bo‘lishi mumkin. || Там может находиться причина сбоя интеграции.'),
                c('Faqat alohida modulning ichki testini yana qaytarish || Повторить только внутренний тест отдельного модуля', 'U modul chegarasidagi kelishuvni qamramasligi mumkin. || Он может не покрывать контракт между модулями.'),
                c('Faqat alohida o‘tgan testni ko‘rsatish || Показать только пройденный отдельный тест', 'Umumiy nosozlik qoladi. || Общий сбой останется.')],
              'Modullar qanday ulanayotganini tekshiring.|Umumiy test kirishini qaytaring. || Проверьте соединение модулей.|Повторите вход общего теста.',
              'Alohida muvaffaqiyat umumiy muvaffaqiyat emas. || Отдельный успех не равен общему.'),
            q('Himoyada jamoaning eng foydali dalili? || Самое полезное подтверждение на защите команды?', [
                c('Har a’zo interfeysni tushuntiradi, umumiy oqim va xato holati test bilan ko‘rsatiladi || Каждый объясняет интерфейс, общий поток и ошибочный случай показываются тестом', 'Hissa, tushunish va natija kuzatiladi. || Наблюдаемы вклад, понимание и результат.'),
                c('Faqat eng ko‘p commit qilgan odam gapiradi || Говорит только автор большинства коммитов', 'Boshqalarning tushunishi bilinmaydi. || Понимание остальных неизвестно.'),
                c('Faqat bosh ekran rasmi || Только снимок главного экрана', 'Funksional oqim isbotlanmaydi. || Рабочий поток не подтверждён.')],
              'Natijani qayta ko‘rsatish mumkin bo‘lsin.|Har a’zo o‘z chegarasini tushuntirsin. || Результат должен быть воспроизводим.|Каждый объясняет границу своего модуля.',
              'Ko‘rinishning o‘zi hamkorlik natijasini isbotlamaydi. || Один внешний вид не подтверждает совместный результат.')])
    ])
