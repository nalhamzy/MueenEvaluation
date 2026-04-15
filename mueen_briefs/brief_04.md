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


## Article FINANCE_016

### Article body (Arabic)

```
واصلت أسواق الأسهم الخليجية التأثر بالأوضاع السياسية غير المستقرة التي تشهدها دول عربية وخليجية فشهدت موجة تراجع جماعية حادة كان أبرز ضحاياها السوق السعودي الذي فقد 15% إلى 27 .5،323 نقطة لتنتشر بعد ذلك عمليات البيع العشوائية في كافة أسواق المنطقة من دون أي استثناء، وتراجع مؤشر بورصة قطر بنسبة 8 .8 في المئة إلى 25 .7،489 نقطة، ومؤشر سوق دبي المالي بنسبة 61 .8 في المئة إلى 24 .1،352 نقطة، فيما تراجع مؤشر سوق أبوظبي للأوراق المالية بنسبة 20 .3 في المئة إلى 82 .2،529 نقطة، وسجل المؤشر السعري لسوق الكويت للأوراق المالية تراجعاً بنسبة 14 .5 في المئة إلى 7 .6،147 نقطة، ومؤشر سوق مسقط 4 .4% إلى 23 .6،352 نقطة، ومؤشر سوق البحرين للأوراق المالية 86 .3 في المئة إلى 36 .1،377 نقطة .
```

### NLI claims to label
1. كان السوق السعودي الأكثر تضرراً بين أسواق الأسهم الخليجية حيث خسر نحو خمسة عشر بالمئة من قيمته
2. انخفض مؤشر بورصة قطر بنسبة تقارب تسعة بالمئة ليصل إلى ما يقرب من 7,489 نقطة
3. هبط مؤشر سوق دبي المالي بنسبة تجاوزت ستة بالمئة ليصل إلى نحو 1,352 نقطة
4. أعلنت هيئة الأوراق المالية السعودية عن تعليق التداول مؤقتاً بسبب حدة التراجعات

### English text to translate to Arabic
```
Gulf stock markets continued to be affected by the unstable political conditions in several Arab and Gulf countries, experiencing a sharp collective decline, with the Saudi market being the hardest hit, losing 15% to drop to 5,323.27 points. Panic selling then spread across all regional markets without exception, as Qatar's exchange index fell by 8.8%, Dubai's financial market index dropped by 8.61%, and Abu Dhabi's securities market index declined by 3.20%. The Kuwait securities market price index also recorded a decline of 5.14%, while the Muscat market index fell by 4.4% and the Bahrain securities market index dropped by 3.86%.
```

---

## Article FINANCE_076

### Article body (Arabic)

```
حافظت أسواق الأسهم المحلية على تحركاتها الهادئة، أمس، ليغلق مؤشر سوق الإمارات منخفضاً 09 .0% إلى 41 .2687 نقطة بخسائر 29 .353 مليون درهم أوصلت القيمة السوقية إلى 09 .390 مليار درهم بتداولات 59 .276 مليون درهم، وذلك نتيجة لانخفاض مؤشر سوق دبي 23 .0% إلى 39 .1659 نقطة بتداولات 7 .165 مليون درهم، ومؤشر سوق أبوظبي 17 .0% إلى 19 .2748 نقطة بتداولات 8 .110 مليون درهم .انخفض إعمار 84 .0% إلى 55 .3 درهم، وأرابتك 49 .0% إلى 03 .2 درهم، ودبي المالي 65 .0% إلى 52 .1 درهم، فيما ارتفع الدار 86 .0% إلى 35 .2 درهم، وصروح 61 .0% إلى 66 .1 درهم .وتستمر الأسواق بالتحرك على أرضية الترقب المستمر لجملة من المتغيرات الأساسية المؤثرة في التداولات في مقدمها مستويات السيولة المحلية والتطورات على صعيد حجم المخصصات المطلوبة من البنوك والتي تحدد مدى قدرتها على الاقراض، حيث لا تزال الشركات المساهمة ومجمل الوضع الاقتصادي يعاني من أزمة التمويل .وترتبط إمكانية دخول الأسواق في مرحلة المتتابع بمدى قناعة المستثمرين بتراجع نسب المخاطرة ما يجعلهم يتمسكون بأسهمهم لفترات أطول فتقل العروض وتصبح الطلبات قادرة على دفع الأسعار نحو مزيد من الانتعاش، وذلك في حال تحسنت صورة الوضع الاقتصادي العام وسادت حالة من التفاؤل لدى المستثمرين حول نتائج الشركات وأحجام التداول خلال الفترات المقبلة .وتسهم قدرة الأسواق على استقطاب السيولة من الداخل والخارج في تحسين فرص تعزيز المكاسب المتراكمة للأسهم بعد ان اجتازت مرحلة انحسار التداولات وباتت الطلبات قادرة على استيعاب العروض لتحد من احتمالات الهبوط السريع وتبقي انخفاض الأسعار عند حدوثه في نطاق طبيعي مقبول . وتزداد صعوبة اتخاذ القرار الاستثماري السليم في ظل التقلبات السعرية المستمرة التي ترفع من درجة المخاطرة لكنها تؤمن في الوقت ذاته إمكانية تحقيق عائد استثماري مجزٍ في حال تم التحرك مع الأسعار في جولات الصعود بكفاءة، الأمر الذي يجعل نسبة مهمة من المستثمرين تقبل المخاطرة للحصول على العائد لكن جزءاً أساسياً منهم قد يتكبدون في المحصلة خسائر سريعة .
```

