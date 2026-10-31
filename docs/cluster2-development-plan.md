# 2-klasterni amalga oshirish rejasi

2026-10-31. Asos: foydalanuvchi tasdiqlagan [loyiha yechimi](cluster2-design.md).

Ijro holati: **1–4-bosqichlar tugadi**: [resurslar hisoboti](cluster2-stage1-summary.md), [backend hisoboti](cluster2-stage2-summary.md), [frontend hisoboti](cluster2-stage3-summary.md), [jonli chiqarish hisoboti](cluster2-stage4-summary.md). I/II klasterlar platformada ishlamoqda.

1. **Resurslar:** olti modul uchun 30 ko‘nikma, 30 dars va ishlangan misol, 120 topshiriq, ikkita ochiq miniloyiha; barcha matnlar UZ/RU. Mualliflik manbalari, canonical JSON, hash bilan bog‘langan tarjima va o‘qiladigan Markdown nusxalar yaratish. Kalitlar, semantika, javoblar, tarjimalar va qamrovni tekshirish. Hisobotdan so‘ng backend bosqichiga tasdiq so‘raladi.
2. **Backend:** yangi kontent shartnomasidagi klaster/indikatorlar, legacy v1 mosligi, klaster metama’lumoti, yangi bundle va locale yuklash, atomik import/nashr, permission va aktiv check himoyasi. Izolyatsiyalangan PostgreSQL tekshiruvlari. Hisobot va frontend bosqichiga tasdiq.
3. **Frontend:** I/II klaster tanlovi, API’dan mavzu raqami, ikki tilli kontent, kod/blok-sxema va mobil ko‘rinish, refresh va til almashganda davom ettirish. Brauzer tekshiruvlari. Hisobot va chiqarishga tasdiq.
4. **Chiqarish:** PostgreSQL regressiya, frontend build, git push va mavjud Render/Neon yo‘liga deploy; jonli o‘qish smoke tekshiruvi. Lokal va production qamrovi ko‘rsatilgan yakuniy hisobot.

Har bosqich alohida commit qilinadi; avvaldan mavjud konfiguratsiya/recovery o‘zgarishlari qo‘shilmaydi. 1-bosqich resurslari draft bo‘ladi; tayyor faylning mavjudligi uni avtomatik nashr qilmaydi. Resurslarning tekshiruvdan o‘tishi tashqi metodist ekspertizasi yoki kalibrlash degani emas.
