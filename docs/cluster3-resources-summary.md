# III klaster resurslari yakuniy hisoboti

Keyingi bosqich ham bajarildi: [integratsiya va jonli Render tekshiruv hisoboti](cluster3-integration-release.md). Quyidagi matn resurslar bosqichining yakuniy holatini qayd etadi.

Sana: 2026-11-01. Holat: **resurslar tayyor va offline tekshirilgan**. Foydalanuvchi tasdig‘iga muvofiq faqat resurslar yakunlandi; platforma integratsiyasi va Render deployi bajarilmadi.

[Barcha resurslarni ochish](content/cluster3/README.md).

## Tayyorlangan mazmun

| Modul | Mavzu | Dars / namuna | Mashq / boshlang‘ich / yakuniy |
|---|---|---|---|
| 3.1 | Kod tahlili va debugging | 5 / 5 | 10 / 5 / 5 |
| 3.2 | Kichik guruh loyihasi va Git | 5 / 5 | 10 / 5 / 5 |
| 3.3 | Diqqat va aniqlik uchun code review | 5 / 5 | 10 / 5 / 5 |
| 3.4 | Hujjatlar asosida yangi bilimni o‘zlashtirish | 5 / 5 | 10 / 5 / 5 |

Jami **20 mikroko‘nikma, 20 dars, 20 ishlangan misol, 40 yordamli mashq, 20 boshlang‘ich va 20 yakuniy savol**. 80 savolning 68 tasi tanlovli, 12 tasi sonli. Barcha dars, namuna, savol, variant, ishora, yechim va xato izohlari UZ/RU. Bir savolning tarjimasi qo‘shimcha mustaqil savol hisoblanmaydi.

II klasterdagi har modul chuqurligi saqlandi; foydalanuvchi hujjatida III klaster aynan to‘rtta mavzu bo‘lgani uchun jami hajm to‘rtta modulga mos. Debugging va review vazifalari alohida o‘quv natijalariga ega.

## Qo‘shimcha amaliy resurslar

1. Uch bosqichli debugging challenge: sintaksis, mantiqiy va chegaraviy xato, gipoteza/jurnal va regressiya. Ataylab xato starter va alohida ishlaydigan o‘qituvchi yechimi bor.
2. 2–3 kishilik kutubxona loyihasi: vazifa va rol, modul shartnomasi, driver/navigator almashishi, branch/commit/review, konflikt simulyatsiyasi, integratsiya va himoya. Ishlaydigan in-memory o‘qituvchi namunasi bor.
3. Hujjatdan o‘rganish laboratoriyasi: berilgan StudyTools 1.0 API hujjati, lokal kod, oldindan bashorat, xato holati, yangi vaziyat va bilim qaydi. Python rasmiy str.split hujjati bilan alohida mashq ham bor.

Har birida UZ/RU o‘quvchi ish varag‘i, o‘qituvchi yechimi va to‘rtta 0–2 mezonli rubrika mavjud. Ochiq ishlar 80 savol soniga kirmaydi. Rubrika topshirilgan ishni baholaydi; sabr, shaxs yoki umumiy o‘rganish tezligini diagnostika qilmaydi.

[Python/Git ko‘prigi UZ](content/cluster3/bridge.uz.md) / [RU](content/cluster3/bridge.ru.md) oldingi psevdokoddan haqiqiy sintaksisga o‘tishni tushuntiradi. Kod va identifikatorlar ikkala tilda aynan bir xil.

## Foydalanish nusxalari

- To‘liq o‘qituvchi nusxalari: `3.1-mavzu.uz.md`–`3.4-mavzu.uz.md` va ruscha juftlari.
- O‘quvchi o‘qish/mashq nusxalari: `*.student.md`; savollarda kalit va variant izohlari chiqarilmaydi.
- Alohida javobsiz pre/post varaqlari: `*.checks.md`; ularda nazariya, namuna, ishora va yechim yo‘q.
- Draft banklar `*.v1.json`, source hashga bog‘langan locale `translations/`, ikki tilli ochiq ishlar `activities.v1.json` va qayta yaratish manbalari.

Tekshiruv varag‘ida precheck va postcheck alohida belgilanadi, ammo bir faylda; uni kerakli bosqichda ochishni o‘qituvchi/o‘quvchi nazorat qiladi. O‘qituvchi nusxasi va JSONlar studentga to‘liq tarqatiladigan payload emas. Offline fayllar platformadagi kirish nazoratini amalga oshirmaydi.

## Tekshiruv dalillari

`python -X utf8 docs/content/cluster3/verify_resources.py` muvaffaqiyatli o‘tdi:

- To‘rtta modul, 20 noyob ko‘nikma va dars, har ko‘nikmada 2/1/1 savol qamrovi, prerequisite grafigi, blueprint, pre/post ajratilishi va manba hashlari.
- Barcha ko‘rinadigan matnlarning UZ/RU qamrovi, kod bloklari va sonli konstantalari, variant IDlari va source hash mosligi.
- **12 sonli javob** mustaqil reference hisoblari bilan; **68 tanlovli savolda** aylantirishdan keyingi kalit mosligi. Variantlarning mazmuniy to‘g‘riligi va izohlari ichki tahririy ko‘rib chiqildi; bu avtomatik semantik isbot emas.
- **143 Python reference tekshiruvi:** debugging yechimlari, StudyTools normal/chegara/xato holatlari, str.split, kutubxonaning rad holatida o‘zgarmasligi va resurs saqlanishi. Talaba kodi yoki savol matni eval qilinmadi.
- **13 Git reference tekshiruvi:** vaqtinchalik mahalliy repozitoriyda staging/working tree/commit farqi, qayta add, remote yo‘qligi, merge joriy branchga ishlashi va haqiqiy konfliktni shartnoma asosida hal qilish.
- **14 salbiy holat** rad etildi: yetishmaydigan tarjima, bo‘sh sarlavha, yaroqsiz kalit, takror savol, locale option yo‘qligi, check ishorasi, noma’lum skill, prerequisite sikli, blueprint/pair xatosi, o‘zgargan konstanta/kod, noto‘g‘ri import holati va eskirgan hash.
- Hosil qilingan Markdownning manbalarga mosligi, lokal havolalar va o‘quvchi/tekshiruv savollarida kalit/feedback chiqmasligi.

[Mashina o‘qiydigan natija](content/cluster3/verification-result.json), [tahririy tekshiruv](content/cluster3/editorial-review.md).

## Amaliy chegaralar

Resurslar `resource_format=mindmetric-cluster3-draft-v1` formatida; **amaldagi backend importeriga hali moslashtirilmagan**. Hozirgi schema 2 faqat II klasterni qabul qiladi. [Integratsiyaga topshirish qaydi](content/cluster3/integration-handoff.md) texnik talablarni saqlaydi; uni yozish integratsiya bajarilganini anglatmaydi.

Backend, frontend, DB import/migratsiya, remote Git, push va Render deployi bu bosqichda bajarilmadi. I/II klaster fayllari va foydalanuvchining oldindan mavjud konfiguratsiya/recovery o‘zgarishlari o‘zgartirilmadi. Tekshiruv natijasi production yoki brauzer tekshiruvi deb ko‘rsatilmaydi.

Haqiqiy o‘quvchilar bilan pilot, tashqi metodist ekspertizasi va psixometrik kalibrlash o‘tkazilmagan. Mazmun kurs bilimlari va amaliy jarayonni mashq qildiradi; diagnostika ballari yoki shaxs xususiyatlari o‘sishini da’vo qilmaydi.
