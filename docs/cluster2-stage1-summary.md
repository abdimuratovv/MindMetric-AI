# 2-klaster, 1-bosqich: ikki tilli resurslar

Sana: 2026-10-31. Holat: resurslar tayyorlandi va offline tekshirildi; backend/frontend integratsiyasi boshlanmagan.

## Natija

Manba `Oqitish moduli.docx` dagi II klaster xaritasi asosida oltita yangi mualliflik modulining to‘liq UZ/RU nusxasi yaratildi:

| Mavzu | Mazmun | Dars / namuna | Mashq / precheck / postcheck |
|---|---|---|---|
| 2.1 | Algoritmizatsiya va blok-sxemalar | 5 / 5 | 10 / 5 / 5 |
| 2.2 | Shart va taqqoslash operatorlari | 5 / 5 | 10 / 5 / 5 |
| 2.3 | Takrorlash operatorlari va rekursiya | 5 / 5 | 10 / 5 / 5 |
| 2.4 | Ko‘p variantli yechimlar va optimizatsiya | 5 / 5 | 10 / 5 / 5 |
| 2.5 | Hayotiy muammolarni algoritmga aylantirish | 5 / 5 | 10 / 5 / 5 |
| 2.6 | Kreativ dasturlash va kichik ilova dizayni | 5 / 5 | 10 / 5 / 5 |

Jami **30 mikroko‘nikma, 30 dars, 30 ishlangan namuna, 120 topshiriq va 2 ochiq miniloyiha**. Barcha dars, misol, savol, variant, ishora, yechim va xato izohlari ikki tilda. Bir savolning tarjimalari bitta topshiriq hisoblanadi.

Har darsda tushuntirish va qadamli namuna, har ko‘nikmada ikki yordamli mashq hamda alohida boshlang‘ich/yakuniy topshiriq bor. 2.6 da internetsiz o‘quv rejalashtirgichi va kutubxona navbati loyihalarining yo‘riqnomasi, cheklovlari, topshiriladigan natijalari va o‘zini tekshirish mezonlari qo‘shildi. Ochiq loyihalar avtomatik baholanadigan savollar sifatida ko‘rsatilmaydi.

## Foydalaniladigan fayllar

- [Resurslar ko‘rsatkichi — barcha UZ/RU mavzular](content/cluster2/README.md).
- [Psevdokod qo‘llanmasi — UZ](content/cluster2/pseudocode.uz.md) / [RU](content/cluster2/pseudocode.ru.md).
- `docs/content/cluster2/*.v1.json` — canonical banklar; `translations/*.v1.ru.json` — hashga bog‘langan ruscha resurslar.
- `module21.py`–`module26.py`, `projects.py`, `authoring.py` va `build_resources.py` — qayta yaratish manbalari.
- [Tahririy tekshiruv](content/cluster2/editorial-review.md), [modullar ro‘yxati](content/cluster2/inventory.json), [avtomatik natija](content/cluster2/verification-result.json).

O‘qituvchi nusxalarida javoblar va yechimlar ham bor; platformada ular to‘liq student JSON sifatida tarqatilmaydi. Birinchi klaster canonical resurslari va frozen versiyalari o‘zgartirilmadi.

## Tekshiruv dalillari

`python -X utf8 docs/content/cluster2/verify_resources.py` muvaffaqiyatli o‘tdi:

- 6 modul va har birida 5 ko‘nikma/dars, 20 savol, 2/1/1 mikroko‘nikma qamrovi; kalitlar, prerequisite grafigi va blueprint tekshirildi.
- Ruscha qamrov, manba hash, sonli konstantalar, savollardagi boshqaruv operatorlari, variant IDlari va yechim bosqichlari mosligi tekshirildi.
- Barcha **56 sonli javob** alohida reference hisoblar bilan tekshirildi; bankdagi matn yoki talaba kodi bajarilmadi.
- **64 tanlovli savol** va chalg‘ituvchi variantlarning mazmuni tahririy ko‘rib chiqildi. Bu avtomatik semantik isbot yoki tashqi metodist tasdig‘i emas.
- Yetishmaydigan tarjima, noto‘g‘ri hash/indikator, grading override, check hint, aralash pre/post bank, o‘zgargan konstantalar/operator, prerequisite sikli va loyiha tarjimasi yo‘qligi kabi **11 salbiy holat** rad etildi.
- Foydalanuvchi bergan curriculum faylining SHA-256si va mualliflik manbalarining hash manifesti tekshirildi.

Manbalar yangi mualliflik ishlari sifatida belgilandi. Qo‘shimcha o‘qish havolalari Python rasmiy qo‘llanmasi, MIT OCW va W3C WAI sahifalarida ochib tekshirildi; to‘liq matn yoki tayyor test banklari ko‘chirilmadi.

## Integratsiyaga topshiriladigan qarorlar

Yangi banklar `schema_version=2`, `cluster=2` va `topic_number=2.x` metama’lumotlari bilan tayyor. Amaldagi importer hali schema 2 ni qo‘llamaydi; uni rad etishi ham tekshirildi. Offline tekshiruv eski validatorning faqat umumiy kontent shaklini xotiradagi proyeksiyada qayta ishlatadi; bu production import tekshiruvi emas.

Keyingi bosqichda haqiqiy schema-2 validator/importer, klaster metama’lumoti va ikki tilli locale yuklash implementatsiya qilinadi. Neytral psevdokod qoidalarini boshlang‘ich tekshiruvdan avval taqdim etish, miniloyihalarni study resursi sifatida ochish va active check paytida yopish talab qilinadi. Diagnostik savol xaritasi tasdiqlanmaguncha boshlang‘ich tekshiruv ishlatiladi.

Bu bosqichda bazaga yozuv, backend kodi/migratsiya, frontend o‘zgarishi, push yoki deploy bajarilmadi. PostgreSQL va jonli brauzer tekshiruvlari keyingi integratsiya bosqichlariga tegishli. Oldindan mavjud recovery/konfiguratsiya fayllari bu ishga qo‘shilmadi.

Keyingi bosqich: foydalanuvchi tasdig‘idan so‘ng **2-bosqich — backend integratsiyasi**.
