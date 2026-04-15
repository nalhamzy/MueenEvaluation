# Arabic LLM Benchmark — Manual Evaluation Brief

You are evaluating an LLM on Arabic NLP tasks. For each article below, perform 4 tasks
and return a single JSON object with the results.

## Tasks (per article)

1. **NER** — Extract named entities into 4 categories: PERSON, LOCATION, ORGANIZATION, MISC
2. **SUMMARY** — Write a 2-sentence summary in formal Modern Standard Arabic (فصحى).
   Do not copy verbatim from the source. Maintain formal register throughout.
3. **NLI** — For each provided claim, label it as SUPPORTED, REFUTED, or NOT_ENOUGH_INFO
   based solely on the article body.
4. **TRANSLATION** — Translate the provided English text to formal Arabic (فصحى).
   Be faithful to the source. No additions, no omissions, no dialect.

## Output format

Return ONE JSON object (and nothing else) with this exact structure:

```json
{
  "model_name": "<your-model-name-here>",
  "outputs": [
    {
      "article_id": "ARTICLE_ID_HERE",
      "ner_output": {
        "PERSON": ["..."],
        "LOCATION": ["..."],
        "ORGANIZATION": ["..."],
        "MISC": ["..."]
      },
      "summary_output": "<2-sentence Arabic summary>",
      "nli_output": [
        {"claim": "<the same claim text>", "label": "SUPPORTED|REFUTED|NOT_ENOUGH_INFO"},
        ...
      ],
      "translation_output": "<Arabic translation>"
    },
    ...
  ]
}
```

**IMPORTANT**:
- Replace `<your-model-name-here>` with the model you used (e.g. "claude-opus-via-cursor")
- Use the EXACT article_id values from the brief below
- For NLI, return labels in the SAME order as the claims provided
- Do not include any text outside the JSON object
- Do not wrap the JSON in markdown code fences in your final answer

---

# Articles to evaluate


## Article POLITICS_027

### Article body (Arabic)

```
قال وزير الدفاع الفرنسي ايرفيه موران، أمس، في الرياض انه ناقش مع القيادة السعودية الملف النووي الإيراني الذي قال انه مصدر قلق للبلدين، كما ذكر انه اطلع على رغبة المملكة بالحصول على أقمار اصطناعية للمراقبة .وفي ختام زيارة للمملكة استمرت يومين، أكد الوزير أن السعودية تشاطرنا نفس القلق . . . والتحليل حيال الملف النووي الإيراني وما يمثله هذا البرنامج من مخاطر على الاستقرار والتوازن في المنطقة .وأشار إلى وجود خطر انتشار السلاح النووي في المنطقة إذا ما حصلت طهران على القنبلة النووية إذ أن دولا أخرى ستسلك الطريق نفسه .وأكد موران انه اطلع من السعوديين على رغبة المملكة في الحصول على اقمار اصطناعية للمراقبة بهدف امتلاك قدرة ذاتية مستقلة للمراقبة، مشيرا إلى أن فرنسا تملك خبرة كبيرة في المجال . (أ .ف .ب)
```

### NLI claims to label
1. أعرب وزير الدفاع الفرنسي عن أن الملف النووي الإيراني يثير مخاوف مشتركة بين باريس والرياض
2. أشار الوزير الفرنسي إلى أن المملكة العربية السعودية ترغب في امتلاك أقمار صناعية لأغراض الرصد والمراقبة
3. استغرقت زيارة وزير الدفاع الفرنسي للمملكة العربية السعودية ثلاثة أيام
4. تم خلال الزيارة توقيع اتفاقية تعاون عسكري بين فرنسا والسعودية في مجال تكنولوجيا الأقمار الاصطناعية

### English text to translate to Arabic
```
French Defense Minister Hervé Morin discussed the Iranian nuclear file with the Saudi leadership during a two-day visit to Riyadh, stating that it is a shared source of concern for both countries and warning that Iran obtaining a nuclear weapon could trigger nuclear proliferation in the region. Morin also noted that Saudi Arabia expressed its desire to acquire surveillance satellites to develop an independent monitoring capability. He emphasized that France possesses significant expertise in the satellite field, signaling potential cooperation between the two nations.
```

---

## Article POLITICS_072

### Article body (Arabic)

