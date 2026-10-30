# 5-bosqich hisoboti: shaxsiy reja va interfeys

Sana: 2026-10-30. Holat: bajarildi. Asos: foydalanuvchining 5-bosqichga o‘tish tasdig‘i va [development plan](cluster1-development-plan.md).

## Qilingan ishlar

- `recommendations.py` va `GET /api/development/plan/` yaratildi. Talaba eng dolzarb ikki modulni, tavsiya sababini va to‘liq katalogni ko‘radi. Boshlangan mashg‘ulotni davom ettirish birinchi o‘rinda.
- Ko‘nikma bo‘yicha diagnostik tavsiya faqat tugallangan testning joriy siklidagi kamida uchta alohida, xaritada mos savolga tayanadi. Eski sikllar, tugallanmagan test va boshqa talabaning javoblari hisoblanmaydi. Umumiy past math/IQ bali o‘zidan o‘zi muayyan mavzuni sust deb belgilamaydi.
- Dalil yetarli bo‘lmasa boshlang‘ich tekshiruv tavsiya qilinadi; soxta nol natija berilmaydi. Matritsalarga mos diagnostika savoli yo‘qligi hisobga olindi. IQ faqat mos ketma-ketlik ko‘nikmalariga bog‘lanadi.
- Tugallangan precheck/postcheck xatolari ko‘nikma va darslar bo‘yicha ko‘rsatildi. Har ko‘nikmadagi bitta tekshiruv savoli dastlabki kuzatuv sifatida belgilandi. Yangi tugallangan tekshiruv eski diagnostik dalildan ustun; undan keyingi yetarli yangi diagnostika tavsiyani yangilashi mumkin. Practice mustaqil o‘sish dalili hisoblanmaydi.
- Xato qilingan ko‘nikma va tasdiqlanmagan mahalliy tayanch ko‘nikma darslari tartib bilan tavsiya etiladi. To‘g‘ri javob berilgan tayanch darslar majburiy takrorlatilmaydi. Precheck 80% dan past bo‘lsa tegishli darslarni yakunlash practice bosqichini ochadi; boshqa darslar ham ochiq. 80% qoidasi saqlandi.
- Boshqa moduldagi tayanch ko‘nikmada ham tasdiqlangan qiyinchilik bo‘lsa, u bog‘liq mavzudan oldin qo‘yiladi. Avtomatik enrollment va katalogga qattiq cheklov kiritilmadi. Modulni boshlash sababi serverda hisoblanib o‘zgarmas snapshot sifatida saqlanadi.
- Shaxsiy reja kartalari, yakunlangan modullar ko‘rsatkichi, ko‘nikma holati/manbasi/javoblar soni, tavsiya darsga havolalar va klaviatura fokusi qo‘shildi. Natijalar sahifasidagi kirish “Rivojlanish rejam” deb nomlandi; sidebar va avvalgi integratsiya saqlandi.
- O‘zbekcha/ruscha interfeys va oddiy javob tekshiruvi xabarlari tayyorlandi. Kurs kontenti o‘zbekcha ekanligi ruscha interfeysda aniq ko‘rsatiladi.
- Bir talabada bir vaqtda faqat bitta aktiv mashg‘ulot ochiladi. Tekshiruv davomida barcha modullardagi nazariya, oldingi yechimlar va ko‘nikma tafsilotlari yashiriladi; davom etayotgan sessiyaga qaytish tugmasi bor.

## Tekshirish natijalari

- Izolyatsiyalangan SQLite bazada 95 ta backend testi muvaffaqiyatli o‘tdi. Yangi testlar dalil yetarliligi, sikl va talaba ajratilishi, IQ mosligi, tayanch dars tartibi, ikki darsdan keyin practice ochilishi, yangi dalil ustuvorligi, tekshiruvdagi yashirish, ruscha validatsiya va GET so‘rovlarining yozmasligini qamraydi.
- Django system check: muammo yo‘q. `makemigrations --check --dry-run`: yangi migratsiya kerak emas.
- Frontend production build muvaffaqiyatli. Oldindan mavjud 500 kB dan katta bundle ogohlantirishi saqlanadi.
- Haqiqiy Chrome brauzerida React/Django oqimi vaqtinchalik bazada tekshirildi: beshta modul, jami 40 javob, boshlang‘ich 0% → yakuniy 80%, +80 foiz punkt. Bu faqat sintetik test ssenariysi; mahsulot samaradorligi natijasi emas.
- Refresh/resume, noto‘g‘ri javob formatini tuzatish, server saqlagan javob javobi tarmoqda yo‘qolganda aynan o‘sha UUID bilan retry, yordamli practice, uz/ru almashtirish va 390 px mobil ko‘rinish tekshirildi. JavaScript xatolari va gorizontal chiqib ketish kuzatilmadi.
- Brauzer dalillari: `C:/Users/Asus/.codex/visualizations/2026/10/28/01a18264-3f77-7a02-a3d2-c4d4e2010e21/stage5-browser/`; `result.json`, katalog/reja, dars, mashq va hisobot rasmlari saqlandi.
- Testdagi avvaldan mavjud qisqa lokal JWT secret va yo‘q `staticfiles` katalogi haqidagi ogohlantirishlar testlarni to‘smadi; staging konfiguratsiyasi 6-bosqichda tekshiriladi.

## Ma’lumotlar holati va chegaralar

Asosiy lokal baza faqat o‘qib tekshirildi: beshta modul draft, enrollment soni nol. Accounts/assessments/scoring guruhidagi 24 jadvalning SHA-256 qiymati 4-bosqich backupi bilan teng: `bcefc283b9911dcc03499c6c94ac25f71671b9d7060613a46b7799577f5272af`. Avvalgi diagnostika va ballar o‘zgarmadi. Pilot flagining standart holati o‘chiq; real bazada modullar e’lon qilinmadi.

Ko‘nikmaga uchta javob va modulga 80% kabi chegaralar mahsulot qoidalari; ilmiy kalibrlangan qobiliyat o‘lchovi emas. O‘sish modul tekshiruvidagi foiz punktida ko‘rsatiladi, umumiy IQ o‘sishi deb talqin qilinmaydi. Yangi postcheck banki tugasa bir xil savollar bilan mustaqil o‘sish qayta tasdiqlanmaydi.

## Navbatdagi bosqich

6-bosqich — yakuniy tekshiruv va pilot tayyorgarligi: productionga mos PostgreSQLda parallel so‘rov/lock sinovlari, staging migratsiyasi va seed, konfiguratsiya va mavjud test oqimlari, kichik guruh bilan pilot hamda topilgan muhim tuzatishlar. Staging/pilot muhiti imkoniyatlari tekshiriladi; haqiqiy foydalanuvchi kuzatuvi avtomatik test natijasi bilan almashtirilmaydi.

6-bosqich boshlanmadi. Davom etish uchun foydalanuvchi tasdig‘i kutiladi.
