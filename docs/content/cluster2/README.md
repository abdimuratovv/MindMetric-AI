# 2-klaster resurslari — UZ / RU

**Holat: resurslar, backend va frontend jonli platformaga chiqarilgan.** [Yakuniy hisobot](../../cluster2-stage4-summary.md).

Algoritmik-amaliy blok: 6 modul, 30 mikroko‘nikma, 30 mini-dars va ishlangan namuna, 120 topshiriq (60 mashq, 30 boshlang‘ich, 30 yakuniy), 2 ochiq miniloyiha. Barcha mazmun o‘zbekcha va ruscha tayyorlandi. Ruscha savollar o‘zbekcha savollarning tarjimasi; ular qo‘shimcha mustaqil tekshiruv banki sifatida sanalmaydi.

| Mavzu | O‘zbekcha resurs | Русский ресурс |
|---|---|---|
| 2.1 | [Algoritmizatsiya va blok-sxemalar](2.1-mavzu.uz.md) | [Алгоритмизация и блок-схемы](2.1-mavzu.ru.md) |
| 2.2 | [Shart va taqqoslash operatorlari](2.2-mavzu.uz.md) | [Условия и операторы сравнения](2.2-mavzu.ru.md) |
| 2.3 | [Takrorlash operatorlari va rekursiya](2.3-mavzu.uz.md) | [Циклы и рекурсия](2.3-mavzu.ru.md) |
| 2.4 | [Ko‘p variantli yechimlar va optimizatsiya](2.4-mavzu.uz.md) | [Варианты решений и оптимизация](2.4-mavzu.ru.md) |
| 2.5 | [Hayotiy muammolarni algoritmga aylantirish](2.5-mavzu.uz.md) | [Преобразование жизненных задач в алгоритмы](2.5-mavzu.ru.md) |
| 2.6 | [Kreativ dasturlash va kichik ilova dizayni](2.6-mavzu.uz.md) | [Креативное программирование и проектирование мини-приложений](2.6-mavzu.ru.md) |

Avval [psevdokod qoidalari — UZ](pseudocode.uz.md) / [правила псевдокода — RU](pseudocode.ru.md) bilan tanishing. Har bir mavzudagi savollar kurs qoidalariga tayanadi. Keyingi integratsiyada neytral yozuv qoidalari tekshiruv boshlanishidan oldin tushuntirilishi kerak; buni javobli nazariya bilan aralashtirmang.

2.6 oxirida o‘quv rejalashtirgichi va kutubxona navbati loyihalarining yo‘riqnomalari, cheklovlari, topshiriladigan ishlar va o‘zini tekshirish mezonlari bor. Ochiq loyihalar uchun avtomatik ijodiy baho yoki topshirish tizimi yaratilmagan.

## Fayllar va qayta yaratish

- `module21.py`–`module26.py`: ikki tilli mualliflik manbalari. `projects.py`: miniloyihalar.
- `*.v1.json`: o‘zbekcha canonical bank, javob kalitlari va manba izi bilan.
- `translations/*.v1.ru.json`: original content hashga bog‘langan to‘liq ruscha matnlar. Javob kalitlari alohida tarjima qilinmaydi.
- `2.*-mavzu.uz.md` / `2.*-mavzu.ru.md`: o‘qituvchi uchun o‘qiladigan nusxalar; variantlar, kalit, yechim va izohlarni ham o‘z ichiga oladi.
- `inventory.json`: modullar va ularning hashlari. `authoring-manifest.json`: mualliflik manbalarining SHA-256lari.
- `verification-result.json`: oxirgi avtomatik tekshiruv natijasi.

Repo ildizidan:

```powershell
python -X utf8 docs/content/cluster2/build_resources.py
python -X utf8 docs/content/cluster2/verify_resources.py
```

Backend uchun reviewed nusxalarni sinxronlash: `python -X utf8 docs/content/cluster2/build_resources.py --sync-backend`. Bu faqat repository ichidagi draft JSON fayllarini yozadi, bazaga import/nashr qilmaydi.