### NLI claims to label
1. تراجع مؤشر سوق دبي بنسبة 0.23% ليصل إلى 1659.39 نقطة مع تداولات بلغت 165.7 مليون درهم
2. ارتفع سهم الدار بنسبة 0.86% ليصل إلى 2.35 درهم بينما صعد سهم صروح بنسبة 0.61% ليبلغ 1.66 درهم
3. انخفض سهم إعمار بنسبة 0.49% ليصل إلى 3.55 درهم في جلسة التداول
4. أعلنت هيئة الأوراق المالية عن إجراءات جديدة لتعزيز السيولة في الأسواق المحلية خلال الفترة المقبلة

### English text to translate to Arabic
```
The UAE stock markets maintained their calm movements, with the UAE market index closing down 0.09% at 2687.41 points, as Dubai's index fell 0.23% and Abu Dhabi's dropped 0.17%, amid total trading volumes of 276.59 million dirhams. Key stocks such as Emaar, Arabtec, and Dubai Financial declined, while Aldar and Sorouh posted modest gains, as markets continued to operate under a climate of anticipation driven by concerns over local liquidity levels, bank provisioning requirements, and an ongoing financing crisis affecting listed companies and the broader economy. Analysts noted that a sustained market recovery depends on investors' confidence in reduced risk levels, the ability of markets to attract domestic and foreign liquidity, and improved economic conditions, though persistent price volatility continues to make sound investment decisions increasingly difficult.
```

---

## Article FINANCE_055

### Article body (Arabic)

```
دبي «الخليج»: شهد سوق دبي المالي تداولات بقيمة 631.470 مليون درهم بتنفيذ 6.281 صفقة توزعت على 440.220 مليون سهم. وأغلق المؤشر على 4.055.820 نقطة بانخفاض قدره 13.100 نقطة عن إغلاقه السابق. من أكثر الشركات ارتفاعاً من حيث التغير في أسعارها: هيتس تليكوم بإغلاق 0.360 درهم بنسبة تغير بلغت 3.710%، مصرف السلام - السودان بإغلاق 1.800 درهم بنسبة 2.860%، السلام القابضة بإغلاق 0.6 درهم بنسبة 2.760%، داماك العقارية دبي بإغلاق 3.150 درهم بنسبة 1.61%.وكانت أكثر الشركات انخفاضاً في أسعارها:دريك آند سكل إنترناشيونال بإغلاق 0.840 درهم بنسبة 4.55%، دار التكافل بإغلاق 0.590 درهم بنسبة 2.8%، بنك المشرق بإغلاق 115 درهماً بنسبة تغير بلغت 2.5%، الإمارات دبى الوطني بإغلاق 9.6 درهم بنسبة تغير بلغت 2.040%. وفيما يتعلق بالشركات الأكثر نشاطاً من حيث قيمة التداول فقد حققت أملاك للتمويل تداولات بقيمة 189.578.855.630 درهم، ثم جاءت بيت التمويل الخليجي تداولات بقيمة 123.836.383.130 درهم، ثم جاءت إعمار العقارية تداولات بقيمة 50.590.603.580 درهم. أما بالنسبة للشركات الأكثر نشاطاً حسب حجم التداول فقد تم تداول:169.319.995 سهماً من بيت التمويل الخليجي، 73.839.306 سهماً من أملاك، 44.876.662 سهماً من دريك آند سكل إنترناشيونال.
```

### NLI claims to label
1. أغلق مؤشر سوق دبي المالي على مستوى 4,055,820 نقطة متراجعاً بمقدار 13,100 نقطة مقارنة بالإغلاق السابق
2. تصدرت أملاك للتمويل قائمة الشركات الأكثر نشاطاً من حيث قيمة التداول في سوق دبي المالي
3. احتلت إعمار العقارية المرتبة الأولى من حيث حجم التداول بعدد أسهم بلغ 169 مليون سهم
4. شهد سوق دبي المالي في ذلك اليوم تداولات من قبل مستثمرين أجانب تجاوزت نسبتهم 40% من إجمالي التداولات

