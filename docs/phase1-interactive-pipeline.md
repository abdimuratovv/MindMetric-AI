# 1-bosqich — Interaktiv topshiriq quvuri (Interactive Task Pipeline)

> Texnik reja. Kod holati: `e1e4cf1` (main).

## 0. Maqsad va qamrov

**Maqsad:** mavjud MCQ/CAT infratuzilmasini buzmasdan, uning ustiga umumiy interaktiv
topshiriq quvurini qurish va shu quvurda 4 ta formatni yetkazib berish.

**Qamrovda:**

- Umumiy quvur — model maydonlari, validator reyestri, API shartnomasi, frontend
  renderer reyestri, jarayon telemetriyasi
- 4 format — `drag_order`, `formula_builder` (math), `grid_logic` (logic), `cpt` (attention)
- Kontent — maqsadli 3 indikator uchun ~80 item
- Adaptiv tanlovda format kvotasi

**Qamrovdan tashqarida:**

- Likert indikatorlarini almashtirish → 2-bosqich
- O'qituvchi uchun jarayon takrori UI → 3-bosqich. Lekin **ma'lumot shu bosqichda
  yig'ila boshlaydi** — bu ataylab qilingan qaror
- Admin panelda interaktiv item yaratish formasi → 2-bosqich. 1-bosqichda kontent
  faqat seed orqali keladi
- Rasm talab qiladigan formatlar (`spot_diff`) — alohida asset quvuri kerak

---

## 1. Asosiy arxitektura qarori

**Yangi model/endpoint oilasi yaratilmaydi.** Interaktiv itemlar `CognitiveQuestion`
ning yangi `question_type` qiymatlari sifatida yashaydi.

Sabab — mavjud zanjir allaqachon *(savol → 0..1 correctness)* atamalarida ishlaydi:

| Komponent | Nimaga tayanadi |
|---|---|
| `AdaptiveTestingEngine.select_next_question` | `difficulty` / `discrimination` bo'yicha MFI reyting |
| `record_answer` → `irt.estimate_theta` | `correctness` **float** — essay allaqachon 0..1 qaytaradi |
| `state_tracker._score_mcq` | `sum(correctness) / n` |
| `ResultsMistakesView` | `prompt` + `feedback` + `correctness < 1.0` — tur-agnostik |

Ya'ni qisman ball beruvchi interaktiv topshiriq **IRT dvigateliga bir qator ham
o'zgartirmasdan** ulanadi. Bu — butun rejaning tayanch nuqtasi.

---

## 2. Ma'lumotlar modeli

Migration: `apps/assessments/migrations/0009_interactive_items.py`

### CognitiveQuestion

| Maydon | O'zgarish | Izoh |
|---|---|---|
| `question_type` | `max_length=10` → `24`, yangi choices | `drag_order`, `formula_builder`, `grid_logic`, `cpt` |
| `payload_ru` / `payload_uz` | **yangi** `JSONField(default=dict, blank=True)` | Formatga xos kontent. `_ru/_uz` juftligi — uydagi konvensiya (`options_ru/uz` kabi) |
| `answer_key` | **yangi** `JSONField(default=dict, blank=True)` | To'g'ri javob. Talabaga **hech qachon** serializatsiya qilinmaydi |

`options_ru/uz` va `correct_indices` — eski `single`/`multi` uchun o'z joyida qoladi,
tegilmaydi.

**Invariant:** `payload_ru` va `payload_uz` bir xil strukturaga ega bo'lishi shart —
bir xil kalitlar, massivlar uzunligi bir xil. Chunki `answer_key` ikkalasiga ham
indeks bo'ylab murojaat qiladi. Buni seeder va admin serializer tekshiradi (§4).

### CognitiveResponse

| Maydon | O'zgarish | Izoh |
|---|---|---|
| `answer` | **yangi** `JSONField(default=dict, blank=True)` | Talabaning strukturali javobi |
| `process_trace` | **yangi** `JSONField(default=list, blank=True)` | Telemetriya. Server tomonda cheklanadi: ≤500 hodisa / ≤32 KB |

`selected_indices`, `essay_text`, `rubric_scores` qoladi. `rubric_scores` yangi
formatlarda **subscore** uchun qayta ishlatiladi (masalan CPT: `hits`, `misses`,
`false_alarms`, `mean_rt_ms`, `rt_sd_ms`) — maydon allaqachon "stable-key convention"
deb hujjatlangan, mos keladi.

