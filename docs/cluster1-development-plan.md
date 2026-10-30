# MindMetric AI birinchi klasterni ishlab chiqish rejasi

2026-10-30 yangilanishi: foydalanuvchining alohida so‘rovi bilan dastlab manbasi yo‘q bo‘lgan 1.4 mavzu uchun yangi mualliflik resursi yaratildi. Sonlar nazariyasi va diskret matematika endi oltinchi modul sifatida, katalogda 1.3 va 1.5 orasida joylashadi. Joriy hajm: 6 modul, 30 ko‘nikma, 30 dars va 120 topshiriq. Quyidagi dastlabki besh-modulli reja va bosqich hisobotlari tarixiy qamrovni ko‘rsatadi. Yangi Word va Markdown manbalar `docs/content/cluster1/` ichida; eski 1.4 DOCX fayli taqdim etilgandek ko‘rsatilmaydi.

Sana: 2026-10-28

Ijro holati: 1–5-bosqichlar bajarildi. 6-bosqich tasdiqlandi: texnik tekshiruvlar yakunlandi, foydalanuvchi o‘zi bajaradigan pilot kuzatuvlari kutilmoqda. Natijalar: [birinchi bosqich hisoboti](cluster1-stage1-summary.md), [ikkinchi bosqich hisoboti](cluster1-stage2-summary.md), [uchinchi bosqich hisoboti](cluster1-stage3-summary.md), [to‘rtinchi bosqich hisoboti](cluster1-stage4-summary.md), [beshinchi bosqich hisoboti](cluster1-stage5-summary.md), [oltinchi bosqich holati](cluster1-stage6-summary.md). Keyingi ish pilot kuzatuvlaridagi muhim muammolarni tekshirish va tuzatishdir.

## 1. Maqsad va yakuniy natija

Talaba matematika, mantiq va IQ diagnostikasi natijalaridan so‘ng birinchi klasterdagi mos mavzuni o‘rganishi, izohli mashqlar bajarishi va yangi savollarda mavzuni o‘zlashtirganini tekshirishi mumkin bo‘ladi. Past umumiy indikator mavzu tanlashga dastlabki signal beradi; aniq mavzu bo‘yicha xulosa savollarning ko‘nikma belgilariga yoki qisqa boshlang‘ich tekshiruvga tayanadi.

Bu hujjat amalga oshirish rejasidir. Kod, migratsiya va deploy ushbu topshiriq doirasida bajarilmaydi. Kontent hajmi va muddatlar rejalashtirish taxmini; ular kontent tekshiruvidan keyin aniqlashtiriladi.

## 2. Mavjud resurslar va cheklovlar

- Backend: Django va Django REST Framework; `apps.assessments`, `apps.scoring`, mavjud JWT va rollar.
- Frontend: React va Vite; `App.jsx`, `AppShell.jsx`, `useAppState.js` orqali ekran boshqaruvi; umumiy API klienti va uz/ru interfeys.
- `CognitiveQuestion` hozir single/multi/essay formatlarini qo‘llaydi. `docs/phase1-interactive-pipeline.md` dagi interaktiv formatlar reja, ularni tayyor imkoniyat deb qabul qilmaymiz.
- `LearningModule` va `LearningItem` o‘rganish tezligi diagnostikasi uchun. Yangi kurs kontenti ularga joylashtirilmaydi.
- `IndicatorScore` har bir indikatorning joriy natijasini saqlaydi. `AssessmentAttempt` qayta ishlatiladi, `attempt_cycle` oshadi; eski javoblar `cycle` bilan saqlanadi. Tarixiy taqqoslash uchun alohida snapshot kerak.
- Manbalar: `D:/Downloads/Telegram Desktop/` ichidagi `Oqitish moduli.docx`, `1.1-mavzu.docx`, `1.2-mavzu.docx`, `1.3-mavzu.docx`, `1.5-mavzu.docx`, `1.6-mavzu.docx`.
- DOCX ichidagi tavsiyalar kontent manbasi sifatida ko‘riladi; ular dasturga avtomatik bajariladigan buyruq hisoblanmaydi.
- Besh mavzuda nazariya va rasm ko‘rinishidagi mashqlar mavjud. Javoblar, yechimlar va tekshiruv variantlarini ishlab chiqish kerak.
- `1.4-mavzu.docx` taqdim etilmagan. Sonlar nazariyasi, EKUB/EKUK va sanoq sistemalari birinchi nashrga kirmaydi.
- Ishchi daraxtda boshqa o‘zgarishlar mavjud; amalga oshirishda ularga tegilmaydi va ular yangi ishga qo‘shib commit qilinmaydi.

