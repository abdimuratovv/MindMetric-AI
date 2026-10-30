# Uchinchi bosqich yakuni

Sana: 2026-10-30. Bosqich: 1.1-mavzu uchun birinchi to‘liq talaba oqimi.

Holat: 3-bosqich bajarildi. 4-bosqich foydalanuvchi tasdig‘ini kutmoqda.

## Ishlaydigan jarayon

Talaba modulga yoziladi, beshta boshlang‘ich savolga javob beradi, beshta mini-darsni o‘rganadi, o‘nta izohli mashqni bajaradi va beshta yangi yakuniy savolda natijasini tekshiradi. Dastlabki va yakuniy natija hamda foiz punktidagi farq hisobotda ko‘rsatiladi.

Boshlang‘ich tekshiruvdan kamida 80% olgan talaba nazariya va mashqlarni ixtiyoriy o‘rganib, bevosita yakuniy tekshiruvga o‘ta oladi. Aks holda darslar va mashq bosqichi ochiladi. Dars tugallanishi talabaning belgilashi orqali qayd etiladi; uning o‘zi o‘zlashtirish ballini oshirmaydi.

## Backend

- Server boshqaradigan oqim `progress.py`, aniq sonli/variantli baholash `grading.py`, ruxsat etilgan javob shakllari va xavfsiz chiqish obyektlari `serializers.py`da amalga oshirildi.
- `/api/development/` URLlari asosiy backendga ulandi.
- Kontent mavjudligi va feature flag uchun capability endpointi yaratildi. Flag o‘chiq bo‘lsa o‘qitish endpointlariga kirish bloklanadi.
- Enrollment yaratish mavjud talabaning modul versiyasini saqlaydi; yangi foydalanuvchi eng so‘nggi e’lon qilingan versiyani oladi.
- Diagnostika ballari, qobiliyat bahosi va assessment sikli enrollment boshlanganda snapshot sifatida olinadi. Mashq va tekshiruvlar diagnostika natijalarini yozmaydi.
- Sessiya savollari serverda tanlanadi va snapshotga biriktiriladi. Javoblar joriy savol tartibida qabul qilinadi; mijoz yuborgan score, status yoki boshqa ortiqcha maydonlar qabul qilinmaydi.
- Mutatsiyalar transaction ichida avval enrollment, keyin sessiyani qulflaydi. Enrollment yaratishda talaba qatori ham qulflanadi. PostgreSQLdagi haqiqiy parallel yuklama sinovi hali keyingi bosqichga tegishli.
- Javob qayta yuborilganda bir xil UUID va payload avvalgi natijani qaytaradi; shu UUID bilan boshqa javob yuborilsa konflikt qaytadi.
- Mashqlarda izoh va ishora bor. Tekshiruv tugamaguncha javob kaliti, to‘g‘rilik, yechim va review berilmaydi. Faol tekshiruv vaqtida avvalgi sessiya reviewlari va darslar ham berilmaydi.
- Barcha shaxsiy endpointlar student egasi bo‘yicha filtrlanadi; boshqa talaba IDsi 404 qaytaradi. Rol, profil, feature flag va yozish tezligi cheklovlari qo‘llanadi.
- Darslar progressi uchun `completed_lesson_keys` maydoni va `0002` migratsiyasi qo‘shildi.

## API

| Endpoint | Vazifasi |
|---|---|
| `GET /api/development/capabilities/` | Pilot va e’lon qilingan kontent mavjudligi |
| `GET /api/development/modules/` | Katalog va saqlangan modul holati |
| `POST /api/development/modules/{key}/enroll/` | Modulga yozilish yoki mavjudini davom ettirish |
| `GET /api/development/enrollments/{id}/` | Darslar, joriy sessiya va hisobot |
| `POST /api/development/enrollments/{id}/lessons/{key}/complete/` | O‘rganilgan darsni qayd etish |
| `POST /api/development/enrollments/{id}/sessions/` | Ruxsat etilgan tekshiruv/mashqni boshlash yoki davom ettirish |
| `GET /api/development/sessions/{id}/next/` | Joriy savol va umumiy progress |
| `POST /api/development/sessions/{id}/answers/` | Javobni serverda tekshirish va saqlash |
| `POST /api/development/sessions/{id}/hints/` | Faqat mashqda yordam olish |
| `POST /api/development/sessions/{id}/finish/` | Barcha javoblardan keyin natijani hisoblash |
| `GET /api/development/progress/` | Faqat talabaning o‘z modullari bo‘yicha progress |