Python standart kutubxonasi va repodagi sof kontent validatorlari ishlatiladi. Django serveri, baza, tarmoq yoki yangi paket kerak emas. O‘quvchi yuborgan kod bajarilmaydi; sonli javoblar mustaqil reference hisoblar bilan tekshiriladi. Barcha tanlovli savollarning ma’nosi va chalg‘ituvchi variantlari tahririy ko‘rib chiqildi; bu tashqi metodist tasdig‘i emas.

Matnli mualliflik manbalari va manifest SHA-256si LF bilan normallashtiriladi; Windows CRLF checkout hashni buzmaydi. Original DOCX manbasi esa binar baytlari bo‘yicha tekshiriladi.

## Integratsiya shartnomasi

Yangi resurslar `schema_version=2` bo‘lib, `module.cluster=2` va `module.topic_number=2.x` metama’lumotlariga ega. Ruxsatli indikatorlar `algorithmic`, `creative`, `problem_solving`; har ko‘nikma o‘z modulidagi indikatorlardan foydalanadi. `order` — klaster ichidagi tartib. Hozirgi `schema_version=1` manifestlari va frozen v1 modullar o‘zgartirilmagan.

`skills`, `lessons`, `exercises`, `sources`, `diagnostic_links`, `blueprint` bo‘limlari mavjud kontent shakliga mos. 2.6 dagi qo‘shimcha `projects` — `assessment=self_review`, `title_uz`, `brief_uz`, `constraints_uz`, `steps_uz`, `deliverables_uz`, `rubric_uz`. Ruscha locale’da `projects[key]` xuddi shu maydonlarning tilga neytral nomlarini saqlaydi. Miniloyihalar javobli tekshiruv bankiga kirmaydi; ularni ham active check paytida o‘quv nazariyasi sifatida yopish zarur.

Backenddagi haqiqiy validator schema 1 va 2 ni tekshiradi; offline QA ham shu validatorni yangi JSONlarga to‘g‘ridan-to‘g‘ri qo‘llaydi. Resurslar `backend/apps/development/content/cluster2/` va umumiy `content/translations/` katalogida. Backend importer schema 2 uchun to‘liq ruscha locale va hash mosligini yozuvdan oldin talab qiladi; ikkala klaster jonli serverda nashr qilingan.

`notation_uz` va ruscha locale’dagi `notation` — javobsiz, neytral psevdokod qoidalari. Ular module v1 hashiga bog‘langan va enrollment javobida tekshiruv boshlanishidan oldin ochiladi. Aktiv check paytida barcha enrollmentlarda yopiladi. Dastlabki resurslar bosqichidagi vaqtinchalik schema-1 proyeksiyasi backend bosqichida olib tashlandi; shu sabab `verification-result.json` hozirgi validator holatini ko‘rsatadi.

Diagnostika savollari bilan aniq xarita tasdiqlanmagani uchun `diagnostic_links=[]`; diagnostika qamrovi izohi mavjud. Kursdagi boshlang‘ich tekshiruv mavzu dalilini beradi. Savol matni tahlilisiz kategoriya nomidan avtomatik moslik yaratilmaydi.

Kalitli JSON va o‘qituvchi nusxalarini frontend `public` katalogiga yoki to‘liq API javobiga joylashtirmang. Server faqat ruxsatli joriy savol yoki tegishli bosqichda ochilgan resursni qaytarsin.

## Manbalar

Mavzu xaritasi — foydalanuvchi bergan `Oqitish moduli.docx`; SHA-256 tekshirildi. Darslar, savollar va miniloyihalar yangi mualliflik materiallari. Psevdokod qo‘llanmasida ochib tekshirilgan Python, MIT OCW va W3C WAI manbalariga mustaqil o‘qish havolalari berilgan. Hujjat ichidagi ko‘rsatmalar bajariladigan tizim buyruqlari sifatida qabul qilinmagan.