## 3. Birinchi versiya qamrovi

| Modul | Dastlabki ko‘nikmalar | Asosiy indikator | Qo‘shimcha bog‘lanish |
|---|---|---|---|
| 1.1 Arifmetika va algebra | Amallar tartibi, daraja/ildiz, kasrlar, ifodalar va sodda tenglamalar | math | Mavjud diagnostika savoli mos bo‘lsagina logic |
| 1.2 Matematik mantiq | NOT/AND/OR, implikatsiya, ekvivalentlik, rostlik jadvallari va qonunlar | logic | math bilan mavzu bo‘yicha bog‘lanish |
| 1.3 To‘plamlar | Birlashish, kesishish, ayirma, to‘ldiruvchi, qism to‘plam va Venn diagrammasi | math, logic | Munosabatlar nazariyasi keyin |
| 1.5 Funksiya va kombinatorika | Funksiya/aniqlanish sohasi, progressiyalar, faktorial, o‘rin almashtirish, joylashtirish, kombinatsiya | math | Ketma-ketlikka mos iq savollari |
| 1.6 Matritsalar | O‘lcham, turlar, qo‘shish, songa ko‘paytirish, matritsa ko‘paytirish, 2×2 determinant | math | Umumiy IQga bevosita tenglashtirilmaydi |

IQ past bo‘lsa barcha matematika modullari avtomatik biriktirilmaydi. Raqamli ketma-ketlik bilan bog‘liq javoblardagina 1.5 tavsiya qilinadi. Fazoviy yoki boshqa qoplanmagan IQ ko‘nikmasi uchun hozircha mos modul yo‘qligi ko‘rsatiladi. Mavzuni o‘zlashtirish natijasi umumiy IQ o‘sishi sifatida taqdim etilmaydi.

Birinchi versiya: beshta modul, shaxsiy tavsiya, nazariya va ishlangan namuna, yordamli mashq, boshlang‘ich/yakuniy tekshiruv, davom ettirish va rivojlanish hisoboti. Talaba barcha e’lon qilingan modullarni ixtiyoriy ochishi ham mumkin.

Qamrovdan tashqarida: qolgan ikki klaster, AI chat yoki generativ baholash, kod sandboxi, to‘liq vizual kurs muharriri, o‘qituvchi uchun yangi analitika paneli, ilmiy kalibrlangan yangi IRT modeli, drag-and-drop va murakkab interaktiv konstruktorlar.

## 4. Talaba jarayoni

1. Natijalar sahifasidagi “Rivojlanish rejam” orqali o‘qitish bo‘limiga o‘tadi.
2. Tavsiya kartasida mavzu, tanlash sababi va mavjud dalilni ko‘radi. Test tugallanmagan bo‘lsa, soxta past ball berilmaydi; katalog va boshlang‘ich tekshiruv taklif qilinadi.
3. Modulni boshlaganda beshta yordamsiz boshlang‘ich savolni bajaradi.
4. Qisqa nazariya, ishlangan namuna va yordamli mashqlarni o‘taydi. Har bir xatodan keyin sabab va tegishli nazariya ko‘rsatiladi.
5. Mashqda oxirgi beshta turli topshiriqdan kamida to‘rttasini birinchi urinishda, yordam olmasdan bajarsa yakuniy tekshiruv ochiladi. Bu boshlang‘ich mahsulot qoidasi, ilmiy standart emas.
6. Besh yangi yakuniy savolni yordamsiz bajaradi. Kamida 4/5 — “o‘zlashtirildi”; aks holda xatolarga mos takrorlash tavsiya qilinadi.
7. Dastlabki va yakuniy natijani, qaysi ko‘nikmada qiyinchilik qolganini ko‘radi. Birinchi tekshiruvdan yuqori natija olgan talaba nazariyani o‘qimasdan ham yakuniy tekshiruvga o‘ta oladi.

