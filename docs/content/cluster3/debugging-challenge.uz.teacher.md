# Uch bosqichli debugging challenge

O‘qituvchi nusxasi — yechimlar mavjud

[README](README.md)

## Maqsad

Xatoni tasodifiy tahrir bilan emas, kuzatuv, gipoteza va regressiya bilan tuzatish.

## Vositalar

- Python 3, matn muharriri; debugging-starter.py.txt dan mahalliy exercise.py nusxasi. Original o‘zgarmasin.

- Jurnal ustunlari: bosqich, kirish, kutilgan, haqiqiy, xato turi, gipoteza, bitta tahrir, qayta test, xulosa.

## Shartnoma

- 1-bosqich add(a, b) ikki son yig‘indisini qaytaradi. Tekshirish kirishlari: (2, 5), (-3, 3), (0, 0).

- 2-bosqich discount(price, percent): price >= 0; 0 <= percent <= 100. Foiz chegirilgan narx. Kirishlar: (200, 15), (200, 0), (200, 100), (0, 25). Shu cheklovdan tashqari validatsiya bu vazifaga kirmaydi.

- 3-bosqich can_borrow(available): available manfiy bo‘lmagan butun. Kamida bitta nusxa bo‘lsa True. Kirishlar: 0, 1, 2.

## Bosqichlar

1. Avval starterdagi sintaksis xatosini kuzating. 1-bosqich sababini yozing, bitta tahrir qiling va uning testlarini ishga tushiring.

2. 2-bosqichda kutilgan narxni qo‘lda hisoblang. Haqiqiy natija bilan farqini yozib, amallarni izlang.

3. 3-bosqichda 0, 1, 2 chegaralarini tekshiring. Har tuzatishdan keyin avvalgi bosqich testlarini ham qaytaring.

4. Birinchi mashqda 1-bosqich ishorasi: funksiya sarlavhasini ko‘ring. 2-bosqichda faqat kutilgan/haqiqiy jadval beriladi. 3-bosqichda ishora berilmaydi.

5. Test yana yiqilsa, ayni taxminni ko‘r-ko‘rona takrorlamang: yangi kuzatuv va yangi gipoteza yozing. Zarur bo‘lsa tanaffus qiling yoki aniq savol bilan yordam so‘rang.

## Topshiriladigan ish

- Tuzatilgan exercise.py; to‘ldirilgan jurnal; test natijalari; qaysi tuzatish nega kerakligini tushuntiruvchi qisqa qayd.

## Rubrika

- Sabab va dalil: 0 — yo‘q; 1 — qisman; 2 — uch bosqich uchun xato turi va aniq kuzatuv bor.

- Tuzatish: 0 — talab buzilgan; 1 — faqat oddiy holat; 2 — barcha berilgan kirishlar va cheklovlarda mos.

- Regressiya: 0 — qayta test yo‘q; 1 — ayrim holatlar; 2 — oldingi bosqichlar ham qayta tekshirilgan.

- Jarayon qaydi: 0 — yo‘q; 1 — tahrirlar bor, sabab yo‘q; 2 — gipoteza, tahrir va natija ajratilgan. Jami 8 gacha — ish dalili, sabr yoki shaxs tashxisi emas.

## O‘qituvchi yechimi

- 1-bosqich: def add(a, b): sarlavhasida : zarur. Natijalar 7, 0, 0.

- 2-bosqich: price - price * percent / 100. Natijalar 170, 200, 0, 0. Qo‘shish narxni oshirgan.

- 3-bosqich: available > 0. Natijalar False, True, True. >= bo‘sh omborga ham ruxsat bergan.

- debugging_reference.py — o‘qituvchi namunasi. Uni o‘quvchi ishga kirishishidan oldin ochmang. Qayta urinishda savol turi yoki asosiy shartnomani yashirin o‘zgartirmang.
