# 2-klaster tahririy tekshiruvi

Sana: 2026-10-31. Bu muallifning ichki kontent tekshiruvi, tashqi metodist ekspertizasi yoki psixometrik kalibrlash emas.

| Modul | Ko‘rib chiqilgan mazmun | Yechim va chegaralar |
|---|---|---|
| 2.1 | Kirish/chiqish, dekompozitsiya, assignment, blok-sxema, trace | Nusxalangan qiymat va keyingi yangilanish ajratildi; INPUT/OUTPUT va romb vazifalari tekshirildi; maksimumdagi yetishmaydigan yo‘l uchun qarshi misol bor |
| 2.2 | Taqqoslash, mantiq, if, ichma-ich shart, switch | ≥/>, OR/AND, bloklanmagan rol qavslari, birinchi rost tarmoq va default mosligi tekshirildi; faqat bitta javob to‘g‘ri bo‘lishi uchun inkor savolining chalg‘ituvchi varianti aniqlashtirildi |
| 2.3 | for, while, do-while, nested, recursion | TO yuqori chegarani kiritadi; o‘suvchi siklda teskari oraliq bo‘sh; while nol marta, do-while kamida bir marta; div butun; rekursiv tayanch va boshlang‘ich chaqiruv ham sanaladi |
| 2.4 | Mos spetsifikatsiya, vaqt, xotira, reuse, tanlash | Ketma-ket va ichma-ich ish ajratildi; qo‘shimcha xotiradan kirish chiqarildi; tayyorlash narxi umumiy xarajatga kiritildi; yaroqsiz tez variant mos deb olinmadi |
| 2.5 | Shartnoma, validation, taxi, ATM, tests | Tarifda faqat ortiqcha masofa narxlanadi; bazadan past masofaga manfiy qo‘shimcha yo‘q; ATM rad holatida balans o‘zgarmaydi; nol so‘rov musbatlikdan o‘tmaydi |
| 2.6 | Ehtiyoj, funksiya, holat, mezon, prototype | Success tasdiqlanmaguncha berilmaydi; bo‘sh natija xato emas; majburiy talab ballardan ustun; kichik kuzatuv barcha foydalanuvchi haqida hukm bermaydi |

Barcha 64 tanlovli savolda to‘g‘ri variant va har bir chalg‘ituvchi variantning izohi o‘qib ko‘rib chiqildi. Variant pozitsiyalari aylantiriladi; doim birinchi variantni to‘g‘ri qilish qoidasi yo‘q. Barcha 56 sonli javob manba matni bajarilmasdan, alohida hisoblar/chegaralangan reference dasturlar bilan tekshirildi.

30 ishlangan namunada kirish, bosqichlar va javob tahririy solishtirildi. Miniloyihalarda ikki tilda vazifa, cheklovlar, bosqichlar, natija materiallari va o‘zini tekshirish mezonlari borligi tekshirildi.

Tarjimada bir `OUTPUT` tokeni oddiy gapga aylangan edi — kod ko‘rinishi tiklandi. Bir yechimda raqam o‘rnida ruscha son so‘zi ishlatilgan edi — konstantalarni qat’iy avtomatik solishtirish uchun bir xil raqam ko‘rinishi olindi. Ruscha va o‘zbekcha operand/operatorlar, konstantalar, variant IDlar va yechim bosqichlari mosligi qayta tekshirildi.

Boshlang‘ich/yakuniy savollar maqsad va kalit bo‘yicha ajratilgan, barcha mikroko‘nikmalarda 2/1/1 qamrov bor. Ba’zi savollar o‘xshash konstruksiyani boshqa yo‘l yoki chegarada tekshiradi; juftlar statistik tenglashtirilgan deb aytilmaydi. Har mavzuda bitta precheck va bitta postcheck to‘plami bor; tarjima yangi mustaqil test emas.

Platforma oqimi, mobil render, PostgreSQL importi va jonli RU/UZ almashishi hali tekshirilmagan: ular resurslardan keyingi integratsiya bosqichlaridir. `verification-result.json`dagi natija aynan offline resurs tekshiruvi.
