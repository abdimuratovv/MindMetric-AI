# 2-klaster: ikki tilli resurslar va platforma integratsiyasi

Sana: 2026-10-31. Holat: foydalanuvchi tasdiqlagan loyiha yechimi; resurslar bosqichi tugagan, backend integratsiyasi tasdig‘i kutilmoqda.

## Maqsad va manba

Avval o‘zbekcha va ruscha o‘quv resurslarini yaratish, keyin ularni MindMetric AI rivojlanish bo‘limiga integratsiya qilish. Asosiy mavzu xaritasi: `D:/Downloads/Telegram Desktop/Oqitish moduli.docx`, II klaster — Algoritmik-amaliy blok. Ushbu hujjatdagi xarita `MindMetricAI-study.txt`dagi umumiy tavsiyadan aniqroq: debugging alohida III klasterda qoladi. II klaster uchun tayyor alohida dars fayllari taqdim etilmagan; resurslar yangi mualliflik materiali sifatida belgilanadi. Original hujjatlar o‘zgartirilmaydi.

## Yondashuv tanlovi

Tavsiya: mavjud o‘quv mexanizmi, yangi klaster metama’lumoti va ikki tilli resurslar. Bu variant boshlang‘ich tekshiruv, nazariya, yordamli mashq, yakuniy tekshiruv, davom ettirish va RU/UZ almashishini birgalikda beradi.

Muqobil: faqat o‘qish uchun materiallar katalogi. Integratsiya sodda, ammo mashq va o‘zlashtirish oqimi to‘liq bo‘lmaydi.

Muqobil: kod muharriri, kod bajarish muhiti va loyiha topshirish/baholash tizimi. Erkin dasturlashni qo‘llaydi, ammo alohida infratuzilma va baholash loyihasini talab qiladi. Ushbu birinchi chiqarishda tavsiya etilmaydi.

## Resurslar qamrovi

Har modul: 5 mikroko‘nikma, 5 mini-dars, 5 ishlangan misol, 10 yordamli mashq, 5 yangi boshlang‘ich va 5 yangi yakuniy tekshiruv topshirig‘i. Jami 30 dars, 30 namuna va 120 alohida topshiriq; har biri to‘liq UZ va RU matnga ega. Ruscha nusxa ayni topshiriqning tarjimasi, qo‘shimcha mustaqil test banki emas.

| Modul | O‘zbekcha nom | Ruscha nom | Besh mikroko‘nikma |
|---|---|---|---|
| 2.1 | Algoritmizatsiya va blok-sxemalar | Алгоритмизация и блок-схемы | Kirish/chiqish; dekompozitsiya; ketma-ket amallar va qiymat berish; blok-sxema belgilari/yo‘nalishlar; algoritmni qadam bilan tekshirish |
| 2.2 | Shart va taqqoslash operatorlari | Условия и операторы сравнения | Taqqoslash; AND/OR/NOT; if-else; ichma-ich va ko‘p tarmoqli shart; switch-case hamda chegaraviy qiymatlar |
| 2.3 | Takrorlash operatorlari va rekursiya | Циклы и рекурсия | for; while; do-while; ichma-ich sikllar; rekursiyaning tayanch sharti va kichik chaqiruvlar izi |
| 2.4 | Ko‘p variantli yechimlar va optimizatsiya | Варианты решений и оптимизация | Bir masalaga bir necha yechim; amallar soni; xotira xarajati; takroriy hisobni kamaytirish; shartlarga mos yechim tanlash |
| 2.5 | Hayotiy muammolarni algoritmga aylantirish | Преобразование жизненных задач в алгоритмы | Talab/kirish/chiqish; cheklov va tekshirish; taksi tarifi; soddalashtirilgan bankomat modeli; test holatlari va modelni tekshirish |
| 2.6 | Kreativ dasturlash va kichik ilova dizayni | Креативное программирование и проектирование мини-приложений | Foydalanuvchi ehtiyoji; funksiyalarni ajratish; interfeys holatlari va fikr-mulohaza; variantlarni mezon bilan taqqoslash; prototip va tekshirish rejasi |

