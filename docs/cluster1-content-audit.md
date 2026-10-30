# Birinchi klaster kontent auditi

Sana: 2026-10-28. Bosqich: 1. Holat: kontent tayyorlandi, mahsulotga e’lon qilinmagan.

## Natija

Beshta mavzu uchun 25 mikroko‘nikma xaritasi, tahrirlar ro‘yxati va 1.1-mavzu uchun mashinada o‘qiladigan kontent tayyorlandi. `content/cluster1/arithmetic-algebra.v1.json` ichida beshta mini-dars, har biriga ishlangan namuna, 10 ta mashq va beshtadan boshlang‘ich/yakuniy tekshiruv savoli bor. Manbadagi barcha 10 mashq izohli shaklga keltirildi; tekshiruv uchun 10 yangi savol yozildi.

Material tahririy va hisoblash tekshiruvidan o‘tkaziladi. Holati `draft`: tashqi metodist tasdig‘i va ilovadagi ko‘rinish tekshiruvi o‘rniga avtomatik nashr qilinmaydi. Ushbu bosqichda backend, migratsiya yoki frontend yaratilmaydi.

## Mikroko‘nikma xaritasi

Kalitlar tilga bog‘liq emas va keyingi kontentda ham aynan saqlanadi. Bog‘lanishlar tavsiyaviy; katalogdagi modullarni avtomatik yopmaydi.

| Modul | Mikroko‘nikma kaliti | Mazmuni | Tayanch ko‘nikma |
|---|---|---|---|
| 1.1 | arith-order | Amallar tartibi, daraja va ildiz | — |
| 1.1 | arith-fractions | Kasrlar va ratsional ifoda qiymati | arith-order |
| 1.1 | arith-substitution | Manfiy sonni ham qavs bilan o‘rniga qo‘yish | arith-order |
| 1.1 | arith-identities | Taqsimot, kvadrat va kub formulalari | arith-order |
| 1.1 | arith-equations | Chiziqli tenglama va proporsiya | arith-fractions, arith-substitution |
| 1.2 | logic-propositions | Mulohaza va rost/yolg‘on qiymat | — |
| 1.2 | logic-basic-operations | NOT, AND, OR | logic-propositions |
| 1.2 | logic-implication | Implikatsiya va ekvivalentlik | logic-propositions |
| 1.2 | logic-truth-tables | Rostlik jadvalini qurish | logic-basic-operations, logic-implication |
| 1.2 | logic-laws | De Morgan, yutilish va qo‘sh inkor | logic-basic-operations |
| 1.3 | sets-membership | Element, qism to‘plam va bo‘sh to‘plam | — |
| 1.3 | sets-operations | Birlashish, kesishish, ayirma | sets-membership |
| 1.3 | sets-complement | Universal va to‘ldiruvchi to‘plam | sets-membership |
| 1.3 | sets-venn | Venn diagrammasini o‘qish | sets-operations, sets-complement |
| 1.3 | sets-counting | Elementlar soni va qo‘sh hisoblash | sets-venn, arith-order |
| 1.5 | functions-domain | Funksiya va aniqlanish sohasi | arith-fractions, arith-substitution |
| 1.5 | sequences-arithmetic | Arifmetik progressiya hadi va yig‘indisi | arith-substitution |
| 1.5 | sequences-geometric | Geometrik progressiya hadi va yig‘indisi | arith-order |
| 1.5 | counting-factorial | Faktorial va o‘rin almashtirish | arith-order |
| 1.5 | counting-selection | Joylashtirish va kombinatsiyani farqlash | counting-factorial |
| 1.6 | matrices-shape | Qator, ustun, o‘lcham va element | arith-order |
| 1.6 | matrices-types | Kvadrat, diagonal va birlik matritsa | matrices-shape |
| 1.6 | matrices-addition | Qo‘shish va songa ko‘paytirish | matrices-shape |
| 1.6 | matrices-product | O‘lchamlar mosligi va ko‘paytirish | matrices-shape, arith-order |
| 1.6 | matrices-determinant | 2×2 determinant | matrices-shape, arith-order |

1.1 va 1.6 asosiy indikatori `math`, 1.2 — `logic`, 1.3 — `math`/`logic`. 1.5 uchun `math`; faqat sonli ketma-ketlik ko‘nikmalari mos `iq` savollariga bog‘lanadi. Bular kontent aloqalari, umumiy IQni oshirish isboti emas. Hozir 1.1 diagnostika aloqalari kontent faylida aniq kalitlar bilan berildi; qolgan to‘rtta moduldagi savollar bilan bog‘lash 4-bosqichda bajariladi.

## Manbalar auditi va tahrirlar

