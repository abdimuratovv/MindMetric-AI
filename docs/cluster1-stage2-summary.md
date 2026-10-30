# Ikkinchi bosqich yakuni

Sana: 2026-10-28. Bosqich: backend asosi.

Holat: 2-bosqich bajarildi. 3-bosqich foydalanuvchi tasdig‘ini kutmoqda.

## Bajarilgan ishlar

- `backend/apps/development/` ilovasi yaratildi va Django sozlamalariga qo‘shildi.
- Sakkiz model va `0001_initial` migratsiyasi tayyorlandi: modul, mikroko‘nikma, dars, mashq, diagnostika aloqasi, enrollment, sessiya va javob.
- Modul kaliti/versiyasi, enrollment va sessiyalar, javob idempotency kaliti va urinish raqami uchun unique constraintlar; ball va musbat raqamlar uchun DB check constraintlar qo‘shildi.
- Kontent nashr qilingach yoki foydalanish boshlangach odatiy save/delete va prerequisite o‘zgarishlari bloklanadi. Yangi nashr eski enrollmentni o‘zgartirmaydi.
- Enrollment diagnostika snapshoti va sessiyadagi savollar tarkibi o‘zgarmas saqlanadi; javoblar yangi urinish sifatida qo‘shiladi.
- Student roli, to‘ldirilgan profil, feature flag va obyekt egasi uchun qayta ishlatiladigan permissionlar tayyorlandi.
- Django admin uchun faqat ko‘rish rejimi va tekshirilgan draftni aniq nashr qilish amali yaratildi. Kirish uchun product admin roli bilan birga Django staff huquqi yoki superuser kerak.
- `seed_development_content` komandasi yaratildi: `--dry-run`, `--path`, atomik import, qayta importda dublikat yaratmaslik, draftni yangilash va muzlatilgan versiyani himoyalash.
- JSON shartnomasi bo‘yicha tuzilma, kalit, savol qamrovi, prerequisite sikli, javob formati va mavjud diagnostika savollariga havolalar tekshiriladi.
- Sonli javoblarni aniq kasr sifatida o‘qish yordamchisi yaratildi; uzunlik cheklanadi, nol maxraj va kod/ifoda qabul qilinmaydi.
- 1.1 kontenti backend bilan deploy qilinadigan katalogga joylashtirildi. Original DOCX va Downloads yo‘li runtime uchun talab qilinmaydi.

## Tekshiruv natijalari

Quyidagi tekshiruvlar muvaffaqiyatli yakunlandi:

```powershell
backend\venv\Scripts\python.exe backend/manage.py test apps.development --settings=apps.development.tests.settings
backend\venv\Scripts\python.exe backend/manage.py check --settings=apps.development.tests.settings
backend\venv\Scripts\python.exe backend/manage.py makemigrations --check --dry-run --settings=apps.development.tests.settings
```

Natija: **44 ta test o‘tdi**; Django system check muammosiz; yaratilmay qolgan model migratsiyasi yo‘q. Testlar alohida in-memory SQLite bazada bajarildi. Django admin action haqiqiy HTTP so‘rovi orqali ham tekshirildi. Test muhitida `staticfiles` katalogi hali yaratilmaganligi haqida ogohlantirish chiqdi; testlar muvaffaqiyatli yakunlandi.

Testlar quyidagilarni qamrab oldi:

- Noto‘g‘ri yoki yetishmayotgan kontentning rad etilishi, sikllar va noto‘g‘ri blueprint.
- Yordamchi ishoraning tekshiruv savoliga kiritilmasligi va sonli javob formatining xavfsizligi.
- Seedning qayta bajarilishi, dry-run yozuv yaratmasligi, yetishmayotgan diagnostika havolasida xato va qisman importdagi to‘liq rollback.
- Kontent versiyasining muzlatilishi, eski versiyadagi progressning saqlanishi, snapshot va javoblar himoyasi.
- Begona talaba obyektlariga kirish, profil va flag cheklovlari, staff o‘qituvchining kontent adminiga kirishi bloklanishi.
- Yangi import mavjud diagnostika ballari, qobiliyat taxminlari, umumiy natija, yo‘nalish tavsiyalari, yutuqlar va akkauntlarni o‘zgartirmasligi.

## Lokal bazadagi amaliy tekshiruv

Muhitda `DATABASE_URL` va Render belgisi yo‘qligi tekshirildi. Faqat mavjud lokal `backend/db.sqlite3` bilan ishlandi.

Migratsiyadan oldin SQLite backup API orqali zaxira nusxa olindi:

`backups/cluster1-stage2-20261028T140739Z.sqlite3`

Zaxira Git tomonidan e’tiborsiz qoldiriladigan katalogda saqlanadi. Migratsiya rejasi faqat `development.0001_initial`dan iborat edi; u muvaffaqiyatli qo‘llandi. Dry-run, haqiqiy import va takroriy import bajarildi.

| Obyekt | Lokal bazadagi soni |
|---|---|
| Modul | 1, `draft` |
| Mikroko‘nikma | 5 |
| Mini-dars | 5 |
| Topshiriq | 20 |
| Diagnostika aloqasi | 14 qator, 13 savol |
| Talaba enrollmenti | 0 |

Bitta diagnostika savoli ikki ko‘nikmaga bog‘langani uchun 13 savolga 14 aloqa to‘g‘ri keladi. Eski accounts, assessments va scoring jadvallarining barcha qatorlari oldin/keyin hash bilan solishtirildi; o‘zgarish aniqlanmadi. Production bazasiga ulanish yoki deploy bajarilmadi.

## Hozirgi chegaralar

- Feature flag standart holatda o‘chiq. Kontent lokal bazada draft, haqiqiy nashr qilinmagan.
- Talaba APIlari, tavsiya/tekshirish oqimi va frontend 3-bosqichga tegishli. Permissionlar aynan o‘sha endpointlarga ulanishi va querysetlar egaga qarab filtrlanishi kerak.
- Runtime til fallbacki API bilan birga 3-bosqichda yoziladi; hozir uz kontent va ru uchun bo‘sh maydonlar saqlanadi.
- PostgreSQLdagi row lock va parallel HTTP so‘rovlar staging tekshiruvi keyingi bosqichlarda bajariladi; SQLite natijasi ularning o‘rnini bosmaydi.
- Model himoyalari odatiy ORM amallarida ishlaydi; bulk update/raw SQL faqat ishonchli ichki kodda qo‘llanishi mumkin.
- Avvaldan mavjud `.gitignore`, Render konfiguratsiyasi, backup skriptlari va settingsdagi PostgreSQL talablari saqlandi. Settingsga faqat yangi ilova va pilot flag qo‘shildi.

## Keyingi bosqich

3-bosqichda 1.1-mavzu uchun to‘liq oqim quriladi: enroll → precheck → dars → practice → postcheck → hisobot. Bunga talaba APIlari, serverdagi baholash/bosqich boshqaruvi va dastlabki React ekranlari kiradi. Ish foydalanuvchi tasdig‘idan keyin boshlanadi.