## React interfeysi

- `frontend/src/pages/Development/`da katalog, bosqichlar, mini-darslar, mashq/tekshiruv shakli, feedback va natija ekranlari yaratildi.
- Sidebar va natijalar sahifasiga capability holatiga bog‘liq kirish tugmalari qo‘shildi. Hozircha faqat e’lon qilingan kontent va yoqilgan flag bo‘lsa ko‘rinadi.
- `#development` orqali sahifani yangilaganda kerakli bo‘limga qaytiladi. Tanlangan enrollment foydalanuvchi IDsi bilan ajratilgan sessionStorage yozuvida saqlanadi, asosiy progress serverdan olinadi.
- Yuborilayotgan javob UUID va payload bilan vaqtincha saqlanadi. Internet xatosida o‘sha javob qayta yuboriladi; server tasdiqlamaguncha takror hisoblanmaydi. Sintaktik noto‘g‘ri son uchun 400 javob kelganda maydonni tuzatish mumkin.
- Raqamli javoblar uchun son yoki kasr kiritish, variantli savollar uchun klaviatura bilan boshqariladigan radio tugmalar mavjud.
- O‘zbek/rus interfeysi, modul ichidagi til almashtirgich va o‘zbekcha kontent fallback belgisi qo‘shildi. Formulalar mavjud Unicode matn orqali xavfsiz chiqariladi; HTML yoki kod bajarilmaydi.
- Bosqich belgilarida haqiqatan bajarilgan dars/mashq ko‘rsatiladi: yuqori precheck sabab o‘tkazib yuborilgan qadam bajarilgan deb belgilanmaydi.
- Telefon ko‘rinishi, yuklanish, xato, bo‘sh katalog, yordam va qayta yuborish holatlari tayyorlandi.

## Pilot qoidalarining aniqlashtirilishi

- Mashq sessiyasidagi oxirgi beshta turli topshiriqning kamida to‘rttasi birinchi urinishda va yordamsiz to‘g‘ri bo‘lsa, yakuniy tekshiruv ochiladi.
- Mashqlar banki qayta ishlatilishi mumkin. Yangi mashq raundidagi birinchi urinish faqat takrorlashga tayyorlikni belgilaydi; u yangi mustaqil o‘sish deb ko‘rsatilmaydi. Interfeysda bu farq izohlangan.
- Boshlang‘ich va yakuniy tekshiruvlar har enrollment uchun bittadan. Yangi savollar bo‘lmasa qayta postcheck ochilmaydi. Past yakuniy natijadan keyin mashqlar ochiq qoladi, ammo o‘sha savollar bilan yangi o‘sish hisoblanmaydi.
- Yakuniy 80% va yuqori natija — ushbu modul bo‘yicha mahsulot mezoni. Natija umumiy IQ yoki ilmiy tasdiqlangan qobiliyat o‘sishi sifatida berilmaydi; kichik to‘plamlar statistik tenglashtirilmagan.
- Mikroko‘nikma asosida avtomatik tavsiyalar hali 5-bosqichga tegishli. Hozir katalogdan tanlash, precheck va o‘qitish oqimi ishlaydi; sun’iy shaxsiy tavsiya chiqarilmaydi.

## Tekshirish natijalari

**63 ta backend testi muvaffaqiyatli o‘tdi.** Ularning 19 tasi ushbu bosqichdagi API oqimiga tegishli; oldingi 44 ta backend testi ham saqlandi va o‘tdi.

