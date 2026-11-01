# III klaster uchun o‘quv resurslari loyihasi

Sana: 2026-11-01. Holat: foydalanuvchi yechimni tasdiqladi; resurslar tayyorlandi va offline tekshiruvdan o‘tdi. [Yakuniy hisobot](cluster3-resources-summary.md). Quyidagi matn tasdiqlangan loyiha qarorlarini qayd etadi.

## Maqsad va manba

III klaster — Shaxsiy-psixologik blok uchun II klasterdagi chuqurlik va ikki tilli tuzilmani saqlagan o‘quv resurslarini tayyorlash. Foydalanuvchi so‘rovi resurslarni tayyorlashga qaratilgan; platformaga integratsiya va jonli chiqarish alohida ish hisoblanadi.

Asosiy manba: `D:/Downloads/Telegram Desktop/Oqitish moduli.docx`. SHA-256: `c11956549286d3f6c99ae327b0dc0ee6dcdc4714e4e069d385901f0f8d58a473`. Hujjat o‘quv dasturi manbasi sifatida o‘qildi; undagi metodik ko‘rsatmalar yordamchiga berilgan amaliy buyruq sifatida qabul qilinmadi. Original fayl o‘zgartirilmadi.

Manbada III klasterda aynan to‘rtta mini-modul bor. II klasterdagi olti modul sonini takrorlash uchun qo‘shimcha mavzu ixtiro qilinmaydi. Sabr va qat’iyat debugging jarayonida; diqqat va aniqlik review jarayonida; hamkorlik guruh loyihasida; yangi bilimni qo‘llash hujjat asosidagi topshiriqlarda mashq qilinadi.

## II klasterdagi sifat namunasi

`docs/content/cluster2/` ichidagi mualliflik manbalari, o‘qituvchi Markdown nusxalari, canonical JSONlar, ruscha locale, build va verification vositalari ko‘rib chiqildi. Har modulda besh mikroko‘nikma, besh dars, besh ishlangan misol, o‘nta yordamli mashq, beshta boshlang‘ich va beshta yakuniy topshiriq mavjud. Har bir ko‘nikmaga 2 practice / 1 precheck / 1 postcheck ajratilgan. Savollarda javob kaliti, yechim bosqichlari va xato izohi; tanlovli savollarda har bir variantning izohi mavjud. Yordam faqat mashq bosqichiga tegishli.

III klasterda ushbu sifat mezoni saqlanadi: jami 20 mikroko‘nikma, 20 dars, 20 ishlangan misol va 80 mustaqil topshiriq. Barchasi UZ/RU. Tarjima qo‘shimcha mustaqil savol hisoblanmaydi.

## Yondashuvlar

1. **Tavsiya etiladi: ikki tilli to‘liq resurslar to‘plami.** O‘qishga qulay Markdown, strukturali draft JSON, ruscha locale, amaliy yo‘riqnomalar va qayta bajariladigan kontent tekshiruvi. II klaster namunasi bilan mos va keyingi integratsiya uchun aniq asos beradi.
2. **Faqat o‘qish matnlari.** Tayyorlash osonroq, ammo savol banki, tekshirish kalitlari va platformaga topshirish tuzilmasi yetishmaydi.
3. **Darhol interaktiv kod muhiti va Git hamkorligi.** Haqiqiy kod topshirish imkonini beradi, biroq resurs tayyorlashdan tashqari bajarish muhiti, repozitoriy boshqaruvi va baholash infratuzilmasini talab qiladi. Hozirgi so‘rov doirasida tavsiya etilmaydi.

## Mavzular va mikroko‘nikmalar xaritasi

| Modul | O‘zbekcha nom | Ruscha nom | Beshta mikroko‘nikma |
|---|---|---|---|
| 3.1 | Kod tahlili va debugging | Анализ кода и отладка | Sintaksis, bajarilish va mantiqiy xatoni ajratish; xatoni qayta hosil qilish va minimal misol; qiymatlar izini va tracebackni o‘qish; breakpoint va qadam bilan kuzatish; chegaraviy test, minimal tuzatish va regressiya |
| 3.2 | Kichik guruh loyihasi va Git | Командный мини-проект и Git | Vazifa va modul shartnomalarini taqsimlash; driver/navigator va rol almashish; working tree, staging va commit; branch, diff, review va merge; konfliktni mazmun bilan hal qilish, integratsiya va natijani himoya qilish |
| 3.3 | Diqqat va aniqlik uchun code review | Внимательность и точность при ревью кода | Talab va o‘zgarish diffini solishtirish; nom, operator va blok xatolarini aniqlash; chegaraviy holat va invariant; aniq, hurmatli va dalilli izoh; tuzatishni qayta tekshirish va review ro‘yxati |
| 3.4 | Hujjatlar asosida yangi bilimni o‘zlashtirish | Освоение нового по документации | Savol, versiya va ishonchli bo‘limni topish; funksiya imzosi, parametr va qaytish qiymati; minimal ishlaydigan misol; cheklov, xato va moslikni tekshirish; yangi vaziyatga ko‘chirish va qisqa bilim qaydi |