```
أعلن مصدر في وزارة الداخلية اليمنية أن الوزارة وضعت يدها على عدد من الوثائق لعناصر كانت تعد لتنفيذ عمليات إرهابية في البلاد، وأوضح أن الأجهزة الأمنية وضعت يدها خلال ملاحقتها للعناصر الإرهابية على عدد من الوثائق المهمة التي تحتوي على أسماء وهواتف ومخططات لعمليات إرهابية، بالإضافة إلى أسلحة خطط لاستخدامها في عمليات انتحارية.وأشار المصدر إلى أن الحملة التي تنفذها الداخلية لملاحقة المطلوبين أمنياً من العناصر الإرهابية بتنظيم القاعدة والمعممة صورهم في الدليل الأمني لا تزال متواصلة بوتائر عالية، مؤكداً أن الأجهزة الأمنية حققت نتائج إيجابية من خلال كشفها وإحباطها لعدد من العمليات التي كان يخطط تنظيم القاعدة لتنفيذها في اليمن، وضبط عناصر إرهابية مطلوبة.وقال إن العناصر الإرهابية المطلوبة أمنياً يجري رصدها على مدار الساعة من قبل مختلف الأجهزة التي تؤدي مهمة التعقب والملاحقة بتنسيق كامل وتؤدي هذه المهمة بروح الفريق.من جهته، تبنى فرع تنظيم القاعدة في اليمن، (أ.ف.ب) في بيان على موقع إسلامي على الانترنت، الاعتداء الانتحاري الفاشل على قافلة مسؤولين كوريين جنوبيين في 18 آذار/مارس الماضي قرب مطار صنعاء.وجاء في بيان القاعدة في جزيرة العرب الذي تعذر التأكد من صحته، إن الأمر يتعلق ب عملية استشهادية استخباراتية نوعية على وفد المحققين الكوريين الجنوبيين في إشارة واضحة إلى عجز أجهزة الأمن اليمنية التي استعانت بوفد المحققين الكوريين ولم تستطع حمايتهم. وقالت القاعدة في بيانها الجديد أن اعتداء 18 آذار/مارس نفذه الشهيد شامل الصنعاني. غير أن وزارة الداخلية اليمنية قالت في بيان نشرته وكالة الأنباء اليمنية الحكومية في ضوء إجراء فحوصات الحمض النووي (دي.أن.إيه) لأشلاء الانتحاري تبين لأجهزة الأمن أن منفذ هذه العملية الإجرامية هو الإرهابي خالد عبد الله الضياني (20 عاما).
```

### NLI claims to label
1. عثرت الأجهزة الأمنية اليمنية على وثائق تتضمن أسماء وأرقام هواتف ومخططات لعمليات إرهابية أثناء ملاحقتها لعناصر متطرفة
2. أكدت وزارة الداخلية اليمنية أن حملة ملاحقة عناصر تنظيم القاعدة المطلوبين أمنياً لا تزال مستمرة بشكل مكثف
3. أظهرت نتائج فحوصات الحمض النووي أن منفذ الهجوم الانتحاري قرب مطار صنعاء يبلغ من العمر خمسة وعشرين عاماً
4. أسفر الهجوم الانتحاري على القافلة الكورية الجنوبية عن مقتل عدد من أفراد الوفد الكوري

### English text to translate to Arabic
```
Yemen's Interior Ministry announced that security forces seized documents containing names, phone numbers, and plans for terrorist operations, along with weapons intended for suicide attacks, during their ongoing campaign against Al-Qaeda suspects. Al-Qaeda's branch in Yemen claimed responsibility for the failed suicide attack on a convoy of South Korean officials near Sanaa airport on March 18, stating it was carried out by a militant they named Shamel al-Sanaani. However, the Yemeni Interior Ministry contradicted Al-Qaeda's claim, stating that DNA tests on the bomber's remains identified the attacker as 20-year-old Khaled Abdullah al-Dhayani.
```

---

## Article POLITICS_031

### Article body (Arabic)

```
وصل، أمس، إلى دمشق نائب الرئيس العراقي عادل عبدالمهدي في زيارة خاصة لم يعلن عنها من قبل .وتأتي زيارة عبدالمهدي إلى دمشق بعد طرح العاهل السعودي الملك عبدالله بن عبدالعزيز مبادرة لاجتماع القوى السياسية في العراق للاجتماع في الرياض بعد موسم الحج، لبحث أزمة تشكيل الحكومة العراقية . وكان عبدالمهدي قد بحث في بغداد أمس مع سفير تركيا في بغداد مراد أوزجليك، العلاقات الثنائية وسبل تطويرها في المجالات المختلفة، والقضايا ذات الاهتمام المشترك . وأكد عبدالمهدي حرص العراق على إقامة امتن العلاقات مع دول المنطقة، ولاسيما تركيا التي تربطها بالعراق علاقات وثيقة وتاريخية، وأشار إلى أهمية الارتقاء بمستوى التعاون الثنائي في مجال الاقتصاد والاستثمار، مثمناً مشاركة تركيا في معرض بغداد الدولي الذي افتتح أمس الأول، والجهود التي تبذلها الحكومة التركية من أجل المساهمة في إعادة إعمار البنى التحتية في العراق من خلال تواجد الشركات التركية . من جانبه، أكد السفير التركي حرص بلاده على تطوير العلاقات مع العراق وفي كافة المستويات، وخاصة في مجالات الاستثمار والتجارة والاقتصاد . واعتبر مشاركة بلاده في معرض بغداد بدورته الحالية مؤشراً على اهتمام تركيا بتطوير العلاقات مع الجانب العراقي .
```

### NLI claims to label
1. وصل نائب الرئيس العراقي عادل عبدالمهدي إلى العاصمة السورية في زيارة لم يُعلن عنها مسبقاً
2. اقترح العاهل السعودي الملك عبدالله بن عبدالعزيز عقد لقاء للقوى السياسية العراقية في الرياض بعد موسم الحج لمناقشة أزمة تشكيل الحكومة
3. التقى عبدالمهدي في بغداد مع سفير إيران لبحث العلاقات الثنائية وسبل تطويرها
4. شارك عبدالمهدي شخصياً في افتتاح معرض بغداد الدولي

### English text to translate to Arabic
```
Iraqi Vice President Adel Abdul-Mahdi arrived in Damascus on an unannounced private visit, which came after Saudi King Abdullah bin Abdulaziz proposed an initiative to convene Iraqi political forces in Riyadh after the Hajj season to discuss the crisis of forming the Iraqi government. Prior to his visit, Abdul-Mahdi had met in Baghdad with Turkey's Ambassador Murat Özçelik to discuss bilateral relations and ways to develop them across various fields, with both sides emphasizing the importance of enhancing cooperation in economy, investment, and trade. Abdul-Mahdi praised Turkey's participation in the Baghdad International Fair and the efforts of Turkish companies in contributing to the reconstruction of Iraq's infrastructure.
```