Nazariyani ochish yoki uzoq vaqt sarflashning o‘zi o‘zlashtirish hisoblanmaydi. Internet uzilishi yoki sahifa yangilanishida javoblar va joriy bosqich saqlanadi.

## 5. Kontentni tayyorlash

Har bir modul uchun kamida: 3–5 mikroko‘nikma, har biriga tushuntirish va ishlangan namuna; 10 ta mashq; 5 ta boshlang‘ich va 5 ta yakuniy tekshiruv savoli. Jami kamida 100 ta alohida topshiriq yozuvi rejalashtiriladi. Berilgan mashqlar tahrirlanib mashq bankiga olinadi; mustaqil tekshiruvlar uchun yangi savollar yaratiladi. Bu minimal pilot bank, keng adaptiv tanlov uchun keyin kengaytiriladi.

Har bir savol: barqaror kalit, modul/ko‘nikma, format, tahririy qiyinlik, topshiriq, variantlar yoki javob sxemasi, to‘g‘ri javob, yechim, ishora, manba va versiya. Tekshiruvlar ko‘nikma va qiyinlik bo‘yicha juftlashtiriladi. Bu juftlashtirish hali statistik tenglashtirish hisoblanmaydi.

Kontent ishlari:

- Rasmdagi nazariya va savollarni tahrirlanadigan matn/formulaga ko‘chirish; manba topshiriq raqamini saqlash. Dekorativ yozuvlar va kesilgan rasm o‘rniga toza kontent tayyorlash.
- 1.1: kasr va tenglamalar bo‘yicha yetarli izoh; yechimsiz tenglamalarni tekshirib, ataylab berilgan bo‘lsa ko‘rsatmani aniq yozish.
- 1.2: yutilish va qo‘sh inkor qonunlarini kiritish; formulalardagi qavs va inkor sohasini tekshirish.
- 1.3: “A raqami” iborasini tuzatish, kesishish xossasini to‘ldirish, qism to‘plam belgilashini izchil qilish.
- 1.5: aniqlanish sohasi, progressiya yig‘indilari va kombinatorik tanlash shartlarini tushuntirish.
- 1.6: “birlik matritsa” atamasini tuzatish; ko‘paytirish va determinant namunalari; kesilgan mashqni tiklash yoki almashtirish. 3×3 determinant bo‘yicha batafsil modul keyingi nashrga qoldiriladi.
- Har bir javobni yechib tekshirish va noto‘g‘ri variant sababini yozish; material tekshiruvdan o‘tmaguncha draft holatda qoladi.

Birinchi pilot kontenti o‘zbekcha. Uz/ru interfeys saqlanadi. Ruscha kontent tayyor bo‘lmasa API o‘zbekchaga aniq fallback qiladi va `content_language=uz` qaytaradi; interfeys “Material o‘zbek tilida” deb bildiradi. Tizimdagi ru standart tili sabab bo‘sh sahifa chiqmasligi tekshiriladi. Ruscha nashr keyingi kontent bosqichi.

## 6. Backend arxitekturasi

Yangi `backend/apps/development/` ilovasi va `/api/development/` namespace yaratiladi. Mavjud autentifikatsiya, `IsStudent`, `HasCompletedProfile`, til aniqlash va DRF yondashuvlari qayta ishlatiladi.

Asosiy modellar:

