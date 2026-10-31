# 2-klaster chiqarish tekshiruvi

Sana: 2026-10-31. Foydalanuvchi 4-bosqich — yakuniy tekshiruv, push va deployni tasdiqlagan.

## Chiqarishdan oldin

- [x] Tasdiqlangan loyiha va 1–3-bosqichlar tayyor; asosiy kod commit: `9de950c01c0922b68ef66f4b3c9c2a41f63489c1`.
- [x] `origin/main` bilan konflikt yo‘q; chiqarish oldidan remote `9ebed6f` edi.
- [x] Izolyatsiyalangan PostgreSQL’da yakuniy **137 test muvaffaqiyatli, 284.080 soniya**. Test bazasi o‘chirildi va lokal PostgreSQL serveri to‘xtatildi.
- [x] Frontend build hamda ikki haqiqiy Chrome fixture sinovi avvalgi bosqichda o‘tgan: jami 95 javob, 30 dars/misol UZ/RU, mobil va retry tekshiruvlari.
- [x] Offline resurs QA qayta o‘tdi: hash, tarjima, blueprint, 56 numeric reference, 11 salbiy holat.
- [x] `.github` workflow yo‘q; CI yashil deb ko‘rsatilmaydi. Tekshiruvlar lokal izolyatsiyalangan bazada va brauzerda bajarildi.
- [x] Additive migratsiya eski published modul, hash, enrollment va sessiya snapshotlarini saqlashi testda tasdiqlangan.
- [x] Production baseline o‘qish orqali olindi: 6 modul va bitta mavjud demo enrollment; holati deploydan keyin solishtiriladi.
- [x] Oldindan mavjud `.gitignore`, `backend/mindmetric/settings.py`, `render.yaml`, `backend/scripts/`, PostgreSQL recovery hujjatlari release commitlariga qo‘shilmadi.

## Chiqarish

- [x] Tasdiqlangan Render workspace: My Workspace, `tea-d77dc494tr6s73e376f0`.
- [x] Backend `srv-d9p29cfavr4c73afq1k0`, frontend `srv-d9p293favr4c73afpgsg`; ikkalasi `main` commitlariga auto-deploy qiladi.
- [x] `DEVELOPMENT_CLUSTER2_PUBLISH_ON_DEPLOY=1` backendda Render vositasi orqali merge qilindi, boshqa env qiymatlari almashtirilmadi. Neon `DATABASE_URL` o‘zgartirilmadi.
- [x] `main` va `codex/cluster1-stages-1-5` branchlariga push qilindi.
- [x] Yangi backend deploy `dep-dbj1nq92tl4s73e7dj9g` 2026-10-31 17:43:14 UTC da live bo‘ldi.
- [x] Frontend deploy `dep-dbj1nqbncjis73d4ap3g` 2026-10-31 16:48:57 UTC da live bo‘ldi. Yangi frontend eski API’da ham jonli o‘qish sinovidan o‘tdi.
- [x] `development.0003_developmentmodule_cluster` 2026-10-31 17:10:27 UTC da muvaffaqiyatli qo‘llandi.
- [x] Server logi: `Development release ready: 12 published modules in clusters 1/2; database=postgresql.`
- [x] Jonli API va brauzer smoke o‘tdi: I/II klasterlar, 2.1–2.6, UZ/RU, eski progress, mobil va JS holati.
- [x] Runtime error loglari 17:43:11–17:50:24 UTC oralig‘ida bo‘sh; smoke API so‘rovlari HTTP 200.

Render env vositasi flagni saqlaganda avvalgi `9ebed6f` commitiga API deploy ham yaratdi (`dep-dbj1nlp42hec73bpt8l0`). Yangi commit shu sabab navbatga tushdi; ulanishda cancel amali mavjud emas. Avvalgi deploy 17:09:53 UTC da yakunlangach, to‘g‘ri `9de950c` backend buildi 17:09:53.994 UTC da boshlandi. Alohida takroriy deploy trigger yuborilmadi.

## Muammo bo‘lsa

Ishga tushish/locale/import xatosida yangi deploy muvaffaqiyatli deb hisoblanmaydi. Release importi bitta transaction; yarim tayyor II klaster nashr qilinmaydi. Avvalgi live backend deploy `dep-dbiuee2vcj2c73ed5th0`, frontend `dep-dbiuee2vcj2c73ed5to0` edi. Render yangi versiya tayyor bo‘lmaguncha avvalgi ishlayotgan versiyaga trafik uzatishini hujjatlashtiradi. [Render deploy jarayoni](https://render.com/docs/deploys).

0003 migratsiya additive va eski kod bilan mos. DB yozuvlarini qayta tiklash yoki migratsiyani teskari yuritish ushbu chiqarishning avtomatik qismi emas. Jonli nashrdan keyingi tuzatishda avval o‘quv ma’lumotlarini saqlaydigan oldinga tuzatish afzal; dastur rollbacki ma’lumotlar bazasini ortga qaytarmaydi. [Render rollback hujjati](https://render.com/docs/rollbacks).

Qabul mezoni: yangi commitning ikkala xizmati live, API’da ikkita klaster va 12 modul, II klaster resurs nomlari/ko‘nikmalari RU/UZ, oldingi enrollment holati o‘zgarmagan, yangi tekshiruvlarda 5xx yoki JS xatosi yo‘q. Jonli smoke yangi enrollment yoki javob yaratmaydi; to‘liq o‘quv oqimi lokal fixture sinovlarida tekshirilgan.