---

## Article POLITICS_081

### Article body (Arabic)

```
أفادت صحيفة صنداي تليغراف، أمس، أن إيرلندياً ليبي الأصل عمره 16 عاماً، قتل في سوريا، بعد انضمامه للقتال إلى جانب المعارضين العام الماضي .وقالت الصحيفة إن شمس الدين غيدان انتقل مع عائلته من ليبيا إلى جمهورية إيرلندا عام ،2001 وافتتح والده لاحقاً متجراً للأطعمة في بلدة نافان، وأمضى عطلته الصيفية العام الماضي في ليبيا، وكان من المقرر أن يعود إلى ايرلندا منتصف أغسطس/آب الماضي، عن طريق تركيا . وأضافت أن عائلة شمس الدين علمت أن ابنها عبر الحدود التركية إلى سوريا للانضمام إلى المتمردين مع ابن عمه الذي سافر إلى سوريا من ليبيا في وقت سابق، والذي يُعتقد أنه قُتل هناك أيضاً، فيما أكد المتحدث باسم الرابطة الإسلامية في جمهورية إيرلندا حسين بوهدمة، أن الصبي قُتل في سوريا الأسبوع الماضي .ونسبت الصحيفة إلى والد شمس الدين قوله لا نعرف كيف وأين قُتل ومكان جثته، ومن الصعب جداً الحصول على أي معلومات عن ذلك، ما يجعل حزننا أسوأ بكثير . وأشارت إلى أن شمس الدين هو ثاني إيرلندي يلقى حتفه في سوريا بعد المصري المولد حذيفة السيد (22 عاماً)، الذي قُتل في ديسمبر الماضي . (يو .بي .آي)
```

### NLI claims to label
1. انتقلت عائلة شمس الدين غيدان من ليبيا إلى إيرلندا في عام 2001 وقام والده بافتتاح محل لبيع المواد الغذائية في بلدة نافان
2. يُعدّ شمس الدين غيدان ثاني مواطن إيرلندي يُقتل في الصراع السوري بعد حذيفة السيد ذي الأصول المصرية
3. كان شمس الدين غيدان يبلغ من العمر 18 عاماً حين لقي مصرعه في سوريا
4. قامت السلطات الإيرلندية بفتح تحقيق رسمي حول ملابسات سفر شمس الدين إلى سوريا

### English text to translate to Arabic
```
A 16-year-old Irish teenager of Libyan origin, named Shamseddine Gheidan, was killed in Syria after crossing the Turkish border to join the rebels alongside his cousin, who is also believed to have been killed there. His family, who had moved from Libya to Ireland in 2001, learned of his death last week, with his father stating that they do not know how or where he was killed or the location of his body. Shamseddine is the second Irish national to die in Syria, following the death of Egyptian-born Hudhaifa Al-Sayed, aged 22, who was killed in December.
```

---

## Article POLITICS_085

### Article body (Arabic)

