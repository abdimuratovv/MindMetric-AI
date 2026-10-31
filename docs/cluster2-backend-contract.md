# 2-klaster backend shartnomasi

Sana: 2026-10-31. Ushbu bosqich repository kodi va izolyatsiyalangan test bazasini qamraydi. Production deploy va yangi frontend hali bajarilmagan.

## Kontent va migratsiya

`DevelopmentModule.cluster` yangi maydon: 1 — akademik, 2 — algoritmik-amaliy. Migration `0003_developmentmodule_cluster` avvalgi modullarga 1 qiymatini beradi; original JSON, content hash, sessiya savollari va diagnostika snapshotlarini qayta yozmaydi. Klaster ichidagi tartib mavjud `order`; `topic_number` serverda `cluster.order` sifatida hosil qilinadi. Bir kalit yangi versiyada boshqa klasterga ko‘chirilmaydi.

Schema 1 faqat mavjud I klaster indikatorlarini qabul qiladi. Schema 2 uchun `module.cluster=2`, mos `topic_number`, 1–6 tartib, `algorithmic`/`creative`/`problem_solving` indikatorlari, `notation_uz` talab qilinadi. Asosiy ko‘nikma, dars, savol, javob va blueprint tekshiruvlari saqlanadi. `projects` faqat `assessment=self_review` resurslari; kalit va ro‘yxat maydonlari qat’iy tekshiriladi. Loyihaga avtomatik javob kaliti qo‘shib bo‘lmaydi.

Canonical nusxalar `backend/apps/development/content/cluster2/` ichida; ruscha nusxalar mavjud `content/translations/` katalogida. Barcha oltita ruscha locale birinchi importdan boshlab majburiy. Locale modul/versiya/hash, to‘liq dars/savol/variant/notation/loyiha qamrovi, sonli konstantalar va savoldagi operatorlar bilan tekshiriladi. Tarjima mustaqil grading kalitini bermaydi. I klaster tarjimalari va to‘rtta tarjimasiz modulning aniq `uz` fallbacki saqlanadi.

`ContentLocale` ikki klasterdagi original fayllarni topadi. Pinned v1 enrollment va sessiyalar o‘sha modul hashi bilan lokalizatsiya qilinadi; til almashtirish savol snapshoti, javob yoki bosqichni o‘zgartirmaydi.

## Import va chiqarish

Quyidagi komandalar `backend/` ichidan beriladi. Bu bosqichda ular faqat test settings/bazasida tekshirildi.

```powershell
# Eski xatti-harakatlar o‘zgarmaydi:
python manage.py seed_development_content --dry-run
python manage.py seed_development_content --all --dry-run

# Faqat II klasterning draft importi yoki ikkala klaster:
python manage.py seed_development_content --all --cluster 2 --dry-run
python manage.py seed_development_content --all --cluster all --dry-run
python manage.py seed_development_content --all --cluster all

# Keyingi tasdiqlangan chiqarish uchun tayyor komanda:
python manage.py activate_development_cluster2
```

Default bitta 1.1 moduli; `--all` defaultda faqat I klaster. `--cluster` faqat `--all` bilan ishlatiladi. II klaster hozir o‘z ichida prerequisite-larga ega va mustaqil draft sifatida import qilinishi mumkin; mavjud bo‘lmagan I klaster bog‘lanishlari uydirilmagan. Har qanday tashqi prerequisite berilsa, uning mavjudligi tekshiriladi. Har bir ko‘nikma kaliti bundle ichida noyob; `(cluster, order)` takrorlansa import rad etiladi.

`activate_development_cluster2` I va II klasterning barcha 12 modulini bitta tranzaksiyada import/nashr qiladi. Har bir klasterdagi 6 mavzu mavjudligi majburiy. Lokalizatsiya yetishmasligi yoki keyingi moduldagi xato butun chiqarishni bekor qiladi. Identik qayta chiqarish modul/savol IDlarini saqlaydi. Komanda user, enrollment yoki diagnostika natijalarini yaratmaydi. I klaster diagnostika havolalari uchun mavjud savollar oldindan bo‘lishi kerak; seed ularni qondirish maqsadida demo akkauntlar yaratmaydi.

