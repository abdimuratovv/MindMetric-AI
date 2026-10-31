# 2-klaster, 4-bosqich: yakuniy tekshiruv va jonli chiqarish

Sana: 2026-10-31. Holat: **bajarildi**. I va II klaster [jonli platformada](https://mindmetric-frontend.onrender.com/#development) ishlamoqda.

## Chiqarilgan natija

II klasterning oltita yangi moduli to‘liq o‘zbekcha/ruscha resurslar bilan platformaga qo‘shildi: 30 dars va ishlangan misol, 120 topshiriq va 2 self-review miniloyiha. I klasterning oltita moduli saqlangan; katalogda jami 12 modul bor. Sahifada klaster tanlovi, to‘g‘ri 2.1–2.6 raqamlari, notation, miniloyihalar, RU/UZ almashishi va mashg‘ulotni tiklash mavjud.

Ishchi branch va `main`ga barcha kod commitlari yuborildi. Jonli xizmatlar ishlatayotgan kod: `9de950c01c0922b68ef66f4b3c9c2a41f63489c1`.

| Xizmat | Deploy ID | Jonli bo‘lgan vaqt |
|---|---|---|
| Frontend | `dep-dbj1nqbncjis73d4ap3g` | 2026-10-31 16:48:57 UTC / 21:48:57 Toshkent |
| Backend | `dep-dbj1nq92tl4s73e7dj9g` | 2026-10-31 17:43:14 UTC / 22:43:14 Toshkent |

Tasdiqlangan My Workspace va mavjud Render xizmatlari ishlatildi. Backendning Neon ulanishi almashtirilmadi. `DEVELOPMENT_CLUSTER2_PUBLISH_ON_DEPLOY=1` merge orqali qo‘shildi; boshqa maxfiy env qiymatlari chop etilmadi yoki repository’ga yozilmadi.

`development.0003_developmentmodule_cluster` migratsiyasi serverda 17:10:27 UTC da muvaffaqiyatli o‘tdi. Startup logida ikkala klasterdagi 12 modul nashr qilingani va `database=postgresql` tasdiqlandi. Render env saqlash vositasi avvalgi commit uchun ham API deploy boshlagani sabab yangi backend navbatga tushgan; bu oraliqda yangi frontend eski API bilan jonli tekshiruvdan o‘tdi. Alohida takroriy deploy trigger yuborilmadi.

## Tekshiruv dalillari

- **137 PostgreSQL testi** yakuniy chiqarish oldidan yana o‘tdi (284.080 soniya): migratsiya, atomik/idempotent import va release, ikki tilli kontent, o‘quv oqimi, ruxsatlar va 8 parallel HTTP testi. Lokal vaqtinchalik baza o‘chirildi, PostgreSQL serveri to‘xtatildi.
- Frontend build va oldingi bosqichdagi **95 javobli ikki Chrome sinovi** o‘tgan; 30 dars va misolning ikkala tildagi ko‘rinishi tekshirilgan. [Frontend hisoboti](cluster2-stage3-summary.md).
- Offline kontent QA qayta o‘tdi: 56 mustaqil numeric reference hisob, qamrov, source hash, locale va 11 salbiy holat.
- Remote `main` va ishchi branch chiqarish commitiga mosligi tekshirildi. GitHub combined-status javobida tashqi CI statuslari yo‘q; `.github` workflow mavjud emas. Lokal test natijalari CI natijasi sifatida ko‘rsatilmaydi.

## Jonli smoke natijasi

Haqiqiy Chrome va production API orqali:

- I/II klaster metama’lumotlari, har birida 6 modul va jami 12 modul tasdiqlandi.
- II klasterdagi oltita sarlavha, 30 ko‘nikma nomi, `content_language=ru/uz`, v1 versiyalari va 2.1–2.6 raqamlari repository resurslari bilan aynan solishtirildi. RU → UZ → RU almashishi o‘tdi.
- Klaster va til tanlovi sahifa yangilangach saqlandi. I klasterdagi 1.1 ruscha resursi va tarjimasiz mantiq modulining aniq o‘zbekcha fallbacki saqlandi.
- Deploydan oldingi mavjud demo enrollment holati **o‘zgarmagan**: v1, precheck, ayni session/question, 0/5 javob, lesson/check holatlari saqlangan. Script yangi enrollment yoki javob yaratmagan; development API’ga POST/PUT/DELETE yuborilmagan.
- JavaScript exception yo‘q; 390 px mobil kenglikda overflow yo‘q. Desktop/mobil skrinshotlar olindi, jonli katalog ko‘rinishi vizual ko‘rib chiqildi.
- Backend error-level runtime loglari 17:43:11–17:50:24 UTC oralig‘ida bo‘sh; jonli smoke’dagi API so‘rovlari HTTP 200 qaytargan. HTTP metrics endpointi bo‘sh ma’lumot qaytardi, shuning uchun undan xato ulushi yoki latency statistikasi chiqarilmadi.

Jonli smoke o‘qish bilan chegaralangan: yangi II klaster darslari va testlari production’da yangi enrollment ochib bajarilmadi. Ularning to‘liq oqimi PostgreSQL/API va lokal Chrome fixture sinovlarida tekshirilgan. Bu haqiqiy talabalardagi o‘quv samaradorligi yoki yangi qobiliyat o‘sishi isboti emas.

## Artifacts va foydalanish

Jonli baseline, frontendning eski API bilan moslik natijasi, yakuniy `result.json` va skrinshotlar:

`C:/Users/Asus/.codex/visualizations/2026/10/28/01a18264-3f77-7a02-a3d2-c4d4e2010e21/production-cluster2/`

Tekshiruv scripti: yuqoridagi ildiz katalogda `production-cluster2-smoke.py`. JWT va parol natija fayllariga yozilmagan.

[Platformani oching](https://mindmetric-frontend.onrender.com/#development) va **II klaster / Algoritmik-amaliy blok**ni tanlang. Avval boshlangan tekshiruv bo‘lsa, yangi mashg‘ulot boshlashdan oldin uni yakunlang; shaxsiy rejadagi davom ettirish tugmasi unga qaytaradi. Eski asset ko‘rinsa Ctrl+F5 bilan yangilang.

[Chiqarish checklisti](cluster2-release-checklist.md). Avvaldan mavjud `.gitignore`, `backend/mindmetric/settings.py`, `render.yaml`, `backend/scripts/` va recovery hujjatlari chiqarish commitlariga qo‘shilmadi. Yakuniy hujjatlar alohida `[skip render]` commitida yuboriladi; bu jonli kodni qayta build qilishni talab qilmaydi.