```
هدمت جرافات الاحتلال «الإسرائيلي» أمس الاثنين، منازل ثلاثة شهداء في بلدة قباطية قرب جنين شمال الضفة الغربية المحتلة؛ بحجة تنفيذهم عملية طعن وإطلاق نار في باب العامود في مدينة القدس المحتلة، وسلمت إخطاراً لهدم منزل رابع، وأقدمت على هدم 4 منازل أخرى في القدس المحتلة والخليل ونابلس، بحجة البناء من دون ترخيص، وتم اعتقال أكثر من 20 فلسطينياً في بلدات ومدن الضفة الغربية المحتلة، في وقت أعلنت سلطات الاحتلال عن مشروع استيطاني كبير؛ لشرعنة البؤر العشوائية منذ 1998، لإسكان 77 ألف مستوطن في شرق رام الله.فقد اقتحمت قوات كبيرة من جيش الاحتلال تساندها جرّافات بلدة قباطية، وانتشرت في أحيائها كافة، وحولت منازل عدة إلى نقاط عسكرية قبل الشروع بعمليات الهدم، ودارت مواجهات في محيط المكان عقب محاولة أهالي البلدة التصدي لقوات الاحتلال، الأمر الذي أدى إلى إصابة شابين بالرصاص الحي في الساقين، كما أصيب العشرات بحالات الاختناق، وسلمت سلطات الاحتلال عائلة أسير محرّر إخطاراً بهدم منزله؛ بحجة قيامه بنقل الشهداء الثلاثة إلى القدس. كما هدمت قوات الاحتلال منزلاً في منطقة خلة عين الحمام، في بلدة صوريف قرب الخليل، جنوب الضفة الغربية، بحجة عدم الترخيص، إضافة إلى هدم منزل في بلدة «خربة المراجم» قرب نابلس شمال الضفة الغربية المحتلة. وهدمت قوات الاحتلال منزلين، إضافة إلى عشرات الأمتار من السلاسل الحجرية في خربة المراجم غرب قرية دوما جنوب مدينه نابلس. وقال مسؤول ملف الاستيطان في شمال الضفة الغربية غسان دغلس إن ثلاث جرافات عسكرية، إضافة إلى أكثر من عشر جيبات عسكرية اقتحمت خربة المراجم الواقعة غرب قرية دوما، وشرعت بأعمال الهدم لمنزلين.هدمت جرافات الاحتلال منزلاً فلسطينياً في جبل المبكر جنوب القدس، وقال صاحب المنزل عبد الباسط أبو أرميلة، إن قوات كبيرة من الاحتلال وطواقم الهدم حاصرت منزله الواقع في حي الفاروق بجبل المبكر، وأخرجت من فيه بالقوة قبل أن تشرع بهدمه. من جهته قال كبير المفاوضين الفلسطينيين صائب عريقات، إن «إسرائيل» هدمت 157 منزلاً فلسطينياً في شرق القدس والضفة الغربية منذ منتصف سبتمبر الماضي، وندد في بيان بهدم قوات الاحتلال سبعة منازل فلسطينية في شرق القدس وبلدات صوريف وقباطية ودوما في الضفة الغربية يوم أمس، وقال: «إنه يتم توثيق كل جريمة ترتكبها «إسرائيل» السلطة القائمة بالاحتلال، ضد أبناء شعبنا وحقوقه غير القابلة للتصرف، ويتم تقديمها إلى الهيئات الدولية ذات الصلة، بما في ذلك المحكمة الجنائية الدولية».وأضاف: «إن مواصلة سلطات الاحتلال اتباع سياسة العقاب الجماعي ضد أبناء شعبنا من المدنيين الفلسطينيين، هو انتهاك للقانون الدولي والتزامات «إسرائيل» بوصفها القوة القائمة بالاحتلال، ويتطلب رداً ملموساً من قبل المجتمع الدولي»، وشدد عريقات على أن «منح الحصانة لجرائم الاحتلال، والسماح ل«إسرائيل» بالتصرف كدولة فوق القانون من شأنه فقط إطالة أمد الاحتلال وانتهاكاته لحقوق الفلسطينيين، وتقويض أي أفق سياسي واقعي لإنهاء الاحتلال، وتدمير حل الدولتين».إلى جانب ذلك اعتقلت قوات الاحتلال أمس الاثنين، 19 فلسطينياً بمناطق متفرقة من الضفة الغربية، وقال نادي الأسير الفلسطيني في بيان، إن قوات الاحتلال دهمت مدن الخليل وبيت لحم ونابلس ورام الله وجنين، وسط إطلاق كثيف للنيران، واعتقلت من تزعم أنهم مطلوبون، وذكر النادي أن ثلاثة فلسطينيين اعتقلوا من بلدة تقوع ومخيم عايدة شرق وشمال بيت لحم، وأشار إلى أن الفتية الثلاثة تتراوح أعمارهم بين 16 و17 عاماً. وأفادت وسائل إعلام «إسرائيلية» أمس الاثنين، بأن قوات من جيش الحرب اعتقلت الليلة قبل الماضية 13 فلسطينياً في مناطق مختلفة بالضفة الغربية.في غضون ذلك بادرت الحركة الاستيطانية «أماناه» بدعم وزير الحرب «الإسرائيلي» موشيه يعالون ومجلس مستوطنات «ماطيه بنيامين» إلى تطوير مخطط هيكلي استيطاني شرس، لما يسمى بمستوطنة «مخماش مزراح» القاضي بتحويل كل من: مستوطنات «معاليه مخماش»، و«ريمونيم»، و«بساغوت»، و«كوخاف»، و«يئير» الواقعة شرقي رام الله، إلى ضاحية سكنية ريفية وشبه مدنية يسكنها 77 ألف مستوطن.ومن بين مجمل أهداف الخطة الاستيطانية الجديدة، شرعنة البؤرة الاستيطانية غير القانونية «متسببيه داني» التي أقيمت عام 1998 بطريقة غير قانونية، ويهدف المخطط الذي مر بعدة تغييرات، إلى إيجاد تواصل جغرافي من الجهة الشرقية للشارع الاستيطاني الالتفافي رقم 60.وقد أقر ما يسمى مجلس التنظيم الأعلى للإدارة المدنية قبل أشهر عدة، التقدم في المخطط الهيكلي الذي تعكف عليه ما تسمى «مديرية الاستيطان»، ليشتمل على خطة لتوسيع مكثف لمستوطنات المنطقة، وإقامة ما يقارب 2500 وحدة سكنية جديدة على مساحة 790 دونماً على مراحل عدة.ويسكن اليوم في المستوطنات الأربع، وفي البؤرة الاستيطانية «متسببيه داني» وفق معطيات دائرة الإحصاء المركزية، نحو ستة آلاف مستوطن، ويبلغ إجمالي عدد سكان المجلس الإقليمي «ماطيه بنيامين» الذي تتبع له هذه المستوطنات وغيرها، نحو 55 ألف مستوطن.وبناء على المخطط الاستيطاني، فمن المقدر زيادة 70 ألف مستوطن في المستوطنات الأربعة والبؤرة الاستيطانية «متسببيه داني» في غضون أقل من 25 عاماً.أما مستوطنة «معاليه مخماش» فمن المقدر وفق المخطط أن يصل عدد سكانها إلى سبعة آلاف مستوطن في عام 2040. (وكالات)
```

