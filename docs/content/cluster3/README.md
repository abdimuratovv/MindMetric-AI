# III klaster o‘quv resurslari

Shaxsiy-psixologik blok uchun to‘rtta mualliflik modul. Har birida **5 mikroko‘nikma, 5 dars, 5 ishlangan misol, 10 yordamli mashq, 5 boshlang‘ich va 5 yakuniy savol** mavjud. Jami **20 dars, 20 misol va 80 topshiriq**, to‘liq o‘zbekcha/ruscha. Qo‘shimcha uch amaliy ish avtomatik savollar soniga kirmaydi.

Avval [Python/Git ko‘prigi — UZ](bridge.uz.md) yoki [RU](bridge.ru.md)ni o‘qing. Asosiy tayanch: II klasterdagi algoritm, shart, sikl, kirish/chiqish va test tushunchalari. III klaster hujjatdagi to‘rtta mini-modulni qamraydi; olti modulga sun’iy kengaytirilmagan.

## O‘quvchi uchun

Boshlang‘ich savollarni darsdan oldin bajaring. Keyin dars va namuna, yordamli mashqlar, so‘ng yakuniy savollar. Precheck va postcheck bir varaqda aniq belgilangan; boshlang‘ich bosqichda yakuniy savollarni ochmaslikni o‘qituvchi yoki o‘quvchi nazorat qiladi. Bu fayllar offline resurslar, platformadagi sessiya himoyasi emas.

| Mavzu | O‘qish va mashq UZ | O‘qish va mashq RU | Javobsiz tekshiruv UZ | Javobsiz tekshiruv RU |
|---|---|---|---|---|
| 3.1 Kod tahlili va debugging | [Darslar](3.1-mavzu.uz.student.md) | [Уроки](3.1-mavzu.ru.student.md) | [Savollar](3.1-mavzu.uz.checks.md) | [Вопросы](3.1-mavzu.ru.checks.md) |
| 3.2 Kichik guruh loyihasi va Git | [Darslar](3.2-mavzu.uz.student.md) | [Уроки](3.2-mavzu.ru.student.md) | [Savollar](3.2-mavzu.uz.checks.md) | [Вопросы](3.2-mavzu.ru.checks.md) |
| 3.3 Diqqat va aniqlik uchun code review | [Darslar](3.3-mavzu.uz.student.md) | [Уроки](3.3-mavzu.ru.student.md) | [Savollar](3.3-mavzu.uz.checks.md) | [Вопросы](3.3-mavzu.ru.checks.md) |
| 3.4 Hujjatlar asosida yangi bilimni o‘zlashtirish | [Darslar](3.4-mavzu.uz.student.md) | [Уроки](3.4-mavzu.ru.student.md) | [Savollar](3.4-mavzu.uz.checks.md) | [Вопросы](3.4-mavzu.ru.checks.md) |

Har modulning birinchi yordamli mashqida nishonga yo‘naltiruvchi ishora, ikkinchisida qisqaroq tekshiruv savoli yoki mezon beriladi. Boshlang‘ich va yakuniy tekshiruvda ishora, kalit va xato variant izohi yo‘q. Har tekshiruv 5 savol, har to‘g‘ri javob 1; o‘zini tekshirishda 4/5 keyingi mashqqa o‘tish uchun tavsiya. Past bo‘lsa tegishli ko‘nikmaga qayting. Ayni postcheckni qayta bajarish mustaqil o‘sish o‘lchovi emas.

## O‘qituvchi uchun kalitlar

To‘liq nusxalarda barcha savol javoblari, yechim bosqichlari, xato izohlari va har bir variantning fikr-mulohazasi bor. Ularni tekshiruv paytida talabaga bermang; katalogdagi mavjudligi texnik kirish nazorati degani emas.

| Modul | UZ | RU |
|---|---|---|
| 3.1 | [To‘liq nusxa](3.1-mavzu.uz.md) | [Полная копия](3.1-mavzu.ru.md) |
| 3.2 | [To‘liq nusxa](3.2-mavzu.uz.md) | [Полная копия](3.2-mavzu.ru.md) |
| 3.3 | [To‘liq nusxa](3.3-mavzu.uz.md) | [Полная копия](3.3-mavzu.ru.md) |
| 3.4 | [To‘liq nusxa](3.4-mavzu.uz.md) | [Полная копия](3.4-mavzu.ru.md) |

## Uch amaliy ish

Har ishda maqsad, vosita, shartnoma, bosqich, topshiriladigan natija va 0–2 ballik to‘rtta mezondan iborat rubrika bor. Maksimum 8 — topshirilgan ish sifati mezoni; shaxs xususiyatlari o‘lchovi emas. Ochiq ishlar o‘qituvchi yoki o‘zini tekshirish uchun; avtomatik kod baholash yo‘q.

