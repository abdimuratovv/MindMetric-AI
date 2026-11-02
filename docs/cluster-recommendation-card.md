# Indikator → klaster → izohli tavsiya

2026-11-02. Foydalanuvchi natijalar oynasida izohli klaster kartasini darhol qo‘llashni buyurdi.

`Oqitish moduli.docx`dagi xarita: I — math/logic/iq; II — algorithmic/creative/problem_solving; III — teamwork/patience/learning_speed/attention. Barcha o‘n indikator bir martadan hisoblanadi. Faqat joriy holati completed bo‘lgan o‘nta test va ularning 0–100 oralig‘idagi chekli ballari mavjud bo‘lganda tavsiya beriladi. Retake boshlanganda, eskirgan score saqlansa ham, karta yashiriladi.

Har klaster ichidagi indikatorlar teng vaznli o‘rtachaga ega; klaster hajmi summaga ta’sir qilmaydi. Ikki kasrgacha yaxlitlangan eng past o‘rtacha — o‘quv ustuvorligi; teng klasterlar birgalikda chiqadi. Barcha indikatorlar kamida 80 bo‘lsa, matn ko‘nikmalarni mustahkamlash haqida bo‘ladi. Bu usul pedagogik yo‘naltirish bo‘lib, psixometrik tashxis yoki yangi iqtidor balli emas.

Natijalar va Rivojlanish APIlari bitta read-only siyosatdan foydalanadi. Kartada klaster, sabab, uning barcha indikator ballari va uchala klasterning o‘rtachasi bor. UZ/RU qo‘llanadi. Natijadagi tugma aniq klasterni ochadi; oldin saqlangan enrollment tanlovi bu yo‘naltirishni bosib ketmaydi. Enrollment va javoblar bazadan o‘chirilmaydi. Modul tavsiyalari oldingi alohida ko‘nikma dalillariga asoslanadi; III klasterda aniq mavzuni boshlang‘ich tekshiruv belgilaydi. Aktiv rivojlanish tekshiruvida plan kartasi yashiriladi.

Tekshiruv: siyosat/API testlari uchala klaster, tengliklar, yuqori natija, nol ball, yo‘q/noto‘g‘ri ma’lumot, retake, egaga tegishlilik, autentifikatsiya, ballar o‘zgarmasligi va plan bilan moslikni qamraydi. Haqiqiy Chrome/disposable DB sinovi UZ/RU karta, III klasterga o‘tish, eski tanlov ustidan aniq yo‘naltirish, refresh va 390px mobil ko‘rinishni tekshiradi. Frontend build o‘tdi.

Tekshiruv natijalari: development suite **152 test — OK, 8 PostgreSQL-only test skipped** (132.016s). Qo‘shimcha yakuniy policy/API tekshiruvi **7/7** (0.132s). Lokal Chrome testi real API bilan o‘tdi; mobil tasvir ko‘rib chiqildi. Dalillar: `C:/Users/Asus/.codex/visualizations/2026/11/01/01a1971d-7998-7240-92b8-9f1a43b9ec8a/cluster-guidance/`.

Renderga yuborilgan kod: `991d7b3e02faa1c7bc2859d222629b279101a767`. Frontend deploy `dep-dbk6qjjm8hqs738gkutg` 2026-11-02 16:01:09 Asia/Tashkentda live bo‘ldi. Backend deploy `dep-dbk6qjjm8hqs738gkulg` 16:23:05 da live bo‘ldi. Backend logi PostgreSQLda uch klaster va 16 published modul tayyorligini tasdiqladi. Builddagi mavjud seed/recompute buyruqlari sabab backend chiqarilishi taxminan 23 daqiqa davom etdi.

Jonli smoke **o‘tdi**: UZ/RU natijalar va plan APIlari bir xil siyosatni qaytardi. Demo hisobda joriy completed+valid score qamrovi 1/10 bo‘lgani uchun tavsiya yashirilgan; eski saqlangan indikator ballari tugallangan test o‘rnida ishlatilmagan. Jonli bazada barcha testlarni sun’iy tugallash yoki yangi javob yozish bajarilmadi. To‘liq profil hisoblash qoidasi real DB bilan lokal API testida tekshirilgan; deployed komponentning UZ/RU kartasi va III klasterga o‘tishi production brauzerida faqat tarmoq javobini sinov profili bilan almashtirib tekshirildi. Bu synthetic UI profili bazaga yuborilmadi.

Jonli tekshiruvda development write so‘rovi va JavaScript xatosi yo‘q; natijalar oldin/keyin aynan mos. RU mobil tasvir ko‘rib chiqildi. Backend error loglari bo‘sh. Dalillar yuqoridagi ildizning `cluster-guidance-production/` papkasida (`result.json`, `synthetic-card-uz.png`, `synthetic-card-ru.png`). Sinov skriptidagi callback imzosi va production uchun qisqa timeout tuzatilgach yakuniy run to‘liq o‘tdi.

Yakuniy dalillar faqat hujjat commiti bilan `[skip render]` orqali saqlanadi; jonli dastur kodi yuqoridagi `991d7b3` commitidir.
