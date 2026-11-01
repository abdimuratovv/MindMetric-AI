# III klaster tahririy tekshiruvi

Sana: 2026-11-01. Bu muallifning ichki mazmun va til tekshiruvi; tashqi metodist ekspertizasi yoki psixometrik kalibrlash emas.

## Manba va qamrov

Foydalanuvchi hujjatidagi to‘rtta mavzu alohida modulga moslandi. Sabr/qat’iyat debugging jarayonidagi gipoteza va qayta sinash orqali, hamkorlik umumiy loyiha orqali, aniqlik review orqali, yangi bilimni qo‘llash hujjat laboratoriyasi orqali mashq qilinadi. Kurs natijalari shaxs xususiyatining diagnostik o‘lchovi deb taqdim etilmaydi.

| Modul | Mazmunni ko‘rib chiqish | Tekshirilgan muhim farqlar |
|---|---|---|
| 3.1 | Xato turi, qayta hosil qilish, iz, traceback, debugger va regressiya | SyntaxError/NameError/mantiqiy xato; bajarilmagan breakpoint satri; eski va yangi qiymat; >= chegarasi; sabab va simptom |
| 3.2 | Shartnoma, pair programming, staging, branch/merge va konflikt | Commit/push; working tree/index/HEAD; merge joriy branchga; matn va semantika; hissa va commitlar soni |
| 3.3 | Talab/diff, identifikator, blok, invariant, review izohi va qayta tekshirish | Python uchun ; majburiy emas; total/tota1; sikl ichidagi print; manfiy maksimum; rad javobida holat saqlanishi |
| 3.4 | Kerakli bo‘lim, versiya, imzo, minimal misol, cheklov va ko‘chirish | Sukut/aniq parametr; limit/uzunlik; indeks/qiymat; 0/None; 1.0 va simulyatsiyadagi 2.0; API va ommaviy paket |

20 darsning har birida aniq o‘quv natijasi, uch nazariy paragraf va qadamli namuna bor. Misollarning kirish va natijalari matn bilan birga solishtirildi. 80 topshiriq 40 practice, 20 precheck va 20 postcheckga bo‘lingan. Tarjima yangi mustaqil savol hisoblanmaydi.

## Javob va variantlar tekshiruvi

68 tanlovli savolning to‘g‘ri javobi va uchala variantiga berilgan izohlar mazmunan ko‘rib chiqildi. Variantlar aniq berilgan talabga nisbatan baholandi; javob pozitsiyasi avtomatik aylantiriladi. Dastur aylantirishdan keyingi kalitning muallif belgilagan javobga mosligini tekshiradi. Bu avtomatik semantik isbot emas.

12 sonli javob mualliflik bankidagi kalitlardan alohida yozilgan reference hisoblar bilan tekshiriladi. Darsdagi kod va savol matnlari eval qilinmaydi. Ishonchli lokal reference kodlar va ularning oldindan belgilangan testlari bajariladi.

Dastlabki tahrirdagi ayrim mavzuga aloqasiz chalg‘ituvchilar o‘rniga keng tarqalgan tushunmovchiliklar kiritildi: bir xil int turi birlik mosligini kafolatlaydi deb olish; commit tavsifini diff o‘rniga qabul qilish; alohida modul testini integratsiya isboti deb olish; rad xabari to‘g‘ri bo‘lsa holat ham saqlangan deb o‘ylash. Savollar statistik kalibrlangan yoki pre/post qiyinligi tenglashtirilgan deb ko‘rsatilmaydi.

## Amaliy ishlar

- Debugging starterda ataylab sintaksis xatosi saqlandi; keyingi bosqichlarda mantiqiy va chegara xatosi bor. O‘qituvchi yechimi alohida. Chegirma validatsiyasi berilgan old shartlar tashqarisiga kengaytirilmaydi.
- Kutubxona loyihasida aniq shartnoma, ikki va uch kishilik rollar, kuzatiladigan review, konflikt simulyatsiyasi, rad holati va saqlanish invarianti bor. Lokal namuna bitta jarayon uchun; real ko‘p foydalanuvchili xizmat sifatida berilmaydi.
- StudyTools hujjati to‘liq topshiriq ichida berilgan; manfiy limit, bool, indeks 0, sayoz nusxa va versiya farqi ochiq yozilgan. Rasmiy str.split misoli ham alohida tekshiriladi.

Har amaliy ishda to‘rtta 0–2 mezonli rubrika bor. Maksimum 8 ish sifati uchun; psixologik ball emas. O‘quvchi va o‘qituvchi nusxalari alohida yaratiladi. Kutubxona demo kodi va debugging reference fayli o‘qituvchi resurslari sifatida ko‘rsatilgan.

## Til va foydalanish

UZ/RU bo‘yicha dars, namuna, savol, variant, ishora, xato izohi, amaliy yo‘riqnoma, rubrika va o‘qituvchi yechimi mavjud. Kod va identifikatorlar aynan saqlangan. Tarjimadagi bir gapda Python versiyasi natija ifodasidan keyin kelgan edi; avtomatik sonlar mosligi uchun gap tartibi moslashtirildi.

O‘quvchi nusxasi nazariya, namuna va yordamli mashqlarni beradi; tekshiruv varag‘i alohida. Tekshiruvdagi pre/post savollar bir faylda belgilangan: ularni kerakli bosqichda berish o‘qituvchi yoki mustaqil o‘quvchi zimmasida. Bu offline tarqatish usuli, platforma ruxsat nazorati emas. To‘liq JSON va activities JSON o‘qituvchi javoblarini saqlaydi, ulardan to‘liq student payloadi sifatida foydalanilmaydi.

## Dalil va cheklov

[verify_resources.py](verify_resources.py) qamrov, tarjima, kod/sonlar, kalit, hash, prerequisite, blueprint va hosil qilingan nusxalarni tekshiradi. O‘quvchi savol bo‘limlarida kalit/feedback, tekshiruvlarda ishora/yechim chiqmasligi ham tekshiriladi. Lokal Git repozitoriysida staging va konflikt retsepti bajariladi. Salbiy holatlar validatsiya tekshiruvlarini sinaydi. Yakuniy raqamlar [verification-result.json](verification-result.json)da.

Tekshiruv backend schema-2 importerini, frontendni, PostgreSQLni yoki Renderni tekshirmaydi. Bu bosqichda ular o‘zgarmagan. Haqiqiy o‘quvchilar bilan pilot va tashqi pedagogik ekspertiza o‘tkazilmagan; o‘quv samaradorligi haqida empirik da’vo yo‘q.
