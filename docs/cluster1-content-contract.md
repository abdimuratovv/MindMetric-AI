# Birinchi klaster kontent shartnomasi

Versiya: 1. Sana: 2026-10-28. Birinchi backend implementatsiyasi uchun kirish formati.

## Fayl va versiya

UTF-8 JSON, `schema_version=1`. `module.key` barqaror slug, `module.version` musbat butun son. Kalit va versiya birgalikda nashrni aniqlaydi; keyingi nashr eski enrollment tarkibini almashtirmaydi. `module.status=draft` kontentning talabaga avtomatik ochilmasligini bildiradi. `review_status=internally_checked` tashqi metodist tasdig‘i degani emas.

Ko‘rib chiqilgan nusxa `docs/content/cluster1/`da saqlanadi. 2-bosqichdan boshlab deploy qilinadigan nusxa `backend/apps/development/content/cluster1/`da; seed standart holatda shu nusxani o‘qiydi. Ikkala nusxaning hash mosligi testda tekshiriladi. DOCX fayllari import paytida kerak emas.

## Tuzilma

- `sources`: manba kaliti, fayl nomi va SHA-256. Original hujjat o‘zgarsa farq aniqlanadi. Yangi savol uchun `origin=authored` va manba identifikatori yoziladi.
- `module`: key, version, status, review_status, order, title_uz, title_ru, content_language, indicator_keys.
- `skills`: key, title_uz, indicator_keys va prerequisite_keys. Boshqa modulga bog‘lanish bo‘lsa katalogdagi kalit bilan tekshiriladi.
- `lessons`: key, skill_key, title_uz, theory_uz satrlari va `worked_example` (prompt_uz, solution_steps_uz, answer_uz). Har bir ko‘nikmaga kamida bir dars va namuna.
- `exercises`: key, skill_key, purpose, format, difficulty, prompt_uz, options, answer_key, solution_steps_uz, hint_uz, common_error_uz, source. Version parent moduldan olinadi.
- `diagnostic_links`: mavjud savol kaliti, skill_keys va inson o‘qiy oladigan asos. U savol matni asosida tekshiriladi, kategoriya nomidan hosil qilinmaydi.
- Mos mavjud diagnostika bo‘lmasa `diagnostic_links=[]` bo‘lishi mumkin; bunda `module.diagnostic_coverage_note_uz` orqali bo‘sh bo‘lmagan izoh talab qilinadi. Soxta havola yaratilmaydi, boshlang‘ich baho precheckdan olinadi.
- `blueprint`: precheck, practice va postcheck tartibi, juftlashgan ko‘nikma/qiyinlik hamda bank cheklovi.

Hozir ruscha o‘quv kontenti yo‘q: `title_ru=null`, kontent tili `uz`. Keyingi backend tarjima yo‘qligida uz fallback va uning tilini aniq qaytarishi kerak; bo‘sh ruscha dars yuborilmaydi.

## Savollar

`purpose`: `practice`, `precheck`, `postcheck`. `difficulty`: `easy`, `medium`, `hard` — tahririy daraja, IRT parametri emas. `format`: ushbu versiyada `numeric` yoki `single`; `multi` keyingi kontentda zarur bo‘lsa qo‘shiladi.

`numeric`: `options=[]`; `answer_key={"value":"7/4"}` kabi aniq ratsional qiymat. Backend butun son, chekli o‘nli kasr yoki bir dona kasrni qabul qiladi. Son yozuvi uzunligi cheklanadi; maxraj nol bo‘lishi rad etiladi. `7/4`, `14/8`, `1.75`, `1,75` ekvivalent; `1+3/4` ifodasi yoki kod qabul qilinmaydi. Kasr/Decimal orqali aniq solishtirish, `eval` ishlatmaslik talab qilinadi. Umumiy yaqinlashtirish toleransi yo‘q.

`single`: options — barqaror `id`, `text_uz`, `feedback_uz`li obyektlar. `answer_key={"option_id":"b"}`. Variant tartibi almashtirilsa ham id o‘zgarmaydi. `feedback_uz` har bir variant uchun to‘g‘ri yoki noto‘g‘ri sababni bildiradi.

`hint_uz` faqat practice uchun satr, tekshiruvlarda null. `solution_steps_uz` va `common_error_uz` hamma savolda bor, lekin precheck/postcheck tugamaguncha ochilmaydi. Sonli savoldagi umumiy xato izohi har bir mumkin bo‘lgan noto‘g‘ri son uchun individual tahlil da’vosi emas.

Matematik yozuvlar hozir oddiy matn va Unicode belgilarida; ifodalar kod emas. Renderer kiritilganda asl mazmun va kalitlar saqlangan holda formula bloklariga ko‘chiriladi. Nazoratsiz HTML ishlatilmaydi.

## Majburiy validatsiya

Kalitlar takrorlanmasligi; barcha havolalar mavjudligi; prerequisite grafigi siklsizligi; 10/5/5 ta maqsad bo‘yicha ajratish; har bir ko‘nikmaning 2/1/1 qamrovi; precheck/postcheck bir-biriga aralashmasligi tekshiriladi. Numeric javoblar aniq kasr sifatida parse qilinadi. Single variantlarida kamida ikkita noyob id va aynan bitta mavjud to‘g‘ri id bo‘ladi. Savol/yechim bo‘sh emas, manba va lokator mavjud.

Seed faqat validatsiyadan keyin atomik bajariladi. Mavjud savollarga diagnostika havolasi topilmasa yashirin tashlab ketilmaydi; ko‘rinadigan xato qaytariladi. Qayta seed dublikat yaratmaydi. E’lon qilingan versiya mazmuni o‘zgartirilmaydi.

4-bosqichdan boshlab `--all` beshta modulni bitta atomik transaction ichida prerequisite tartibida import qiladi; `--all --dry-run` to‘liq klaster grafigini yozuvsiz tekshiradi. Alohida importda tashqi prerequisite modullar avval import qilingan bo‘lishi kerak. Oddiy seed hali 1.1 modulini oladi. Bir bundle ichida har modul kalitining bittadan versiyasi bo‘ladi; standart bundled tanlov eng yangi versiyani oladi.

## Oshkor qilish chegarasi

Bu fayl va kontent JSON maxfiy javoblari bor backend resursidir: frontend `public/` katalogiga ko‘chirilmaydi va to‘liq API javob sifatida berilmaydi. Talaba savoli faqat key, format, prompt, variant id/matni va kerakli ko‘rinish metama’lumotlarini oladi. Practice feedback javob yuborilgach, ishora alohida endpointdan keladi. Tekshiruvda kalit, variant feedbacki, natija va yechim faqat sessiya tugagach ochiladi.

## Pilotning chegaralari

Har bir tekshiruvdagi beshta savol — beshta ko‘nikmaning bittadan namunasi. Natija mavzu bo‘yicha kuzatuv bo‘lib, umumiy qobiliyat yoki IQ o‘sishini isbotlamaydi. Tekshiruvlar kalibrlanmagan. Mustaqil takroriy postcheck uchun yangi bank zarur. Besh dars va 20 savol birinchi to‘liq mahsulot oqimini yaratishga yetadi; boshqa to‘rtta modulning to‘liq kontenti 4-bosqichda qo‘shiladi.
