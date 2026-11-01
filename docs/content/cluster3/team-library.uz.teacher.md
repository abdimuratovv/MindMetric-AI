# Kutubxona uchun jamoaviy miniloyiha

O‘qituvchi nusxasi — yechimlar mavjud

[README](README.md)

## Maqsad

2–3 kishilik guruhda modul shartnomasi, Git, review va integratsiyani amalda qo‘llash.

## Vositalar

- Python 3, Git va alohida yangi lokal repozitoriy; haqiqiy talaba yoki kitobxon ma’lumotlari kerak emas. Remote ixtiyoriy.

- Boshlang‘ich catalog = {"b1": {"title": "Algorithms", "total": 1, "available": 1}}; loans = {}. loans kaliti (reader, book_id), qiymati musbat butun miqdor.

## Shartnoma

- find_book(catalog, book_id) yangi dict yoki None qaytaradi; asl catalog o‘zgarmaydi. borrow(catalog, loans, reader, book_id): ok, not_found yoki unavailable. return_book shu parametrlar bilan: ok, not_found yoki no_loan.

- Old shart: reader va book_id bo‘sh bo‘lmagan matn; catalog izchil, total va available manfiy bo‘lmagan butun; available <= total; mavjud qarzlar hisobga mos. Paralellik, saqlash bazasi va autentifikatsiya bu mashqqa kirmaydi.

- Muvaffaqiyatli berish available ni 1 kamaytiradi va qarzni 1 oshiradi. Qaytarish faqat shu reader qarzi bo‘lsa bajariladi. Rad holatida catalog va loans o‘zgarmaydi; nol qarz kaliti o‘chiriladi.

- Har kitob uchun available + barcha reader qarzlari yig‘indisi = total. Shu invariant har muvaffaqiyatli amaldan keyin saqlansin.

## Bosqichlar

1. Rollar: katalog va interfeys; berish/qaytarish; integratsiya/test. 2 kishi bo‘lsa integratsiya birga. Driver/navigator rolini almashing, har a’zo boshqa modulni ham review qilsin.

2. CONTRACT.md da imzo, qaytish kodi va rad holatini yozing. Har vazifa uchun mas’ul va qabul testini belgilang. Avval shartnomaga mos kichik stub bilan bog‘lanishni tekshiring.

3. Alohida branchlar va kichik commitlarda ishlang. git status, git diff va git diff --staged ni ko‘ring. Birlashtirishdan oldin hamkor reviewsi va test bo‘lsin.

4. Konflikt simulyatsiyasi: toza bazada POLICY.md ga display_limit=2 yozib commit qiling. review-a va review-b ayni bazadan chiqsin. Birida 3, boshqasida 5 qiling. main ga birini, keyin ikkinchisini merge qiling; konfliktni yakuniy kelishuv display_limit=4 bilan hal qiling. Bu ko‘rsatish limiti, qarz olish cheklovi emas.

5. Umumiy oqim: b1 topish → r1 ga berish → r2 ga takror berishni rad qilish → r1 qaytarishi → r2 ga berish. Yo‘q kitob va qarzsiz qaytarishni ham sinang.

6. Har a’zo o‘z modulini, boshqa modulga bog‘lanishini, bitta xato holatini va bitta review qarorini tushuntirsin.

## Topshiriladigan ish

- Kod; CONTRACT.md; vazifalar/rollar jadvali; kichik Git log va diff dalillari; konflikt yechimi qaydi; umumiy test natijalari; qisqa himoya. Commitlar soni bo‘yicha a’zolarni reyting qilmang.

## Rubrika

- Shartnoma: 0 — yo‘q; 1 — qisman; 2 — imzo, holat kodi va old shartlar mos.

- Integratsiya: 0 — umumiy oqim yo‘q; 1 — faqat oddiy yo‘l; 2 — umumiy yo‘l, rad holati va invariant tekshirilgan.

- Hamkorlik dalili: 0 — yo‘q; 1 — ish bo‘lingan, review yo‘q; 2 — rol almashish va dalilli o‘zaro review bor.

- Git va himoya: 0 — iz yo‘q; 1 — commit yoki tushuntirish yetishmaydi; 2 — mazmunli diff, konflikt sababi va har a’zoning tushuntirishi bor. Jami 8 gacha — loyiha rubrikasi.

## O‘qituvchi yechimi

- library_reference.py ishlaydigan o‘qituvchi namunasi; u real ko‘p foydalanuvchili tizim arxitekturasi sifatida berilmaydi.

- b1/r1 berish: ok, available=0, loans[("r1", "b1")]=1. r2 so‘rovi unavailable va ikkala holat o‘zgarmaydi. r1 qaytarishi ok, available=1, qarz kaliti o‘chadi. So‘ng r2 berish ok.

- Yo‘q kitobda not_found; o‘z qarzi yo‘q reader qaytarsa no_loan. Ikki holatda holat aynan saqlanadi. find_book natijasini tahrirlash asl katalogni o‘zgartirmasligi tekshiriladi.

- Konfliktning yakuni display_limit=4. Nega 3 yoki 5 emasligi kelishuvga asoslanib yoziladi. Merge muvaffaqiyati umumiy test o‘rnini bosmasligi himoyada so‘ralsin.