### English text to translate to Arabic
```
The Dubai Financial Market recorded trades worth 631.470 million dirhams through 6,281 transactions covering 440.220 million shares, with the index closing at 4,055.820 points, down 13.100 points from the previous close. Among the top gainers were Hits Telecom, which rose 3.71%, and Al Salam Bank – Sudan, which gained 2.86%, while the biggest decliners included Drake & Scull International, which fell 4.55%, and Dar Al Takaful, which dropped 2.8%. Amlak Finance led in trading value at approximately 189.58 million dirhams, while Gulf Finance House led in trading volume with 169.32 million shares traded.
```

---

## Article FINANCE_067

### Article body (Arabic)

```
شهد سوق دبي المالي تداولات بقيمة 240 .1 مليار درهم بتنفيذ 150 .9 صفقة توزعت على 150 .933 مليون سهم، وأغلق المؤشر على 330 .100 .3 نقطة بارتفاع وقدره 380 .44 نقطة عن إغلاقه السابق، وشهد التداول ارتفاع 23 شركة وهبوط 7 شركات وثبات أسعار شركة واحدة .ومن أكثر الشركات ارتفاعاً من حيث التغير في أسعارها جاءت اجيليتي بإغلاق 50 .9 درهم بنسبة تغير بلغت 56 .5% ديار للتطوير بإغلاق 77 .0 درهم بنسبة تغير بلغت 31 .5% دار التكافل بإغلاق 43 .1 درهم بنسبة تغير بلغت 15 .5% الاتحاد العقارية بإغلاق 09 .1 درهم بنسبة تغير بلغت 81 .4% مصرف السلام - السودان بإغلاق 45 .1 درهم بنسبة تغير بلغت 57 .3% .وكانت أكثر الشركات انخفاضاً في أسعارها الشركة الوطنية للتأمينات العامة بإغلاق 50 .5 درهم بنسبة تغير بلغت 84 .9% مصرف عجمان بإغلاق 32 .2 درهم بنسبة تغير بلغت 11 .2% اكتتاب القابضة بإغلاق 94 .0 درهم بنسبة تغير بلغت 260 .1% بنك المشرق بإغلاق 00 .86 درهماً بنسبة تغير بلغت 15 .1% شركة سوق دبي المالى بإغلاق 30 .2 درهم بنسبة تغير بلغت 86 .0% .وفيما يتعلق بالشركات الأكثر نشاطاً من حيث قيمة التداول فقد حققت اعمار العقارية تداولات بقيمة 7 .215 مليون درهم، ثم جاءت ديار للتطوير تداولات بقيمة 9 .147 مليون درهم، ثم جاءت الاتحاد العقارية تداولات بقيمة 7 .141 مليون درهم، ثم جاءت دريك آند سكل انترناشيونال تداولات بقيمة 7 .102 مليون درهم، ثم جاءت بنك دبي الإسلامي تداولات بقيمة 7 .97 مليون درهم .أما بالنسبة للشركات الأكثر نشاطاً حسب حجم التداول فقد تم تداول 3 .196 مليون سهم من ديار للتطوير 7 .132 مليون سهم من الاتحاد العقارية 3 .103 مليون سهم من بيت التمويل الخليجي 5 .78 مليون سهم من الخليج للملاحة القابضة 5 .73 مليون سهم من دريك آند سكل انترناشيونال .وبالنظر إلى أداء القطاعات في سوق دبي المالي فقد بلغ مؤشر قطاع البنوك 580 .787 .1 نقطة مؤشر قطاع السلع الاستهلاكية 000 .545 نقطة، الاستثمار والخدمات المالية 470 .910 .3 نقطة، الصناعة 280 .150 نقطة، التأمين 050 .334 .2 نقطة، العقارات والإنشاءات الهندسية 750 .289 .6 نقطة، الخدمات 100 .871 نقطة، الاتصالات 770 .093 .1 نقطة، النقل 610 .735 نقطة .
```

### NLI claims to label
1. حققت شركة إعمار العقارية أعلى قيمة تداول في سوق دبي المالي بما يقارب 215.7 مليون درهم
2. ارتفعت أسعار أسهم ثلاث وعشرين شركة في سوق دبي المالي بينما تراجعت أسعار سبع شركات
3. جاءت شركة ديار للتطوير في المرتبة الأولى من حيث حجم التداول بأكثر من 200 مليون سهم
4. شهد سوق أبوظبي للأوراق المالية في نفس الجلسة ارتفاعاً مماثلاً لسوق دبي المالي

### English text to translate to Arabic
```
The Dubai Financial Market (DFM) witnessed trading worth 1.240 billion dirhams across 9,150 transactions covering 933.150 million shares, with the index closing at 3,100.330 points, up 44.380 points from the previous close, as 23 companies rose, 7 declined, and 1 remained unchanged. Agility was the top gainer with a 5.56% increase closing at 9.50 dirhams, while the National General Insurance Company was the biggest loser, dropping 9.84% to close at 5.50 dirhams. Emaar Properties led in trading value at 215.7 million dirhams, while Deyaar Development led in trading volume with 196.3 million shares traded.
```

