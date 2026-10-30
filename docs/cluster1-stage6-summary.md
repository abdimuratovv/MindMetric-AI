# 6-bosqich: yakuniy tekshiruv va pilot holati

Sana: 2026-10-30. Asos: foydalanuvchining 6-bosqichga o‘tish tasdig‘i. Holat: texnik tekshiruvlar bajarildi; haqiqiy foydalanuvchi pilotining natijasi kutilmoqda. Bosqich to‘liq yopilgan deb belgilanmaydi.

## Tekshiruv va natijalar

| Yo‘nalish | Natija va amaliy chegarasi |
|---|---|
| Izolyatsiyalangan SQLite | 105 test topildi: 98 muvaffaqiyatli; PostgreSQL talab qiladigan 7 test ataylab skip qilinadi. |
| Izolyatsiyalangan PostgreSQL 18.0 | 105 testning hammasi muvaffaqiyatli; yangi migratsiyalar bo‘sh test bazada qo‘llandi. Neon bazasiga test yozuvlari kiritilmadi. |
| Parallel API so‘rovlari | 7 test: dublikat enrollment, dublikat sessiya boshlash, ikki modulda birdan boshlash, bir xil UUID bilan javob, turli UUID bilan bir savolga raqobat, parallel yakunlash va ishora/javob poygasi. |
| Xavfsizlik va bosqichlar | Mavjud testlar talaba/egalik/profile/flag ruxsati, maxfiy javoblar, idempotency, score chegaralari, versiya va snapshot o‘zgarmasligi, tavsiya dalillari va diagnostika ballari o‘zgarmasligini qamraydi. |
| Seed/publication | Butun bundle, qayta import idempotency, kech xatoda rollback va release buyrug‘i tekshirildi. |
| Django check | Muammo yo‘q; makemigrations dry-run yangi migratsiya talab qilmadi. |
| Frontend build | Muvaffaqiyatli. 932.11 kB JS bundle haqida Vite ogohlantirishi qoladi; bo‘lish/optimallashtirish keyingi performance ishidir. |
| Kontent | 5 modul, 25 ko‘nikma, 25 dars, 100 mashq javobi, 20 yangi ishlangan misol, Boolean qonunlar, prerequisite grafigi, manba hash/paritet va 28 diagnostika savoli havolasi tekshirildi. |
| Haqiqiy brauzer, vaqtinchalik baza | 40 javobli besh-modul ssenariysi muvaffaqiyatli; refresh, noto‘g‘ri formatni tuzatish, yo‘qolgan HTTP javobidan keyingi retry, ishora, postcheck, uz/ru va 390 px mobil ekran tekshirildi. JS xatosi va gorizontal overflow kuzatilmadi. |

Parallel testlar HTTP view/API so‘rovlarini turli threaddan, har biriga alohida PostgreSQL ulanishi bilan yuboradi. Bu haqiqiy tranzaksiya/row lock sinovi, ammo tarmoq yuklamasi yoki Neon pooler/region konfiguratsiyasining load testi emas. Ular SQLite’da o‘tgan deb hisoblanmaydi.

Mahalliy PostgreSQL Windows portable binaries orqali ishga tushirildi: faqat `127.0.0.1:55436`, `stage6test` roli, test nomi `test_mindmetric_stage6`. Binar/data `backups/stage6-postgresql/` ichida, Git’ga qo‘shilmaydi. Run yakunida vaqtinchalik server to‘xtatiladi. `tests/postgres_settings.py` production `DATABASE_URL` o‘rniga qat’iy loopback sozlamadan foydalanadi.

## Jonli deploy va smoke

Deploy 6-bosqichdan oldingi alohida foydalanuvchi topshirig‘i bilan chiqarilgan:

- Backend release: `9a50f7df538a3adf79de09b6c9d404fc8c4761e9`, Render deploy `dep-dbia95akdidc73be0ef0`, holat `live`.
- Frontend: https://mindmetric-frontend.onrender.com/#development .
- Release logi: beshta modul published, database `postgresql`. Backendning amaldagi bazasi foydalanuvchi tasdiqlagan Neon; eski to‘xtatilgan Render PostgreSQL o‘zgartirilmadi.
- Production smoke real demo talaba hisobida qayta muvaffaqiyatli bajarildi: `enabled=true`, `available=true`, beshta modul, ikkita tavsiya va sidebar kirishi. Mobil overflow va JavaScript xatosi yo‘q; natija alohida JSON’da saqlangan.
- Production smoke yangi enrollment yoki javob yaratmaydi. Sintetik brauzer natijasi haqiqiy o‘quv samaradorligi sifatida talqin qilinmaydi.
- 14:52:59 UTC relizdan keyingi ko‘rilgan Render error-log so‘rovida xato yozuvi topilmadi. HTTP metrikaning javobi bo‘sh bo‘ldi: bu nol xato yoki yetarli trafik borligining isboti emas.

Artefaktlar katalogi: `C:/Users/Asus/.codex/visualizations/2026/10/28/01a18264-3f77-7a02-a3d2-c4d4e2010e21/`. Izolyatsiyalangan ssenariy `stage6-browser/result.json`, production o‘qish ssenariysi `production-cluster1/result.json`; desktop/mobil rasmlar yonida saqlanadi.

## Pilot va qolgan ish

Foydalanuvchi “Avval o‘zim sinab ko‘raman” variantini tanladi. [Pilot yo‘riqnomasi va feedback shakli](cluster1-pilot-guide.md) tayyorlandi. Unda kirish, boshlang‘ich tekshiruv, refresh, tavsiya darsi, ishora, yakuniy natija, telefon va RU interfeysini sinash tartibi bor.

Haqiqiy pilot javoblari hali olinmadi. O‘zlashtirish o‘sishi, foydalilik va foydalanishdagi barcha to‘siqlar haqida yakuniy mahsulot xulosasi chiqarilmadi. Alohida masofaviy staging xizmati yaratilmagan; migratsiya/seed tekshiruvi mahalliy izolyatsiyalangan PostgreSQL muhitida bajarilgan. Production Neon’da parallel stress-test yoki test bazasi yaratilmadi.

Pilotdan keyin: foydalanuvchining kuzatuvini qayd etish, aniqlangan muhim muammolarni reproduksiya qilish/tuzatish, zarur bo‘lsa masofaviy staging/Neon test branchida konfiguratsiyani tasdiqlash, so‘ng bosqichni yopish. Bir kishilik pilotdan keyin kengroq guruhga o‘tish qarori alohida olinadi.

## Orqaga qaytish

Kritik muammo aniqlansa backendda `DEVELOPMENT_CLUSTER1_ENABLED=0` qilib bo‘lim yopiladi; enrollment va natijalar saqlanadi. Mavjud ma’lumotni o‘chirish yoki eski DB’ga ko‘r-ko‘rona qaytish talab etilmaydi. E’lon qilingan kontent xatosi yangi versiya orqali tuzatiladi. Boshqa lokal PostgreSQL recovery o‘zgarishlari ushbu tekshiruvga qo‘shilmadi.