3.1 dagi debugging mavjud nosozlik sababini topish jarayonini o‘rgatadi. 3.3 dagi review talab va o‘zgarishni dalil bilan tekshirishga urg‘u beradi. Bir xil savollar ikkala modulda takrorlanmaydi.

## Kod va o‘quv darajasi

II klasterdan kelgan o‘quvchi uchun qisqa UZ/RU ko‘prik qo‘llanma beriladi: psevdokoddan Python 3 ga o‘tish, qiymat berish va taqqoslash, ikki nuqta va chekinish, `range`ning yuqori chegarasi, nol indeks, funksiya va qaytish qiymati. Har snippet tilini aniq ko‘rsatadi. Python misolida nuqtali vergulni majburiy sintaksis deb o‘rgatish mumkin emas.

Kodlar kichik, deterministik va ko‘rsatilgan kirish qiymatlariga ega bo‘ladi. Xato ataylab kiritilgan snippet alohida belgilanadi. Natija topshirig‘ida istisno yuz bersa, uni sonli javobga aylantirish o‘rniga xato turi va sababini tanlash ishlatiladi. O‘quvchiga oldindan kutubxona yoki professional IDE bilimini yuklamaslik kerak.

Debugger misollarida pauza qilingan satr hali bajarilmaganmi yoki bajarilganmi aniq yoziladi. Git misollarida joriy branch, fayl holati va mahalliy/masofaviy holat aytiladi. `commit` va `push`, matn konflikti va mantiqiy integratsiya xatosi ajratiladi.

## Har bir darsning tuzilishi

1. Kuzatiladigan o‘quv natijasi va zarur oldingi bilim.
2. Aniq nazariya, kichik kod yoki vaziyat va amaliy ma’nosi.
3. Kirish, kutilgan natija, qadamli yechim va yakuniy javobli namuna.
4. Tayyor iz yoki skelet va ishora bilan birinchi mashq.
5. Kamroq yordam bilan mustaqilroq ikkinchi mashq.
6. Mazkur ko‘nikmani tekshiradigan boshqa vaziyatli precheck va postcheck.
7. Keng tarqalgan xato, uning sababi va qisqa o‘zini tekshirish.

Precheck va postcheck darsdagi misolni yoki bir-birini aynan takrorlamaydi. Yordamli mashqdagi javobni eslab qolishning o‘zi yakuniy topshiriqni yechishga yetmasligi kerak. Variantlar bir ma’noli, chalg‘ituvchilar esa aniq xato fikrga bog‘langan bo‘ladi.

## Qo‘shimcha amaliy resurslar

**Debugging challenge.** Uch bosqichli bitta mashg‘ulot: sintaksis, mantiqiy va chegaraviy nosozlik. Har bosqichda xatoni qayta hosil qilish, gipoteza, bitta o‘zgarish, qayta sinash va regressiya qaydi. O‘qituvchi yechimi va o‘quvchi ish varag‘i ajratiladi. Qayta urinish uchun yangi kuzatuvni yozish talab qilinadi.

**2–3 kishilik kutubxona miniloyihasi.** Katalog, kitob berish/qaytarish va integratsiya vazifalari; ikki kishi bo‘lsa integratsiya birgalikda. Umumiy ma’lumot va funksiya shartnomasi, rollar almashishi, kichik branch/commitlar, review, oldindan tayyorlangan konflikt, umumiy test va qisqa himoya. Har a’zoning hissasi va yakuniy ishlaydigan oqim uchun rubrika beriladi.

**Hujjatdan o‘rganish laboratoriyasi.** Tashqi tarmoqqa bog‘liq bo‘lmagan, mualliflik mini-API hujjati va uning versiyasi beriladi. O‘quvchi undan to‘g‘ri parametr, qaytish qiymati, xato holati va yangi vaziyat uchun foydalanish yo‘lini topadi. Hujjat ichidagi ko‘rsatmalar o‘quv topshirig‘ining ma’lumoti bo‘ladi. Rasmiy Python hujjatidan foydalanish bo‘yicha alohida kichik amaliy mashq ham beriladi.

Har bir ochiq amaliy ishda maqsad, zarur vositalar, bosqichlar, topshiriladigan dalillar, o‘qituvchi/o‘zini tekshirish rubrikasi va namunaviy natija bo‘ladi. Ular 80 avtomatik topshiriq soniga qo‘shilmaydi.

## Baholashning mazmuni

Savollar kursdagi bilim va qarorlarni tekshiradi. Ular jamoada ishlash qobiliyati, sabr yoki shaxs xususiyatini bevosita o‘lchagan deb ko‘rsatilmaydi. Jamoaviy ish amaliy dalillar va rubrika bilan ko‘rib chiqiladi. Tez o‘rganish modulida avval aniqlik va yangi vaziyatga qo‘llash tekshiriladi; tezlik bo‘yicha majburiy cheklov yoki shaxslarni taqqoslash kiritilmaydi.

