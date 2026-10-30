# To‘rtinchi bosqich yakuni

Sana: 2026-10-30. Bosqich: birinchi klasterning qolgan to‘rtta modulini tayyorlash.

Holat: 4-bosqich bajarildi. 5-bosqich foydalanuvchi tasdig‘ini kutmoqda.

## Tayyorlangan kontent

| Modul | Mini-dars va ishlangan namuna | Mashq | Precheck | Postcheck |
|---|---|---|---|---|
| 1.2 Matematik mantiq va mulohazalar algebrasi | 5 | 10 | 5 | 5 |
| 1.3 To‘plamlar nazariyasi va Venn diagrammalari | 5 | 10 | 5 | 5 |
| 1.5 Funksiyalar, ketma-ketliklar va kombinatorika | 5 | 10 | 5 | 5 |
| 1.6 Matritsalar va chiziqli algebra elementlari | 5 | 10 | 5 | 5 |
| Ushbu bosqichda qo‘shildi | 20 | 40 | 20 | 20 |

Oldingi 1.1 bilan birga klasterda **5 modul, 25 mikroko‘nikma, 25 mini-dars, 25 ishlangan namuna va 100 topshiriq** mavjud. Har ko‘nikmaga 2 mashq, 1 precheck va 1 postcheck to‘g‘ri keladi. 1.4 fayli berilmagani uchun qo‘shilmadi.

Har topshiriqda javob kaliti, bosqichli yechim, odatiy xato, ko‘nikma va manba lokatori bor. Mashqlarga ishora, variantli savollarning har bir variantiga tushuntirish yozildi. Yangi 80 topshiriqdan 29 tasi manbadan moslashtirilgan, 51 tasi yangi yozilgan. Kontent ichki tekshiruvdan o‘tgan draft; tashqi metodist tasdig‘i yoki statistik kalibrlash o‘rnini bosmaydi.

## Manbalarni to‘ldirish

- 1.2: mulohaza va ochiq ifoda farqi, rostlik jadvali, kontrapozitsiya, yutilish, qo‘sh inkor va taqsimot qonunlari tushuntirildi. De Morgan formulalarida inkor sohasi aniq qavslar bilan yozildi.
- 1.3: element, qism to‘plam, A⊆B va A⊊B, kesishish xossasi, to‘ldiruvchi va qo‘sh hisoblash izohlandi. Munosabatlar to‘liq yoritilmagani uchun sarlavha mavjud Venn mazmuniga moslashtirildi.
- 1.5: aniqlanish sohasi, ildiz/maxraj cheklovlari, progressiya yig‘indilari, tartib va takrorlanish shartlari qo‘shildi.
- 1.6: birlik matritsa atamasi, qator/ustun yozuvi, matritsa ko‘paytirishi va 2×2 determinant yechimlari tayyorlandi. Kesilgan manba savollari taxminan tiklangan deb ko‘rsatilmadi; yangi savollar alohida belgilandi. 3×3 determinant bu nashrga kirmaydi.

Original DOCX fayllari o‘zgartirilmadi. Matn, Unicode formulalar, matn orqali berilgan Venn hududlari va qatorlari ichki qavslarda ko‘rsatilgan matritsalar ishlatildi. Yangi interaktiv diagramma muharriri yoki formula kutubxonasi yaratilmagan.

## Diagnostika aloqalari

| Modul | Mavjud savollarga moslik |
|---|---|
| 1.1 | 13 savol, 14 aloqa |
| 1.2 | 2 savol: kontrapozitsiya va implikatsiya zanjiri |
| 1.3 | 3 savol: qism to‘plamga asoslangan xulosa |
| 1.5 | 10 savol: faktorial/kombinatsiya va mos sonli ketma-ketliklar |
| 1.6 | 0; bevosita mos mavjud savol yo‘q |

Jami **28 savol va 29 aloqa**. IQ havolalari faqat arifmetik/geometrik ketma-ketliklarga tegishli. Matritsalarga sun’iy havola qo‘shilmadi. Qolgan modullardagi qisman qamrov cheklovlari ham `diagnostic_coverage_note_uz` orqali qayd etildi. Mos dalil bo‘lmagan bilim precheck bilan aniqlanadi; kam havola yetarli diagnoz deb talqin qilinmaydi.

## Import va integratsiya

