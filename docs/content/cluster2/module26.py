from authoring import lesson as l, module, n, s


def build():
    return module('creative-mini-apps', 6,
        'Kreativ dasturlash va kichik ilova dizayni || Креативное программирование и проектирование мини-приложений', ['creative', 'problem_solving'], [
        l('design-needs', 'Foydalanuvchi ehtiyoji va maqsad || Потребность пользователя и цель', [
            'Kreativ yechim foydalanuvchi muammosidan boshlanadi. “Noodatiy” funksiya o‘zi foydali degani emas: kimga, qaysi vaziyatda va qanday yordam berishini tushuntiring. || Креативное решение начинается с проблемы пользователя. «Необычная» функция сама по себе не означает полезность: объясните, кому, в какой ситуации и как она помогает.',
            'Talaba topshiriq muddatini unutsa, eslatma, haftalik taqvim yoki ustuvorlik ro‘yxati turli yechimlar bo‘lishi mumkin. Ularni ehtiyoj va cheklov bo‘yicha taqqoslang. || Если студент забывает сроки заданий, напоминание, недельный календарь или список приоритетов могут быть разными решениями. Сравнивайте их по потребности и ограничениям.',
            '“Talaba vazifani kiritadi, muddatni belgilaydi, kelgusi vazifani ko‘radi” kabi foydalanuvchi ssenariysi funksiyani aniq qiladi. Shaxsiy ma’lumotni faqat zarur bo‘lsa so‘rang. || Сценарий «студент вводит задачу, задаёт срок, видит ближайшую задачу» уточняет функцию. Запрашивайте персональные данные только при необходимости.'
        ], 'Talaba uy vazifalarining muddatini unutadi. Minimal foydali ssenariyni tuzing. || Студент забывает сроки домашних заданий. Постройте минимальный полезный сценарий.',
           'Ehtiyoj — yaqin muddatni bilish.|Vazifa nomi va muddat kiritiladi.|Yaqin vazifalar ro‘yxati ko‘rsatiladi. || Потребность — знать ближайший срок.|Вводятся название задачи и срок.|Показывается список ближайших задач.',
           'Kiritish → muddat → yaqin vazifalar || Ввод → срок → ближайшие задачи', [
            s('Ehtiyoj: talaba muddatni unutadi. Qaysi funksiya bevosita yordam beradi? || Потребность: студент забывает срок. Какая функция помогает непосредственно?', [
                ('Muddat bo‘yicha yaqin vazifalarni ko‘rsatish || Показ ближайших задач по сроку', 'Bu aynan kerakli ma’lumotni ochadi. || Это показывает именно нужную информацию.'),
                ('Har bosishda fon rangini tasodifiy o‘zgartirish || Случайная смена фона при каждом нажатии', 'Bu muddatni eslash muammosini hal qilmaydi. || Это не решает проблему сроков.'),
                ('Vazifa nomini yashirish || Скрыть название задачи', 'Bu kerakli vazifani tanishni qiyinlashtiradi. || Это затрудняет распознавание нужной задачи.')],
              'Funksiyani muammo bilan bog‘lang.|Muddatga oid ko‘rsatish ehtiyojga to‘g‘ri keladi. || Свяжите функцию с проблемой.|Показ сроков соответствует потребности.',
              'Yangilikni foydalilik bilan tenglashtirmang. || Не отождествляйте новизну и полезность.',
              'Qaysi variant foydalanuvchi xatosini kamaytiradi? || Какой вариант уменьшает ошибку пользователя?'),
            s('Oddiy vazifa ro‘yxati uchun qaysi ma’lumot eng zarur? || Какие данные нужнее всего для простого списка задач?', [
                ('Vazifa nomi va bajarilganlik holati || Название задачи и состояние выполнения', 'Bular ro‘yxatning asosiy funksiyasini ta’minlaydi. || Они обеспечивают основную функцию списка.'),
                ('Pasport va bank karta raqami || Номер паспорта и банковской карты', 'Bunday ma’lumot bu vazifa uchun zarur emas. || Эти данные не нужны для этой задачи.'),
                ('Faqat foydalanuvchi sevimli rangi || Только любимый цвет пользователя', 'Bu vazifalarni yuritishga yetmaydi. || Этого недостаточно для учёта задач.')],
              'Har maydonning maqsadini tekshiring.|Nom va holat asosiy ro‘yxat uchun yetarli. || Проверьте цель каждого поля.|Названия и состояния достаточно для основного списка.',
              'Zarur bo‘lmagan ma’lumotni yig‘mang. || Не собирайте ненужные данные.',
              'Funksiya ishlashi uchun aynan nima kerak? || Что именно нужно для работы функции?'),
            s('“Ilova zamonaviy bo‘lsin” talabini qaysi yozuv aniqroq qiladi? || Какая запись уточняет требование «пусть приложение будет современным»?', [
                ('Talaba yangi vazifani kiritib, saqlanganini ko‘ra oladi || Студент может ввести новую задачу и увидеть подтверждение сохранения', 'Tekshiriladigan harakat va natija bor. || Есть проверяемое действие и результат.'),
                ('Juda zo‘r va noyob bo‘lsin || Пусть будет очень крутым и уникальным', 'O‘lchanadigan xatti-harakat yo‘q. || Нет измеримого поведения.'),
                ('Barcha funksiyalar birga bo‘lsin || Пусть будут все функции сразу', 'Qamrov va qabul mezoni noaniq. || Неопределённы объём и критерий приёмки.')],
              'Mavhum sifatni ssenariyga aylantiring.|Harakat va kutilgan natija tekshirilishi mumkin. || Превратите абстрактное качество в сценарий.|Действие и ожидаемый результат можно проверить.',
              'Tekshirib bo‘lmaydigan sifat so‘zlariga suyanmang. || Не опирайтесь на непроверяемые оценочные слова.'),
            s('Internetsiz ishlash talab qilingan. Qaysi g‘oya cheklovga mos? || Требуется работа без интернета. Какая идея соответствует ограничению?', [
                ('Vazifalarni qurilmada saqlab, keyin ko‘rsatish || Хранить задачи на устройстве и показывать их позже', 'Asosiy ssenariy tarmoqsiz bajariladi. || Основной сценарий выполняется без сети.'),
                ('Har ochishda majburiy server javobini kutish || При каждом открытии обязательно ждать ответ сервера', 'Tarmoqsiz asosiy oqim to‘xtaydi. || Без сети основной поток останавливается.'),
                ('Internet yo‘qligida barcha vazifalarni o‘chirish || Удалять все задачи при отсутствии интернета', 'Bu foydalanuvchi ma’lumotini yo‘qotadi. || Это теряет данные пользователя.')],
              'Cheklov tarmoqsiz asosiy ishni talab qiladi.|Mahalliy saqlash shu ssenariyni ta’minlashi mumkin. || Ограничение требует основной работы без сети.|Локальное хранение может обеспечить этот сценарий.',
              'Qiziqarli g‘oya majburiy cheklovni buzmasin. || Интересная идея не должна нарушать обязательное ограничение.')]),
        l('design-functions', 'Funksiyalar va minimal ko‘lam || Функции и минимальный объём', [
            'Kichik ilovani mustaqil vazifalarga ajrating: ma’lumotni olish, tekshirish, saqlash, ko‘rsatish. Har qismda bitta ravshan mas’uliyat bo‘lsin. || Разделите мини-приложение на задачи: получение, проверка, сохранение и показ данных. У каждой части должна быть одна ясная ответственность.',
            'Minimal ishlaydigan nusxa foydalanuvchining bitta muhim ssenariysini oxirigacha bajaradi. Keraksiz statistika yoki bezakdan oldin asosiy saqlash va qayta ko‘rsatishni tugating. || Минимальная рабочая версия выполняет один важный сценарий пользователя до конца. Прежде ненужной статистики или украшений завершите основное сохранение и повторный показ.',
            'Ma’lumot oqimi: INPUT title → VALIDATE title → SAVE task → SHOW list. Tekshirish xato topsa SAVE ga o‘tilmaydi. || Поток данных: INPUT title → VALIDATE title → SAVE task → SHOW list. Если проверка нашла ошибку, перехода к SAVE нет.'
        ], 'Vazifa nomi bo‘sh bo‘lsa saqlanmasin. To‘g‘ri oqimni yozing. || Задача с пустым названием не должна сохраняться. Запишите правильный поток.',
           'Kirish nomi olinadi.|Bo‘shlik tekshiriladi; bo‘lsa xabar va qaytish.|Yaroqli bo‘lsa saqlash va yangilangan ro‘yxat. || Получается введённое название.|Проверяется пустота; при ней сообщение и возврат.|Если допустимо, сохранение и обновлённый список.',
           'Olish → tekshirish → saqlash → ko‘rsatish || Получить → проверить → сохранить → показать', [
            s('Faqat ma’lumotni tekshiradigan qism nima qaytarishi ma’qul? || Что удобно возвращать части, которая только проверяет данные?', [
                ('Yaroqli yoki tuzatish kerakligi haqidagi natija || Результат допустимости или необходимости исправления', 'Tekshirishning mas’uliyati aniq saqlanadi. || Ответственность проверки остаётся ясной.'),
                ('O‘zi yashirin buyurtma yuborishi || Скрыто отправлять заказ самостоятельно', 'Bu tekshirishdan tashqari yon ta’sir. || Это побочный эффект вне проверки.'),
                ('Barcha vazifalarni o‘chirishi || Удалять все задачи', 'Tekshirish bunday o‘chirishni talab qilmaydi. || Проверка не требует такого удаления.')],
              'Tekshiruvchi ma’lumotni baholaydi.|Keyingi amalni boshqaruvchi qism natijadan foydalanadi. || Проверяющая часть оценивает данные.|Управляющая часть использует результат для следующего действия.',
              'Bir qismga bog‘liq bo‘lmagan vazifalarni yig‘mang. || Не собирайте в одной части несвязанные задачи.',
              'Qismning nomi uning haqiqiy vazifasiga mos bo‘lsin. || Название части должно соответствовать её действительной задаче.'),
            s('Minimal vazifa ilovasi uchun birinchi to‘liq oqim qaysi? || Каков первый полный поток минимального приложения задач?', [
                ('Vazifa qo‘shish → ro‘yxatda ko‘rish → bajarilgan deb belgilash || Добавить задачу → увидеть в списке → отметить выполненной', 'Bitta foydali ssenariy oxirigacha ishlaydi. || Один полезный сценарий работает до конца.'),
                ('Faqat fon animatsiyasi || Только анимация фона', 'Asosiy ma’lumot bilan ish yo‘q. || Нет основной работы с данными.'),
                ('Hisob-kitobi yo‘q statistik panel || Статистическая панель без вычислений', 'Bu ishlaydigan asosiy oqim emas. || Это не работающий основной поток.')],
              'Minimal degani faqat tashqi ko‘rinish emas.|Asosiy vazifa hayot sikli bajariladi. || Минимальный не означает только внешний вид.|Выполняется основной жизненный цикл задачи.',
              'Bezakni asosiy funksiyaning o‘rniga qo‘ymang. || Не подменяйте основную функцию украшением.',
              'Talaba vazifasini boshidan oxirigacha bajara oladimi? || Может ли пользователь выполнить задачу от начала до конца?'),
            s('Nom bo‘sh. Qaysi oqim talabga mos? || Название пустое. Какой поток соответствует требованию?', [
                ('VALIDATE → ERROR → INPUT || VALIDATE → ERROR → INPUT', 'Saqlashsiz tuzatish imkoniyati beriladi. || Предоставляется исправление без сохранения.'),
                ('SAVE → VALIDATE → SHOW || SAVE → VALIDATE → SHOW', 'Yaroqsiz vazifa avval saqlanib bo‘lgan. || Недопустимая задача уже сохранена.'),
                ('SAVE → SUCCESS || SAVE → SUCCESS', 'Tekshirish butunlay tashlab ketilgan. || Проверка полностью пропущена.')],
              'Bo‘sh nom talabga mos emas.|Saqlashga o‘tmay kirishga qaytiladi. || Пустое название недопустимо.|Происходит возврат к вводу без сохранения.',
              'Tekshirish saqlashdan avval ishlashi kerak. || Проверка должна работать до сохранения.'),
            n('Ro‘yxatda 4 vazifa bor. Bitta yaroqli yangi vazifa saqlanadi, keyingi bo‘sh nomli so‘rov rad etiladi. Oxirida nechta vazifa? || В списке 4 задачи. Одна новая допустимая задача сохраняется, следующий запрос с пустым названием отклоняется. Сколько задач в конце?', 5,
              'Yaroqli saqlash sonni 4 dan 5 ga oshiradi.|Rad etilgan kirish yangi vazifa yaratmaydi. || Допустимое сохранение увеличивает число с 4 до 5.|Отклонённый ввод не создаёт новой задачи.',
              'Rad etilgan urinishni saqlangan obyekt deb sanamang. || Не считайте отклонённую попытку сохранённым объектом.')], ['design-needs']),
        l('design-states', 'Interfeys holatlari va qayta aloqa || Состояния интерфейса и обратная связь', [
            'Interfeys boshlang‘ich, yuklanish, muvaffaqiyat, bo‘sh va xato holatlarini farqlashi kerak. Bo‘sh ro‘yxat xato emas: hali vazifa yo‘q bo‘lishi mumkin. || Интерфейс должен различать исходное состояние, загрузку, успех, пустоту и ошибку. Пустой список не ошибка: задач ещё может не быть.',
            'Saqlash tugamaguncha “saqlandi” demang. Tugma bloklanishi takroriy bosishni kamaytiradi; natijaning dublikat bo‘lmasligi ma’lumotni saqlash qismida ham ta’minlanadi. || Не говорите «сохранено», пока сохранение не завершилось. Блокировка кнопки уменьшает повторные нажатия; отсутствие дублей обеспечивается и в части сохранения данных.',
            'Xato faqat rang bilan berilmasin: aniq matn va tuzatish yo‘lini ko‘rsating. Klaviaturada foydalanish va fokusning qayerga o‘tishini ham ssenariyga kiriting. || Не обозначайте ошибку только цветом: покажите понятный текст и способ исправления. Добавьте в сценарий использование клавиатуры и перемещение фокуса.'
        ], 'Saqlash so‘rovi davom etmoqda, keyin xato qaytdi. Holatlar ketma-ketligi? || Запрос сохранения выполняется, затем приходит ошибка. Какова последовательность состояний?',
           'Avval SAVING holati.|Xato kelgach ERROR holati va tuzatish/qayta urinish.|Muvaffaqiyat tasdiqlanmagani uchun SUCCESS ko‘rsatilmaydi. || Сначала состояние SAVING.|После ошибки — ERROR и исправление/повтор.|SUCCESS не показывается, потому что успех не подтверждён.',
           'SAVING → ERROR || SAVING → ERROR', [
            s('So‘rov hali tugamadi. Qaysi xabar to‘g‘ri? || Запрос ещё не завершён. Какое сообщение правильно?', [
                ('Saqlanmoqda || Сохранение…', 'Haqiqiy oraliq holat ifodalangan. || Отражено реальное промежуточное состояние.'),
                ('Muvaffaqiyatli saqlandi || Успешно сохранено', 'Muvaffaqiyat hali tasdiqlanmagan. || Успех ещё не подтверждён.'),
                ('Ma’lumot butunlay yo‘qoldi || Данные полностью потеряны', 'Bunday xulosa uchun dalil yo‘q. || Для такого вывода нет данных.')],
              'Jarayon natijasi hali noma’lum.|Yuklanish holatini ko‘rsating. || Результат процесса пока неизвестен.|Покажите состояние загрузки.',
              'Kutilayotgan natijani yakuniy fakt deb ko‘rsatmang. || Не показывайте ожидаемый результат как завершившийся факт.',
              'Hozir qaysi holat tasdiqlangan? || Какое состояние подтверждено сейчас?'),
            s('Faqat qizil ramka bilan xato belgilangan. Qaysi qo‘shimcha foydali? || Ошибка отмечена только красной рамкой. Какое дополнение полезно?', [
                ('Maydon yonida aniq xato va tuzatish matni || Понятный текст ошибки и исправления рядом с полем', 'Ma’no rangga qaram bo‘lib qolmaydi. || Смысл не зависит только от цвета.'),
                ('Matnni ham qizilga yashirish || Скрыть текст красным цветом', 'Tushuntirish yo‘qoladi. || Объяснение исчезает.'),
                ('Xatoni ovozsiz yopish || Молча закрыть ошибку', 'Foydalanuvchi nima bo‘lganini bilmaydi. || Пользователь не понимает, что произошло.')],
              'Rangning o‘zi yetarli ma’no bermaydi.|Matn xato va keyingi qadamni bildiradi. || Один цвет не передаёт достаточного смысла.|Текст указывает ошибку и следующий шаг.',
              'Ko‘rinishni o‘zgartirishni tushuntirish o‘rniga ishlatmang. || Не используйте изменение вида вместо объяснения.',
              'Rang ajratilmasa ham xabar tushunarli bo‘lsin. || Сообщение должно быть понятно и без различения цвета.'),
            s('Ro‘yxat muvaffaqiyatli yuklandi, lekin unda vazifa yo‘q. Qaysi holat? || Список успешно загружен, но задач нет. Какое это состояние?', [
                ('Bo‘sh holat va vazifa qo‘shish taklifi || Пустое состояние с предложением добавить задачу', 'So‘rov muvaffaqiyatli, ma’lumot esa bo‘sh. || Запрос успешен, а данные пусты.'),
                ('Server xatosi deb ko‘rsatish || Показать как ошибку сервера', 'Bunga asos yo‘q. || Оснований для этого нет.'),
                ('Cheksiz yuklanish || Бесконечная загрузка', 'So‘rov allaqachon tugagan. || Запрос уже завершён.')],
              'Yuklanish tugaganini ajrating.|Bo‘sh natija alohida, tushunarli holat bo‘ladi. || Отметьте завершение загрузки.|Пустой результат — отдельное понятное состояние.',
              'Bo‘sh natijani texnik xato bilan aralashtirmang. || Не путайте пустой результат и техническую ошибку.'),
            s('Saqlash xato qaytardi. Qaysi holat o‘tishi mos? || Сохранение вернуло ошибку. Какой переход состояний подходит?', [
                ('SAVING → ERROR, kirish saqlanib qayta urinish taklif qilinadi || SAVING → ERROR, ввод сохранён и предложен повтор', 'Kiritilgan ish yo‘qolmasdan xato ko‘rsatiladi. || Ошибка показывается без потери введённой работы.'),
                ('SAVING → SUCCESS, xato yashiriladi || SAVING → SUCCESS, ошибка скрывается', 'Bu natijani yolg‘on tasdiqlaydi. || Это ложно подтверждает результат.'),
                ('SAVING → barcha ma’lumotni o‘chirish || SAVING → удаление всех данных', 'Bunday yon ta’sir talab qilinmagan. || Такой побочный эффект не требовался.')],
              'Xato natijasi ERROR ni tanlaydi.|Foydalanuvchi ishini saqlab, qayta urinish yo‘li beriladi. || Ошибочный результат выбирает ERROR.|Работа пользователя сохраняется, предоставляется повтор.',
              'Muvaffaqiyatsiz so‘rovni tayyor natija deb ko‘rsatmang. || Не показывайте неуспешный запрос как готовый результат.')], ['design-functions']),
        l('design-alternatives', 'G‘oyalarni mezon bilan taqqoslash || Сравнение идей по критериям', [
            'Bir ehtiyoj uchun bir nechta g‘oya yozing, keyin foydalilik, bajarish murakkabligi va cheklovlarga moslik bilan taqqoslang. Avval yozilgan g‘oya avtomatik g‘olib emas. || Запишите несколько идей для одной потребности, затем сравните по полезности, сложности реализации и ограничениям. Первая записанная идея не становится победителем автоматически.',
            'Baholash jadvali tanlovni ochiq qiladi, lekin ballar mezon va vaznlarga bog‘liq. Masalan, internetsiz ishlash majburiy bo‘lsa bu talabni ball yig‘indisi bilan chetlab bo‘lmaydi. || Таблица оценки делает выбор прозрачным, но баллы зависят от критериев и весов. Например, обязательную работу без интернета нельзя обойти суммой баллов.',
            'Ushbu yopiq savollar berilgan mezonga mos qarorni tekshiradi. Ular erkin ijodiy mahsulotning noyobligi yoki insonning umumiy kreativlik darajasiga ball qo‘ymaydi. || Закрытые вопросы проверяют решение по заданному критерию. Они не оценивают уникальность свободного творческого продукта или общую креативность человека.'
        ], 'A g‘oya: foydalilik 4, soddalik 3. B: foydalilik 3, soddalik 5. Vaznlar teng, katta jami afzal. Qaysi tanlanadi? || Идея A: полезность 4, простота 3. B: полезность 3, простота 5. Веса равны, большая сумма предпочтительнее. Что выбрать?',
           'A jami 4 + 3 = 7.|B jami 3 + 5 = 8.|Berilgan mezonda B ustun. || A всего: 4 + 3 = 7.|B всего: 3 + 5 = 8.|По заданному критерию выигрывает B.', 'B || B', [
            n('G‘oya uchun foydalilik 5, soddalik 3. Baho = 2 × foydalilik + soddalik. Baho? || Для идеи полезность 5, простота 3. Оценка = 2 × полезность + простота. Какова оценка?', 13,
              'Foydalilik vazni bilan 2 × 5 = 10.|10 + 3 = 13. || С весом полезности: 2 × 5 = 10.|10 + 3 = 13.',
              'Vaznni barcha mezonlarga bir xil qo‘llamang. || Не применяйте вес одинаково ко всем критериям.',
              'Har mezonning koeffitsiyentini alohida tekshiring. || Отдельно проверьте коэффициент каждого критерия.'),
            s('Majburiy talab: internetsiz ishlash. A balli yuqori, lekin tarmoqqa bog‘liq. B balli pastroq, lekin talabga mos. Qaror? || Обязательное требование: работа без интернета. У A балл выше, но нужна сеть. У B ниже, но требование выполнено. Каково решение?', [
                ('Talabga mos B ni tanlash yoki A ni qayta ishlab chiqish || Выбрать соответствующий B или переработать A', 'Majburiy talab ustuvor. || Обязательное требование имеет приоритет.'),
                ('Faqat yuqori jami uchun A ni tanlash || Выбрать A только за большую сумму', 'Ball majburiy cheklovni bekor qilmaydi. || Балл не отменяет обязательное ограничение.'),
                ('Talabni foydalanuvchidan yashirish || Скрыть требование от пользователя', 'Bu kelishilgan shartni buzadi. || Это нарушает согласованное условие.')],
              'Avval nomos variantlar ajratiladi.|Keyin mos variantlar ball bilan solishtiriladi. || Сначала исключаются несоответствующие варианты.|Затем допустимые сравниваются по баллам.',
              'Mezon ballari bilan majburiy talabni farqlang. || Различайте баллы критериев и обязательное требование.',
              'Ushbu talab bajarilmasa asosiy ssenariy ishlaydimi? || Работает ли основной сценарий без выполнения этого требования?'),
            s('Ikki g‘oya berilgan barcha mezonda teng. Qaysi xulosa asosli? || Две идеи равны по всем заданным критериям. Какой вывод обоснован?', [
                ('Qo‘shimcha mezon yoki kichik foydalanuvchi sinovi kerak || Нужен дополнительный критерий или небольшой пользовательский тест', 'Mavjud jadval yagona tanlov bermaydi. || Текущая таблица не даёт единственного выбора.'),
                ('Birinchi g‘oya ilmiy jihatdan ustun || Первая идея научно превосходит другую', 'Tartib ustunlik dalili emas. || Порядок не является доказательством превосходства.'),
                ('Ikkalasi mutlaqo foydasiz || Обе совершенно бесполезны', 'Tenglik foydasizlikni bildirmaydi. || Равенство не означает бесполезности.')],
              'Berilgan mezonlar farq ko‘rsatmadi.|Yangi dalil bilan tanlov aniqlashtiriladi. || Заданные критерии не показали различия.|Выбор уточняется новыми данными.',
              'Teng natijadan uydirma g‘olib chiqarmang. || Не выводите вымышленного победителя из равенства.'),
            n('A: foydalilik 4, soddalik 2. B: foydalilik 3, soddalik 5. Baho = 2 × foydalilik + soddalik. B bahosi A dan nechaga katta? || A: полезность 4, простота 2. B: полезность 3, простота 5. Оценка = 2 × полезность + простота. На сколько оценка B больше A?', 1,
              'A = 2 × 4 + 2 = 10.|B = 2 × 3 + 5 = 11; farq 1. || A = 2 × 4 + 2 = 10.|B = 2 × 3 + 5 = 11; разность 1.',
              'Jami ball o‘rniga so‘ralgan farqni qaytaring. || Возвращайте запрошенную разность, а не общий балл.')], ['design-needs', 'opt-choice']),
        l('design-prototype', 'Prototip va tekshirish rejasi || Прототип и план проверки', [
            'Prototip g‘oyani tekshirish uchun eng sodda namuna: qog‘oz ekranlar, bosiladigan maket yoki kichik ishlaydigan qism. Unda qaysi taxmin tekshirilishi oldindan yoziladi. || Прототип — простейший образец для проверки идеи: бумажные экраны, кликабельный макет или небольшая работающая часть. Заранее записывается проверяемое предположение.',
            'Sinovda foydalanuvchiga vazifa bering, masalan yangi vazifani kiritib bajarilganini belgilang. Qayerda to‘xtagani, adashgani va natijani tushunganini kuzating; oldindan barcha bosishlarni aytib bermang. || В тесте дайте пользователю задачу, например добавить новую задачу и отметить выполненной. Наблюдайте остановки, ошибки и понимание результата; не подсказывайте заранее все нажатия.',
            'Kuzatuvdan keyin bitta muammoni tanlab o‘zgartiring va yana tekshiring. Ochiq miniloyihalarda mustaqil tekshiruv mezonlari ishlatiladi; o‘zini tekshirish platformadagi avtomatik tekshiruv natijasi o‘rniga o‘tmaydi. || После наблюдения выберите одну проблему, измените решение и проверьте снова. В открытых мини-проектах используются критерии самопроверки; самопроверка не заменяет результат автоматической проверки платформы.'
        ], 'Foydalanuvchi “saqlash” tugmasini topolmadi. Keyingi kichik tajriba? || Пользователь не нашёл кнопку сохранения. Каков следующий небольшой эксперимент?',
           'Kuzatuv: tugma topilmayapti.|Yorliq va joylashuvni ravshanlashtiring.|Xuddi shu vazifa bilan qayta sinang. || Наблюдение: кнопка не находится.|Уточните подпись и расположение.|Повторите тест с той же задачей.',
           'Kuzatish → o‘zgartirish → qayta tekshirish || Наблюдение → изменение → повторная проверка', [
            s('Sinov maqsadi: vazifa qo‘shish tushunarliligini bilish. Qaysi topshiriq mos? || Цель теста: проверить понятность добавления задачи. Какое задание подходит?', [
                ('Ertangi topshirig‘ingizni ro‘yxatga kiriting || Добавьте завтрашнее задание в список', 'Bu haqiqiy foydalanuvchi ssenariysini bajaradi. || Это выполняет реальный пользовательский сценарий.'),
                ('Men aytgan barcha tugmalarni bosib chiqing || Нажмите все кнопки, которые я назову', 'Ko‘rsatma mustaqil topish qiyinligini yashiradi. || Подсказка скрывает трудность самостоятельного поиска.'),
                ('Faqat ekran rangini ayting || Назовите только цвет экрана', 'Qo‘shish oqimi tekshirilmaydi. || Поток добавления не проверяется.')],
              'Vazifa maqsadni bajarishga yo‘naltiriladi.|Bosish ketma-ketligini oldindan ko‘rsatmasdan kuzating. || Задание направлено на выполнение цели.|Наблюдайте, не указывая заранее последовательность нажатий.',
              'Mustaqil foydalanish sinovini yo‘riqnoma bajarishga aylantirmang. || Не превращайте тест самостоятельного использования в выполнение инструкции.',
              'Sinov foydalanuvchi o‘zi nima topishini ko‘rsatsin. || Тест должен показывать, что пользователь находит самостоятельно.'),
            s('Bitta foydalanuvchi tugmani topmadi. Qaysi xulosa ehtiyotkor va foydali? || Один пользователь не нашёл кнопку. Какой вывод осторожен и полезен?', [
                ('Tugma topilishida muammo bo‘lishi mumkin; o‘zgartirib qayta tekshirish kerak || Возможна проблема обнаружения кнопки; нужно изменить и проверить снова', 'Kuzatuv muammoni ko‘rsatadi, umumiy hukm bermaydi. || Наблюдение указывает на проблему, но не даёт всеобщего вывода.'),
                ('Hech kim bu ilovadan foydalana olmaydi || Никто не может пользоваться этим приложением', 'Bitta kuzatuv bunday umumiy hukmni bermaydi. || Одно наблюдение не даёт такого общего вывода.'),
                ('Foydalanuvchini ayblab sinovni tugatish || Обвинить пользователя и прекратить тест', 'Bu dizaynni yaxshilashga dalilni ishlatmaydi. || Это не использует данные для улучшения дизайна.')],
              'Muammo aniq ssenariyda kuzatildi.|Taxminni kichik o‘zgarish va qayta sinov bilan tekshiring. || Проблема наблюдалась в конкретном сценарии.|Проверьте предположение небольшим изменением и повторным тестом.',
              'Kichik kuzatuvdan barcha foydalanuvchiga hukm chiqarmang. || Не делайте вывод обо всех пользователях из малого наблюдения.',
              'Kuzatuv va umumlashtirish orasini ajrating. || Разделяйте наблюдение и обобщение.'),
            s('Qog‘oz prototipi nimani yaxshi tekshiradi? || Что хорошо проверяет бумажный прототип?', [
                ('Ekranlar ketma-ketligi va yozuvlarning tushunarliligini || Порядок экранов и понятность подписей', 'Buning uchun haqiqiy server shart emas. || Для этого не нужен реальный сервер.'),
                ('Serverning aniq sekunddagi tezligini || Точную скорость сервера в секундах', 'Qog‘ozda server ishlamaydi. || На бумаге сервер не выполняется.'),
                ('Ma’lumotlar bazasi parallel tranzaksiyalarini || Параллельные транзакции базы данных', 'Bular ishlaydigan tizim sinovini talab qiladi. || Это требует проверки работающей системы.')],
              'Prototipning tekshira oladigan qatlamini belgilang.|Qog‘oz ekranlar oqim va matnni sinaydi. || Определите слой, который способен проверить прототип.|Бумажные экраны проверяют поток и текст.',
              'Prototip turidan tashqaridagi xususiyatni isbotlangan demang. || Не считайте доказанным свойство вне возможностей типа прототипа.'),
            s('Tugma yorlig‘i o‘zgartirildi. Yaxshilanishni qanday tekshirish kerak? || Подпись кнопки изменена. Как проверить улучшение?', [
                ('Bir xil vazifani qayta berib topish va xatolarni kuzatish || Повторить ту же задачу и наблюдать поиск и ошибки', 'Oldingi muammo bilan bog‘langan dalil olinadi. || Получаются данные, связанные с прежней проблемой.'),
                ('Faqat muallifga chiroyli ko‘rinishi yetarli || Достаточно, что автору красиво', 'Bu foydalanuvchining tushunishini tekshirmaydi. || Это не проверяет понимание пользователя.'),
                ('Barcha boshqa funksiyani o‘chirib tashlash || Удалить все остальные функции', 'Bu faqat yorliq ta’sirini ajratmaydi. || Это не выделяет эффект одной подписи.')],
              'Bir muammodagi o‘zgarishni tekshiring.|Shu ssenariyda yangi kuzatuv bilan solishtiring. || Проверяйте изменение одной проблемы.|Сравните с новым наблюдением в том же сценарии.',
              'O‘zgartirishning o‘zi foyda isboti emas. || Само изменение не доказывает пользу.')], ['design-states', 'design-alternatives'])])
