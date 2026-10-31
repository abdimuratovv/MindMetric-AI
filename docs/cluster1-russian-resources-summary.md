# 1.1 va 1.6 modullarining ruscha resurslari

Sana: 2026-10-31. Foydalanuvchi so‘rovi: sahifada RU tanlanganda ruscha, UZ tanlanganda o‘zbekcha resurslarni ko‘rsatish.

## Amalga oshirildi

- 1.1 arifmetika/algebra va 1.6 matritsalar uchun to‘liq ruscha kontent yaratildi: modul va ko‘nikma nomlari, jami 10 dars, nazariya va ishlangan misollar, 40 savolning matni, variantlari, yordam va yechim izohlari.
- Tarjima qatlami modul kaliti, v1 versiyasi va original content hashga bog‘landi. E’lon qilingan asosiy JSONlar, DB kontent versiyasi, savol snapshotlari va javob kalitlari tahrirlanmadi. Avval boshlangan v1 mashg‘ulot ham ruscha ko‘rinadi.
- API mavjud `X-Language`/`lang` tanlovidan foydalanadi. Katalog, reja, enrollment, sessiya, yordam, progress va tugallangan yechimlar shu tanlovda qaytadi. `content_language` haqiqiy kontent tilini bildiradi.
- Frontendda statik `lang=uz` belgilar almashtirildi. Material tili belgisi RU resurs uchun ruscha deb ko‘rsatiladi. Qolgan to‘rtta modulda tarjima yo‘q bo‘lsa o‘zbekcha fallback aniq ko‘rsatiladi.
- Til almashganda joriy dars, ochilgan misol, tanlangan variant, olingan yordam va ochilgan practice izohi saqlanadi. Kech qaytgan eski tildagi mutation javobidan keyin joriy tilda qayta o‘qiladi.
- Tarjima fayllari frontend bundle’ga qo‘shilmadi. Tekshiruvda yechimlar, kalitlar yoki yordamlar ochilmaydi; option ID, UUID retry va baholash tartibi avvalgidek ishlaydi.

## Tekshiruv

- PostgreSQL 18.0’dagi izolyatsiyalangan bazada 116 test muvaffaqiyatli, jumladan 7 parallel API testi.
- Tarjima resurslari bo‘yicha alohida validator/testlar: barcha maydonlar to‘liq, raqamli konstantalar va option IDlar saqlangan, manba hash mos, check hint va grading override taqiqlangan, reviewed/backend nusxalari teng.
- API: 1.1/1.6 RU ↔ UZ, qolgan modullar fallbacki, v1 davom ettirish, savol soni va snapshot o‘zgarmasligi, idempotent javob, yordam/feedbackni tiklash, dars/misol va review/progress tekshirildi.
- Haqiqiy Chrome brauzerida 6 modul, 45 javobli oqim o‘tdi. RU ↔ UZ katalog, tekshiruvdagi tanlangan variant, uchinchi dars, ochilgan misol, hint, feedback, yakuniy hisobot va matritsalardagi besh darsda tekshirildi. JS xatosi va 390 px mobil overflow kuzatilmadi.
- Django check va migratsiya dry-run muammosiz: yangi migratsiya yo‘q. Frontend build muvaffaqiyatli; avvaldan mavjud katta bundle ogohlantirishi qolgan.

Asosiy fayllar: `backend/apps/development/translations.py`, `content/translations/`, serializers/views va `frontend/src/pages/Development/`. Tarjima authoring manbasi va reviewed JSONlar `docs/content/cluster1/` ichida.

## Chiqarish

Lokal tekshiruvlar tugadi. Ushbu hisobot tayyorlanayotganda push/deploy va jonli RU ↔ UZ smoke tekshiruvi navbatdagi amaldir. Yakuniy natija shu chatda qayd etiladi. Asosiy Neon bazasida sinov uchun yangi javob yoki enrollment yaratish talab etilmaydi; jonli tekshiruv avval e’lon qilingan kontentni o‘qish bilan cheklanadi.