- To‘rtta yangi manifest `docs/content/cluster1/` va deploy qilinadigan `backend/apps/development/content/cluster1/` kataloglariga joylandi. Nusxalar mosligi tekshiriladi.
- `build_stage4_content.py` tahrirlanadigan mualliflik manbasi, `verify_stage4_content.py` esa undan alohida hisoblash/tekshirish vositasi sifatida yaratildi.
- `seed_development_content --all` beshta modulni avval tekshiradi, keyin prerequisite tartibida bitta transaction ichida import qiladi. Xatoda butun bundle qaytariladi.
- `--all --dry-run` o‘zaro havolalarni yozuv yaratmasdan tekshiradi. Oddiy komanda hali 1.1 modulini, `--path` esa alohida faylni oladi.
- Diagnostika ro‘yxati bo‘sh bo‘lsa, aniq coverage izohi talab qilinadi.
- Katalogdagi barcha kartaga “1.1” chiqaruvchi yozuv o‘rniga haqiqiy modul raqami va ko‘nikmalar qo‘yildi. Avtomatik shaxsiy tavsiyalar 5-bosqichda qoladi.
- Yangi DB modeli yoki migratsiya kerak bo‘lmadi.

## Tekshirish natijalari

```powershell
backend\venv\Scripts\python.exe -X utf8 docs/content/cluster1/verify_stage4_content.py --source-dir 'D:\Downloads\Telegram Desktop'
backend\venv\Scripts\python.exe backend/manage.py test apps.development --settings=apps.development.tests.settings
backend\venv\Scripts\python.exe backend/manage.py check --settings=apps.development.tests.settings
backend\venv\Scripts\python.exe backend/manage.py makemigrations --check --dry-run --settings=apps.development.tests.settings
```

80 yangi kalit hisoblangan yoki mazmuniy tekshirilgan javob bilan solishtirildi; oldingi 20 savol tekshiruvi saqlandi. Yangi 20 namuna, mantiqiy qonunlarning barcha kirish holatlari, variantlar, 25 ko‘nikmaning grafigi va original manbalar SHA-256 qiymatlari tekshirildi. Variantlarning mazmuni ham ichki tahririy ko‘rib chiqildi.

**73 backend testi o‘tdi**: oldingi 63 test va 10 yangi bundle testi. Har bir yangi modulda precheck → 5 dars → 10 mashq → postcheck API orqali bajarildi; jami 80 javob saqlandi va diagnostika balli yaratilmaganligi tekshirildi. Oxirgi kontent tahriridan keyin ushbu to‘liq yangi modul oqimi testi va 100 savol tekshiruvi yana o‘tkazildi. Django system check muammosiz; yaratilmay qolgan migratsiya yo‘q. Frontend `npm run build` muvaffaqiyatli.

Chrome headless sinovida beshta kartali katalog, to‘rtta yangi modulni ochish, har birining precheckini refreshdan keyin davom ettirish va telefon ko‘rinishi tekshirildi. 1.1 to‘liq oqimi, ruscha interfeys, noto‘g‘ri kiritishni tuzatish va javob xabari yo‘qolganidan keyingi idempotent retry ham qayta tekshirildi. JavaScript page error: 0. Desktop va mobil skrinshotlar ko‘zdan kechirildi.

```powershell
python backend/apps/development/tests/browser_smoke.py --all-modules --artifacts ABSOLUTE_DIRECTORY --browser-executable 'C:\Program Files\Google\Chrome\Application\chrome.exe'
```

Brauzer sinovi alohida sun’iy bazada bajariladi; test serverlari tugagach to‘xtatiladi. PostgreSQLdagi parallel yuklama tekshiruvi keyingi bosqichda qoladi. Build katta chunk haqida avvaldan mavjud ogohlantirish bilan muvaffaqiyatli yakunlandi.

## Lokal baza

Zaxira: `backups/cluster1-stage4-20261030T131916Z.sqlite3`. Dry-run, haqiqiy va takroriy `--all` importlar bajarildi. Bazada 5 draft modul, 25 ko‘nikma, 25 dars, 100 topshiriq, 29 diagnostika aloqasi va 0 enrollment bor. Qayta import dublikat yaratmadi.

Accounts, assessments va scoring jadvallaridagi barcha qatorlar oldin/keyin hash bilan solishtirildi: o‘zgarish yo‘q. Asosiy bazada kontent nashr qilinmadi, pilot yoqilmadi va production deploy bajarilmadi.

## Keyingi bosqich

5-bosqich: mikroko‘nikmalar bo‘yicha dalilga asoslangan tavsiyalar, beshta modulni shaxsiy rivojlanish rejasiga bog‘lash va interfeysni yakunlash. Faqat foydalanuvchi tasdig‘idan keyin boshlanadi.