---

## 3. Format spetsifikatsiyalari

### 3.1 `drag_order` — ketma-ketlikni tartiblash

Eng arzon format. **Birinchi qilinadi** — quvur uchdan-uchgacha shu orqali sinaladi.
Barcha MCQ indikatorlarida ishlatiladi.

```json
// payload_uz
{
  "instruction": "Qadamlarni to'g'ri tartibda joylashtiring",
  "items": ["Ma'lumotni o'qish", "Saralash", "Natijani chiqarish"]
}

// answer_key
{ "order": [0, 1, 2] }

// answer (talabadan)
{ "order": [1, 0, 2] }
```

**Ball:** to'liq mos → `1.0`; aks holda normallashtirilgan **Kendall tau**,
`max(0, tau)` — silliq qisman ball.

### 3.2 `formula_builder` — ifoda tuzish (math)

```json
// payload_uz
{
  "instruction": "Berilgan tokenlardan natijasi 24 bo'lgan ifoda tuzing",
  "tokens": ["3", "4", "2", "+", "×", "(", ")"],
  "max_slots": 7,
  "reuse_tokens": false
}

// answer_key
{ "mode": "evaluate", "target": 24, "tolerance": 0, "partial_if_valid": 0.3 }

// answer — token indekslari tartibi
{ "sequence": [0, 4, 1] }
```

`mode: "exact"` varianti ham bor: `{"mode": "exact", "sequence": [0, 4, 1]}`.

**Ball:** natija `target` ga teng → `1.0`; sintaktik to'g'ri lekin noto'g'ri natija →
`partial_if_valid`; buzuq ifoda → `0.0`.

**Xavfsizlik — majburiy:** `eval()` ishlatilmaydi. `ast.parse(expr, mode='eval')` +
tugun turlari oq ro'yxati (`Expression`, `BinOp`, `UnaryOp`, `Constant`, `Add`, `Sub`,
`Mult`, `Div`, `Pow`, `USub`), `Pow` ko'rsatkichi ≤ 6 bilan cheklanadi, hisob `Fraction`
orqali yuritiladi. `×` → `*`, `÷` → `/` xaritalash validator ichida.

### 3.3 `grid_logic` — panjara-jumboq (logic)

```json
// payload_uz
{
  "instruction": "Kim qaysi rangni yoqtirishini aniqlang",
  "rows": ["Ali", "Vali", "Sami"],
  "cols": ["Qizil", "Ko'k", "Yashil"],
  "clues": ["Ali qizilni yoqtirmaydi", "Sami Validan keyin turadi"]
}

// answer_key — qator indeksi → ustun indeksi
{ "assignment": { "0": 2, "1": 0, "2": 1 } }

// answer
{
  "assignment": { "0": 2, "1": 0, "2": 1 },
  "marks": { "0": { "0": "x", "2": "v" } }
}
```

**Ball:** to'g'ri qatorlar ulushi.

`marks` **ballanmaydi** — bu jarayon ma'lumoti (o'quvchi qaysi tartibda variantlarni
chiqarib tashlagani), o'qituvchi takrori uchun saqlanadi.

### 3.4 `cpt` — uzluksiz diqqat testi (attention)

Bitta "blok" item, ichida ~40 sinov (trial).

```json
// payload_uz
{
  "instruction": "X harfi chiqqanda bosing, boshqasida bosmang",
  "stimuli": ["A", "X", "B", "X", "K"],
  "target": "X",
  "display_ms": 250,
  "isi_ms": 1100
}

// answer
{
  "trials": [
    { "i": 0, "responded": false, "rt_ms": null },
    { "i": 1, "responded": true,  "rt_ms": 412 }
  ]
}
```

**Ball:** `correctness = clamp(hit_rate − false_alarm_rate, 0, 1)`

**Subscores** (`rubric_scores`): `hits`, `misses`, `false_alarms`, `mean_rt_ms`,
`rt_sd_ms`. Reaksiya vaqti o'zgaruvchanligi (`rt_sd_ms`) — diqqat beqarorligining eng
kuchli belgisi; hozircha ballga kirmaydi, lekin yig'iladi va 3-bosqichda ishlatiladi.