---

## Article FINANCE_007

### Article body (Arabic)

```
أعلن بنك دبي التجاري عن تعيين موراي سمز مديراً عاماً جديداً للأعمال المصرفية للأفراد . ومن خلال منصبه الجديد، سيقوم موراي بالإشراف على كافة أعمال وخدمات البنك في مجال الخدمات المصرفية للأفراد .عمل موراي على مدى ثلاثة عقود في مناصب قيادية مهمة في عدد من المصارف الدولية مثل مجموعة HSBC، وستاندرد تشارترد، وبنوك في الشرق الأوسط مثل بنك رأس الخيمة الوطني، وبنك عمان الدولي، والبنك السعودي الهولندي .وقال بيتر بالتوسن، الرئيس التنفيذي لبنك دبي التجاري، معلقاً على قرار التعيين: يسعدنا أن نرحب بموراي في عائلة بنك دبي التجاري ونتمنى له التوفيق في منصبه الجديد . إننا على ثقة بأن تعيين موراي سوف يمثل إضافة مهمة لفريق العمل المؤهل في البنك، حيث إن خبرته الطويلة في مجال الخدمات المصرفية للأفراد، إضافة إلى المؤهلات المتميزة التي يتمتع بها ستمكنه من المساهمة في تحقيق الأهداف الاستراتيحية للبنك .
```

### NLI claims to label
1. تم تعيين موراي سمز في منصب المدير العام للخدمات المصرفية للأفراد في بنك دبي التجاري
2. يمتلك موراي سمز خبرة تمتد لنحو ثلاثين عاماً في مواقع قيادية بمؤسسات مصرفية دولية وإقليمية
3. عمل موراي سمز سابقاً في البنك السعودي البريطاني ضمن تجربته المصرفية في منطقة الشرق الأوسط
4. حصل موراي سمز على درجة الماجستير في إدارة الأعمال من إحدى الجامعات البريطانية

### English text to translate to Arabic
```
Commercial Bank of Dubai announced the appointment of Murray Sims as the new General Manager of Retail Banking, where he will oversee all of the bank's retail banking operations and services. Sims brings over three decades of leadership experience at major international and regional banks, including HSBC, Standard Chartered, National Bank of Ras Al Khaimah, Oman International Bank, and Saudi Hollandi Bank. CEO Peter Baltussen welcomed the appointment, expressing confidence that Sims's extensive experience and qualifications will contribute to achieving the bank's strategic objectives.
```

---

## Article FINANCE_045

### Article body (Arabic)

