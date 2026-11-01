# Hujjatdan yangi API ni o‘rganish

O‘quvchi ish varag‘i

[README](README.md)

## Maqsad

Berilgan kichik hujjatdan qoida topib, yangi vaziyatda mustaqil qo‘llash.

## Vositalar

- Python 3 va lab_studytools.py; internet shart emas. StudyTools 1.0 — ushbu kursning mualliflik API si; pip bilan o‘rnatilmaydi.

- Import: from lab_studytools import take, find, clip. Quyidagi hujjat asosiy manba.

## Shartnoma

- take(items, limit=2): items ro‘yxat; dastlabki ko‘pi bilan limit elementdan yangi sayoz ro‘yxat qaytadi. Elementlar o‘zi chuqur nusxalanmaydi. items o‘zgarmaydi. limit >= 0 butun, bool emas; manfiyga ValueError, boshqa turga TypeError.

- find(items, target, default=None): items ro‘yxat; == bo‘yicha birinchi mos elementning noldan indeksini qaytaradi. Moslik yo‘q bo‘lsa default. Kirish o‘zgarmaydi.

- clip(x, low=0, high=10): bu laboratoriyada faqat chekli int/float sonlar beriladi; low <= high. Oraliq yopiq; pastda low, yuqorida high, ichkarida x qaytadi. low > high — ValueError. Kirish o‘zgarmaydi.

- Versiya taqqoslash kartasi: faqat simulyatsiyadagi 2.0 take(items, *, count=2) nomli count talab qiladi. Lokal kod faqat 1.0 ni bajaradi.

## Bosqichlar

1. Dastlab ishga tushirmasdan natijani taxmin qiling: take([7, 8, 9]); take([7], limit=3); find([4, 4, 9], 4); find([], 2, default=-1); clip(15, low=3, high=12).

2. Keyin bitta chaqiruvni ishga tushirib, bashorat bilan solishtiring. Qaysi hujjat jumlasi javobni berganini belgilang.

3. Xato holatlarini oldindan nomlang va sinang: take([1], limit=-1); take([1], limit=True); clip(5, low=8, high=2). Har biri uchun sababni yozing.

4. Yangi vaziyat: tasks=["A", "B", "C", "D"]. Dastlabki 3 topshiriqni ko‘rsating; "A" topilganini indeks 0 bo‘lsa ham to‘g‘ri aniqlang; 14 ballni [0, 10] ga cheklang.

5. Rasmiy hujjat mashqi: Python str.split bo‘limini oching. sep va maxsplit ma’nosini o‘qing. Python 3 da "a,b,c".split(",", maxsplit=1) uchun natijani avval yozib, keyin tekshiring. Internet bo‘lmasa help(str.split)dan foydalaning.

6. Savol, versiya, imzo, ishlagan misol, xato/chegara va manbadan iborat bilim qaydi yozing. Vaqtni ixtiyoriy o‘zingiz uchun qayd etishingiz mumkin; aniqlik birinchi o‘rinda.

## Topshiriladigan ish

- Bashorat/haqiqiy natija jadvali; kichik lab_solution.py; xatolar sababi; yangi vaziyat yechimi; str.split qaydi va bilim kartasi.

## Rubrika

- Hujjatdan dalil: 0 — taxmin; 1 — ayrim javoblar; 2 — har javob shartnomaga bog‘langan.

- Aniqlik: 0 — asosiy natijalar noto‘g‘ri; 1 — qisman; 2 — berilgan natijalar va istisnolar to‘g‘ri.

- Ko‘chirish: 0 — faqat ko‘chirilgan misol; 1 — yangi vaziyatning bir qismi; 2 — topshiriq, indeks 0 va ball chegarasi to‘g‘ri.

- Qayd: 0 — yo‘q; 1 — versiya yoki cheklov yetishmaydi; 2 — qayta foydalanishga yetarli. Jami 8 gacha — ish rubrikasi, umumiy o‘rganish tezligi bahosi emas.

## Ish qaydi

| Kirish | Kutilgan | Haqiqiy | Gipoteza / qaror | Qayta test |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
