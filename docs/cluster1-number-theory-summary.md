# 1.4 Sonlar nazariyasi va diskret matematika

Sana: 2026-10-30. Foydalanuvchi so‘ragan qo‘shimcha modul.

## Resurslar

- `docs/content/cluster1/1.4-mavzu.docx`: 8 sahifali o‘quv resursi, nazariya, beshta ishlangan misol, mashqlar va tekshiruvlarning yechimlari bilan. Native Word’da yaratildi, LibreOffice’da PDF’ga aylantirilib barcha sahifalar ko‘zdan kechirildi. PDF va PNG faqat QA uchun, asosiy topshiriladigan resurs Word fayli.
- `docs/content/cluster1/1.4-mavzu.md`: yangi mualliflik manbasi. U foydalanuvchi bergan mavzu asosida tuzilgan; avval taqdim etilmagan DOCX’dan ko‘chirilgan deb ko‘rsatilmaydi. SHA-256 manifestda qayd etilgan, Git’da LF satr tugashi belgilangan.
- `number-theory-discrete-mathematics.v1.json`: ko‘rib chiqilgan va backendga qo‘shilgan bir xil nusxalar. E’lon qilish mavjud release buyrug‘i orqali amalga oshirildi.

## Qamrov

1. Musbat bo‘luvchi va manfiy bo‘lmagan bo‘linuvchida div/mod, `a=bq+r`, `0≤r<b`; nolga bo‘lish va manfiy sonlar kelishuvi aniq ajratilgan.
2. Tub/murakkab son, 0 va 1 holati, √n gacha tekshirish, tub ko‘paytuvchilarga ajratish.
3. EKUB: tub ko‘paytuvchilar va Evklid algoritmi, teng guruh/kvadrat masalalari.
4. EKUK: tub ko‘paytuvchilar, EKUB orqali formula va takrorlanadigan hodisalar.
5. 2/8/10/16 lik sanoq sistemalari: ruxsat etilgan raqamlar, pozitsion qiymat, ketma-ket bo‘lish va bitlarni 3/4 tadan guruhlash.

Modul: 5 ko‘nikma, 5 dars, 10 practice, 5 precheck va 5 postcheck. Mavjud UI, grading, focus, resume va hisobot ishlatiladi. Diagnostika xaritasi hali tasdiqlanmagan: mos bo‘lmagan savolga sun’iy bog‘lanish qo‘shilmadi, mavzu o‘z prechecki bilan aniqlanadi. Avvalgi beshta published manifest va versiya o‘zgartirilmadi.

## Verifikatsiya

- PostgreSQL 18.0 izolyatsiyalangan bazada 108 test muvaffaqiyatli, shu jumladan 7 parallel API sinovi.
- SQLite: 108 test, 7 PostgreSQL-only skip, qolgan 101 muvaffaqiyatli.
- 20 yangi javob va beshta misol mustaqil integer, gcd/lcm, primality va base-conversion orakllari bilan tekshirildi; eski 100 topshiriq auditi ham qayta o‘tdi.
- Haqiqiy brauzerda 6 modul, 45 javobli ssenariy, refresh/resume, retry, uz/ru va mobil ko‘rinish muvaffaqiyatli. To‘liq modul oqimi API testida o‘tdi.
- Frontend build muvaffaqiyatli; avvalgi katta bundle ogohlantirishi saqlanadi.

## Deploy

Backend `eb07c0fcbfc6e03759f5d040d5258ab2aa7a1f88`, Render deploy `dep-dbidcd7b9u1s73facfcg`: `live`. Release logi PostgreSQL’da 6 ta published modulni tasdiqladi. Frontend ham yangilandi. Word resursi `1a5867c` commitida qo‘shilgan. Jonli tekshiruv mavjud demo talaba bilan o‘qish so‘rovlarida muvaffaqiyatli bajarildi: 6 modul, 1.4 kaliti va ko‘nikmalari, 1–6 tartib, sidebar, mobil overflow yo‘qligi va JavaScript xatolari yo‘qligi tasdiqlandi. Yangi enrollment yoki diagnostika javobi yaratilmagan.

Katalog: https://mindmetric-frontend.onrender.com/#development . Yangi mavzu tartibi 4, jami tartib 1–6. QA artefaktlari `number-theory-browser/`, `number-theory-docx-qa/` va `production-number-theory/` nomlari bilan Codex visualizations katalogida saqlanadi.

Vaqtinchalik renderer papkasini tozalash avtomatik xavfsizlik tekshiruvida “blocked by policy” bilan rad etildi. Katta vaqtinchalik fayllar `backups/number-theory-docx-qa/` ichida qoldi; Git’ga qo‘shilmadi.
