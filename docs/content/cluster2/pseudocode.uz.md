# 2-klaster uchun psevdokod qo‘llanmasi

Bu kurs yozuvi muayyan dasturlash tilida ishga tushirish uchun mo‘ljallanmagan. Kodni o‘qish va qiymatlarni kuzatish mashqlari uchun qoidalar quyidagicha.

| Yozuv | Ma’nosi |
|---|---|
| `x ← ifoda` | O‘ng tomonni hozirgi qiymatlarda hisoblab, x ga yozish |
| `==`, `!=`, `<`, `>`, `≤`, `≥` | Taqqoslash; o‘zgaruvchiga qiymat yozmaydi |
| `TRUE`, `FALSE` | Mantiqiy rost va yolg‘on |
| `AND`, `OR`, `NOT` | Ikkala shart; kamida bittasi; inkor. OR ikkala rost holatni ham qamraydi |
| `{ ... }` | Bitta boshqaruv konstruksiyasining tanasi; ichki qavslar o‘z blokini bildiradi |
| `;` | Ketma-ket buyruqlar ajratgichi |
| `INPUT x`, `OUTPUT x` | Kiritish va chiqarish; OUTPUT qiymatni o‘zgartirmaydi |
| `RETURN ifoda` | Funksiya natijasini qaytarib, shu chaqiruvni tugatish |
| `if shart {...} else {...}` | Faqat bitta tarmoq bajariladi |
| `else if` | Birinchi rost shart tanlanadi; keyingi shartlar tashlanadi |
| `switch x {case qiymat: ...; default: ...}` | Aniq mos bitta case, moslik bo‘lmasa default; keyingi case ga avtomatik o‘tish yo‘q |
| `for i ← a TO b {...}` | Butun qiymatlarni a dan b gacha 1 qadam bilan, ikkala chegara bilan; a > b da tana ishlamaydi |
| `while shart {...}` | Shart avval tekshiriladi; tana nol marta bajarilishi mumkin |
| `do {...} while shart` | Tana avval bajariladi; TRUE da takrorlanadi, FALSE da tugaydi |
| `a div b`, `a mod b` | Ushbu resursda a manfiy bo‘lmagan butun, b musbat butun: butun bo‘linma va qoldiq |

Arifmetikada qavs, ko‘paytirish/bo‘lish, qo‘shish/ayirish ustuvorligi ishlatiladi. Bir xil ustuvorlikda chapdan o‘ngga yuriladi. Mantiqiy shartlar qavs bilan yoziladi. Savolda alohida aytilmasa katta butun sonlar uchun toshib ketish hisobga olinmaydigan aniq arifmetika olinadi; haqiqiy tilda son turi va diapazoni tekshirilishi kerak.

**Til farqi:** ushbu `for ... TO` yuqori chegarani kiritadi; Python `range` yuqori chegarani kiritmaydi. Kursdagi `switch` keyingi tarmoqqa o‘tmaydi; boshqa tillarda qoidalar farq qiladi. Tarjimada operatorlar, o‘zgaruvchi nomlari va konstantalar o‘zgarmaydi. `n ≥ 0` kabi kirish sohasi rekursiyada ham majburiy.

**Blok-sxema:** oval — START/END; parallelogramm — INPUT/OUTPUT; to‘g‘ri to‘rtburchak — amal; romb — DECISION. Qarordan TRUE/FALSE yo‘llari chiqadi. Matnli sxemada har yo‘l va yakun alohida ko‘rsatiladi; ma’no faqat shakl yoki rangga bog‘lanmaydi.

## Mustaqil o‘qish manbalari

- [Python rasmiy qo‘llanmasi: boshqaruv oqimi](https://docs.python.org/3/tutorial/controlflow.html) — real til bilan solishtirish uchun. Kurs psevdokodi Python kodi emas.
- [MIT OpenCourseWare: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — keyingi chuqur o‘qish uchun algoritmlar kursi.
- [W3C WAI: foydalanuvchiga natija va xato xabarlari](https://www.w3.org/WAI/tutorials/forms/notifications/) — interfeys qayta aloqasini o‘rganish uchun.

Mavzu xaritasi — `Oqitish moduli.docx`; barcha dars, misol va savollar yangi mualliflik materiali. Yuqoridagi manbalardan savollar yoki katta matnlar ko‘chirilmadi. Havolalar 2026-10-31 kuni ochib tekshirildi.