```
أبوظبي: مهند داغر سيطر التباين مجدداً على أداء أسواق المال المحلية في آخر جلسات شهر يونيو/ حزيران، وسط أداء ضعيف نتيجة شح السيولة، بعد إجازة عيد الفطر، وتزامناً مع دخول بعض المتعاملين في موسم الإجازات الصيفية.تزايدت الضغوط أمس على أسهم استحوذت على نسبة مهمة من التداولات في جلسات سابقة، مثل جي إف إتش، والاتحاد العقارية، وإشراق، ودريك آند سيكل، فيما تمكن سهم أرابتك من الارتداد متصدراً الارتفاعات في سوق دبي.وبلغت السيولة الكلية للأسواق 336.24 مليون درهم، منها 217 مليون درهم في دبي، و119.2 مليون درهم في أبوظبي، والكميات المتداولة من الأسهم 241.6 مليون سهم، منها 144.8 مليون سهم في دبي، و96.8 مليون سهم في أبوظبي.وجرى تداول أسهم 58 شركة، وارتفعت أسعار أسهم 23 شركة، بينما تراجعت أسعار أسهم 29 شركة أخرى، وجاء ذلك من خلال 3930 صفقة.وعاود سوق دبي المالي للاتجاه الصعودي بنسبة 0.38% إلى مستوى 3392 نقطة، رابحاً 12.99 نقطة، مع عودة النشاط لأسهم شركات العقار والبنوك والنقل.وارتفع قطاع العقار بنسبة 0.67%، معززاً بمكاسب سهم أرابتك 4.36% وداماك 3.27% في وقت قلص سهم إعمار من مكاسب القطاع بتراجعه 0.13%.وارتفع قطاع البنوك 0.53% بعد ارتفاع سهم الإمارات دبي الوطني 2.26%، بينما أغلق سهم دبي الإسلامي مستقراً دون تغيير.وارتد قطاع النقل 1.26% بدعم من سهم العربية للطيران 0.99% وأرامكس 1.57%.في المقابل انخفض قطاع الاستثمار بنسبة 0.6% مع استمرار الضغط على سهم سوق دبي المالي 2.63% وشعاع كابيتال 2.7%.بدوره، هبط مؤشر سوق أبوظبي بنسبة 0.55% عند 4425.40 نقطة، خاسراً 24.28 نقطة، بالضغوط على قطاعات البنوك والعقار والطاقة والسلع.وانخفض قطاع البنوك بنسبة 1.13% بفعل تراجع سهم أبوظبي الأول 1.41%، كما تراجع قطاع العقار 0.73% مع تزاد الضغوط على سهم إشراق بنسبة 8.51% رغم ارتفاع سهم الدار 0.44%.وانخفض قطاع الطاقة بنسبة 2.86%، متأثراً بتراجع سهم دانة غاز 3.03% وطاقة 2%. في المقابل ارتفاع قطاع الاتصالات 0.58% مع ارتفاع سهم اتصالات بالنسبة ذاتها.وبشأن التداولات حافظ سهم جي إف إتش على الصدارة في دبي، بقيمة 44.7 مليون درهم، وهبط بنسبة 9.5% إلى 1.81 درهم، وجاء ثانياً سهم إعمار بتداولات بلغت 41.3 مليون درهم، وهبط أيضاً 0.13% إلى 7.78 درهم، ثم سهم أرابتك الذي شهد تداولات وصلت إلى 32.6 مليون درهم، وصعد بنسبة 4.36% إلى 2.87 درهم.وفي سوق العاصمة، وتصدر سهم أبوظبي الأول التداولات ب36.5 مليون درهم، وتراجع بنسبة 1.41% مغلقاً عند 10.5 درهم، وجاء ثانياً سهم إشراق بتداولات بلغت18.72 مليون درهم، وهبط 8.51% إلى 0.86 درهم، ثم سهم دانة غاز الذي شهد تداولات بقيمة 16.34 مليون درهم، وانخفض 3.03% ليغلق عند 0.64 درهم.وفيما يتعلق بالأسهم الأكثر ارتفاعاً في دبي، جاء في المقدمة سهم أرابتك وصعد 4.36% إلى 2.87 درهم، فيما كان أكبر الخاسرين سهم جي إف إتش، وتراجع 9.5% وأغلق عند 1.81 درهم.وسجل سهم الأول سهم سيراميك رأس الخيمة، الارتفاع الأكبر في أبوظبي، وصعد بنسبة 6.47% إلى 2.47 درهم، فيما سجل سهم إشراق التراجع الأكبر بنسبة 8.51% وأغلق عند 0.86 درهم.وبشأن التداولات حسب الجنسيات، اتجه المستثمرون الأجانب والعرب نحو الشراء، بصافي استثمار بلغ 39.4 مليون درهم محصلة شراء، منها 30 مليون درهم محصلة شراء الأجانب، و9.35 مليون درهم محصلة شراء العرب، في المقابل اتجه المستثمرون الخليجيون والمواطنون نحو التسييل، بصافي استثمار بلغ 39.4 مليون درهم محصلة بيع، منها 9.3 مليون درهم محصلة بيع الخليجيين، و30 مليون درهم محصلة بيع المواطنين.وركز المستثمرون الأجانب غير العرب مشترياتهم على أسهم شركات أرابتك ودريك آند سيكل والدار العقارية وجي إف إتش المالية، بينما تركزت مبيعاتهم على أسهم شركات دانة غاز وبنك الاستثمار والاتحاد العقارية ومنازل العقارية.بدورها اتجهت المحافظ الاستثمارية نحو التسييل، بصافي استثمار بلغ 20 مليون درهم محصلة بيع، منها 10.7 مليون درهم محصلة بيع في أبوظبي، و9.3 مليون درهم محصلة بيع في دبي. في المقابل اتجه المستثمرون الأفراد نحو التسييل، بصافي استثمار بلغ 20 مليون درهم محصلة بيع، منها 10.7 مليون درهم محصلة بيع في أبوظبي، و9.3 مليون درهم محصلة بيع في دبي. الإفصاحات تقضي على الشائعات قالت هيئة الأوراق المالية والسلع، إن الإفصاح الفوري من جانب الشركات (عن القرارات الجوهرية والبيانات المالية الدورية والحسابات الختامية) يقطع الطريق على الشائعات، ويوفر الشفافية للأسواق المالية التي تعد مسألة الثقة بها وبمصداقيتها على درجة عالية من الحساسية والدقة.
```