**IRT ogohlantirishi:** CPT ballari to'g'ri/noto'g'ri emas, **shkala** ballari.
Kalibratsiyagacha `difficulty=0.0`, `discrimination=1.0` bilan seed qilinadi.
Bitta attempt siklida **1 tadan ortiq CPT bloki bo'lmasligi kerak** — aks holda theta
bitta o'lchov turiga qiyshayadi. Buni §5.2 kvota mantig'i ta'minlaydi.

---

## 4. Backend — validator reyestri

Yangi paket: `backend/apps/assessments/validators/`

```
validators/
  __init__.py          # VALIDATORS reyestri + validate() + check_content()
  base.py              # ValidationResult dataclass
  drag_order.py
  formula_builder.py
  grid_logic.py
  cpt.py
```

Har bir modul ikkita **sof funksiya** beradi:

```python
# base.py
@dataclass(frozen=True)
class ValidationResult:
    correctness: float    # 0.0 .. 1.0
    subscores: dict       # -> CognitiveResponse.rubric_scores


# har bir format moduli
def validate(question, answer: dict) -> ValidationResult: ...

def check_content(payload_ru: dict, payload_uz: dict, answer_key: dict) -> None:
    """Yaroqsiz kontentda django.core.exceptions.ValidationError ko'taradi."""
```

`validate` — DB ga murojaat qilmaydi, deterministik. Shu sabab test yozish oson va tez.

`check_content` seed komandasi va admin serializerda chaqiriladi — buzuq kontent bazaga
tushmasligi uchun. `payload_ru`/`payload_uz` shakl mosligini ham shu tekshiradi.

**Xato javoblarga munosabat:** `validate` **hech qachon exception ko'tarmaydi**.
Tanib bo'lmaydigan yoki buzuq `answer` uchun `ValidationResult(0.0, {'malformed': True})`
qaytaradi. Sabab — talabaning testini 500 xato bilan buzmaslik.

---

## 5. Engine o'zgarishi — eng nozik joy

### 5.1 `record_answer` — javobni baholash

Hozirgi if-zanjiri (ESSAY / MULTI / SINGLE) oldiga bitta shox qo'shiladi:

```python
if question.question_type in validators.VALIDATORS:
    result = validators.validate(question, answer or {})
    correctness = result.correctness
    rubric_scores = result.subscores
    stored_answer, stored_indices, stored_essay = (answer or {}), [], ''
elif question.question_type == CognitiveQuestion.QuestionType.ESSAY:
    ...   # o'zgarishsiz
```

Qolgan hamma narsa — `update_or_create`, `created` gardi, `avg_response_ms` EMA,
`estimate_theta` qayta hisobi — **tegilmaydi**.

### 5.2 `select_next_question` — format kvotasi

Hozir tanlov faqat MFI bo'yicha. Interaktiv itemlar bankning kichik ulushi bo'lgani
uchun ular deyarli hech qachon tanlanmaydi. Yechim — **yugurib boruvchi kvota**:

```python
INTERACTIVE_TARGET_SHARE = 0.4   # settings orqali override qilinadi
MAX_PER_TYPE = {'cpt': 1}        # attempt siklida qattiq limit
```

