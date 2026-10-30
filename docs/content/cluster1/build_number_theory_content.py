"""Author the requested 1.4 resource and manifest without changing published courses."""
import hashlib
import json
from pathlib import Path

from build_stage4_content import Course

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def build():
    c=Course('number-theory-discrete-mathematics',4,'Sonlar nazariyasi va diskret matematika',
             ['math'],'numbers','0'*64)
    c.data['sources']=[{'id':c.source,'filename':'1.4-mavzu.md','sha256':'0'*64}]
    c.data['module']['diagnostic_coverage_note_uz']='Ushbu modul uchun diagnostika xaritasi hali tasdiqlanmagan. Umumiy math yoki IQ bali o‘rniga modulning boshlang‘ich tekshiruvidan foydalaniladi.'
    c.lesson('numbers-divmod','Qoldiq bilan bo‘lish va div mod',['arith-order'],[
        'Bu darsda a manfiy bo‘lmagan butun son, b esa musbat butun son. a = bq + r va 0 ≤ r < b shartlarini qanoatlantiruvchi q va r yagona bo‘ladi.',
        'a div b = q — butun bo‘linma; a mod b = r — qoldiq. Masalan, 23 div 5 = 4 va 23 mod 5 = 3, chunki 23 = 5 × 4 + 3.',
        'Qoldiq bo‘luvchidan kichik bo‘lishi shart. Qoldiq 0 bo‘lsa, a soni b ga qoldiqsiz bo‘linadi. Nolga bo‘lish, div va mod amallari aniqlanmagan.',
        'Masalan, 35 ta buyum 6 tadan qutilansa, 35 div 6 = 5 ta to‘liq quti va 35 mod 6 = 5 ta ortiqcha buyum chiqadi. Barcha buyum uchun yana bitta quti kerak.',
        'Python tilida manfiy bo‘lmagan butun sonlar uchun // butun bo‘linmani, % qoldiqni beradi. Manfiy sonlar bo‘yicha dasturlash tillari kelishuvi farq qilishi mumkin; bu moduldagi topshiriqlar ularni ishlatmaydi.'
    ],'59 ta detalni 8 tadan ajratsak, nechta to‘liq guruh va qancha qoldiq qoladi?',
       ['8 × 7 = 56 ≤ 59, ammo 8 × 8 = 64 > 59.','q = 7; r = 59 − 56 = 3.','59 = 8 × 7 + 3 va 0 ≤ 3 < 8.'],
       '59 div 8 = 7; 59 mod 8 = 3')
    c.lesson('numbers-primes','Tub va murakkab sonlar',['numbers-divmod'],[
        '2 dan kichik bo‘lmagan natural sonning faqat ikkita musbat bo‘luvchisi — 1 va o‘zi — bo‘lsa, u tub son. Masalan, 2, 3, 5, 7, 11 tub.',
        '1 dan katta natural sonning ikkitadan ortiq musbat bo‘luvchisi bo‘lsa, u murakkab. Masalan, 12 ning bo‘luvchilari 1, 2, 3, 4, 6, 12. 0 va 1 tub ham, murakkab ham emas.',
        '2 — yagona juft tub son. 2 dan katta barcha juft sonlar 2 ga bo‘lingani uchun murakkab, ammo har bir toq son tub emas: 9 = 3 × 3.',
        'n sonining tub ekanini tekshirishda √n dan katta bo‘lmagan tub bo‘luvchilarni tekshirish yetarli. Agar n = ab murakkab bo‘lsa, ko‘paytuvchilardan kamida biri √n dan oshmaydi.',
        'Tub ko‘paytuvchilarga ajratishda sonni 2, 3, 5 va keyingi tub sonlarga qoldiqsiz bo‘linguncha bo‘lamiz. Masalan, 90 = 2 × 3² × 5. Olingan ko‘paytuvchilarni qayta ko‘paytirib tekshiring.'
    ],'97 soni tubmi?',
       ['9² < 97 < 10²; tekshiriladigan tub bo‘luvchilar 2, 3, 5, 7.','97 juft emas; raqamlar yig‘indisi 16, 5 bilan tugamaydi; 97 = 7 × 13 + 6.','Ularning hech biri 97 ni bo‘lmaydi, demak 97 tub.'],'97 tub son')
    c.lesson('numbers-gcd','EKUB va Evklid algoritmi',['numbers-divmod','numbers-primes'],[
        'EKUB(a,b) — ikkala sonni ham qoldiqsiz bo‘ladigan eng katta musbat butun son. Bu modulda a va b musbat; algoritmning so‘nggi qoldig‘i nol bo‘lishi mumkin.',
        'Tub ko‘paytuvchilarda umumiy tub sonlarning kichik darajalari olinadi. 36 = 2² × 3² va 60 = 2² × 3 × 5 uchun EKUB(36,60) = 2² × 3 = 12.',
        'Evklid qoidasi: EKUB(a,b) = EKUB(b,a mod b). Sonlar juftini (b,a mod b) bilan almashtirib boramiz. Ikkinchi son 0 bo‘lganda birinchi son javobdir.',
        'Psevdokod: b ≠ 0 ekan, (a,b) ← (b,a mod b); yakunda a ni qaytaring. Almashtirishda eski b va eski a mod b birga hisoblanadi.',
        'Eng katta teng guruhlar yoki eng katta kvadratga qoldiqsiz ajratish masalalari EKUBga olib keladi. EKUB 1 bo‘lsa, sonlar o‘zaro tub deyiladi; ularning har biri alohida tub bo‘lishi shart emas.'
    ],'EKUB(252,105) ni Evklid algoritmi bilan toping.',
       ['252 = 105 × 2 + 42.','105 = 42 × 2 + 21.','42 = 21 × 2 + 0; oxirgi noldan farqli qoldiq 21.'],'21')
    c.lesson('numbers-lcm','EKUK va takrorlanadigan hodisalar',['numbers-gcd'],[
        'EKUK(a,b) — musbat a va b sonlarining eng kichik musbat umumiy karralisi. EKUB bo‘luvchini, EKUK esa karralini topadi.',
        'Tub ko‘paytuvchilarda barcha uchragan tub sonlarning katta darajalari olinadi. 12 = 2² × 3 va 18 = 2 × 3² uchun EKUK = 2² × 3² = 36.',
        'Musbat butun sonlarda EKUB(a,b) × EKUK(a,b) = a × b. Shuning uchun EKUK(a,b) = (a div EKUB(a,b)) × b; avval bo‘lish katta oraliq ko‘paytmani kamaytiradi.',
        'Ikki hodisa bir vaqtda boshlangan va mos ravishda a hamda b daqiqada takrorlansa, yana bir vaqtda kelishi EKUK(a,b) daqiqadan keyin bo‘ladi.',
        'O‘zaro tub sonlarda EKUK(a,b) = a × b; umumiy bo‘luvchi bo‘lsa, shunchaki ko‘paytirish eng kichik javobni bermasligi mumkin. Bu darsdagi EKUK topshiriqlarida nol ishlatilmaydi.'
    ],'6 va 15 daqiqada chalinadigan ikki signal birga chalindi. Yana qachon birga chalinadi?',
       ['EKUB(6,15) = 3.','EKUK(6,15) = (6 div 3) × 15 = 30.','30 musbat soni 6 ga ham, 15 ga ham bo‘linadi va eng kichik umumiy karralidir.'],'30 daqiqadan keyin')
    c.lesson('numbers-bases','Ikki sakkiz o‘n va o‘n oltilik sanoq sistemalari',['numbers-divmod'],[
        'Pozitsion b asosli sanoq sistemasida raqamlar 0 dan b−1 gacha. Son qiymati o‘ngdan boshlab raqam × b⁰, raqam × b¹ va hokazo hadlar yig‘indisidir.',
        '2 likda 0,1; 8 likda 0…7; 10 likda 0…9; 16 likda 0…9,A,B,C,D,E,F ishlatiladi. A=10, B=11, C=12, D=13, E=14, F=15. Masalan, 8 raqami sakkizlik yozuvda mumkin emas.',
        'Boshqa asosdan o‘nlikka: 1011₂ = 1 × 2³ + 0 × 2² + 1 × 2¹ + 1 = 11₁₀; 27₈ = 2 × 8 + 7 = 23₁₀; 1F₁₆ = 16 + 15 = 31₁₀.',
        'O‘nlikdan b asosga o‘tishda sonni b ga ketma-ket butun bo‘lamiz, qoldiqlarni yozamiz va oxiridan boshiga o‘qiymiz. Masalan, 13 = 2 × 6 + 1, 6 = 2 × 3 + 0, 3 = 2 × 1 + 1, 1 = 2 × 0 + 1; javob 1101₂.',
        '2³=8 bo‘lgani uchun ikkilik raqamlar o‘ngdan uchlikka, 2⁴=16 bo‘lgani uchun to‘rtlikka guruhlanadi. Masalan, 101111₂ = 101 111₂ = 57₈ = 0010 1111₂ = 2F₁₆. Chapga qo‘shilgan nollar qiymatni o‘zgartirmaydi.',
        '0 barcha ushbu asoslarda 0 deb yoziladi. Asosni yonida ko‘rsating: 10₂=2₁₀, 10₈=8₁₀ va 10₁₆=16₁₀; bir xil yozuv har xil qiymat berishi mumkin.'
    ],'2A₁₆ sonini o‘nlik ikkilik va sakkizlikda yozing.',
       ['2A₁₆ = 2 × 16 + 10 = 42₁₀.','Har bir hex raqam to‘rt bit: 2 → 0010, A → 1010; 00101010₂ = 101010₂.','Ikkilikni uchlikka ajratamiz: 101 010₂ → 5 2; demak 52₈.'],'2A₁₆ = 42₁₀ = 101010₂ = 52₈')
    skills=[s['key'] for s in c.data['skills']]
    def q(p,i,prompt,answer,steps,hint,error,wrong=None):
        c.question(p,skills[i],prompt,answer,steps,hint,error,wrong=wrong)
    q('practice',0,'73 div 9 ni hisoblang.',8,['9 × 8 = 72, 9 × 9 = 81 > 73.','73 = 9 × 8 + 1; butun bo‘linma 8.'],'73 dan oshmaydigan eng katta 9 karralisini toping.','Qoldiq bilan butun bo‘linmani aralashtirmang.')
    q('practice',0,'104 mod 9 ni hisoblang.',5,['9 × 11 = 99.','104 − 99 = 5; 0 ≤ 5 < 9.'],'a − b × (a div b) formulasidan foydalaning.','Qoldiq bo‘luvchidan kichik bo‘lishi kerak.')
    q('practice',1,'25, 27, 29, 33 sonlaridan qaysi biri tub?',29,['25 = 5², 27 = 3³, 33 = 3 × 11.','29 ni √29 dan oshmaydigan 2, 3, 5 tub sonlari bo‘lmaydi.'],'Har bir sonning 1 va o‘zidan boshqa bo‘luvchisi borligini tekshiring.','Toq son har doim tub emas.',wrong=[('25','25 = 5 × 5.'),('27','27 = 3 × 9.'),('33','33 = 3 × 11.')])
    q('practice',1,'84 ning tub ko‘paytuvchilarga to‘g‘ri ajratilishini tanlang.','2² × 3 × 7',['84 = 2 × 42 = 2² × 21.','21 = 3 × 7; demak 84 = 2² × 3 × 7.'],'84 ni avval 2 ga ketma-ket bo‘ling.','Ajratishning qiymati ham, har bir ko‘paytuvchining tubligi ham tekshiriladi.',wrong=[('2 × 3 × 7','Bu ko‘paytma 42.'),('2² × 3² × 7','Bu ko‘paytma 252.'),('4 × 21','4 va 21 tub emas.')])
    q('practice',2,'EKUB(48,18) ni toping.',6,['48 mod 18 = 12; 18 mod 12 = 6.','12 mod 6 = 0; EKUB = 6.'],'Evklid algoritmini qoldiq nol bo‘lguncha davom ettiring.','Oxirgi nol qoldiq emas, undan oldingi noldan farqli son javob.')
    q('practice',2,'45 ta qizil va 60 ta ko‘k tugma teng tarkibli eng ko‘p nechta to‘plamga qoldiqsiz ajratiladi?',15,['To‘plamlar soni 45 ni ham, 60 ni ham bo‘lishi kerak.','EKUB(45,60) = 15; har to‘plamda 3 qizil va 4 ko‘k tugma.'],'Eng katta umumiy bo‘luvchini qidiring.','Bu vaziyatda umumiy karrali emas, umumiy bo‘luvchi kerak.')
    q('practice',3,'EKUK(8,12) ni toping.',24,['EKUB(8,12) = 4.','EKUK = (8 div 4) × 12 = 24.'],'EKUB orqali EKUK formulasini ishlating.','8 × 12 = 96 umumiy karrali, ammo eng kichigi emas.')
    q('practice',3,'Bir signal 9 daqiqada, boshqasi 15 daqiqada takrorlanadi. Hozir birga chalindi. Necha daqiqadan keyin yana birga chalinadi?',45,['EKUB(9,15) = 3.','EKUK = (9 div 3) × 15 = 45 daqiqa.'],'Takrorlanishlar uchun EKUK ishlatiladi.','EKUB davrlarning yana mos kelish vaqtini bermaydi.')
    q('practice',4,'110101₂ ning o‘nlik qiymatini kiriting.',53,['110101₂ = 32 + 16 + 0 + 4 + 0 + 1.','Yig‘indi 53.'],'O‘ngdan boshlab 1, 2, 4, 8, 16, 32 xonalarini belgilang.','Ikkilikdagi yozuvni o‘nlikdagi 110101 deb olmang.')
    q('practice',4,'58₁₀ sonining sakkizlik yozuvini tanlang.','72₈',['58 = 8 × 7 + 2; 7 = 8 × 0 + 7.','Qoldiqlar teskari o‘qiladi: 72₈; 7 × 8 + 2 = 58.'],'8 ga ketma-ket bo‘ling va qoldiqlarni teskari o‘qing.','Qoldiqlarning yozilish va o‘qilish tartibi farq qiladi.',wrong=[('27₈','2 × 8 + 7 = 23.'),('58₈','Sakkizlikda 8 raqami ishlatilmaydi.'),('70₈','7 × 8 = 56; qoldiq 2 qolgan.')])
    q('precheck',0,'85 div 7 ni hisoblang.',12,['85 = 7 × 12 + 1.','Butun bo‘linma 12.'],None,'Qoldiq va bo‘linma turli miqdorlardir.')
    q('precheck',1,'1, 39, 43, 49 sonlaridan tubini tanlang.',43,['1 tub emas, 39 = 3 × 13, 49 = 7².','43 ni 2, 3, 5 bo‘lmaydi; √43 < 7.'],None,'1 soni tub deb hisoblanmaydi.',wrong=[('1','1 ning faqat bitta musbat bo‘luvchisi bor.'),('39','39 = 3 × 13.'),('49','49 = 7 × 7.')])
    q('precheck',2,'EKUB(84,126) ni toping.',42,['126 mod 84 = 42.','84 mod 42 = 0; EKUB = 42.'],None,'Eng katta umumiy bo‘luvchini tanlang.')
    q('precheck',3,'EKUK(12,18) ni toping.',36,['EKUB(12,18) = 6.','(12 div 6) × 18 = 36.'],None,'EKUK ikkala sonning ham karralisi bo‘lishi kerak.')
    q('precheck',4,'101101₂ sonining o‘nlik qiymati nechaga teng?',45,['32 + 8 + 4 + 1 = 45.'],None,'Har bir bitning xonasini hisobga oling.')
    q('postcheck',0,'a div 7 = 9 va a mod 7 = 4. a ni toping.',67,['a = bq + r = 7 × 9 + 4.','a = 67; 4 < 7 sharti bajarilgan.'],None,'Qoldiqni bo‘linmaga emas, bo‘luvchi bilan bo‘linma ko‘paytmasiga qo‘shing.')
    q('postcheck',1,'20 dan katta va 30 dan kichik nechta tub son bor?',2,['21, 22, 24, 25, 26, 27, 28 murakkab.','23 va 29 tub; jami 2 ta.'],None,'Toq sonlar orasida ham murakkablari bor.')
    q('postcheck',2,'48 cm × 180 cm to‘g‘ri to‘rtburchakni qoldiqsiz teng kvadratlarga bo‘lamiz. Eng katta kvadratning tomoni necha cm?',12,['Kvadrat tomoni 48 ni ham, 180 ni ham bo‘lishi kerak.','180 mod 48 = 36; 48 mod 36 = 12; 36 mod 12 = 0.','EKUB(48,180) = 12 cm.'],None,'Eng katta umumiy bo‘luvchi uzunlikni beradi.')
    q('postcheck',3,'Ikki qurilma 09:00 da birga signal berdi. Davrlari 8 va 14 daqiqa. 09:00 dan keyin yana birga signal berishigacha necha daqiqa o‘tadi?',56,['EKUB(8,14) = 2.','EKUK = (8 div 2) × 14 = 56 daqiqa; keyingi vaqt 09:56.'],None,'Boshlang‘ich birgalikdagi hodisani keyingi uchrashuv deb sanamang.')
    q('postcheck',4,'202₁₀ sonining o‘n oltilik yozuvini tanlang.','CA₁₆',['202 = 16 × 12 + 10.','12 → C va 10 → A; demak CA₁₆.'],None,'O‘n oltilikda A=10 va C=12.',wrong=[('AC₁₆','10 × 16 + 12 = 172.'),('C2₁₆','12 × 16 + 2 = 194.'),('12A₁₆','1 × 256 + 2 × 16 + 10 = 298.')])
    return c.finish()


