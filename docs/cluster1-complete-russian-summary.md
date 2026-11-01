# 1.2–1.5 ruscha resurslaridagi aralash til tuzatishi

Sana: 2026-10-31.

## Sabab

Avvalgi tarjima so‘rovi faqat 1.1 va 1.6 mavzularini qamragan.
1.2–1.5 uchun ruscha JSON resurslari bo‘lmagan. RU interfeys tanlanganda
API shu modullarning o‘zbekcha asl matnini fallback sifatida qaytargan.
Shuning uchun ruscha tugmalar yonida o‘zbekcha sarlavha va nazariya ko‘ringan.
Bu brauzer keshi yoki til tugmasining xatosi emas.

## Tuzatish

- 1.2 mantiq, 1.3 to‘plamlar, 1.4 sonlar nazariyasi va 1.5 funksiyalar,
  progressiyalar, kombinatorika to‘liq rus tiliga tarjima qilindi: 20 ko‘nikma,
  20 dars/nazariya/ishlangan misol va 80 savol, variant, yordam, yechim va xato izohi.
- Review uchun va backend uchun bir xil UTF-8 nusxalar yaratildi.
- Barcha birinchi klaster modullari RU ↔ UZ tanloviga mos kontent qaytaradi.
- Har ikkala release buyrug‘i endi barcha mavzularda to‘liq, manba hashiga mos
  ruscha resurs mavjudligini bazaga importdan oldin tekshiradi. Yetishmagan yoki
  eskirgan tarjima butun relizni to‘xtatadi.
- Asl v1 JSONlar, savol/variant IDlari, javob kalitlari, baholash va sessiya
  snapshotlari saqlandi. Migratsiya talab qilinmaydi. Mavjud v1 mashg‘ulotlar
  yangi ruscha resurslardan foydalanadi.
- Noma’lum kelajakdagi versiya yoki mos kelmaydigan hash uchun runtime fallback
  saqlangan; tekshirilgan hozirgi relizlarda bunday to‘liqsizlikka yo‘l qo‘yilmaydi.

## Tekshiruvlar

Tarjima validatori barcha oltita modulni qabul qildi: har bir maydon va paragraf
to‘liq, raqamli konstantalar, manba hash va variant IDlari mos; tekshiruvdagi
yordam va javob kalitini almashtirish taqiqlangan.

API regressiya testlari barcha olti modulning katalogi, ko‘nikmalari, darslari,
misollari, tugallangan tekshiruv izohlari va progressini RU/UZ da qamraydi.
Release regressiya testi to‘rtta yangi tarjimaning har biri yo‘q yoki hash xato
bo‘lganda ikkala release buyrug‘i ham importni boshlamasligini tekshiradi.

Brauzer regressiyasi barcha olti modulning ruscha katalogi, faol tekshiruvdagi
til almashinuvi va 1.2–1.6 dagi barcha dars/nazariyalarni RU ↔ UZ da tekshiradi.
1.1 dagi misol, tanlangan javob, hint va feedbackni saqlash tekshiruvlari ham bor.

- Izolyatsiyalangan PostgreSQL bazasida **138 test muvaffaqiyatli**, 413.622 soniya;
  parallel sessiya/javob testlari va migratsiya mosligi ham qamralgan.
- Haqiqiy Chrome brauzerida **45 javobli oqim muvaffaqiyatli**; barcha olti modul
  RU katalogida, 1.2–1.6 ning 25 darsi va ishlangan misollari RU ↔ UZ da tekshirildi.
  JavaScript xatosi va tekshirilgan 390 px mobil ko‘rinishda overflow yo‘q.
- `manage.py check` muammosiz; `makemigrations --check --dry-run`: o‘zgarish yo‘q.
- Yangi to‘rtta tarjima matnida kutilmagan lotincha so‘zlar qolmagan; matematik
  belgilar, o‘zgaruvchilar va dasturlash atamalari tarjima qilinmagan holda saqlangan.
- Asl klaster-1 kanonik JSONlari Git bo‘yicha o‘zgarmagan.

## Jonli reliz tasdig‘i — 2026-11-01

- Tuzatish `b495c2b05618395adef0b963c45d93eccb07bd51` commitida feature branch va
  `main`ga push qilindi. Render backend deploy `dep-dbj2vl95efls73dj98fg`
  2026-10-31 23:35:28 Toshkent vaqti (18:35:28 UTC) da `live` bo‘ldi.
- 2026-11-01 14:32 Toshkent vaqti atrofida [jonli platforma](https://mindmetric-frontend.onrender.com/#development)
  API va Chrome brauzerida qayta tekshirildi: ikkala klasterning barcha 12 moduli
  RU ↔ UZ da to‘g‘ri sarlavha, ko‘nikma va kontent tili qaytardi. Birinchi
  klaster RU katalogida o‘zbekcha material belgisi qolmagan.
- Reliz oldidan qayd qilingan ikki mashg‘ulotning bosqichi, savol/javob soni,
  faol savol kaliti, tugallangan darslari va ballari saqlangan. Faol 1.1
  tekshiruvining matni ham tanlangan tilga mos; yangi enrollment yoki javob
  yaratilmagan. Jonli darslar ushbu hisobda yopiq bo‘lgani uchun barcha yangi
  dars/misollar lokal API va brauzerda tekshirildi.
- Jonli brauzerda JavaScript xatosi, 390 px mobil overflow va kutilmagan
  development API yozuvlari yo‘q. Tekshiruv davridagi backend error loglari bo‘sh.
- Natija va skrinshotlar:
  `C:/Users/Asus/.codex/visualizations/2026/10/28/01a18264-3f77-7a02-a3d2-c4d4e2010e21/production-complete-russian/`.