| Ish | O‘quvchi UZ / RU | O‘qituvchi UZ / RU |
|---|---|---|
| Debugging challenge | [UZ](debugging-challenge.uz.student.md) / [RU](debugging-challenge.ru.student.md) | [UZ](debugging-challenge.uz.teacher.md) / [RU](debugging-challenge.ru.teacher.md) |
| 2–3 kishilik kutubxona loyihasi | [UZ](team-library.uz.student.md) / [RU](team-library.ru.student.md) | [UZ](team-library.uz.teacher.md) / [RU](team-library.ru.teacher.md) |
| Hujjatdan o‘rganish laboratoriyasi | [UZ](documentation-lab.uz.student.md) / [RU](documentation-lab.ru.student.md) | [UZ](documentation-lab.uz.teacher.md) / [RU](documentation-lab.ru.teacher.md) |

Debugging uchun [ataylab xato starter](debugging-starter.py.txt)ni alohida `exercise.py` ga nusxalang. [Debugging yechimi](debugging_reference.py) va [kutubxona namunasi](library_reference.py) — o‘qituvchi uchun. [StudyTools 1.0 kodi](lab_studytools.py) — o‘quv laboratoriyasi uchun berilgan mualliflik API, ommaviy paket emas. Python kodi va identifikatorlar ikkala tilda bir xil, tushuntirishlar tarjima qilingan.

## Format va tekshirish

`*.v1.json` — o‘zbekcha banklar; `translations/*.v1.ru.json` — barcha ko‘rinadigan matnlarning hashga bog‘langan ruscha nusxalari. Kalitlar va to‘g‘ri javoblar asosiy bankda saqlanadi. [inventory.json](inventory.json) qamrovni, [authoring-manifest.json](authoring-manifest.json) mualliflik manbalari hashlarini qayd etadi. [activities.v1.json](activities.v1.json) ikki tilli ochiq ishlarni, jumladan o‘qituvchi yechimlarini ham saqlaydi: u to‘liq student payloadi emas.

Qayta yaratish va QA uchun loyiha ildizidan:

```text
python -X utf8 docs/content/cluster3/build_resources.py
python -X utf8 docs/content/cluster3/verify_resources.py
```

Python standart kutubxonasi va lokal Git kerak. Tekshiruv vaqtinchalik lokal Git repozitoriysini yaratib tozalaydi; ilova bazasi yoki remote ga murojaat qilmaydi. O‘quvchi kodi va savol matni `eval` orqali bajarilmaydi. [Tahririy tekshiruv](editorial-review.md) va [avtomatik natija](verification-result.json) tekshiruv chegaralarini ko‘rsatadi.

**Ikki alohida format mavjud.** Katalog ildizidagi `resource_format=mindmetric-cluster3-draft-v1` banklar standalone mualliflik nusxalari, importerga bevosita berilmaydi. Keyingi integratsiyada [export_platform.py](export_platform.py) va [platform/inventory.json](platform/inventory.json) qo‘shildi: platforma nusxalari haqiqiy backend schema 3 bilan tekshiriladi. Eksportni standalone builddan keyin bajaring. I/II klaster resurslari o‘zgartirilmagan. [Integratsiya va chiqarish hisoboti](../../cluster3-integration-release.md).

## Manbalar va mazmun chegarasi

Mavzu xaritasi foydalanuvchi taqdim etgan `Oqitish moduli.docx`ning III klasteridan olingan; nazariya, misol, test va loyihalar yangi mualliflik materiali. [Tasdiqlangan loyiha](../../cluster3-design.md) va [ish rejasi](../../cluster3-development-plan.md).

Tekshirilgan qo‘shimcha o‘qish: [Python xatolari](https://docs.python.org/3/tutorial/errors.html), [pdb](https://docs.python.org/3/library/pdb.html), [str.split](https://docs.python.org/3/library/stdtypes.html#str.split), [Pro Git](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging), [Google review qo‘llanmasi](https://google.github.io/eng-practices/review/reviewer/looking-for.html). Rasmiy sahifalar inglizcha; asosiy resurslarning barcha mazmuni UZ/RU berilgan.

Kursdagi bilimni egallash diagnostik IQ, sabr, diqqat yoki umumiy o‘rganish tezligi ballari o‘sganini isbotlamaydi. Jamoaviy ko‘nikmalarni baholashda amaliy hissa, muloqot va tekshiriladigan ish dalillari kerak; bitta test yoki commitlar soni yetmaydi.