| Model | Vazifasi |
|---|---|
| `DevelopmentModule` | Mavzu kaliti, tartib, nom, prerequisite ko‘nikmalar, draft/published holati va kontent versiyasi |
| `DevelopmentSkill` | Moduldagi aniq ko‘nikma va indikator bog‘lanishlari |
| `DevelopmentLesson` | Tartiblangan nazariya, formula, rasm va ishlangan namuna bloklari; uz/ru kontent |
| `DevelopmentExercise` | Ko‘nikma, single/multi/numeric formati, practice/precheck/postcheck maqsadi, qiyinlik, maxfiy javob va izoh |
| `DiagnosticSkillLink` | Mavjud `CognitiveQuestion` bilan bir yoki bir nechta mikroko‘nikma orasidagi tekshirilgan bog‘lanish |
| `DevelopmentEnrollment` | Talaba/modul/versiya, joriy bosqich, tavsiya sababi va boshlang‘ich diagnostika snapshoti |
| `DevelopmentSession` | practice/precheck/postcheck urinishlari, tanlangan savollar snapshoti, holat va natija |
| `DevelopmentAnswer` | Javob, birinchi urinish/to‘g‘rilik, yordamdan foydalanish, server vaqti va qayta yuborishni aniqlash kaliti |

`DevelopmentExercise`ning e’lon qilingan yozuvi o‘zgarmas bo‘ladi; tahrir yangi versiya yaratadi. Boshlangan enrollment eski versiyasida tugaydi. Diagnostika snapshotida indikator ballari, `theta`/`se` mavjud bo‘lsa, `attempt_id`, `cycle` va qayd vaqti saqlanadi. Mashqlar `IndicatorScore`, `StudentAbilityEstimate`, `OverallScore`, tavsiyalar yoki mavjud yutuqlarni yozmaydi.

Servislar: `recommendations.py`, `grading.py`, `progress.py`; kontent uchun `content/cluster1/` va idempotent `seed_development_content` komandasi. Bu komanda demo akkauntlarini yaratmaydi. Tahrirni nazorat qilish uchun minimal Django admin registratsiyasi yetarli; mavjud mahsulot rollari bilan mualliflik ruxsati alohida tekshiriladi.

## 7. Tavsiya va tekshirish qoidalari

- Mavjud savollar mavzularga qo‘lda tekshirilgan xarita orqali bog‘lanadi; kategoriya matnidan avtomatik xulosa chiqarilmaydi.
- Joriy diagnostika siklida mikroko‘nikma bo‘yicha kamida uch javob bo‘lsa, noto‘g‘ri javob ulushi ustuvorlikni belgilaydi. Kamroq dalil bo‘lsa “qo‘shimcha tekshiruv kerak” holati va precheck beriladi.
- Indikator natijasi mavzuni tartiblashga yordam beradi; yagona keskin “past ball” chegarasi barcha talabalarga qo‘llanmaydi. Birinchi navbatda ikki modul tavsiya qilinadi, qolganlari katalogda ochiq.
- Prerequisite precheckda tasdiqlangan bo‘lsa o‘tiladi; aks holda tayanch mikroko‘nikmaga yo‘naltiriladi. Bog‘lanishlarda sikl bo‘lishi kontent validatsiyasida rad etiladi.
- Single/multi serverda tekshiriladi. Numeric format son yoki kasr kabi cheklangan yozuvni qabul qiladi; vergul/nuqta va bo‘shliq normallashtiriladi. Formulani `eval` qilish yo‘q. To‘plam, matritsa va tenglama yechimlari pilotda variant tanlash orqali so‘raladi.
- Practice javobida izoh va ishora beriladi. Precheck/postcheck davomida kalitlar va to‘g‘rilik berilmaydi; natija tekshiruv yakunlangach ochiladi.
- Takroriy postcheck uchun avval ko‘rilmagan to‘plam kerak. Pilot bank tugagan bo‘lsa ishonchli yangi tekshiruv mavjud emasligi qaytariladi; o‘sha savollarni takrorlash “yangi o‘sish” sifatida baholanmaydi. Practice ochiq qoladi.
- Dastlabki/yakuniy natija foiz punktida ko‘rsatiladi: masalan, 40% → 80% = +40 foiz punkt. Kichik va kalibrlanmagan tekshiruv natijasi mavzu doirasidagi kuzatuv sifatida beriladi.
- Asosiy diagnostikani qayta topshirish mavjud assessment oqimi orqali ishlaydi. Oddiy kurs hisoboti diagnostika yoki IRT bo‘yicha ilmiy tasdiqlangan o‘sish deb nomlanmaydi.

## 8. API shartnomasi