Aniq diagnostika savollariga moslik tasdiqlanmagan ekan, uydirma bog‘lanish yoki diagnostika ballariga yozuv yaratilmaydi. Indikatorlarning texnik identifikatorlari keyingi integratsiyada loyihadagi haqiqiy kalitlar bilan tekshiriladi.

## Fayllar va texnik topshirish

Taklif etilayotgan joy: `docs/content/cluster3/`.

- `3.1-mavzu.uz.md`–`3.4-mavzu.uz.md` va mos `.ru.md` o‘qituvchi nusxalari.
- Kod/Git terminlari va Python ko‘prigi uchun UZ/RU qo‘llanma.
- Alohida o‘quvchi ish varaqlari va o‘qituvchi kalitlari bilan uch amaliy yo‘riqnoma.
- Har modulning strukturali draft JSONi va ruscha locale nusxasi.
- Qayta yaratish manbalari, manba/hash manifesti, inventory, tekshirish vositasi va natijasi.
- Barcha resurslarga havolali README va tahririy tekshiruv qaydi.

Muhim mavjud cheklov: backenddagi schema 2 validatori aynan `cluster=2`ni, oltita mavzu tartibini va II klaster indikatorlarini qabul qiladi. `bundled_contents` ham faqat I/II klasterni taniydi. Shuning uchun III klaster draft banki amaldagi importerga tayyor yoki importdan o‘tgan deb ko‘rsatilmaydi. Draft format, versiya va integratsiyaga zarur o‘zgarishlar ochiq hujjatlashtiriladi; ishlashi isbotlanmagan schema raqami ishlab turgan format sifatida taqdim etilmaydi.

Resurs tayyorlash doirasida backend/frontend kodi, ma’lumotlar bazasi yoki production o‘zgartirilmaydi. Ishchi daraxtdagi avvaldan mavjud `.gitignore`, settings, Render va recovery fayllari bu ishga aralashtirilmaydi.

## Qabul va tekshirish mezonlari

- To‘rtta modulning har birida 5 ko‘nikma, 5 dars, 5 namuna, 10 practice, 5 precheck va 5 postcheck.
- Barcha matn, variant, izoh, ishora, amaliy yo‘riqnoma va rubrika UZ/RU bo‘yicha to‘liq.
- Har savolning kaliti mustaqil yechish bilan, Python izlari zarur bo‘lsa cheklangan ishonchli reference dastur bilan tekshiriladi. Git holatlari zarur bo‘lsa alohida vaqtinchalik repozitoriyda tekshiriladi.
- Ikki tildagi kod, konstantalar, option IDlar, javob kalitlari va qadamlar mosligi tekshiriladi.
- Pre/post alohidaligi, 2/1/1 qamrov, kalitlar yagonaligi, prerequisite grafigi va manba hashlari tekshiriladi.
- Yetishmaydigan tarjima, buzilgan kalit/hash, noaniq variant va noto‘g‘ri qamrov kabi salbiy holatlar tekshiruvchi tomonidan aniqlanishi kerak.
- O‘quvchi nusxalarida o‘qituvchi javoblari chiqmasligi tekshiriladi. O‘qituvchi nusxalari to‘liq student API payloadi sifatida ishlatilmaydi.
- Yakuniy hisobot resurslar soni, tekshirish natijalari va integratsiyaga qolgan ishni aniq ajratadi.

## Tekshirilgan qo‘shimcha manbalar

2026-11-01 kuni rasmiy manbalar ochib ko‘rildi. Ular mazmunni tekshirish va qo‘shimcha o‘qish uchun; dars va test banklari yangi mualliflik materiali bo‘ladi.

- [Python Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html) — sintaksis va bajarilish xatolari, traceback.
- [Python pdb](https://docs.python.org/3/library/pdb.html) — breakpoint va qadamli debugging.
- [Pro Git Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging) — branch, merge va konflikt.
- [Google Engineering Practices What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) — talab, funksionallik va chegaraviy holatlarni ko‘rib chiqish.

## Loyiha tekshiruvi

Manbadagi barcha to‘rtta mavzu xaritaga kiritildi. Resurslar hajmi II klasterdagi har modul chuqurligiga mos. Debugging va code review vazifalari farqlangan; ochiq amaliy ish va avtomatik bilim tekshiruvi ajratilgan. Keyingi integratsiya ehtiyoji va mavjud importer cheklovi aniq qayd etilgan. Loyiha tasdiqlandi va resurslar muallifligi tugallandi. Foydalanuvchi keyingi aniqlashtirishda hozircha faqat resurslarni yakunlashni tanladi; integratsiya va deploy bajarilmadi.