Boshlang‘ich daraja — 1-klasterdagi bazaviy matematika va mantiqdan keyingi bosqich. Misollar yagona, aniq belgilangan psevdokod sintaksisida beriladi; for chegaralari, bo‘lish, qiymat berish va switch-case semantikasi ochiq tushuntiriladi. Talaba Python yoki C++ni oldindan bilishi shart emas. Kodlar bajarilmaydi; o‘qish, kuzatish, tushib qolgan amalni tanlash va sonli natija topshiriqlari ishlatiladi. Blok-sxemalar uchun start/end, kiritish/chiqarish, amal, qaror va yo‘nalishlar matn bilan ham tushunarli ko‘rsatiladi.

2.6 da qo‘shimcha ikki ochiq miniloyiha yo‘riqnomasi va o‘zini tekshirish mezonlari bo‘ladi. Avtomatik savollar dizayn qarorlarini tushunishni tekshiradi; ochiq loyiha sifatini, umumiy kreativlikni yoki ijodni avtomatik baholagan deb ko‘rsatilmaydi. Fayl/kod topshirish va o‘qituvchi tekshiruvi ushbu chiqarishga kirmaydi.

Har darsda tushuntirish, kod/blok-sxema yoki keys, yechim qadamlari, keng tarqalgan xato va qisqa xulosa bo‘ladi. Yordamli mashqlarda tayyor namuna va ishoradan mustaqil yechimga o‘tiladi. Tekshiruvlarda yordam va javoblar ko‘rsatilmaydi. Variantlar va izohlar sun’iy umumiy matn bilan to‘ldirilmaydi.

## Kontent va tarjima shartnomasi

O‘zbekcha canonical JSONlar `docs/content/cluster2/` va backend content/cluster2 ichida saqlanadi. Ruscha to‘liq nusxalar mavjud versiya/hash bilan bog‘langan locale qatlamiga mos yaratiladi. O‘qish/tahrirlash uchun UZ va RU Markdown manbalar ham beriladi. Amaldagi 1-klaster fayllari va hashlarini o‘zgartirmasdan, kontent shartnomasi klaster identifikatori hamda mos indikatorlarni qabul qilish uchun kengaytiriladi.

Kalit, option ID, javob, son, kod operatorlari va koddagi o‘zgaruvchi nomlari ikkala tilda mos bo‘ladi. Tarjima javob kalitini almashtirmaydi. UZ/RU uchun barcha dars, misol, variant, ishora va izohlar to‘liq bo‘lishi shart; II klasterda ruscha yetishmasligini yashiruvchi aralash til nashrga o‘tmaydi. Topshiriqlar mustaqil yechib tekshiriladi, kod izlari deterministik misollarda solishtiriladi; talabaning kiritgan kodi eval qilinmaydi.

## Platformaga integratsiya

Modulda klaster identifikatori va klaster ichidagi mavzu raqami aniq ajratiladi. Mavjud modullar uchun 1-klaster mosligi saqlanadi; yangi migration zarur bo‘lsa, u faqat metama’lumotni kengaytiradi va frozen resurslarni qayta yozmaydi. API klaster va mavzu raqamini qaytaradi; frontenddagi hozirgi `1.{order}` va faqat I klaster sarlavhasi shu ma’lumotga almashtiriladi.

Rivojlanish sahifasida I va II klaster tanlovi, har birining sarlavhasi, qisqa tavsifi va mavzulari bo‘ladi. Umumiy shaxsiy reja boshlangan mashg‘ulotni klasterdan qat’i nazar davom ettirishni taklif qiladi. Klaster tanlash mavjud sessiyani yo‘qotmaydi, yashirin sessiya yaratmaydi. RU/UZ tanlovi interfeys bilan birga haqiqiy materiallarni almashtiradi; joriy dars, ochilgan namuna, javob loyihasi va mashg‘ulot natijasi saqlanadi.