### NLI claims to label
1. صرّح صائب عريقات أن قوات الاحتلال هدمت 157 منزلاً فلسطينياً في شرق القدس والضفة الغربية منذ منتصف سبتمبر الماضي
2. يهدف المخطط الاستيطاني الجديد إلى إنشاء نحو 2500 وحدة سكنية على مساحة 790 دونماً عبر مراحل متعددة
3. أُنشئت البؤرة الاستيطانية غير القانونية المعروفة بـ«متسببيه داني» في عام 2001 بشكل مخالف للقانون
4. قدّم الجانب الفلسطيني شكوى رسمية إلى مجلس الأمن الدولي بشأن عمليات الهدم التي جرت في قباطية

### English text to translate to Arabic
```
Israeli occupation forces demolished the homes of three Palestinian martyrs in the town of Qabatiya near Jenin in the northern occupied West Bank, citing a stabbing and shooting attack at Damascus Gate in occupied Jerusalem, while also demolishing four additional homes in Jerusalem, Hebron, and Nablus under the pretext of building without permits and arresting over 20 Palestinians across the West Bank. Chief Palestinian negotiator Saeb Erekat condemned the demolitions, stating that Israel had destroyed 157 Palestinian homes in East Jerusalem and the West Bank since mid-September, and emphasized that all crimes are being documented and submitted to international bodies including the International Criminal Court. Meanwhile, the Amana settlement movement, backed by Israeli War Minister Moshe Ya'alon, announced a major settlement plan to legalize illegal outposts established since 1998 and expand settlements east of Ramallah to house 77,000 settlers within 25 years.
```

---

## Article POLITICS_006

### Article body (Arabic)

```
القاهرة - "الخليج": تضاربت الأنباء، أمس، حول سقوط قتلى ومصابين في الاشتباكات العنيفة التي دارت في عدد من المحافظات المصرية بين قوات الشرطة وأنصار جماعة الإخوان الارهابية، في وقت تحدثت فيه الجماعة عن سقوط ثلاثة من أنصارها قتلى في منطقة شبرا الخيمة التابعة لمحافظة القليوبية، وهو ما أدى إلى اشتعال المواجهات بين الأهالي وقوات الشرطة، رغم نفي مصادر في وزارة الصحة عدم تسجيل أي حالات إصابة أو وفاة في الاشتباكات .وتكشفت أمس ملامح مخطط إخواني يستهدف إثارة الفوضى في القاهرة والمحافظات، في وقت قالت مصادر أمنية رفيعة إن الجماعة تخطط لاستغلال التظاهرات التي دعت إليها بعض القوى في 19 مارس/ آذار الجاري، واعتبار هذه التظاهرات بمثابة إعلان للنفير العام لمختلف قوى تيار الإسلام السياسي المناوئة لثورة التصحيح في 30 يونيو، مشيرة إلى أن الجماعة تستهدف من المشاركة في تلك التظاهرات، لفت نظر النظام الحالي لسلسلة المبادرات التي أطلقتها قوى إسلامية، من أجل مشاركة الجماعة مجددا في المشهد السياسي المصري، ورفعها من قائمة المنظمات الإرهابية .وشهدت القاهرة الكبرى وعدد من المحافظات المصرية، مسيرات متفرقة دعا إليها ما يسمى ب "تحالف دعم الشرعية" الذي يضم جماعة الإخوان وأنصارها من قوى تيار الإسلام السياسي، فيما عرف ب "جمعة الشارع لنا"، غير أن هذه المسيرات لم تسلم من مشاهد عنف، بلغت ذروتها في منطقتي الهرم وفيصل بمحافظة الجيزة، بعدما تسببت الألعاب النارية والشماريخ التي أطلقها أنصار الجماعة باتجاه المنازل والمواطنين المناهضين لهم في الشرفات، إلى احتراق احد محال الملابس في شارع العريش بمنطقة الهرم وامتداد النيران إلى البناية المجاورة للمحل، قبل أن تتمكن قوات الدفاع المدني من السيطرة على الحريق .وقال شهود عيان إن النيران تسببت في إصابة ثلاثة من أهالي المنطقة الذين هرعوا لإطفاء الحريق، في وقت راح فيه أنصار الجماعة يشعلون النيران في عدد من السيارات الخاصة، من بينها سيارة مملوكة لأحد الضباط، وإطلاق الألعاب النارية والشماريخ بكثافة على الأهالي، بعدما قام هؤلاء برشهم بالمياه الملوثة من الشرفات . وشهدت منطقة عين شمس بالقاهرة أحداثا مشابهة في أعقاب اشتباكات بين عناصر الإخوان وأهالي المنطقة، استخدم خلالها الطرفان زجاجات المولوتوف والألعاب النارية، بعدما ردد أنصار الجماعة هتافات مناهضة للجيش أثناء مرورهم بالمنطقة، فيما أشعل أنصار الجماعة النيران في عدد من السيارات الخاصة بضاحية حلوان، قبل أن تنتقل سيارات الحماية المدنية للسيطرة على النيران قبل امتدادها إلى السيارات والبيوت . وبلغت الأحداث ذروتها في منطقة شبرا الخيمة أمس، في أعقاب تنظيم جماعة الإخوان لعدد من المسيرات، انطلقت عصر أمس في مناطق عدة في شبرا الخيمة والخانكة، رفع خلالها المتظاهرون صورا للرئيس السابق محمد مرسي وعلامات رابعة، وسط تحفز أمني، تحسبا لاندلاع أعمال تخريبية تجاه عدد من المنشآت الشرطية . وقال شهود عيان إن عناصر الجماعة قامت بإشعال النيران في إطارات السيارات أمام الوحدة المحلية بحي شبرا الخيمة، وقطعت الطريق أمام السيارات، ما دفع قوات الشرطة للتدخل، وتوقيف عدد من المتظاهرين، قبل أن تتسبب شائعة وفاة ثلاثة منهم على يد ضباط قسم شرطة شبرا الخيمة، في إشعال الموقف وبدء اشتباكات عنيفة بين الأهالي وقوات الشرطة التي لجأت إلى استخدام قنابل الغاز لتفريق المتظاهرين وملاحقتهم في الشوارع الجانبية بعد فتح الطريق أمام السيارات .وفي سياق متصل، نجحت أجهزة الأمن في محافظة الفيوم في توقيف خلية تابعة لجماعة الإخوان، تورطت في إحراق عدد من سيارات الشرطة والأهالي بالمحافظة على مدار الأسابيع الأخيرة، وقالت مصادر أمني إن الخلية تضم 6 من عناصر تنظيم الإخوان، أطلقوا على أنفسهم "مجموعة مولوتوف"، مشيرا إلى أن هذه المجموعة استهدفت حرق سيارات الشرطة بالمحافظة .
```

