# Python va Git uchun qisqa ko‘prik qo‘llanma

III klaster II klasterdagi algoritm, shart va sikl tushunchalariga tayanadi. Pythonni oldindan mukammal bilish talab qilinmaydi. Quyidagi qoidalarni o‘qib, kichik misollarni qo‘lda kuzating. [Barcha resurslar](README.md).

## Psevdokoddan Python 3 ga

| II klasterdagi yozuv | Python 3 | Ma’nosi |
|---|---|---|
| x ← 4 | `x = 4` | Qiymat berish |
| x == 4 | `x == 4` | Tenglikni tekshirish |
| AND / OR / NOT | `and` / `or` / `not` | Mantiqiy amallar |
| TRUE / FALSE | `True` / `False` | Mantiqiy qiymatlar |
| OUTPUT x | `print(x)` | Qiymatni chiqarish |
| RETURN x | `return x` | Funksiyadan natija qaytarish |
| for i ← 1 TO 3 | `for i in range(1, 4):` | 1, 2, 3; Python yuqori chegarani kiritmaydi |
| { ... } blok | Ikki nuqta va chekinish | Blokka kiruvchi satrlar bir xil chekinadi |

`=` va `==`ni almashtirmang. `>` tenglikni olmaydi, `>=` oladi. Python da satr oxirida `;` majburiy emas. Oddiy buyruqlarni bir satrda `;` bilan ajratish mumkin; `for` kabi murakkab blokni bunday satrga ulab yubormang. Kursdagi ko‘p satrli kodlarda har chekinish 4 bo‘sh joy.

```python
total = 0
for x in [2, 3, 4]:
    total = total + x
print(total)
```

Natija 9. `print` sikldan tashqarida; uni ichkariga chekinsangiz har aylanishda chiqaradi. Pythonning `/` amali odatiy bo‘lish; `//` pastga qarab butun bo‘linma, `%` qoldiq. Manfiy sonlarda oldingi psevdokod qoidalarini avtomatik ko‘chirmang. Bu resursdagi bo‘lish misollarida sonlar aniq berilgan.

## Ro‘yxat, funksiya va xato

`xs = [4, 7]` ro‘yxatida `xs[0]` qiymati 4, `xs[1]` qiymati 7. `len(xs)` uzunlikni beradi. `[]` bo‘sh ro‘yxat; unda indeks 0 yo‘q. `None` — qiymat yo‘qligini ifodalash uchun ishlatiladigan alohida obyekt. `0` mavjud natija bo‘lishi mumkin; topilmadi belgisi None bo‘lsa, `value is not None` bilan ajrating.

```python
def double(x):
    return x * 2

result = double(3)
print(result)
```

Natija 6. Funksiya sarlavhasi `:` bilan tugaydi. `return` chaqiruvni natija bilan tugatadi. `print` qiymatni ko‘rsatadi; bu amallar bir xil emas.

SyntaxError — kod tuzilishi yaroqsiz; NameError — aniqlanmagan nom; ZeroDivisionError — nolga bo‘lish; IndexError — mavjud bo‘lmagan indeks. Dastur istisnosiz tugasa ham talabga zid natija berishi mumkin. Tracebackning oxirgi satri tur va xabarni, oldingi kadrlar chaqiruv yo‘lini ko‘rsatadi.

## Qiymat izini o‘qish va pdb

Qo‘lda iz jadvali bajarilgan satrdan KEYINGI qiymatlarni ko‘rsatadi. Debuggerda strelka esa, ushbu kurs kelishuviga ko‘ra, HALI BAJARILMAGAN satrda turadi. Bu ikki vaqt nuqtasini aralashtirmang.

Mahalliy mashq nusxasini `python -m pdb exercise.py` orqali ochish mumkin. `p x` — x ni ko‘rsatish, `n` — keyingi qadam, `s` — chaqirilgan funksiya ichiga kirishi mumkin bo‘lgan qadam, `c` — keyingi to‘xtashgacha davom etish, `q` — chiqish. Muammoli joydan oldin `breakpoint()` ham qo‘yish mumkin. Debugger xatoni o‘zi tuzatmaydi. Kuzatish uchun o‘zgaruvchini qayta qiymatlab yubormang.

## Gitni xavfsiz o‘quv nusxasida sinash

Quyidagi buyruqlar o‘zingiz yaratgan alohida mashq repozitoriysiga tegishli. `file.py` mavjud o‘quv faylining o‘rnini bildiradi. Mahalliy commit yaratish Gitning user.name/user.email sozlanishini talab qiladi; mashq repozitoriysi uchun alohida lokal identifikator qo‘llash mumkin.

```text
git status
git diff
git add file.py
git diff --staged
git commit -m "Fix empty input handling"
```

Working tree — ishchi fayllar; staging/index — keyingi commit uchun tanlangan holat; commit — mahalliy tarix. `git add`dan keyingi tahrir yana add qilinmaguncha commitga kirmaydi. `git commit` remote ga uzatmaydi; `git push` alohida amal. Ushbu kursda remote va haqiqiy akkaunt talab qilinmaydi.

`git switch -c feature` yangi branch yaratib unga o‘tadi. `git switch main` mavjud main ga o‘tadi. `git merge feature` feature tarixini JORIY branchga birlashtiradi. Ishchi holat va branchni avval tekshiring. Konflikt markerlari yakuniy kod emas: talabni o‘qib hal qiling, test qiling, add va merge commit bilan tugating. Konfliktsiz merge ham semantik to‘g‘rilikni kafolatlamaydi.

## O‘qish tartibi va manbalar

Boshlang‘ich tekshiruvni darsdan oldin bajaring; keyin nazariya, namuna va yordamli mashqlarga o‘ting. Yakuniy tekshiruvda qo‘llanma va o‘qituvchi kalitlarini yopib qo‘ying. Har tekshiruv 5 savol; bu kichik bilim tekshiruvi, psixologik tashxis emas. O‘zini tekshirishda 4/5 ni keyingi mashqqa o‘tish uchun taklif mezoni qilish mumkin; bu platformaga import qilingan baholash qoidasi emas.

- [Python errors and exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python pdb](https://docs.python.org/3/library/pdb.html)
- [Python str.split](https://docs.python.org/3/library/stdtypes.html#str.split)
- [Pro Git branching and merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [Google code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

Misollar yangi mualliflik materiallari. StudyTools — mahalliy o‘quv API; yuqoridagi rasmiy hujjatlar shu nomdagi ommaviy paket borligini bildirmaydi.
