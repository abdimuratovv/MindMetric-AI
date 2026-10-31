# 2-klaster, 2-bosqich: backend integratsiyasi

Sana: 2026-10-31. Holat: backend implementatsiyasi va izolyatsiyalangan tekshiruvlar tugadi. Frontend integratsiyasi va production deploy bajarilmagan.

## Amalga oshirildi

- `DevelopmentModule.cluster` hamda additive `0003` migratsiyasi qo‘shildi. Eski modullarning qiymati 1; original JSON/hash, pinned enrollment va savol snapshotlari saqlanadi. Yangi modul boshqa versiyada ham o‘z kalitini boshqa klasterga ko‘chira olmaydi.
- Validator legacy schema 1 va yangi schema 2 ni to‘g‘ridan-to‘g‘ri qabul qiladi. Yangi klaster metama’lumotlari, indikatorlar, tartib, neytral psevdokod qoidalari va faqat self-review turidagi loyihalar tekshiriladi. 1-bosqichdagi vaqtinchalik schema-1 proyeksiyasi olib tashlandi.
- Oltita canonical bank va oltita ruscha locale backend kataloglariga sinxronlandi. `notation_uz`/`notation` modul hashi ichiga qo‘shildi: psevdokod qoidalari boshlang‘ich tekshiruvdan avval tushuntiriladi. Bu qo‘shimcha draft resurslarida qilindi; published I klaster fayllari o‘zgarmadi.
- Schema 2 importidan avval to‘liq ruscha tarjima va hash mosligi majburiy. Savollar/darslar, variant IDlari, konstantalar, savoldagi operatorlar, notation va miniloyihalar qamrovi tekshiriladi. Tarjima grading kalitini almashtira olmaydi.
- API modul kartalariga `cluster` va server hisoblaydigan `topic_number` qo‘shildi. Katalog/rejada lokalizatsiyalangan `clusters` ro‘yxati va modul soni bor. Umumiy katalog klaster/tartib bo‘yicha saralanadi; aktiv mashg‘ulotni davom ettirish umumiy rejaning ustuvor amali bo‘lib qoladi.
- Enrollment javobida `notation` va `projects` bor. Loyihalar precheck bosqichi tugamaguncha yopiq. Istalgan klasterda aktiv check bo‘lsa barcha enrollmentlarda notation, loyiha, dars, skill evidence va tugallangan yechim ko‘rinmaydi. Obyekt egasi, student/profile ruxsatlari, bitta global aktiv sessiya, exact numeric grading va UUID retry saqlanadi.
- `seed_development_content --all --cluster 2|all` qo‘shildi. Avvalgi bitta modul/default I klaster xatti-harakati saqlandi. II klasterning hozirgi ko‘nikma grafigi o‘z ichida yopiq, shuning uchun uning mustaqil draft importi mumkin; mavjud bo‘lmagan I klaster prerequisite-lari uydirilmadi.
- `activate_development_cluster2` barcha 12 modulni, har klasterdagi 6 mavzuning to‘liqligini tekshirib, bitta tranzaksiyada import/nashr qiladi. PostgreSQL qulfini I klaster bilan bo‘lishadi; xatoda butun chiqarish qaytariladi. Komanda user yoki diagnostika ballarini yaratmaydi.
- Gunicorn yangi komandani faqat `DEVELOPMENT_CLUSTER2_PUBLISH_ON_DEPLOY=1` bo‘lganda ishlata oladi. Production flaglari, Render va Neon holati o‘zgartirilmadi.

## Tekshiruvlar

Izolyatsiyalangan **PostgreSQL 18.0** bazasi: `127.0.0.1:55436`, `test_mindmetric_stage6`. Production ulanish manzili testga olinmadi.

```powershell
backend/venv/Scripts/python.exe backend/manage.py test apps.development.tests --settings=apps.development.tests.postgres_settings --noinput
```

**137 test muvaffaqiyatli, 166.849 soniya.** Jumladan:

- 8 parallel HTTP testi: ikki klasterda bir vaqtda sessiya boshlashda faqat bittasi ochiladi; UUID takroriy yuborish, javob/ishora va finish poygalari saqlanadi.
- Migratsiya testi: eski published modul, content hash, enrollment baseline va sessiya savol snapshoti yangi cluster ustunidan keyin saqlanadi.
- I klaster regressiyasi, yangi schema metadata/loyiha validatsiyasi, to‘liq RU talabi, combined dry-run, idempotent import/release, yetishmaydigan mavzu va kech publication xatosida rollback.
- II klasterning har oltita moduli API orqali precheck → study → practice → postcheck oqimidan o‘tdi: jami **120 yangi test javobi**. Bu sun’iy test ma’lumotlari; haqiqiy o‘quv samaradorligi natijasi emas.
- I yoki II klasterda aktiv check bo‘lganda boshqa klasterdagi dars, notation, miniloyiha va completed review yashirilishi tekshirildi. Begona enrollment/sessionga murojaat 404, check paytidagi yordam/dars mutatsiyasi 409.
- Mashqlar davomida diagnostika indikatorlari, IRT estimate va overall natijalari o‘zgarmadi.

Yakuniy metadata turi guardi va kengaytirilgan real-matn assertionlaridan so‘ng ikkita tegishli PostgreSQL testi qayta o‘tkazildi: **2/2 muvaffaqiyatli, 34.467 soniya**. Savol/variant, ishora, dars/nazariya/misol, notation hamda loyihaning barcha maydonlari UZ/RU manba bilan aynan solishtirildi.

Offline resurs QA ham o‘tdi: 56 mustaqil numeric reference hisob, ikki tilli qamrov, source hash va 11 salbiy resurs holati. Django `check`: muammosiz. `makemigrations --check --dry-run`: qo‘shimcha aniqlanmagan o‘zgarish yo‘q; kerakli `0003` migratsiyasi repository’da. Vaqtinchalik PostgreSQL serveri testlardan keyin to‘xtatildi.

## Fayllar va keyingi bosqich

- [Backend/API shartnomasi](cluster2-backend-contract.md).
- [Resurslar ko‘rsatkichi](content/cluster2/README.md).
- Kod: `backend/apps/development/` ichidagi loader, validator, translations, serializers/views, curriculum va yangi migratsiya/release komandasi.
- Testlar: `test_cluster2.py`, `test_cluster_migration.py` va kengaytirilgan `test_concurrency.py`.

Frontend, brauzerda 2-klaster ko‘rinishi va jonli RU/UZ almashishi bu bosqichda tekshirilmagan. Push/deploy qilinmadi; Neon bazasiga yozilmadi. Avvaldan mavjud `.gitignore`, `backend/mindmetric/settings.py`, `render.yaml`, `backend/scripts/` va PostgreSQL recovery hujjatlari ushbu commitga qo‘shilmadi.

Keyingi bosqich: foydalanuvchi tasdig‘idan so‘ng **3-bosqich — frontend integratsiyasi**: I/II klaster tanlovi, `topic_number`, notation va miniloyihalarni ko‘rsatish, mobil ko‘rinish va RU/UZ oqimi.