### NLI claims to label
1. ارتفع مؤشر سوق دبي المالي بنسبة 0.38% ليصل إلى 3392 نقطة محققاً مكاسب بلغت نحو 13 نقطة
2. تصدر سهم أبوظبي الأول قائمة التداولات في سوق العاصمة بقيمة تجاوزت 36 مليون درهم وأغلق منخفضاً عند 10.5 درهم
3. تراجع سهم جي إف إتش بنسبة 8.5% ليغلق عند 1.81 درهم وكان الأكثر خسارة في سوق دبي
4. أعلنت هيئة الأوراق المالية والسلع عن فرض غرامات مالية على الشركات التي تتأخر في الإفصاح عن بياناتها المالية

### English text to translate to Arabic
```
UAE financial markets experienced mixed performance in the last trading session of June, with low liquidity due to the post-Eid al-Fitr holiday period and the onset of summer vacations, as total market liquidity reached 336.24 million dirhams across Dubai and Abu Dhabi exchanges. Dubai's financial market index rose 0.38% to 3,392 points, driven by gains in real estate, banking, and transport sectors, with Arabtec leading the gains at 4.36%, while Abu Dhabi's market index fell 0.55% to 4,425.40 points under pressure from banking, real estate, and energy sectors. Foreign and Arab investors were net buyers with 39.4 million dirhams in net purchases, while Gulf and UAE national investors were net sellers by the same amount, and the Securities and Commodities Authority emphasized that timely corporate disclosures are essential to combating rumors and ensuring market transparency.
```

---

## Article FINANCE_001

### Article body (Arabic)

```
دبي "الخليج":شهد سوق دبي المالي تداولات بقيمة 180 .730 مليون درهم بتنفيذ 785 .6 صفقة توزعت على 690 .426 مليون سهم . وأغلق المؤشر على 390 .941 .3 نقطة بارتفاع وقدره 030 .48 نقطة عن إغلاقه السابق .من أكثر الشركات ارتفاعاً من حيث التغير في أسعارها: شركة أمانات القابضة بإغلاق 890 .0 درهم بنسبة تغير بلغت 330 .5%، مجموعة إعمار مولز بإغلاق 990 .2 درهم بنسبة تغير بلغت 550 .4%، مصرف السلام - البحرين بإغلاق 370 .1 درهم بنسبة تغير بلغت 010 .3%، الإمارات دبي الوطني بإغلاق 200 .9 درهم بنسبة تغير بلغت 220 .2% . وكانت أكثر الشركات انخفاضاً في أسعارها داماك العقارية دبي بإغلاق 790 .2 درهم بنسبة تغير بلغت 710 .9%، الشركة الوطنية للتأمينات العامة بإغلاق 310 .3 دراهم بنسبة تغير بلغت 060 .8%، الشركة الخليجية للاستثمارات العامة بإغلاق 860 .0 درهم بنسبة تغير بلغت 040 .3% .وفي ما يتعلق بالشركات الأكثر نشاطاً من حيث قيمة التداول فقد حققت شركة أرابتك القابضة تداولات بقيمة 840 .934 .606 .209 درهماً، إعمار العقارية تداولات بقيمة 180 .925 .772 .114 درهماً، مجموعة إعمار مولز تداولات بقيمة 360 .182 .119 .99 درهماً .أما بالنسبة للشركات الأكثر نشاطاً حسب حجم التداول فقد تم تداول 409 .827 .119 أسهم من بيت التمويل الخليجي، 603 .031 .65 سهماً من شركة أرابتك القابضة . وبلغ مؤشر قطاع البنوك 720 .686 .2 نقطة بتداول 479 .567 .143 سهم بقيمة 170 .638 .943 .104 درهماً، ومؤشر قطاع العقارات والإنشاءات الهندسية 710 .497 .8 نقطة بتداول 394 .740 .173 سهماً بقيمة 080 .005 .545 .493 درهماً .
```

### NLI claims to label
1. أغلق مؤشر سوق دبي المالي على ارتفاع بلغ نحو 48 نقطة مقارنة بإغلاقه السابق
2. كانت شركة داماك العقارية دبي من أكثر الشركات تراجعاً في أسعارها خلال جلسة التداول
3. حققت إعمار العقارية أعلى قيمة تداول بين الشركات المدرجة في سوق دبي المالي خلال تلك الجلسة
4. شهد سوق دبي المالي دخول مستثمرين أجانب بنسبة تجاوزت ثلاثين بالمئة من إجمالي التداولات

### English text to translate to Arabic
```
Dubai Financial Market witnessed trading worth 730.180 million dirhams through 6,785 transactions covering 426.690 million shares, with the index closing at 3,941.390 points, up 48.030 points from the previous close. Among the top gainers were Amanat Holdings, Emaar Malls Group, Al Salam Bank-Bahrain, and Emirates NBD, while the biggest decliners included DAMAC Properties Dubai, National General Insurance Company, and Gulf General Investments Company. The most active stocks by trading value were Arabtec Holding, Emaar Properties, and Emaar Malls Group, while Gulf Finance House and Arabtec Holding led in trading volume.
```

---

## Article FINANCE_097

### Article body (Arabic)