| Endpoint | Natija |
|---|---|
| `GET /api/development/modules/` | E’lon qilingan beshta modul, talaba holati, kontent tili |
| `GET /api/development/plan/` | Ustuvor modullar, sabablar, dalil yetarliligi |
| `POST /api/development/modules/{key}/enroll/` | Enrollment yaratish yoki mavjudini qaytarish |
| `GET /api/development/enrollments/{id}/` | Darslar, bosqich va davom ettirish holati |
| `POST /api/development/enrollments/{id}/sessions/` | Server ruxsat etgan practice/precheck/postcheck sessiyasini boshlash yoki davom ettirish |
| `GET /api/development/sessions/{id}/next/` | Joriy savol; javob kalitisiz |
| `POST /api/development/sessions/{id}/answers/` | Javob va idempotency kalitini yuborish |
| `POST /api/development/sessions/{id}/hints/` | Faqat practice uchun ishora va foydalanish qaydi |
| `POST /api/development/sessions/{id}/finish/` | Server hisoblagan yakuniy natija; javoblar yetarli bo‘lmasa rad etish |
| `GET /api/development/progress/` | Modul, ko‘nikma, precheck/postcheck va tarixiy urinishlar |

Barcha shaxsiy endpointlar obyekt egasini tekshiradi. Server tanlangan savol, bosqich va completion mezonini boshqaradi; frontend yuborgan score/status qabul qilinmaydi. Javobni qayta yuborish va bir vaqtdagi so‘rovlar transaction hamda unique constraint orqali dublikat yaratmaydi. Kontent bo‘lmasa tushunarli holat, noto‘g‘ri kirishda 400, begona obyekt uchun 404 qaytariladi.

## 9. Frontend integratsiyasi

- `frontend/src/api/development.js` umumiy JWT va til klientidan foydalanadi.
- `frontend/src/pages/Development/` ichida katalog/reja, modul darsi, mashq/tekshiruv va progress ekranlari yaratiladi.
- `App.jsx`, `AppShell.jsx`, `useAppState.js`ga mavjud ekran boshqaruvi usulida yangi bo‘lim qo‘shiladi; butun routing qayta yozilmaydi.
- Natijalar sahifasiga reja havolasi; sidebar ichiga “Rivojlanish” bo‘limi qo‘shiladi. Yangi ekran holati serverdagi enrollment/session orqali tiklanadi.
- Formula, kasr va matritsalar uchun xavfsiz matematik renderer ishlatiladi; kontent HTML sifatida nazoratsiz qo‘yilmaydi. Renderer tanlovi birinchi kontent prototipida ildiz, kasr, inkor va matritsa misollarida tekshiriladi.
- Mobil ko‘rinish, klaviatura boshqaruvi, variantlarning aniq belgilanishi, yuklanish/xato/bo‘sh holatlar va uz/ru interfeys matnlari tayyorlanadi.
- Internet xatosida yuborilgan javob yo‘qolmaydi, qayta urinish dublikat ball bermaydi. Yakuniy hisob faqat server tasdiqlagach ko‘rsatiladi.

## 10. Bajarish bosqichlari

| Bosqich | Ish va konkret natija | Bog‘liqlik | Taxmin |
|---|---|---|---|
| 1. Kontent auditi | Ko‘nikma xaritasi, tahrirlar ro‘yxati, 1.1 uchun to‘liq 20 savol va izoh | Manba hujjatlar | 2–3 ish kuni |
| 2. Backend asosi | Ilova, modellar, migratsiya, permission, admin va seed validatsiyasi | 1-bosqichdagi kontent shartnomasi | 2–3 kun |
| 3. Birinchi to‘liq oqim | 1.1: enroll → precheck → dars → practice → postcheck → hisobot; backend va oddiy frontend | 2 | 3–4 kun |
| 4. Beshta modul kontenti | Qolgan 80 topshiriq, nazariya, yechim va diagnostika xaritasi; matematik tekshiruv | 1 va 3 dagi format tasdig‘i | 3–5 kun |
| 5. Tavsiya va interfeys | Ko‘nikma tavsiyalari, qolgan modullar, natijalar/sidebar integratsiyasi, progress, mobil va tillar | 3–4 | 2–3 kun |
| 6. Tekshiruv va pilot | Avtomatik tekshiruv, staging migratsiyasi/seed, kichik guruhda foydalanish va muhim tuzatishlar | 5 | 2–3 kun |