Manba katalogi: `D:/Downloads/Telegram Desktop/`. Original DOCX fayllari o‘zgartirilmadi. Rasmdagi matn va formulalar ham ko‘rib chiqildi.

| Manba | Aniqlangan masala | Qaror va holat |
|---|---|---|
| Oqitish moduli.docx | Uch klaster xaritasi bor; barcha mavzularning tayyor darsi yo‘q | Birinchi klasterdan beshta mavjud mavzu olindi; qolgan klasterlar tashqarida |
| 1.1-mavzu.docx | Nazariya qisqa, javoblar va ishlangan yechimlar yo‘q | Besh mini-dars, misollar va 20 savol uchun yechim tayyorlandi |
| 1.1, 6-mashq | (2x−3)/4 = (x+1)/2 tenglama 2x−3=2x+2, ya’ni −3=2 beradi | Xato yashirilmagan: “yechim yo‘q” javobli variantli mashqqa aylantirildi |
| 1.1, 7-mashq | Ko‘paytuvchilarga ajratish va x=3 dagi qiymat bir gapda noaniq so‘ralgan | To‘g‘ri ajratma va 19 qiymatni birga tanlash aniq so‘raldi |
| 1.1, 4-mashq | Ratsional ifodada maxraj cheklovi yozilmagan | Yechimda x≠0 va x≠3; berilgan x=4 mumkinligi tushuntirildi |
| 1.2-mavzu.docx | Yutilish va qo‘sh inkor mashqda bor, nazariyada yo‘q | 4-bosqichda qo‘shiladi; inkor qavslari ham tekshiriladi |
| 1.3-mavzu.docx | “A raqami”, tugallanmagan kesishish xossasi, munosabatlar mavzusi ochilmagan | 4-bosqichda atama va xossa tuzatiladi; munosabatlar nazariyasi keyingi nashrga qoladi |
| 1.5-mavzu.docx | Aniqlanish sohasi va geometrik progressiya yig‘indisi yetarli yoritilmagan | 4-bosqichda nazariya va yechimlar to‘ldiriladi |
| 1.6-mavzu.docx | “Birlashtirilgan (birlik)” atamasi, rasmdagi kesilgan savol | 4-bosqichda “birlik” deb tuzatiladi, savol tiklanadi yoki almashtiriladi |
| 1.4 | Alohida fayl yo‘q | Nashrga kirmaydi; mavzu tayyor deb belgilanmaydi |

## 1.1 mashqlarining javoblar ro‘yxati

| Manba mashqi | Kontent kaliti | Javob |
|---|---|---|
| 1 | arith-practice-01 | 20 |
| 2 | arith-practice-02 | 60 |
| 3 | arith-practice-03 | −35 |
| 4 | arith-practice-04 | 7/4 |
| 5 | arith-practice-05 | 9 |
| 6 | arith-practice-06 | Yechim yo‘q |
| 7 | arith-practice-07 | (x−2)(x²+2x+4); 19 |
| 8 | arith-practice-08 | 4 |
| 9 | arith-practice-09 | 16 |
| 10 | arith-practice-10 | 10 |

Har bir ko‘nikmaga ikki practice, bir precheck va bir postcheck biriktirilgan. Precheck va postcheck savollari shaklan/mohiyatan ajratildi: shunchaki manbadagi sonlarni almashtirish bilan cheklanilmadi. Juftlar qiyinligi tahririy baho; statistik tenglik yoki kalibrlash da’vosi yo‘q. Bitta tekshiruv savoli mikroko‘nikma bo‘yicha ishonchli alohida diagnoz uchun yetarli emas.

## Keyingi bosqichga topshiriladigan qarorlar

- Ma’lumotlar shartnomasi: `cluster1-content-contract.md`; kontent: `content/cluster1/arithmetic-algebra.v1.json`.
- Talabaga kalitlar, yechimlar, noto‘g‘ri javob izohlari va diagnostika xaritasi to‘liq kontent JSON orqali yuborilmaydi. U backend seed uchun.
- Birinchi mustaqil urinish va yordamdan foydalanish serverda alohida qayd etiladi; mashq balli diagnostika ballini yozmaydi.
- Practice tartibi ikki davrda beshtadan turli ko‘nikmani qoplaydi. Pilotda precheck/postcheckdan faqat bittadan to‘plam bor; yangi bank bo‘lmasa qayta mustaqil tekshiruv ochilmaydi.
- Keyingi bosqich: alohida backend ilovasi, modellar, migratsiya, ruxsatlar, admin va seed validatsiyasi. Faqat foydalanuvchi tasdig‘idan keyin boshlanadi.