Render’da PostgreSQL majburiy; SQLite bilan release rad etiladi. PostgreSQL advisory lock I klaster komandasidagi qulf bilan bir xil, shuning uchun parallel chiqarishlar serial bajariladi. Gunicorn `DEVELOPMENT_CLUSTER2_PUBLISH_ON_DEPLOY=1` berilgandagina yangi komandani chaqiradi; bu flag hozir production’da o‘zgartirilmadi. Flag bo‘lmasa oldingi I klaster release yo‘li saqlanadi. Release xatosi yangi server startini to‘xtatadi va ulanishlar forkdan oldin yopiladi.

## API qo‘shimchalari

Mavjud `/api/development/` endpointlari ishlatiladi; yangi autentifikatsiya yoki student roli yaratilmaydi. Amaldagi `DEVELOPMENT_CLUSTER1_ENABLED` bu bosqichda butun rivojlanish API’sining eski moslik flagi bo‘lib qoladi.

`GET modules/` va `GET plan/` javobida `clusters` qo‘shildi:

```json
{"clusters":[
  {"id":1,"title":"Intellektual akademik blok","description":"Matematika, mantiq va diskret savodxonlik.","module_count":6},
  {"id":2,"title":"Algoritmik-amaliy blok","description":"Algoritmlar, shartlar, sikllar va amaliy yechimlar.","module_count":6}
]}
```

Faqat ko‘rinadigan published/pinned modullar klasterlari qaytadi. Sarlavha va tavsif `X-Language`/`lang`ga mos. Har modul kartasidagi yangi maydonlar: `cluster`, `topic_number`; `order` klaster ichidagi tartibligicha qoladi. Saralash klaster, tartib va kalit bilan bajariladi. Shaxsiy reja bitta umumiy reja: aktiv mashg‘ulot boshqa klasterda bo‘lsa ham resume ustuvor.

Enrollment javobiga `notation` (matnlar ro‘yxati) va `projects` qo‘shildi. `notation` neytral yozuv qoidasini precheckdan oldin o‘qish imkonini beradi. `projects` elementlari `key`, `assessment`, `content_language`, `title`, `brief`, `constraints`, `steps`, `deliverables`, `rubric`dan iborat. Backend original `_uz` nomlarini yangi project API’sida tilga neytral nomlarga o‘giradi.

`projects` enrollmentning boshlang‘ich precheck bosqichi tugamaguncha yopiq. Har qanday aktiv precheck/postcheck mavjud bo‘lsa **barcha klasterlarda** `notation=[]`, `projects=[]`, `lessons=[]`, skill evidence va completed review yashiriladi. `GET progress/`, enrollment hamda completed-session endpointlari shu qoidani ishlatadi. O‘zga enrollment/session 404, yordam yoki darsni checkda olish 409. Faqat bitta aktiv sessiya global student bo‘yicha qoladi.

Savol va feedbackdagi `content_language` real til; II klaster RU tanlovida savol/variant, dars/misol, ishora, feedback va loyiha ruscha qaytadi. Javob option IDlari, aniq numeric grading, UUID retry, bosqichlar va 4/5 mezoni o‘zgarmagan. Savol matni kod sifatida bajarilmaydi. O‘quv natijalari asosiy indikator/IRT/overall ballarini yangilamaydi.

## Frontend bosqichiga topshirish

Kartalarni `cluster` bo‘yicha guruhlash, `1.{order}` o‘rniga `topic_number`dan foydalanish, `clusters` metama’lumotlari orqali klaster tanlovi, precheckdan oldingi `notation` va study’dagi `projects`ni ko‘rsatish kerak. Yangi boshlash tugmasidan oldin notationni o‘qish imkoniyati bo‘lsin. Aktiv checkda serverning bo‘sh ro‘yxatlarini chetlab o‘tilmasin. Klaster va til o‘zgarishi javob drafti yoki ochiq mashg‘ulotni yo‘qotmasin.