Ketma-ket bajarilsa taxminan 14–21 ish kuni. Taxmin bitta full-stack dasturchi va kontent javoblarini tekshira oladigan mas’ulning o‘z vaqtida ishtirokiga tayanadi. Kontent qayta yozilishi ko‘paysa muddat kengayadi. Avval 1.1 orqali ishlaydigan to‘liq oqimni tasdiqlash, keyin qolgan mavzularni kiritish tavsiya etiladi.

## 11. Tekshirish va qabul mezonlari

Kontent:

- Beshta modul e’lon qilingan, kamida 100 topshiriq tekshirilgan; draft va javobi tasdiqlanmagan kontent talabaga chiqmaydi.
- Har bir savolda kalit, mikroko‘nikma, maqsad, javob, yechim va manba bor; prerequisite sikllari va dublikatlar yo‘q.
- Precheck/postcheckda bir xil yoki faqat soni almashtirilgan mashqning oshkor javobi takrorlanmaydi; savollar mazmunan ham tahririy tekshiriladi.

Backend uchun mazmunli testlar:

- Tavsiya xato ko‘nikmaga, yetarli/yetarli bo‘lmagan dalilga va yo‘q diagnostikaga to‘g‘ri javob beradi.
- Bir talaba boshqasining enrollment, sessiya va javobini o‘qiy/yubora olmaydi.
- Numeric/multi tekshiruvi, ishorali mashqning mustaqil natijaga kirmasligi, bosqichni chetlab o‘tish va vaqtli parallel qayta yuborish tekshiriladi.
- GET javoblarda va tekshiruv davomida javob kalitlari oshkor bo‘lmaydi.
- Seed ikki marta bajarilganda dublikat yaratmaydi; kontent versiyasi eski sessiyani buzmaydi.
- Mashqdan keyin asosiy diagnostika natijalari va yutuqlar o‘zgarmaydi; keyingi assessment retake esa mavjud oqimda ishlaydi.

Tekshiruv komandalarining rejalashtirilgan minimumi: `python manage.py check`, `python manage.py makemigrations --check --dry-run`, `python manage.py test apps.development` va `npm run build`. Ushbu reja bosqichida ular bajarilmadi; yangi kod yozilgach ishga tushiriladi. Parallel yuborish/constraint testlari productionga mos PostgreSQLda ham tekshiriladi.

Frontendda: to‘liq talaba yo‘li, refresh/resume, internet xatosi va retry, diagnostikasiz holat, bank tugashi, uz/ru til almashtirish, telefon va klaviatura bilan ishlash tekshiriladi. Hozir frontendda test runner yo‘q; birinchi oqim uchun takrorlanadigan qo‘lda tekshiruv ssenariysi tayyorlanadi.

## 12. Chiqarish va pilotni baholash

`DEVELOPMENT_CLUSTER1_ENABLED` backend feature flagi orqali bo‘lim pilotga ochiladi; flag o‘chiq bo‘lsa API boshlashni ham to‘sadi. Frontend ko‘rinishi backend capability holatiga tayanadi. Stagingda yangi migratsiyalar, seed va eski test oqimlari tekshiriladi. Nosozlikda flag o‘chiriladi, yig‘ilgan natijalar saqlanadi; diagnostikani orqaga qaytarish talab etilmaydi.

Pilotda tavsiya → modul boshlash → yakunlash ulushi, mikroko‘nikma bo‘yicha birinchi mustaqil javoblar, ishora ehtiyoji va precheck/postcheck farqi kuzatiladi. Natija o‘zgarmagan yoki pasaygan holat ham yashirilmaydi. Pilotdan so‘ng bankni kengaytirish, kechiktirilgan qayta tekshiruv, ruscha kontent va 1.4-mavzu bo‘yicha navbatdagi ish belgilanadi.
