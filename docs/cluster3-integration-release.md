# III klaster integratsiyasi va chiqarish hisoboti

Sana: 2026-11-01. Holat: **integratsiya bajarildi, Renderda jonli, production smoke o‘tdi**. Foydalanuvchi resurs bosqichidan keyin integratsiya va deployni alohida buyurdi.

## Natija

Mavjud 12 modulga III klasterning 3.1–3.4 mavzulari qo‘shildi: 20 dars, 20 misol, 80 savol va uch ochiq amaliy ish to‘liq UZ/RU. Debugging starter va StudyTools kodi dars ichidan yuklanadi. O‘qituvchi yechimlari student kontentiga kiritilmaydi.

Schema 3 aynan III klaster, to‘rtta mavzu va mos indikatorlarni tekshiradi. Standalone draftlar saqlanadi; [export_platform.py](content/cluster3/export_platform.py) ulardan platforma canonical JSON/locale yaratadi. Natijalar nazariya boshida beriladi. [Platforma nusxalari](content/cluster3/platform/inventory.json) backend bundle bilan mos.

`0004_cluster3` migratsiyasi cluster variantlari va DB constraintini kengaytiradi; frozen kontent yoki sessiyalar qayta yozilmaydi. Atomik/idempotent `activate_development_cluster3` barcha 16 modulning 6/6/4 qamrovi va tarjimasini tekshiradi. PostgreSQL advisory lock eski release komandalar bilan umumiy. `DEVELOPMENT_CLUSTER3_PUBLISH_ON_DEPLOY=1` ushbu komandani Gunicorn masterida ishlatadi.

study_files faqat dars ochilganda beriladi. Istalgan klasterda aktiv check bo‘lsa, boshqa enrollmentlarda ham dars, loyiha, fayl va tugallangan yechimlar yopiladi. Obyekt egasi, student/profile ruxsatlari, bitta aktiv session, UUID retry va grading saqlangan. Kurs natijalari diagnostika/IRT ballarini o‘zgartirmaydi.

Frontendda uch klaster, III klaster tavsifi, 3.1–3.4 raqami va kod bloklari bor. Kod HTML sifatida talqin qilinmaydi. Tanlangan klaster, dars, namuna va loyiha sessionStorage orqali saqlanadi.

## Lokal tekshiruv

- Loopback PostgreSQLda to‘liq suite: **146 test**, 383.913 soniya. 145 tasi o‘tdi; bittasi eski `--cluster all` uchun 12 modul kutilmasiga duch keldi. Kutilma 16 modul/320 savolga moslashtirilib, tegishli testlar qayta bajarildi: **7/7 o‘tdi**, 64.079 soniya. Ochiq test xatosi qolmadi; bu yagona 146/146 qayta run deb ko‘rsatilmaydi.
- Schema/locale/filename, to‘rt modulning 80 javobli API oqimi, retry, scorelar o‘zgarmasligi, cross-cluster fayl/javob himoyasi, pinned II klaster, rollback va idempotent release tekshirildi.
- Haqiqiy Chrome/disposable SQLite: **80 UI javobi**, to‘rtta to‘liq modul, 20 darsning ikki tili, kod bloklari, ikki fayl mazmuni, refresh, mobil toshish va JS error yo‘qligi. Katalog tasvirlari til so‘rovi va sidebar animatsiyasi tugagach alohida olindi.
- Frontend build, Django check va makemigrations check o‘tdi. Offline QA: 12 mustaqil sonli javob, 143 Python/13 Git tekshiruvi, 14 salbiy holat.
- I/II klaster resurslari o‘zgarmagan. Oldindan mavjud `.gitignore`, settings, render.yaml va recovery o‘zgarishlari commitga qo‘shilmaydi.

Loglar: `backups/cluster3-postgres-tests.log`, `backups/cluster3-final-targeted.log`. Brauzer dalillari:

`C:/Users/Asus/.codex/visualizations/2026/11/01/01a1971d-7998-7240-92b8-9f1a43b9ec8a/cluster3-local/`

Katalog vizual tekshiruvi shu ildizdagi `cluster3-catalogue/`da. Production’dagi ikki mavjud enrollment holati baseline sifatida saqlandi. Jonli smoke yangi enrollment/javob yaratmaydi.

## Render chiqarish

Avval tasdiqlangan My Workspace va mavjud backend/frontend xizmatlari, GitHubdagi main ishlatildi. `DEVELOPMENT_CLUSTER3_PUBLISH_ON_DEPLOY=1` bitta env kaliti sifatida merge qilindi; boshqa env va DB ulanishi saqlandi. Env yangilanishi avvalgi commit uchun build boshladi, yangi commit undan keyin navbatda avtomatik chiqarildi; qo‘lda takroriy trigger yuborilmadi.

Deployed kod: `718a4a26479319b7e353defade869544349822a7`. Quyidagi vaqtlar Asia/Tashkent:

| Xizmat | Deploy | Holat / yakunlangan vaqt |
|---|---|---|
| Frontend | `dep-dbjkasbm8hqs73fsb87g` | live, 2026-11-01 18:58:22 |
| Backend | `dep-dbjkasdh3lcs738g7030` | live, 2026-11-01 19:49:12 |

Backend logi `development.0004_cluster3... OK`, `Development content release completed: clusters 1/2/3` va PostgreSQLda 16 published modul mavjudligini tasdiqladi.

[Jonli Rivojlanish bo‘limi](https://mindmetric-frontend.onrender.com/#development).

## Jonli tekshiruv

Chrome/API smoke muvaffaqiyatli: 3 klaster, 6/6/4 ta modul, barcha 16 modulning UZ/RU sarlavha va skilllari canonical/locale bilan mos. III klasterning to‘rt kartasi, til almashishi, refreshdan keyin tanlov saqlanishi va 390px mobil ko‘rinish tekshirildi. JS xatosi va gorizontal toshish yo‘q. Screenshot vizual ko‘rib chiqildi.

Demo hisobning deploydan oldin olingan ikki mavjud enrollment holati (stage, darslar, check ballari, aktiv session/savol) deploydan keyin aynan saqlangan. Production’da yangi enrollment yoki javob yaratilmagan; login’dan keyingi development so‘rovlari faqat GET. To‘liq 80 javobli o‘quv oqimi lokal sinovda tekshirilgan. Bu tekshiruv barcha foydalanuvchilar tarixini alohida audit qilmaydi.

Birinchi login so‘rovi xizmat uyqudan ishga tushayotganda 90 soniyadan oshdi; backend ishga tushgach qayta smoke to‘liq o‘tdi. Tekshiruv davridagi backend error loglari bo‘sh.

Dalillar yuqoridagi vizualizatsiya ildizining `cluster3-production/` papkasida: `baseline.json`, `result.json`, UZ/RU desktop va RU mobile tasvirlari. Yakuniy hisobot hujjatlar commiti `[skip render]` bilan saqlanadi; jonli dastur kodi yuqoridagi `718a4a2` commitidir.
