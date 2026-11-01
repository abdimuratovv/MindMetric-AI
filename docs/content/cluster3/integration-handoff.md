# III klaster resurslarini integratsiyaga topshirish qaydi

Yangilanish: foydalanuvchi keyingi so‘rovda integratsiya va Render deployini buyurdi. Quyidagi yozuv resurs bosqichidagi texnik topshirishni saqlaydi; joriy holat [integratsiya hisobotida](../../cluster3-integration-release.md).

Holat: tayyorlanayotgan kontent to‘plami; platforma integratsiyasi ushbu ish doirasiga kirmaydi. Foydalanuvchi 2026-11-01 kuni hozircha faqat resurslarni yakunlashni tanladi. Ushbu fayl keyingi ish uchun ma’lumot, bajarishga buyruq emas.

## Draft shartnomasi

Asosiy format `resource_format=mindmetric-cluster3-draft-v1`, `integration_status=not_importable`. O‘zbekcha banklar, source hashga bog‘langan ruscha locale va `activities.v1.json` tayyorlanadi. Backendning amaldagi schema_version raqami ataylab berilmagan: schema 2 hozir faqat II klasterni qabul qiladi. Draftni production importerga bevosita yuborish mumkin emas.

| Mavzu | Modul kaliti | Mazmunan mos mavjud indikatorlar uchun taklif |
|---|---|---|
| 3.1 | code-debugging | patience, attention, problem_solving |
| 3.2 | teamwork-git | teamwork |
| 3.3 | attention-code-review | attention |
| 3.4 | documentation-learning | learning_speed |

Bu kalitlar assessment kodida mavjudligi ko‘rildi, lekin development modelidagi ruxsat, semantika va baholashga mosligi integratsiyada alohida tekshirilishi kerak. Resurs bankiga tasdiqlanmagan indicator_keys yoki diagnostika savol xaritasi kiritilmadi. Bo‘sh `diagnostic_links` bunday moslik hali tasdiqlanmaganini bildiradi.

## Keyingi texnik ishlar uchun talablar

1. Kontent formatini validatsiya va importerga aniq versiyali shartnoma bilan moslashtirish; to‘rt mavzuli III klaster va yangi indikatorlarni tekshirish. I/II klaster frozen banklarini qayta yozmaslik.
2. Skill, lesson, exercise va locale maydonlarini amaldagi serializerga moslash; `outcome` va ochiq ishlarni ko‘rsatish usulini belgilash. Keyingi importdan avval barcha resurslar va locale atomik validatsiyadan o‘tsin.
3. Backend model/migratsiya, bundle loader, release komandasi va katalog API si III klasterni qabul qilishi kerak. Frontend yangi klaster nomi, 3.1–3.4 raqami va haqiqiy UZ/RU matnini ko‘rsatsin.
4. Teacher/student maydonlari ajratilsin. Tekshiruv API siga answer_key, feedback, solution, hint va ochiq ishlarning teacher yechimi chiqmasin. Boshqa klasterdan javobga kirish yo‘li ham active checkda yopilsin.
5. Mavjud progress, sessiya egasi, idempotent yuborish va bittalik aktiv sessiya qoidalarini saqlash; eski enrollmentlarni buzmaslik.
6. Knowledge check natijasini IQ, patience yoki learning_speed diagnostik balliga yozmaslik. Teamwork uchun loyiha rubrikasi va testdagi nazariy qarorlar farqini UI da tushunarli berish.
7. Import, tarjima, student payloadi, cross-cluster check himoyasi, progress va I/II klaster regressiyasi bo‘yicha tegishli testlar; frontend build va ikkala tildagi brauzer oqimi. Faqat alohida topshiriq doirasida chiqarish rejasiga o‘tish.

Hozirgi resurslar platformada ochilgan, bazaga yuklangan yoki Renderga chiqarilgan deb hisobot berilmaydi. [Ko‘rsatkich](README.md) va [offline tekshiruv](verification-result.json).