Mavjud JWT, student/profile ruxsatlari, obyekt egasini tekshirish, UUID idempotent yuborish, bitta aktiv sessiya va tekshiruv paytidagi javoblarni yashirish qoidalari ishlatiladi. Yangi savollar single/multi/numeric formatlarga mos bo‘ladi. Baholash va 4/5 chegarasi birinchi klasterdagi qoidaga mos qoladi. Faol tekshiruv barcha klasterlardagi nazariya/yechimlar orqali javob topish yo‘lini ham yopadi.

Indikatorlar: `algorithmic`, `creative`, `problem_solving`. Bog‘lanishlar modulning haqiqiy mazmuniga mos belgilanadi. Diagnostika savoli bilan aniq bog‘lanish tekshirilmagan bo‘lsa, savolga uydirma xarita tuzilmaydi: boshlang‘ich tekshiruv taklif qilinadi. Kurs natijalari diagnostika/IRT ballarini yozmaydi, kreativlik yoki IQ o‘sishi deb ko‘rsatilmaydi.

## Bajarish tartibi va qabul mezonlari

1. **Resurslar:** barcha oltita modulning UZ/RU matnlari, ko‘nikma xaritasi, javob/izohlar va 2.6 loyiha yo‘riqnomalarini yozish. Til, semantika va javoblar tekshiruvidan keyin resurslar hisoboti. Ushbu bosqich yakunlanmasdan platforma integratsiyasiga o‘tilmaydi.
2. **Backend:** klaster metama’lumoti, validatsiya, import/release va locale yuklashni kengaytirish; yangi modullarni avval izolyatsiyalangan bazada tekshirish. Bitta noto‘g‘ri modul/locale atomik nashrni to‘xtatishi kerak.
3. **Frontend:** ikki klaster katalogi, to‘g‘ri 2.1–2.6 raqamlari, kod/blok-sxema matnlarining o‘qilishi, mobil holat va RU/UZ almashishi.
4. **Tekshiruv va chiqarish:** PostgreSQL’da mos testlar, har moduldagi javoblarning to‘g‘riligi, ikkala tildagi oqim, refresh/retry, ikki klaster orasida aktiv check himoyasi, I klaster regressiyasi va frontend build. Tasdiqlangan mavjud Render/Neon joylashtirish yo‘lidan foydalanish; production bazada destruktiv test qilinmaydi. Har bosqich tugaganda qisqa ish hisoboti tayyorlanadi.

Yakuniy natija: platformada I klasterning oltita moduli saqlanadi va II klasterning oltita yangi moduli paydo bo‘ladi. II klasterdagi barcha resurslar RU/UZ bo‘yicha to‘liq almashadi; avval boshlangan mashg‘ulotlar ishlaydi. Jonli smoke sinov yangi o‘quv natijalarini sun’iy yaratmasdan imkon qadar o‘qish orqali bajariladi. Yakuniy hisobotda lokal va jonli tekshiruv qamrovi alohida aniq yoziladi.

## Loyihani ko‘rib chiqish

Manbadagi II klasterning olti mavzusi qamralgan. Kod bajarish/erkin loyiha baholash qo‘shilmaydi; II klaster bilim mashqlari bilan ochiq loyiha yo‘riqnomalari farqlangan. Ishchi daraxtdagi oldindan mavjud PostgreSQL recovery va konfiguratsiya o‘zgarishlari bu ishga qo‘shib commit qilinmaydi. Yechim foydalanuvchi tomonidan tasdiqlandi; bosqichma-bosqich bajarish [rejada](cluster2-development-plan.md), resurslar natijasi [1-bosqich hisobotida](cluster2-stage1-summary.md).
