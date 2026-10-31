# 2-klaster, 3-bosqich: frontend integratsiyasi

Sana: 2026-10-31. Holat: frontend implementatsiyasi, production build va lokal haqiqiy brauzer tekshiruvlari tugadi. Push/deploy hali bajarilmadi.

## Natija

- Rivojlanish sahifasida I/II klaster tanlovi bor. Har klaster o‘zining oltita modulini ko‘rsatadi; katalog, shaxsiy reja va ochilgan modulda serverdagi `topic_number` ishlatiladi. Endi II klaster kartalari 1.x deb belgilanmaydi.
- Shaxsiy reja ikkala klaster uchun umumiy qoladi; matnda bu tushuntiriladi. Boshqa klasterni ko‘rish aktiv mashg‘ulotni yashirincha tugatmaydi yoki yangi sessiya yaratmaydi. Reja aktiv checkga qaytishni taklif qiladi.
- `ClusterCatalogue.jsx` katalog va klaster tanlovini, `LearningResources.jsx` notation va miniloyihalarni ko‘rsatadi. Asosiy sahifa mavjud API/session boshqaruvini ishlatadi. Eski backenddan `clusters`/`topic_number` kelmasa I klaster uchun fallback saqlangan.
- Psevdokod qoidalari tekshiruvdan oldin ko‘rinadi. Darsdan keyingi ikkita miniloyiha vazifa, cheklov, bosqichlar, taqdim etiladigan ishlar va o‘zini tekshirish mezonlari bilan beriladi. Ularning testga avtomatik ball qo‘shmasligi tushuntiriladi.
- RU/UZ tanlovi katalog, nazariya, misol, savol/variant, yordam, feedback va loyiha mazmunini almashtiradi. Interfeysning yangi yozuvlari ham ikkala tilda.
- Tanlangan klaster, dars, ochilgan namuna va miniloyihalar shu foydalanuvchi uchun sessionStorage’da saqlanadi. Yuborilmagan sonli yoki variantli javob alohida draft sifatida tiklanadi; serverga yuborilgan UUID/payload retry holatidan ajratilgan. Javob qabul qilingach draft o‘chiriladi.
- Klaster almashtirib qaytganda va sahifa yangilanganda joriy mashg‘ulot/draft saqlanadi. Faol check paytida server yopgan dars, notation va loyihalar UI’da ham ko‘rsatilmaydi. Bu qoida har ikki klaster yo‘nalishida tekshirildi.
- Mavjud Manrope/Montserrat uslubi saqlandi; II klaster uchun yashil aksent va matn sifatida o‘qiladigan psevdokod namunalari qo‘shildi. Klaster tugmalari va native disclosure’lar klaviatura bilan ishlaydi. Mobil loyiha ustunlari bitta ustunga o‘tadi. Yangi frontend kutubxonasi qo‘shilmadi.

## Tekshiruv dalillari

`npm run build` muvaffaqiyatli. Yakuniy bundle `index-BzgJ40dy.js`, 939.95 kB, gzip 256.61 kB. Avvaldan mavjud 500 kB chunk ogohlantirishi qolgan; build xatosi yo‘q.

Haqiqiy headless Chrome, React/Vite va Django bilan ikkita ajratilgan SQLite fixture bazada tekshirildi. Ular `backups/` ostida yaratilgan; asosiy SQLite yoki Neon bazasi ishlatilmagan. JWT faqat test fixture foydalanuvchisiniki. Har sinov oxirida serverlar va brauzer yopiladi.

1. `browser_smoke.py --all-modules` — **muvaffaqiyatli, 45 javob**. I klasterning oltita moduli, birinchi modulning to‘liq oqimi, 1.1/1.6 ruscha resurslari, invalid numeric tuzatish, server qabul qilgan lekin javobi uzilgan POSTni ayni UUID bilan qaytarish, refresh va mobil holatlar saqlangan. JS xatosi va overflow yo‘q.
2. `browser_cluster2_smoke.py` — **muvaffaqiyatli, 50 javob**. Katalogda jami 12 modul, har tanlovda oltita to‘g‘ri raqamlangan mavzu. II klasterning barcha oltita prechecki, **30 dars va 30 misolning har biri UZ/RU matni**, ikki miniloyiha va 2.6 modulining precheck → study → practice → postcheck → completed oqimi tekshirildi. Radio va numeric draftning refreshdan keyin tiklanishi, klasterlar orasidan qaytish, ochiq dars/misol/loyiha, yordam/feedback til almashtirish, I→II va II→I check himoyasi tekshirildi. Klaster va loyiha boshqaruvi klaviaturada ham ishladi. JS xatosi va 390 px mobil overflow yo‘q.

Bu 95 javob sun’iy test fixture’larida; haqiqiy talabaning o‘sish natijasi sifatida talqin qilinmaydi. Oldingi backend bosqichidagi 137 PostgreSQL testi alohida [2-bosqich hisobotida](cluster2-stage2-summary.md) qayd etilgan; ushbu bosqichda backend biznes qoidalari o‘zgartirilmadi.

## Skrinshotlar va natijalar

Artifacts ildizi: `C:/Users/Asus/.codex/visualizations/2026/10/28/01a18264-3f77-7a02-a3d2-c4d4e2010e21/`.

- `cluster2-frontend-browser/catalogue-ru.png` va `catalogue-ru-mobile.png` — II klaster katalogi.
- `cluster2-frontend-browser/creative-projects-ru.png` va `creative-projects-ru-mobile.png` — dars va ochiq miniloyihalar.
- `cluster2-frontend-browser/recursion-lesson-ru.png` va `recursion-lesson-ru-mobile.png` — psevdokod misoli.
- `cluster2-frontend-browser/creative-completed-ru.png` — tugallangan modul.
- `cluster2-frontend-browser/result.json` va `cluster2-legacy-browser/result.json` — mashinada o‘qiladigan natijalar.

Katalog va mobil dars skrinshotlari vizual ko‘rib chiqildi. Jonli sayt shu bosqichda yangilanmagan.

## Keyingi bosqich

Foydalanuvchi tasdig‘idan so‘ng **4-bosqich — yakuniy tekshiruv, push va Render/Neon orqali chiqarish**. Avval mavjud remote bilan moslik va release konfiguratsiyasi tekshiriladi, keyin commitlar chiqariladi va jonli smoke bajariladi. Avvaldan mavjud recovery/configuration o‘zgarishlari ushbu frontend ishiga qo‘shilmadi.