### NLI claims to label
1. أعلنت جماعة الإخوان عن مقتل ثلاثة من مؤيديها في منطقة شبرا الخيمة بمحافظة القليوبية
2. تمكنت الأجهزة الأمنية في محافظة الفيوم من القبض على خلية إخوانية مكونة من ستة أفراد أطلقوا على أنفسهم اسم مجموعة مولوتوف
3. أدت الألعاب النارية التي أطلقها أنصار الجماعة في منطقة الهرم إلى احتراق أحد محلات الأثاث في شارع العريش
4. أسفرت اشتباكات منطقة عين شمس عن سقوط عدد من القتلى في صفوف المدنيين

### English text to translate to Arabic
```
Violent clashes erupted across several Egyptian governorates between police forces and supporters of the Muslim Brotherhood, with conflicting reports about casualties — the Brotherhood claimed three of its supporters were killed in Shubra al-Khaima in Qalyubia, while the Health Ministry denied any recorded injuries or deaths. The clashes, which occurred during marches called by the so-called 'Alliance to Support Legitimacy' under the banner 'Friday the Street is Ours,' escalated in areas including Haram, Faisal, Ain Shams, and Helwan, where Brotherhood supporters set fire to cars and shops using fireworks and Molotov cocktails. Security forces in Fayoum also arrested a six-member Brotherhood cell calling itself the 'Molotov Group,' which was involved in burning police and civilian vehicles in recent weeks.
```

---

## Article POLITICS_018

### Article body (Arabic)

```
اعتبر الرئيس التركي رجب طيب أردوغان، أمس، أن حملة القصف الجوي التي تشنها موسكو في سوريا «خطأ جسيم» وسيحكم التاريخ على دعمها للرئيس السوري بشار الأسد. وقال أردوغان في مؤتمر صحفي قبل توجهه إلى فرنسا «إن الخطوات التي تقوم بها روسيا وحملة القصف في سوريا غير مقبولة مطلقاً من قبل تركيا». وأضاف «للأسف فإن روسيا ترتكب خطأً جسيماً». وتابع أن تصرفات موسكو في سوريا «مقلقة»، محذراً من أنها «ستؤدي إلى عزل روسيا في المنطقة». وتساءل «ما الذي تحاول روسيا أن تحققه؟.. لقد تدخلت لأن هذا مطلب النظام في سوريا. لكن لا يوجد التزام للرد بهذا الشكل في كل مرة يطلب النظام ذلك». واستهدفت طائرات إف-16 التركية 17 موقعاً للحزب في شمالي العراق ودمرت ملاجئ يستخدمها مقاتلوه. وأوضحت وسائل إعلام رسمية أن طائرات سلاح الجو التركي قصفت 17 موقعاً للحزب الكردستاني في مناطق حفتنين ومتينا وقنديل شمالي العراق. ونقلت وكالة أنباء «الأناضول» عن مصادر أمنية أن تسع طائرات من طراز «إف16-» شاركت في القصف، الذي استمر نحو ساعتين أمس، وأسفر عن تدمير المواقع السبعة عشر. وأعلن الجيش أن طائراته دمرت مخازن وقود وذخيرة في محافظتي هكاري على الحدود العراقية وقارس شرقاً.وكان الجيش التركى اتهم حزب العمال بخطف اثنين من جنوده. (وكالات)
```

### NLI claims to label
1. وصف الرئيس التركي أردوغان العمليات العسكرية الروسية في سوريا بأنها خطأ كبير وأنها ستعزل روسيا عن المنطقة
2. شاركت تسع طائرات من نوع إف-16 في عملية قصف استهدفت مواقع حزب العمال الكردستاني في شمال العراق
3. استمرت عملية القصف التركي لمواقع حزب العمال الكردستاني قرابة أربع ساعات ودمرت خمسة عشر موقعاً
4. أدانت الحكومة العراقية رسمياً الغارات التركية على مواقع حزب العمال الكردستاني في شمال العراق

### English text to translate to Arabic
```
Turkish President Recep Tayyip Erdogan described Russia's aerial bombing campaign in Syria as a 'grave mistake' and warned that history would judge Moscow's support for Syrian President Bashar al-Assad, stating that Russia's actions are entirely unacceptable to Turkey and could lead to its isolation in the region. Meanwhile, Turkish F-16 fighter jets targeted and destroyed 17 positions belonging to the Kurdistan Workers' Party (PKK) in the Haftanin, Metina, and Qandil areas of northern Iraq, in a bombing operation lasting approximately two hours involving nine aircraft. The Turkish army also announced the destruction of fuel and ammunition depots in the provinces of Hakkari on the Iraqi border and Kars in the east, following accusations that the PKK had kidnapped two of its soldiers.
```