```powershell
backend\venv\Scripts\python.exe backend/manage.py test apps.development --settings=apps.development.tests.settings
backend\venv\Scripts\python.exe backend/manage.py check --settings=apps.development.tests.settings
backend\venv\Scripts\python.exe backend/manage.py makemigrations --check --dry-run --settings=apps.development.tests.settings
```

Django system check muammosiz; yaratilmay qolgan migratsiya yo‘q. `frontend/`da `npm run build` ham muvaffaqiyatli yakunlandi.

Haqiqiy React va Django serverlari bilan **Chrome headless brauzer sinovi** bajarildi. Alohida test SQLite bazasiga faqat sun’iy talaba va kerakli kontent yuklandi; mavjud lokal bazaning akkauntlari va progressidan foydalanilmadi.

Brauzerda tekshirilganlar:

- 5 precheck, 5 dars, 10 mashq va 5 postcheck orqali to‘liq oqim.
- Joriy tekshiruv vaqtida refreshdan keyin aynan qolgan savoldan davom etish.
- Noto‘g‘ri sonli yozuvni yuborib, xatodan keyin maydonni tuzatish.
- Server javobni saqlagach browserga kelayotgan javobni ataylab uzish va bir xil UUID bilan muvaffaqiyatli qayta yuborish.
- Yordam ishlatilgan mashq va uning feedbacki.
- 390 px telefon ko‘rinishida gorizontal overflow yo‘qligi; desktop va mobil skrinshotlar ko‘zdan kechirildi.
- 0% → 80% sinov natijasi va +80 foiz punkt hisoboti. Bu sun’iy test ssenariysi, haqiqiy talaba natijasi emas.
- Ruscha interfeys va o‘zbekcha material belgisi. JavaScript page errorlari: 0.

Qayta bajariladigan sinov:

```powershell
python backend/apps/development/tests/browser_smoke.py --artifacts ABSOLUTE_DIRECTORY --browser-executable 'C:\Program Files\Google\Chrome\Application\chrome.exe'
```

Bu skript uchun Python Playwright kerak. Mos Playwright Chromium mavjud bo‘lsa `--browser-executable` ixtiyoriy. Skript o‘z test serverlarini to‘xtatadi; sun’iy baza va loglar ignored `backups/development-browser-*` katalogida qoladi. Natija JSONi va skrinshotlar berilgan artifacts katalogiga yoziladi.

Test muhitida avvalgi qisqa development JWT kaliti va yaratilmagan `staticfiles` katalogi haqida ogohlantirishlar chiqdi. Vite build katta chunk haqida ogohlantirdi; build muvaffaqiyatli. Bu bosqichda production konfiguratsiyasi yoki umumiy bundle arxitekturasi o‘zgartirilmadi.

## Lokal baza va joriy holat

Lokal SQLite uchun `backups/cluster1-stage3-20261030T113950Z.sqlite3` zaxirasi olindi va faqat `development.0002` migratsiyasi qo‘llandi. Oldingi accounts, assessments va scoring jadvallari barcha qatorlari oldin/keyin hash bilan solishtirildi: o‘zgarish yo‘q.

Asosiy lokal bazada 1.1 kontenti hali **draft**, enrollmentlar soni 0; pilot flag standart holatda o‘chiq. Yuqoridagi brauzer sinovi alohida disposable bazada e’lon qilingan kontent bilan bajarildi. Asosiy bazani nashrga chiqarish yoki production deploy bajarilmadi. Pilotni ochishda kontent admin orqali nashr qilinadi va flag yoqiladi.

## Keyingi bosqich

4-bosqichda 1.2, 1.3, 1.5 va 1.6 mavzulari uchun qolgan 80 topshiriq, mini-darslar, ishlangan yechimlar va diagnostika aloqalari tayyorlanadi. Ish foydalanuvchi tasdig‘idan keyin boshlanadi.
