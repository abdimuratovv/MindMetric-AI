# Birinchi bosqich yakuni

Sana: 2026-10-28. Bosqich: kontent auditi va 1.1-mavzuni tayyorlash.

Holat: birinchi bosqich bajarildi. Ikkinchi bosqich foydalanuvchi tasdig‘ini kutmoqda.

## Bajarilgan ishlar

1. Mavjud beshta mavzu uchun 25 mikroko‘nikma va ularning tayanch bog‘lanishlari belgilandi.
2. Har bir manba bo‘yicha kamchiliklar, tuzatishlar va keyingi kontent ishlari ro‘yxati yozildi.
3. 1.1-mavzu uchun beshta o‘zbekcha mini-dars va beshta ishlangan namuna tayyorlandi.
4. Asl hujjatdagi 10 mashq raqamli formatga o‘tkazildi; har biriga javob, yechim, ishora va odatiy xato izohi yozildi.
5. Boshlang‘ich va yakuniy tekshiruvlar uchun beshtadan yangi savol tuzildi. Har bir mikroko‘nikmaga 2 mashq, 1 precheck va 1 postcheck to‘g‘ri keladi.
6. Mavjud diagnostika bankidagi 13 savol aniq matni asosida 1.1 ko‘nikmalariga bog‘landi.
7. Seed uchun versiyalangan JSON shartnomasi, javoblarni oshkor qilmaslik va til fallback qoidalari yozildi.
8. Kontentning tuzilmasi, hisoblashlari va manbalarini qayta tekshiradigan offline Python vositasi qo‘shildi.

## Natija fayllari

- `docs/cluster1-content-audit.md` — ko‘nikmalar xaritasi va manbalar auditi.
- `docs/cluster1-content-contract.md` — backend importi uchun ma’lumotlar shartnomasi.
- `docs/content/cluster1/arithmetic-algebra.v1.json` — beshta dars va 20 ta topshiriq.
- `docs/content/cluster1/validate_content.py` — Django va bazadan mustaqil kontent tekshiruvi.

## Tekshirish natijalari

Quyidagi komanda muvaffaqiyatli yakunlandi:

```powershell
python -X utf8 docs/content/cluster1/validate_content.py 'D:\Downloads\Telegram Desktop'
```

Natija: 20 savol, 5 dars, 5 mikroko‘nikma, 13 diagnostika aloqasi; 20 ta mustaqil matematik javob tekshiruvi; 0 xato. Manba fayllari SHA-256 qiymatlari bilan mos keldi. Numeric javoblar aniq kasr arifmetikasi orqali tekshirildi.

Alohida tekshiruv: barcha beshta moduldagi 25 ko‘nikma kaliti noyob, havolalari mavjud, prerequisite grafigida sikl yo‘q. Kontent va audit hujjatlarida TODO/TBD qoldirilmagan.

Tahririy tekshiruvda 1.1 dagi 6-tenglama yechimsizligi aniq izohlandi. 7-mashqning ikki talabi aniqlashtirildi. Hisoblash tekshiruvi 1-mashqning dastlabki kalitidagi xatoni topdi; yakuniy javob 20 va yechim bilan birga tuzatildi.

## Muhim chegaralar

- Kontent `draft` holatida; ichki tekshiruv tashqi metodist tasdig‘i yoki statistik kalibrlash hisoblanmaydi.
- Precheck va postcheck tahririy qiyinlik bo‘yicha juftlangan, statistik tenglashtirilmagan. Natija umumiy IQ yoki qobiliyat o‘sishi deb talqin qilinmaydi.
- Faqat bitta yangi postcheck to‘plami mavjud. Takroriy mustaqil tekshiruv uchun keyin savollar banki kengaytiriladi.
- Qolgan to‘rtta modulning batafsil darslari va 80 topshirig‘i 4-bosqichda yoziladi; ularning tayyorligi da’vo qilinmaydi.
- Backend servislar, model/migratsiya, frontend va deploy bu bosqichga kirmaydi. Faqat kontent, hujjatlar va offline tekshirish vositasi tayyorlandi; ishchi daraxtdagi boshqa o‘zgarishlarga tegilmadi.

## Tasdiqdan keyingi bosqich

2-bosqichda `apps.development` ilovasi, kontent va talaba progressi modellari, migratsiyalar, ruxsatlar, minimal Django admin hamda atomik/idempotent seed va uning validatsiyasi yaratiladi. To‘liq talaba oqimi 3-bosqichda amalga oshiriladi. 2-bosqich yakunida alohida hisobot va 3-bosqichga o‘tish uchun tasdiq so‘raladi.