```
أبوظبي عدنان نجم:أقرت الجمعية العمومية لشركة طيران أبوظبي توزيع أرباح بنسبة 12% نقداً على المساهمين عن سنة 2014 . وأكد نادر الحمادي رئيس مجلس إدارة شركة طيران أبوظبي سعي الشركة الدائم لتحقيق مستوى عال من الربحية من خلال تطبيق أقصى درجات الاحترافية في العمل مع مراعاة الاحتفاظ بالمستوى العالمي المتميز الذي حققته الشركة في ما يتعلق بمعدلات الأمن والسلامة العالية .وأضاف الحمادي في كلمته التي ألقاها في اجتماع الجمعية العمومية للشركة الذي عقد أمس في فندق هيلتون الكورنيش أبوظبي: "لقد شهدت مجموعة طيران أبوظبي العديد من التطورات حيث تتكون مجموعة طيران أبوظبي من شركة طيران أبوظبي "الشركة الأم" وشركة رويال غيت وشركة ماكسيمس للطيران، حيث بلغت إيرادات المجموعة ما يعادل 6 .1 مليار درهم، كما استطاعة المجموعة تحقيق صافي أرباح بلغ 7 .244 مليون درهم، وأثمر السعي الدؤوب إلى اكتساب المجموعة السمعة الفنية العالمية، إذ يدعم هذه السمعة أسطول من الطائرات المختلفة، حيث يتكون أسطول طائرات شركة طيران أبوظبي "الشركة الأم" من 58 طائرة عمودية و3 طائرات من ذات الجناح الثابت، بينما يتكون اسطول طائرات شركة رويال غيت حالياً من 11 طائرة تجارية، أما شركة ماكسيمس فيتكون أسطول طائراتها من ثلاث طائرات للشحن الجوي .وأفاد الحمادي بأن شركات المجموعة تركز حالياً على البحث في فرص العمل عبر التحالف مع شركاء لتبادل الخبرات والاستفادة المشتركة وكذلك البحث عن المناطق التي تحتاج لنوعية أعمال الشركة .وذكر أن شركة طيران أبوظبي أصبحت أكبر مشغل تجاري للطائرات العمودية في الشرق الأوسط وتعمل حالياً على توسيع حظائر الطائرات لتزيد الطاقة الاستيعابية لها .
```

### NLI claims to label
1. بلغ صافي أرباح مجموعة طيران أبوظبي نحو 244.7 مليون درهم
2. يضم أسطول شركة رويال غيت حالياً إحدى عشرة طائرة تجارية
3. قررت الجمعية العمومية لشركة طيران أبوظبي توزيع أرباح نقدية بنسبة عشرة بالمئة على المساهمين عن عام 2014
4. تخطط شركة طيران أبوظبي لإدراج أسهمها في سوق أبوظبي للأوراق المالية خلال العام المقبل

### English text to translate to Arabic
```
The General Assembly of Abu Dhabi Aviation approved a 12% cash dividend distribution to shareholders for the year 2014. Chairman Nader Al Hammadi stated that the Abu Dhabi Aviation Group, comprising the parent company, Royal Gate, and Maximus Aviation, achieved revenues of approximately 1.6 billion dirhams and net profits of 244.7 million dirhams, with a combined fleet of helicopters, fixed-wing aircraft, commercial planes, and cargo aircraft. Al Hammadi noted that Abu Dhabi Aviation has become the largest commercial helicopter operator in the Middle East and is currently expanding its hangars to increase capacity.
```

---

## Article FINANCE_018

### Article body (Arabic)

```
أوصى مجلس ادارة شركة البحيرة الوطنية للتأمين بتوزيع أرباح نقدية على المساهمين بنسبة 30% وذلك بعد مناقشة أرقام الميزانية لعام 2009 في جلسته المنعقدة بتاريخ 22/2/2010 .وأشار الشيخ فيصل بن خالد بن سلطان القاسمي رئيس مجلس إدارة الشركة إلى أن السياسة الاكتتابية المتوازنة وما افرزته من نتائج ايجابية مكّنت الشركة من تحقيق هذه النتائج الجيدة على الرغم من الظروف الاقتصادية الحالية التي ألقت بظلالها على كافة الدول حول العالم .كما أعلن القاسمي عن انتهاء العمل بالمبنى الواقع في منطقة الخان بتكلفة اجمالية تزيد على 100 مليون درهم وتم تأجيره بالكامل في حين تسير الأعمال الانشائية في برج النهدة بتكلفة تصل الى 450 مليون درهم وذلك وفقاً للجدول الزمني المحدد، حيث من المتوقع أن يصبح جاهزاً للتأجير في الربع الأخير من عام 2010 .وأكد نادر توفيق القدومي المدير العام أن الشركة مستمرة في القيام بدورها في سوق التأمين في الدولة وستبقى محافظة على أدائها المتميز في خدمة المجتمع الإماراتي بكافة أطيافه .
```