---

## Article POLITICS_003

### Article body (Arabic)

```
شارك الآلاف في احتجاج وسط لندن أمس الأول السبت، ضد تجديد نظام «ترايدنت» البريطاني للأسلحة النووية. ويتوقع أن تتخذ بريطانيا قراراً في وقت لاحق من هذا العام حول استبدال غواصاتها القديمة التي تحمل صواريخ ترايدنت بكلفة تبلغ 31 مليار جنيه إسترليني (39 مليار يورو، 43 مليار دولار). وتؤيد حكومة رئيس الوزراء ديفيد كاميرون المحافظة هذا الأمر، وتعتبر أن النظام ضروري لحماية أمن بريطانيا. وقال وزير الدفاع فيليب دان قبل المسيرة إن عدم تجديد هذا النظام «سيكون رهاناً طائشاً بأمننا القومي سيفيد أعداءنا». وتملك بريطانيا حالياً أربع غواصات في أسطول «ترايدنت»، وتقوم إحداها على الأقل بدوريات في المحيطات على مدار الساعة. وتريد الحكومة استبدال هذه الغواصات بأربع من غواصات «ساكسيسور» التي ستدخل أولاها الخدمة في مطلع 2030. ويؤكد منظمو المسيرة وجود معارضة شعبية متزايدة لنظام الأسلحة الذي يعود تاريخه إلى الحرب الباردة ومركزه على الساحل الغربي لإسكتلندا. (أ.ف.ب)
```

### NLI claims to label
1. تعتزم الحكومة البريطانية استبدال غواصاتها الحالية بأربع غواصات جديدة من طراز ساكسيسور
2. وصف وزير الدفاع البريطاني فيليب دان عدم تجديد منظومة ترايدنت بأنه مجازفة غير مسؤولة بالأمن الوطني
3. تبلغ تكلفة استبدال غواصات ترايدنت نحو واحد وأربعين مليار جنيه إسترليني
4. شهدت المسيرة مشاركة زعيم حزب العمال البريطاني جيريمي كوربين كأحد المتحدثين الرئيسيين

### English text to translate to Arabic
```
Thousands of protesters marched in central London on Saturday against the renewal of Britain's Trident nuclear weapons system, as the UK government prepares to decide later this year on replacing its aging Trident missile-carrying submarines at an estimated cost of 31 billion pounds sterling. The Conservative government of Prime Minister David Cameron supports the renewal, with Defence Secretary Philip Dann warning that failing to renew the system would be a reckless gamble with national security. Protest organizers emphasized growing public opposition to the Cold War-era weapons system, which is based on the west coast of Scotland, while the government plans to replace the current four submarines with new Successor-class submarines, the first of which would enter service in early 2030.
```

---

## Article POLITICS_099

### Article body (Arabic)

```
علق نائب مستشار الأمن القومي في عهد الرئيس الأمريكي السابق جورج بوش إليوت إبرامز على اصطحاب الرئيس المصري حسني مبارك نجله إلى الولايات المتحدة في زيارته التي يجريها حاليا للمشاركة في إطلاق المفاوضات المباشرة بين الفلسطينيين والإسرائيليين بالقول إن مبارك يرتكب خطأ كبيراً .وأضاف في تصريحات لصحيفة المصري اليوم المستقلة نشرتها أمس، أن وجود جمال، الذي لا يشغل أي منصب رسمي، بين أعضاء الوفد المصري قد يراه عدد كبير من المصريين محاولة لوضع نجل الرئيس داخل المشهد السياسي الدولي بالقوة .وكانت صحيفة هآرتس الإسرائيلية ذكرت أول أمس أن جمال مبارك سيقابل مفاوضين إسرائيليين خلال المحادثات، ربما يكون رئيس الوزراء الإسرائيلي نفسه من بينهم، مضيفةً أن اصطحاب الرئيس مبارك نجله إلى واشنطن يعد مؤشراً واضحاً على إعداده للخلافة في مصر . (د ب أ)
```

### NLI claims to label
1. إليوت إبرامز شغل منصب نائب مستشار الأمن القومي خلال فترة رئاسة جورج بوش
2. أشارت صحيفة هآرتس إلى أن اصطحاب مبارك لنجله إلى واشنطن يُعتبر دلالة على تجهيزه لتولي السلطة في مصر
3. نُشرت تصريحات إبرامز في صحيفة الأهرام الحكومية المصرية
4. رفض جمال مبارك التعليق على انتقادات إبرامز بشأن مرافقته لوالده في الزيارة

### English text to translate to Arabic
```
Elliott Abrams, former U.S. Deputy National Security Advisor under President George W. Bush, criticized Egyptian President Hosni Mubarak for bringing his son Gamal to the United States during his visit to attend the launch of direct Palestinian-Israeli negotiations, calling it a major mistake. Abrams stated that the presence of Gamal, who holds no official position, in the Egyptian delegation could be seen by many Egyptians as a forced attempt to place the president's son on the international political stage. The Israeli newspaper Haaretz reported that Gamal Mubarak was expected to meet Israeli negotiators, possibly including the Israeli Prime Minister himself, adding that his presence in Washington was a clear indication of preparations for presidential succession in Egypt.
```