def write():
    data=build()
    lines=['# 1.4 Sonlar nazariyasi va diskret matematika','',
           'Mualliflik o‘quv resursi. Foydalanuvchi belgilagan 1.4 mavzu asosida 2026-10-30 kuni tayyorlandi. Oldindan mavjud 1.4 DOCX manbasi sifatida ko‘rsatilmaydi.',
           '', 'Maqsad: div va mod, tublik, EKUB, EKUK hamda 2, 8, 10, 16 lik sanoq sistemalarini tushunib qo‘llash.','','## Nazariya va ishlangan misollar','']
    for i,lesson in enumerate(data['lessons'],1):
        lines += [f'### {i} {lesson["title_uz"]}','',*lesson['theory_uz'],'',lesson['worked_example']['prompt_uz'],*lesson['worked_example']['solution_steps_uz'],lesson['worked_example']['answer_uz'],'']
    for purpose,title in [('practice','Mustahkamlash mashqlari'),('precheck','Boshlang‘ich tekshiruv'),('postcheck','Yakuniy tekshiruv')]:
        lines += ['## '+title,'']
        for question in data['exercises']:
            if question['purpose']!=purpose:continue
            lines += [question['key']+' — '+question['prompt_uz']]
            lines += [o['id']+') '+o['text_uz'] for o in question['options']]
            lines += ['Yechim: '+' '.join(question['solution_steps_uz']),'']
    lines += ['## Baholash va qo‘llash','',data['blueprint']['comparison_note_uz'],
              'Dars va mashqlar topshirilgach yakuniy tekshiruv yordamsiz bajariladi. Natija IQ o‘sishi deb talqin qilinmaydi.',
              'Mazkur bank kichik pilot uchun. Mantiqiy qiyinlik juftlangan, statistik tenglashtirish o‘tkazilmagan.','']
    source=HERE/'1.4-mavzu.md'
    source.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    data['sources'][0]['sha256']=hashlib.sha256(source.read_bytes()).hexdigest().upper()
    for directory in (HERE,ROOT/'backend/apps/development/content/cluster1'):
        (directory/'number-theory-discrete-mathematics.v1.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Authored 1.4 resource: 5 lessons, 20 questions, source SHA-256 recorded.')


if __name__=='__main__':write()