### NLI claims to label
1. أوصى مجلس إدارة شركة البحيرة الوطنية للتأمين بتوزيع أرباح نقدية على المساهمين بنسبة ثلاثين بالمئة
2. تبلغ التكلفة الإجمالية للأعمال الإنشائية في برج النهدة نحو أربعمئة وخمسين مليون درهم
3. المبنى الكائن في منطقة الخان تم تشييده بتكلفة إجمالية تتجاوز مئتي مليون درهم
4. حققت شركة البحيرة الوطنية للتأمين نمواً في عدد العملاء بنسبة عشرين بالمئة خلال عام 2009

### English text to translate to Arabic
```
The board of directors of Al Buhaira National Insurance Company recommended distributing 30% cash dividends to shareholders after reviewing the 2009 budget figures at its meeting held on 22/2/2010. Chairman Sheikh Faisal bin Khalid bin Sultan Al Qasimi attributed the positive results to the company's balanced underwriting policy, despite the prevailing global economic conditions, and announced the completion of a building in the Al Khan area costing over 100 million dirhams, which has been fully leased, while construction of Al Nahda Tower, costing 450 million dirhams, is on schedule for completion by the last quarter of 2010. General Manager Nader Tawfiq Al Qudoumi affirmed that the company will continue its role in the UAE insurance market and maintain its distinguished performance in serving the Emirati community.
```

---

## Article FINANCE_031

### Article body (Arabic)

```
تراجع المؤشر العام لسوق أبوظبي للأوراق المالية يوم أمس بنسبة 6 .0% ليغلق عن 2344 نقطة، وذلك محصلة تراجع ثمانية مؤشرات من مؤشرات قطاعاته الرئيسية بنسبة تتراواح بين 06 .0% و1 .4% .وبلغ حجم تداولات السوق في جلسة بداية الأسبوع نحو 53 مليون درهم، توزعت على 952 صفقة، شملت نحو 62 مليون سهم من أسهم 23 شركة من الشركات المدرجة .وشملت قائمة الشركات الرابحة شركة صناعات أسمنت أم القيوين بعد صعود سعر سهمها بنسبة 8 .5%، شركة الهلال الأخضر للتأمين بنسبة ارتفاع 1 .3%، شركة جلفار للأدوية بنسبة 3 .1 %، وأخيراً بنك الاتحاد الوطني بعد ارتفاع سعر سهمه بنسبة 3 .0% .أما قائمة الشركات الخاسرة، فقد جاء في مقدمتها شركة دانة غاز بعد تراجع سعر سهمها بنسبة 5 .7%، شركة أسمنت رأس الخيمة بنسبة تراجع 2 .7%، شركة ميثاق للتأمين بنسبة تراجع 7 .6%، مصرف الشارقة الإسلامي بنسبة 8 .5%، البنك التجاري الدولي بنسبة 8 .5% . وفي ما يتعلق بأكثر الشركات تداولاً من حيث القيمة، فقد استحوذت شركة الدار العقارية على نحو 15 مليون درهم من إجمالي تداولات السوق يوم أمس، تلاها شركة اتصالات بقيمة 2 .12 مليون درهم، دانة غاز 2 .8 مليون درهم، شركة صروح العقارية بقيمة 1 .4 مليون درهم، وبنك الاتحاد الوطني بقيمة 8 .3 مليون .
```

### NLI claims to label
1. أغلق المؤشر العام لسوق أبوظبي للأوراق المالية عند مستوى 2344 نقطة بعد انخفاض بنسبة 0.6%
2. تصدرت شركة الدار العقارية قائمة الشركات الأكثر تداولاً من حيث القيمة بنحو 15 مليون درهم
3. تراجع سعر سهم شركة أسمنت رأس الخيمة بنسبة 5.7% خلال جلسة التداول
4. شهد سوق أبوظبي للأوراق المالية ارتفاعاً ملحوظاً في أحجام التداول مقارنة بالأسبوع السابق

### English text to translate to Arabic
```
The Abu Dhabi Securities Exchange general index declined by 0.6% yesterday to close at 2,344 points, as eight of its main sector indices fell by between 0.06% and 4.1%, with total trading volume reaching approximately 53 million dirhams across 952 transactions covering shares of 23 listed companies. Among the gaining companies, Umm Al Quwain Cement Industries led with a 5.8% rise, while the biggest losers included Dana Gas, which dropped 7.5%, followed by Ras Al Khaimah Cement at 7.2% and Mithaq Insurance at 6.7%. Aldar Properties topped the most-traded companies by value, accounting for approximately 15 million dirhams of total market trading, followed by Etisalat at 12.2 million dirhams and Dana Gas at 8.2 million dirhams.
```

---