---

## Article POLITICS_040

### Article body (Arabic)

```
بغداد:«الخليج»، وكالات واصلت القوات العراقية، أمس، عمليات تطهير ومطاردة الإرهابيين في آخر جيوب لهم في الجانب الشرقي للموصل، غداة إعلان «تحرير» تلك الجهة من المدينة، فيما تمكنت القوات العراقية من استعادة قضاء تلكيف والقصور الرئاسية، وفندق نينوى في شمال الموصل، في وقت أعلن جهاز مكافحة الإرهاب عن انتهاء مهمته في تحرير المحور الشمالي للساحل الأيسر للموصل. وقال الفريق الركن عبدالغني الأسدي، قائد قوات جهاز مكافحة الإرهاب إن قواته تقوم بمساعدة الجيش، باستعادة منطقتين متبقيتين تحت سيطرة الإرهابيين بينها القصور الرئاسية وفندق نينوى. وقال الأسدي إنه حتى صباح أمس، لا تزال هناك اشتباكات بواسطة القناصين وأسلحة ثقيلة، «وقد تم التعامل معهم من قبل طيران التحالف الدولي، وتستعد قواتنا الآن للتقدم لإكمال عمليات التطهير». من جهة أخرى، ذكر قائد عمليات «نينوى» الفريق الركن عبدالأمير يار الله، في بيان، إن «قوات مكافحة الإرهاب تمكنت من خلال قيادة العمليات الخاصة الأولى والثالثة، من إكمال مهمتها بتحرير كل المناطق والأحياء الموكلة إليها ضمن الاتجاه الشمالي لمحور قيادة مكافحة الإرهاب». وأضاف أن المهمة «شملت تحرير ناحية برطلة وكوكجلي وقرى طوبزاوة وطهراوة العليا والموفقية بالاشتراك مع قيادة العمليات الخاصة الثانية». وأردف كما «تمكنت من تحرير الأحياء ضمن الساحل الأيسر، وكما يلي: (حي الزهراء، والتحرير، والعلماء، والمعلمين، والمحاربين، والقاهرة، والنهضة، والمصارف، وحي الجامعة، والبريد، والفلاح، والرحمة، والقادسية الأولى، والثانية، والزهور، والشيخكية، والمرور، و30 تموز، والمشراق، والمثنى، والرفاق، والسكّر، والبلديات، والصدّيق، والكفاءات الأولى، وجامعة الموصل، والأندلس، والشرطة، والمجموعة الثقافية، والمهندسين، والزراعة، والمنطقة الأثرية، وتل نركال، والغابات، والقصور الرئاسية، وفندق نينوى أوبروي والجسرين الثالث والخامس)».في الأثناء حررت القوات الأمنية، أمس، منشأة جابر بن حيان، والقصور الرئاسية في المحور الشمالي للموصل. وقال يارالله في بيان آخر، إن «القوات العراقية حررت منشأة جابر بن حيان والقصور الرئاسية ورفعت العلم العراقي فيها».من جانبها، ذكرت خلية الإعلام الحربي التابعة لقيادة العمليات المشتركة أن القوات الأمنية حررت قضاء تلكيف شمالي مدينة الموصل بالكامل. وذكر بيان للخلية، أن «قطعات عسكرية عراقية، وبإسناد من طيران التحالف الدولي والطائرات العراقية، حررت قضاء تلكيف بالكامل ورفعت العلم العراقي على المباني»، كما حررت قوات مكافحة الإرهاب، الرتل الشمالي فندق نينوى (أوبروي).وفي محافظة ديالى، قال رئيس مجلس ناحية العظيم محمد ضيفان العبيدي، إن «طائرة مسيرة تابعة لتنظيم «داعش» حلقت فوق ناحية العظيم والمناطق القريبة منها، وهي الثانية من نوعها خلال الساعات ال48 الماضية».
```

### NLI claims to label
1. أعلن الفريق الركن عبدالأمير يار الله أن قوات مكافحة الإرهاب أتمت مهمتها في تحرير جميع المناطق المكلفة بها في الاتجاه الشمالي لمحور قيادة مكافحة الإرهاب
2. رصدت طائرة بدون طيار تابعة لتنظيم داعش وهي تحلق فوق ناحية العظيم في محافظة ديالى وكانت الثانية من نوعها خلال يومين
3. أكد الفريق الركن عبدالغني الأسدي أن قواته تساعد الجيش في استعادة ثلاث مناطق لا تزال تحت سيطرة الإرهابيين
4. شاركت قوات البيشمركة الكردية في عمليات تحرير قضاء تلكيف شمالي الموصل

### English text to translate to Arabic
```
Iraqi forces continued operations to clear and pursue terrorists in the last remaining pockets on the eastern side of Mosul, following the announcement of its liberation, while also recapturing Tal Kayf district, the presidential palaces, and the Nineveh Hotel in northern Mosul. Lieutenant General Abdul Ghani al-Asadi, commander of the Counter-Terrorism Service, stated that his forces were assisting the army in reclaiming the final two areas under terrorist control, amid ongoing clashes involving snipers and heavy weapons supported by international coalition airstrikes. Meanwhile, Iraqi military units fully liberated Tal Kayf district north of Mosul and raised the Iraqi flag on its buildings, while in Diyala province, a drone belonging to ISIS was reported flying over the Al-Azim sub-district for the second time in 48 hours.
```

---