Mantiq (MFI reytingdan **oldin** qo'llanadi):

1. Shu siklda javob berilgan interaktiv itemlar ulushini hisoblash
2. Ulush maqsaddan past va nomzodlar orasida interaktiv item bor → nomzodlarni faqat
   interaktivga cheklash
3. Ulush maqsaddan yuqori → klassik itemlarga cheklash
4. `MAX_PER_TYPE` limitiga yetgan turlarni nomzodlardan chiqarib tashlash
5. Cheklovdan keyin pool bo'sh qolsa → cheklovni tashlab yuborish (bank tugagan holat)

Bu mavjud **"ko'rilmagan `question_type` ni afzal ko'rish" blokini almashtiradi** —
kvota o'sha maqsadni (kontent balansi) aniqroq bajaradi. Eski blok olib tashlanadi,
aks holda ikkalasi bir-biriga qarshi ishlaydi.

---

## 6. API shartnomasi

### `POST /api/assessments/mcq/<kind>/answer/`

```json
{
  "question_id": 42,
  "answer": { "order": [1, 0, 2] },
  "response_time_ms": 12345,
  "process_trace": [
    { "t": 0,    "e": "shown" },
    { "t": 1820, "e": "move", "from": 0, "to": 2 },
    { "t": 4210, "e": "undo" }
  ]
}
```

- Eski `selected_indices` / `essay_text` maydonlari **ishlashda davom etadi** —
  klient versiyasi buzilmaydi
- `AnswerMcqView` dagi qattiq "essay yoki selected_indices" tekshiruvi
  `_answer_missing(question, data)` yordamchisiga chiqariladi (tur bo'yicha dispatch)
- `process_trace` server tomonda kesiladi: ≤500 hodisa, ≤32 KB. Oshsa — birinchi 500
  tasi olinadi va `truncated: true` bayrog'i qo'yiladi. Bu maydon ballga **ta'sir
  qilmaydi**, shuning uchun uni soxtalashtirish ballni o'zgartirmaydi

### `GET /api/assessments/mcq/<kind>/next-question/`

```python
class CognitiveQuestionSerializer(serializers.ModelSerializer):
    fields = ['id', 'question_type', 'category', 'prompt', 'options', 'payload']

    def get_payload(self, obj):
        return getattr(obj, f'payload_{self.context["lang"]}')
```

`answer_key` **hech qachon** chiqarilmaydi.

---

## 7. Vaqt byudjeti

Interaktiv item MCQ dan uzoqroq davom etadi, `MCQ_SECONDS_PER_QUESTION = 60` esa global.

**Qaror: yangi model maydoni qo'shilmaydi.** Ikki joyda hal qilinadi:

1. **Attempt darajasi** — `assessments/views.py` da indikator bo'yicha override jadvali:

   ```python
   MCQ_TIME_LIMIT_OVERRIDES = {'math': 50*60, 'logic': 55*60, 'attention': 45*60}
   ```

   `_mcq_time_limit()` avval shu jadvalga qaraydi.

2. **Item darajasi** — formatga xos taymer `payload` ichida (`cpt` ning
   `display_ms`/`isi_ms` kabi), klient tomonda yuritiladi.

Sabab: adaptiv tanlov qaysi itemlar chiqishini oldindan bilmaydi, shuning uchun attempt
byudjetini item tarkibidan hisoblab bo'lmaydi. Override jadvali — oddiy, aniq va seed
kontentiga qarab sozlanadi.

---

## 8. Frontend

### 8.1 Renderer reyestri

Yangi papka: `frontend/src/pages/FocusedTest/tasks/`

```
tasks/
  index.js            # TASK_RENDERERS reyestri
  SingleChoice.jsx    # mavjud option-tugmalar UI si Mcq.jsx dan ko'chiriladi
  Essay.jsx           # mavjud textarea UI si Mcq.jsx dan ko'chiriladi
  DragOrder.jsx
  FormulaBuilder.jsx
  GridLogic.jsx
  Cpt.jsx
  Unsupported.jsx     # noma'lum tur uchun fallback
```

Har bir renderer bir xil shartnoma:

```jsx
export default function DragOrder({ question, value, onChange, onEvent, readOnly }) { ... }

export const emptyAnswer = (question) => ({ order: question.payload.items.map((_, i) => i) });
export const isValid     = (question, answer) => Array.isArray(answer?.order);
export const toPayload   = (answer) => ({ answer });   // API ga nima yuboriladi
```

`SingleChoice` va `Essay` ham shu shartnomaga ko'chiriladi va `toPayload` orqali eski
`selected_indices` / `essay_text` shaklini qaytaradi — ya'ni **barcha turlar bitta
yo'ldan** o'tadi, `Mcq.jsx` da if-zanjiri qolmaydi.

### 8.2 `Mcq.jsx` refaktori

`Mcq.jsx` orkestratorga aylanadi: start / fetch / timer / history / submit / completion.
UI mantig'i renderer ga o'tadi.

**Diqqat:** `Previous` (tarixni ko'rish) ishlashda davom etishi uchun har bir renderer
`readOnly` ni qo'llab-quvvatlashi shart. Bu — shartnomaning eng oson unutiladigan qismi,
code review checklistiga kiritiladi.

### 8.3 Telemetriya hooki

`frontend/src/pages/FocusedTest/useProcessTrace.js`

- Halqa buferi, 500 hodisada to'yinadi
- `push(e, data)` → `{ t: Date.now() - shownAt, e, ...data }`
- Savol almashganda tozalanadi, javob bilan birga yuboriladi

### 8.4 Touch qo'llab-quvvatlash — majburiy

Drag-drop **HTML5 Drag and Drop API da yozilmaydi** — u mobil brauzerlarda umuman
ishlamaydi. Pointer Events (`pointerdown` / `pointermove` / `pointerup` +
`setPointerCapture`) ishlatiladi.

Har bir sudrab-tashlash formatida **klaviatura alternativasi** ham bo'lishi kerak
(strelkalar bilan ko'chirish) — mavjud `mm-btn` fokus uslubi bilan mos.

---

## 9. Kontent

Yangi modul: `backend/apps/assessments/interactive_content.py`

Sabab: `content.py` allaqachon ~14 000 qator — uni yana o'stirmaslik kerak.

```python
INTERACTIVE_ITEMS = {
    'math':      [ {...} ],
    'logic':     [ {...} ],
    'attention': [ {...} ],
}
```

Har bir element: `key`, `difficulty`, `category_ru/uz`, `prompt_ru/uz`, `question_type`,
`payload_ru/uz`, `answer_key`.

Seed komandasi `_seed_interactive_items()` oladi — o'sha `CognitiveQuestion` jadvaliga
`key` bo'yicha upsert, yozishdan oldin `check_content()`.

**Hajm (1-bosqich uchun tavsiya):**

| Indikator | Formatlar | Item soni |
|---|---|---|
| `math` | `formula_builder` + `drag_order` | 30 |
| `logic` | `grid_logic` + `drag_order` | 30 |
| `attention` | `cpt` (5 variant) + `drag_order` | 20 |

40 talik yugurishda kvota `0.4` → ~16 ta interaktiv item. 30 ta bank buni takrorlanishsiz
qoplaydi, qayta topshirishda esa mavjud `seen_ids` mantig'i ishlaydi.

`feedback_content.py` ga yangi kalitlar qo'shiladi — bo'lmasa item "tipik xatolar"
ro'yxatidan jimgina tushib qoladi (bu mavjud, ataylab qilingan xatti-harakat).

---

## 10. Admin paneli — ataylab cheklangan

1-bosqichda interaktiv itemlar admin panelda **faqat ko'rinadi, tahrirlanmaydi**:

- `analytics/views.py` `_serialize_mcq` ga `payload` qo'shiladi
- `QuestionBank.jsx` format nishonchasini (badge) ko'rsatadi va tahrirlash tugmasini
  o'chiradi
- `AdminCognitiveQuestionUpdateSerializer._check_mcq_invariants` klassik bo'lmagan turga
  urinishda `400` qaytaradi — hozir u bunday satrni jimgina noto'g'ri validatsiya qiladi

Sabab: 4 ta format uchun 4 ta authoring UI qurish 1-bosqichni ikki barobar cho'zadi.
Kontent seed orqali keladi; authoring UI — 2-bosqich.

---

## 11. Testlar

Loyihada hozir **umuman test yo'q** — shu yerdan boshlanadi. Validatorlar sof funksiya
bo'lgani uchun bu eng arzon boshlanish nuqtasi.

`backend/apps/assessments/tests/`

| Fayl | Nima tekshiradi |
|---|---|
| `test_validators.py` | Har format: to'liq to'g'ri / qisman / noto'g'ri / buzuq javob |
| `test_content_integrity.py` | Seed dagi **har bir** interaktiv item `check_content()` dan o'tadi; `payload_ru`/`payload_uz` shakli bir xil |
| `test_formula_safety.py` | `formula_builder` parseri: `__import__`, atribut murojaati, ulkan daraja — hammasi rad etiladi |
| `test_selection_quota.py` | Kvota interaktiv itemlarni haqiqatan chiqaradi; `cpt` siklda 1 martadan ko'p chiqmaydi |
| `test_answer_api.py` | Yangi `answer` shakli **va** eski `selected_indices` shakli — ikkalasi ham ishlaydi |

`pytest` + `pytest-django` `requirements.txt` ga qo'shiladi.

---

## 12. Ishga tushirish va xavflar

**Feature flag:** `INTERACTIVE_TARGET_SHARE` env o'zgaruvchisi orqali. `0` qo'yilsa
interaktiv itemlar tanlanmaydi va tizim eski holatga qaytadi — demo oldidan qaytarish
yo'li shu.

| Xavf | Ta'sir | Yumshatish |
|---|---|---|
| Yangi itemlar kalibrlanmagan | Theta qiyshayishi, ballar noaniq | `difficulty` ekspert bahosi, `discrimination=1.0`; ~200 javobdan keyin `calibrate_items`; birinchi kohortada ballarni qo'lda ko'rib chiqish |
| CPT shkala ballari IRT ga to'liq mos emas | Indikator ballini og'diradi | Siklda 1 ta CPT; `difficulty=0`; 2-bosqichda alohida subscore sifatida ajratish |
| Mobil drag-drop ishlamasligi | Testni topshirib bo'lmaydi | Pointer Events + klaviatura alternativasi; mobil qurilmada QA majburiy |
| Eski klient + yangi tur | Bo'sh ekran | `Unsupported.jsx` fallback — "keyingi savol" tugmasi bilan |
| Test uzayishi | Tashlab ketish (drop-off) | Attempt vaqt override jadvali (§7); birinchi kohortada tugatish foizini kuzatish |
| `process_trace` hajmi | DB shishishi | Server tomonda 500 hodisa / 32 KB kesish |

---

## 13. Bajarish tartibi

Ketma-ketlik ataylab shunday: **quvur avval eng arzon format bilan uchdan-uchgacha
ishlab ko'riladi**, keyin qolgan formatlar unga qo'shiladi.

| # | Ish | Hajm |
|---|---|---|
| 1 | Migration `0009` — model maydonlari | S |
| 2 | `validators/` paketi + `base.py` + `drag_order.py` + testlar | S |
| 3 | `record_answer` shoxi + `AnswerMcqView` + serializer `payload` | S |
| 4 | `tasks/` reyestri, `Mcq.jsx` refaktori, `SingleChoice`/`Essay` ko'chirish | M |
| 5 | `DragOrder.jsx` + `useProcessTrace` + touch/klaviatura | M |
| 6 | **Darvoza:** 1 ta seed `drag_order` item bilan to'liq attempt uchdan-uchgacha | S |
| 7 | Kvota mantig'i `select_next_question` da + testlar | S |
| 8 | `formula_builder` — validator + xavfsiz parser + renderer | M |
| 9 | `grid_logic` — validator + panjara renderer | M |
| 10 | `cpt` — validator + taymerli renderer | M |
| 11 | Kontent: 80 item + integritet testi | L |
| 12 | Vaqt override jadvali, admin read-only guard, feature flag | S |
| 13 | Mobil QA + demo yugurish | M |

**6-qadam — darvoza (gate).** U o'tmaguncha qolgan formatlar boshlanmaydi: quvurdagi
xato 4 barobar qimmatga tushadi.

---

## 14. Tegiladigan fayllar

**Yangi**

```
backend/apps/assessments/migrations/0009_interactive_items.py
backend/apps/assessments/validators/{__init__,base,drag_order,formula_builder,grid_logic,cpt}.py
backend/apps/assessments/interactive_content.py
backend/apps/assessments/tests/{test_validators,test_content_integrity,test_formula_safety,test_selection_quota,test_answer_api}.py
frontend/src/pages/FocusedTest/tasks/{index.js,SingleChoice,Essay,DragOrder,FormulaBuilder,GridLogic,Cpt,Unsupported}.jsx
frontend/src/pages/FocusedTest/useProcessTrace.js
```

**O'zgartiriladi**

```
backend/apps/assessments/models.py               # yangi maydonlar + choices
backend/apps/assessments/serializers.py          # payload; admin guard
backend/apps/assessments/views.py                # answer/process_trace; vaqt override
backend/apps/assessments/management/commands/seed_assessment_content.py
backend/apps/assessments/feedback_content.py     # yangi kalitlar
backend/apps/scoring/engine.py                   # record_answer shoxi + kvota
backend/apps/analytics/views.py                  # _serialize_mcq -> payload
backend/mindmetric/settings.py                   # INTERACTIVE_TARGET_SHARE
backend/requirements.txt                         # pytest, pytest-django
frontend/src/pages/FocusedTest/Mcq.jsx           # orkestratorga refaktor
frontend/src/api/assessments.js                  # answer/process_trace shartnomasi
frontend/src/pages/Shell/QuestionBank.jsx        # read-only badge
frontend/src/i18n/translations.js                # yangi format matnlari
```

**Tegilmaydi** — `irt.py`, `calibration.py`, `state_tracker.py`, `calculators.py`,
`achievements.py`, `ResultsMistakesView`.

Bu §1 dagi qarorning to'g'riligini tekshiradigan lakmus: agar shu fayllarni
o'zgartirish kerak bo'lib qolsa, demak quvur noto'g'ri joyga ulanyapti.
