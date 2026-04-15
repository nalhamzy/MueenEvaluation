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


## Article POLITICS_086

### Article body (Arabic)

```
* قالت القوات المسلحة التركية في بيان إن جنودها قتلوا أربعة من متمردي ميليشيا كردية في اشتباك جنوب شرق البلاد. واشار البيان الى أن تبادل إطلاق النار مع مقاتلي حزب العمال الكردستاني وقع بمنطقة ليجة في إقليم ديار بكر أثناء عملية عسكرية هناك. ومن بين القتلى الاربعة امرأتان. وتمت في أعقاب الاشتباك مصادرة بنادق من طراز كلاشنيكوف وذخيرة وقنابل يدوية ووثائق تابعة للحزب المحظور.(رويترز)* احرقت قوات الامن السريلانكية جثة زعيم المتمردين التاميل فيلوبيلاي براباكاران ونثروا رماده في المحيط الهندي. واعلن قائد الجيش سرات فونسيكا في مقابلة تنشر اليوم الاحد انه تم صباح الثلاثاء التعرف إلى جثة زعيم نمور تحرير ايلام التاميل ...لقد احرقنا الجثة في المنطقة نفسها ونثرنا رماده في المحيط. واوضح حتى قبل مقتل براباكاران كنت اعلم اننا انتصرنا لكنني سررت جدا لدى تبلغي نبأ مقتله. وبحسب قيادة الجيش قتل جميع قادة نمور تحرير ايلام التاميل. وبث التلفزيون السريلانكي شريط فيديو تظهر فيه جثة قال انها تعود لبراباكاران. (د.ب.أ)* لقي شخصان على الأقل حتفهما وأصيب 13 آخرون عندما انفجرت قنبلة بكنيسة في العاصمة النيبالية كاتماندو صباح امس السبت. وذكرت الشرطة أن القنبلة انفجرت خلال تجمع في كنيسة الصعود في منطقة دويبيجات إحدى ضواحي بلدة لايليتبور بالقرب من العاصمة. وأفادت الشرطة أن الضحيتين يحملان الجنسية الهندية وأن أحدهما كانت فتاة (14 عاما). وتم نقل الضحيتين بسرعة إلى أحد المستشفيات في حالة حرجة، غير أنهما فارقا الحياة أثناء تلقي العلاج.(د.ب.ا)* تحطمت طائرة ركاب خاصة في البرازيل أثناء هبوطها مساء الجمعة في مطار مدينة ترانكوزو جنوب ولاية باهيا.وذكرت سلطات الطيران البرازيلية في ساعة مبكرة من صباح السبت أن جميع ركاب الطائرة ذات المحركين وعددهم 11 شخصا قد لقوا حتفهم خلال الحادث. وأشارت إلى ارتطام الطائرة من طراز (كينج أير 350) بالأرض بعنف وانفجارها في أعقاب سقوطها وأكدت أن أربعاً من الضحايا من الأطفال. (د.ب.أ)
```

### NLI claims to label
1. لقي جميع ركاب الطائرة الخاصة البالغ عددهم أحد عشر شخصاً مصرعهم عند تحطمها في مطار ترانكوزو بولاية باهيا البرازيلية
2. أعلن قائد الجيش السريلانكي أن جثة براباكاران أُحرقت وتم نثر رماده في المحيط الهندي
3. أسفر انفجار القنبلة في كنيسة العاصمة النيبالية عن مقتل ثلاثة أشخاص وإصابة ثلاثة عشر آخرين
4. تبنّت جماعة ماوية نيبالية مسؤوليتها عن تفجير الكنيسة في ضواحي كاتماندو

### English text to translate to Arabic
```
Turkish armed forces killed four Kurdish militants, including two women, during a clash in the Lice district of Diyarbakir province in southeastern Turkey, seizing Kalashnikov rifles, ammunition, grenades, and documents belonging to the banned PKK. Sri Lankan security forces cremated the body of Tamil Tiger leader Velupillai Prabhakaran and scattered his ashes in the Indian Ocean, with the army commander confirming that all LTTE leaders had been killed. In other events, a bomb explosion at a church in Kathmandu, Nepal killed at least two Indian nationals and injured 13 others, while a private passenger plane crashed in Trancoso, southern Bahia state in Brazil, killing all 11 people on board, including four children.
```

---

## Article POLITICS_013

### Article body (Arabic)

```
أكدت الأمم المتحدة التزامها التام بدعم جهود السودان المتصلة بتنفيذ بنود اتفاقية السلام وتنفيذ استحقاق المشورة الشعبية لمواطني ولاية جنوب كردفان، وشددت الحركة الشعبية على عدم ربط الاستفتاء بترسيم الحدود، مؤكدة أن الخلافات حول الحدود لن تعيد الحرب .وأوضح الممثل الخاص للأمم المتحدة هايلي منقريوس خلال زيارة هي الأولى للولاية تهدف التعرف عن قرب إلى الأوضاع بالمنطقة، ان المنظمة الأممية تعمل بكل جدية للحفاظ على السودان موحداً تسوده الديمقراطية، مبيناً أن جنوب كردفان ومنطقة آبيي تعدان بمثابة مفاتيح للعلاقة بين الشمال والجنوب كيفما كانت نتيجة الاستفتاء للوحدة أو الانفصال .وقال الأمين العام للحركة الشعبية باقان أموم إن الخلاف حول الحدود لن يعيد الحرب، لافتاً إلى أن الحركة مع ترسيمها من دون ربطها مع الاستفتاء . وأضاف أن هناك خيارات منها تأجيل حسمها إلى ما بعد الاستفتاء أو اللجوء إلى التحكيم المحلي أو الدولي ليفصل حول أراضي النزاع وفقاً للخرائط الموجودة والقوانين المعمول بها . وقلل باقان من مخاوف قبائل التمازج حال انفصال الجنوب، مؤكداً على توفير الأمن لهم إذا اختار شعب الجنوب الانفصال أو الوحدة .وسلم نواب بالبرلمان ينتمون إلى الحركة الشعبية وتجمعات العمد والسلاطين والسياسيين بمقاطعة الرنك، مذكرة احتجاج للفريق سلفا كير ميارديت رئيس حكومة الجنوب، حول تقرير لجنة الحدود القومية لجهة رفعها للمؤسسة الرئاسية للنظر فيها . وقال دينق شول عضو البرلمان عن الحركة الشعبية، إن الاعتراض على الترسيم، إضافة إلى مستندات ووثائق خاصة بالحدود سلّمت لسلفاكير . وأشار إلى أن الحدود هي حدود بين القبائل ورجال الإدارة الأهلية أكثر من الدولة هناك، وأكد عدم وجود خريطة بتاريخ 1/1/،1956 مشيراً إلى أن الخلافات حول الحدود تتجاوز ال (40%) . وقال دينق إن الاتفاق في ولاية أعالي النيل تَمّ في نقطة واحدة فقط، وهي الحدود الجنوبية الشرقية بين مقاطعة الرنك ومحافظة الباو بالنيل الأزرق عند جبل تكوتك . وأشار إلى وجود خلاف في الحدود الشرقية بين مقاطعة الرنك بولاية أعالي النيل ومحافظة التضامن بالنيل الأزرق عند جبل بوط، منوهاً إلى وجود خلافات في الحدود الشمالية الشرقية بين مقاطعة الرنك وولاية سنار وخلافات في الحدود الشمالية مع محافظة الجبلين بالنيل الأبيض، وكذلك الحدود التي تقع غرب النيل الأبيض بين محافظة مانجو بولاية أعالي النيل ومحافظة السلام بالنيل الأبيض . من جانب آخر، أكد اجتماع ضم قيادات من المؤتمر الوطني والأحزاب الجنوبية ضرورة توحيد الجهود والتنسيق المشترك لضمان إجراء الاستفتاء على حق تقرير المصير بالجنوب حراً ونزيهاً، وأكد ضرورة التحرك لتوعية المواطن الجنوبي بكيفية الإدلاء بصوته .
```

### NLI claims to label
1. وصف هايلي منقريوس جنوب كردفان ومنطقة آبيي بأنهما مفاتيح أساسية للعلاقة بين شمال السودان وجنوبه بغض النظر عن نتيجة الاستفتاء
2. أشار باقان أموم إلى إمكانية تأجيل البت في مسألة الحدود إلى ما بعد الاستفتاء أو اللجوء إلى التحكيم سواء المحلي أو الدولي
3. ذكر دينق شول أن الاتفاق في ولاية أعالي النيل تم في نقطتين هما الحدود الجنوبية الشرقية والحدود الشمالية لمقاطعة الرنك
4. طالبت الأمم المتحدة بتأجيل موعد الاستفتاء على تقرير المصير لحين الانتهاء من ترسيم الحدود بشكل كامل

### English text to translate to Arabic
```
The United Nations reaffirmed its full commitment to supporting Sudan's peace agreement implementation and the popular consultation process in South Kordofan, with UN Special Representative Haile Menkerios visiting the state and emphasizing that South Kordofan and Abyei are key to North-South relations regardless of the referendum outcome. The Sudan People's Liberation Movement (SPLM) Secretary-General Pagan Amum insisted that border disputes should not be linked to the referendum and would not lead to a return to war, suggesting options such as postponing border resolution until after the referendum or resorting to local or international arbitration. Meanwhile, SPLM parliamentarians submitted a protest memorandum to Southern Government President Salva Kiir regarding the national border committee's report, noting that over 40% of the borders in Upper Nile state remain disputed, and a joint meeting of the National Congress Party and southern parties stressed the need to coordinate efforts to ensure a free and fair self-determination referendum in the South.
```

---

## Article POLITICS_075

### Article body (Arabic)

```
صنعاء - «الخليج»: حذر المجلس الأعلى للحراك الجنوبي ممن أسماه الطابور الخامس المشكل من خلايا جماعة الحوثي وعلي عبد الله صالح والقوى المتربصة بقضية الجنوب، وقال إن هذا الطابور بدأ يرتب أوراقه بعد الهزيمة العسكرية وتحرير عدن والضالع ولحج وأبين وشبوة، وبدأ بأعمال التخريب والانتقام واستهداف رجال المقاومة.ودعا المجلس، وهو اكبر مكونات الحراك الجنوبي، إلى اليقظة والحذر و«التعامل بحزم وحسم تجاه هذه الخلايا الشيطانية العدوانية». كما دعا على وجه السرعة إلى «تشكيل لجنة تحقيق مشتركة بين الجهات الجنوبية المعنية في السلطة والحراك الجنوبي لكشف ملابسات وأسباب حادثتي الحرائق التي طالت غرف جرحى المقاومة الوطنية الجنوبية الذين يتلقون العلاج في مشفى 22 مايو ومشفى النقيب بعدن، والتي أدت إلى حالة وفيات عصر الأحد الماضي». ودان المجلس الأعلى، في بلاغ له حصلت «الخليج» على نسخة منه، ما وصفها «المحاولات التخريبية بقصد تعطيل وإيقاف تشغيل مطار عدن الدولي».
```

### NLI claims to label
1. وصف المجلس الأعلى للحراك الجنوبي نفسه بأنه أكبر مكونات الحراك الجنوبي
2. طالب المجلس الأعلى للحراك الجنوبي بتشكيل لجنة تحقيق مشتركة للنظر في حوادث الحرائق التي وقعت في مستشفيات بعدن
3. أسفرت حوادث الحرائق في المستشفيات عن حالات وفاة صباح يوم الأحد الماضي
4. تبنت جماعة الحوثي مسؤوليتها عن حوادث الحرائق في مستشفيات عدن

### English text to translate to Arabic
```
The Supreme Council of the Southern Movement in Sana'a warned against what it called a 'fifth column' composed of Houthi and Ali Abdullah Saleh cells, stating that these groups have begun sabotage and revenge operations after the military liberation of Aden, Al-Dhale, Lahj, Abyan, and Shabwa. The Council urgently called for the formation of a joint investigation committee between southern authorities and the Southern Movement to uncover the circumstances behind fires that broke out in rooms housing wounded resistance fighters at the 22 May Hospital and Al-Naqeeb Hospital in Aden, which resulted in deaths the previous Sunday. The Council also condemned what it described as sabotage attempts aimed at disrupting and halting operations at Aden International Airport.
```

---

## Article POLITICS_083

### Article body (Arabic)

```
غزة «الخليج»، وكالات: رفض الأسير الصحفي محمد القيق المضرب عن الطعام منذ 75 يوماً، عرضاً «إسرائيلياً» بالإفراج عنه في 1 مايو/‏أيار المقبل، وأصر على الافراج الفوري عنه وإلغاء اعتقاله بشكل نهائي. وقالت «هيئة شؤون الأسرى والمحررين» التابعة لمنظمة التحرير إن العرض قدمته النيابة العسكرية «الإسرائيلية» للنائب العربي في «الكنيست «الإسرائيلي» أسامة السعدي ولمحامي الهيئة أشرف أبو أسنينة خلال الاتصالات المكثفة التي جرت ليل السبت/‏الأحد، تزامناً مع التدهور الخطير على وضع القيق الصحي، حيث هناك خشية من تعرضه لجلطة أو موت فجائي في أي لحظة.وذكرت الهيئة أن موقف القيق واضح برفضه التام لهذا العرض، ولأي عروض أخرى لا تنهي اعتقاله الإداري. وحملت الاحتلال وجهاز مخابراتها المسؤولية الكاملة عن أي مكروه أو ضرر يؤثر في صحته. وأعلنت الهيئة أن 700 معتقل إداري يقبعون في معتقلات الاحتلال، في ظل تصاعد إصدار أوامر الاعتقال الإداري وتجديدها بحق الأسرى، من بينهم أسيرتان وتسعة قاصرين يرزحون في الاعتقال الإداري. وحمل أمين سر اللجنة التنفيذية لمنظمة التحرير الفلسطينية صائب عريقات سلطات الاحتلال المسؤولية الكاملة عن حياة الأسير محمد القيق.وقال عريقات في بيان، إنه طالب مسؤولين دوليين التدخل لإنقاذ حياة الأسير القيق الذي يضرب عن الطعام احتجاجاً على اعتقاله الإداري.
```

### NLI claims to label
1. رفض الأسير محمد القيق عرضاً بالإفراج عنه وطالب بإنهاء اعتقاله الإداري فوراً وبشكل كامل
2. أفادت هيئة شؤون الأسرى والمحررين بأن نحو سبعمائة معتقل إداري محتجزون في سجون الاحتلال
3. قُدّم العرض الإسرائيلي بالإفراج عن القيق في الأول من يونيو المقبل
4. انضم عدد من الأسرى الآخرين إلى إضراب محمد القيق عن الطعام تضامناً معه

### English text to translate to Arabic
```
Palestinian journalist prisoner Mohammad al-Qiq, who has been on hunger strike for 75 days, rejected an Israeli offer to release him on May 1, insisting on his immediate and unconditional release and the full cancellation of his administrative detention. The Commission of Detainees and Ex-Detainees, affiliated with the Palestine Liberation Organization, stated that the offer was made by the Israeli military prosecution amid intensive contacts, while al-Qiq's health condition deteriorated dangerously with fears of a stroke or sudden death at any moment. PLO Executive Committee Secretary-General Saeb Erekat held the Israeli occupation authorities fully responsible for al-Qiq's life and called on international officials to intervene to save him.
```

---

## Article POLITICS_034

### Article body (Arabic)

```
حذر رئيس الوزراء التونسي المؤقت الباجي قائد السبسي، أمس، قبيل إحياء تونس بعد غدٍ الأحد، ذكرى استقلالها سنة 1956 من مخاطر الانزلاق عن ثوابت الدولة التونسية ومن محاولات الركوب على الثورة التي أطاحت نظام زين العابدين بن علي .وقال في كلمة افتتح بها، أمس، ملتقى دولياً حول التحول الديمقراطي في تونس إن الثورة لا تعني ضرورة الديمقراطية . فهناك مسالك عديدة (ممكنة) فإما أن نصل إلى الديمقراطية وهذا ما نريد ويجب أن نعمل من اجله وإما أن ننزلق . ورأى أن دعاة الانزلاق موجودون ويعملون ولا بد أن ننتبه إلى هذا الأمر . وأكد أن ما حصل في تونس ثورة تونسية خالصة لها خصوصياتها وكانت نتيجة تداعيات داخلية ترتبط بأخلاقية السلطة وتجاوزات السلطات في إشارة إلى الفساد الذي استشرى في عهد ابن علي . وأضاف أن من خصوصيات هذه الثورة أنها ليست مؤطرة وليس لها زعامات . (أ .ف .ب)
```

### NLI claims to label
1. ألقى الباجي قائد السبسي كلمة في افتتاح ملتقى دولي تناول موضوع التحول الديمقراطي في تونس
2. وصف رئيس الوزراء التونسي المؤقت الثورة التونسية بأنها لم تكن مؤطرة ولم يكن لها قيادات
3. أشار قائد السبسي إلى أن تونس تحتفل بذكرى استقلالها الذي تحقق عام 1958
4. طالب قائد السبسي في كلمته بتشكيل لجنة وطنية للتحقيق في قضايا الفساد خلال عهد بن علي

### English text to translate to Arabic
```
Interim Tunisian Prime Minister Beji Caid Essebsi warned against deviating from the foundational principles of the Tunisian state and against attempts to exploit the revolution that toppled Zine El Abidine Ben Ali's regime, ahead of Tunisia's celebration of its 1956 independence anniversary. Speaking at an international forum on democratic transition in Tunisia, Essebsi stated that revolution does not necessarily lead to democracy, noting that advocates of derailment exist and are actively working. He emphasized that the Tunisian revolution was purely homegrown, driven by internal factors related to the ethics and abuses of power, and characterized by having no organized framework or specific leadership.
```

---

## Article POLITICS_097

### Article body (Arabic)

```
أعلنت المحكمة الجزائية المتخصصة في جدة غرب السعودية أمس أنها استأنفت محاكمة أول امرأة سعودية متورطة في نشاطات إرهابية، وهي هيلة القصير (45 عاماً) التي لعبت دوراً بارزاً في جمع الأموال لمصلحة تنظيم القاعدة، والترويج لأفكاره وإيواء بعض المطلوبين وحيازة الأسلحة .وذكرت وكالة الأنباء السعودية أمس أن المحكمة الجزائية المتخصصة استأنفت في جلستها الثانية نظر القضية المرفوعة على امرأة، وهي المرة الأولى، بتهمة الانضمام لتنظيم القاعدة وإيواء بعض المطلوبين أمنياً وتجنيد عناصر لتنظيم القاعدة وتمويل الأعمال الإرهابية وحيازة أسلحة لاستخدامها في الجرائم الإرهابية، بالإضافة إلى شروعها في الخروج إلى مواطن الفتنة والقتال من دون إذن ولي الأمر والمشاركة في تزوير بطاقات هوية شخصية . وأضافت الوكالة أن الجلسة التي تمت بحضور المدعى عليها وأربعة من أقاربها خصصت لتقديم رد المدعى عليها على لائحة الدعوى العامة حيث قدم وكيلها مذكرة من إحدى عشرة ورقة تضمنت إنكار المدعى عليها للتهم الموجهة إليها . (وكالات)
```

### NLI claims to label
1. هيلة القصير تبلغ من العمر خمسة وأربعين عاماً وتواجه اتهامات تتعلق بدعم تنظيم القاعدة مالياً
2. قدّم محامي المتهمة مذكرة دفاعية تتكون من إحدى عشرة صفحة أنكرت فيها جميع التهم المنسوبة إليها
3. عُقدت جلسة المحاكمة في المحكمة الجزائية المتخصصة بالرياض بحضور المتهمة وعدد من أقاربها
4. صدر حكم ابتدائي بسجن هيلة القصير عدة سنوات قبل استئناف المحاكمة

### English text to translate to Arabic
```
The Specialized Criminal Court in Jeddah, western Saudi Arabia, resumed the trial of Hailah al-Qusair, a 45-year-old woman described as the first Saudi woman tried for involvement in terrorist activities, including fundraising for al-Qaeda, harboring wanted individuals, and possessing weapons. The charges against her also include joining al-Qaeda, recruiting members for the organization, financing terrorist operations, forging identity cards, and attempting to travel to conflict zones without authorization. During the second hearing, attended by the defendant and four of her relatives, her lawyer submitted an eleven-page memorandum in which she denied all charges brought against her.
```

---

## Article POLITICS_008

### Article body (Arabic)

```
عرضت الهند تقديم خبرات إلكترونية في إدارة عملية الانتخابات على مصر ومن ضمنها تجهيزها بمعدات رخيصة الكلفة تستخدم في الاقتراع .وقالت وسائل إعلام مصرية أن وفداً برئاسة رئيس لجنة الانتخابات الهندية شهاب الدين قريشي أنهى مباحثات مع المسؤولين المصريين أمس أطلعهم خلالها على النظام المتبع فى الهند بإجراء الانتخابات إلكترونياً . وأشارت إلى أن الوفد عرض التعاون مع مصر لتطوير تقنية محلية مصرية لتصنيع المعدات الإلكترونية الخاصة بالاقتراع وتزويد مصر بهذه الأجهزة حتى يتم تصنيعها . ونقلت عن قريشى أن الهند على استعداد لإطلاع الجانب المصري على كافة خبرات بلاده الانتخابية وفى مقدمتها الاقتراع الإلكتروني من خلال ماكينات صغيرة الحجم وسهلة التقنية لا يتجاوز ثمنها 200 دولار، تتيح للناخبين وخاصة الأميين منهم الإدلاء بأصواتهم بسهولة ويسر . (يو .بي .آي)
```

### NLI claims to label
1. ترأس شهاب الدين قريشي الوفد الهندي الذي أجرى محادثات مع المسؤولين المصريين حول نظام الانتخابات الإلكترونية
2. عرضت الهند مساعدة مصر في تطوير قدرات محلية لإنتاج الأجهزة الإلكترونية المستخدمة في التصويت وتزويدها بهذه الأجهزة إلى حين تصنيعها محلياً
3. أوضح قريشي أن تكلفة أجهزة الاقتراع الإلكترونية الهندية لا تتعدى خمسمائة دولار للجهاز الواحد
4. وقّعت مصر والهند اتفاقية رسمية لاستيراد أجهزة الاقتراع الإلكترونية خلال زيارة الوفد الهندي

### English text to translate to Arabic
```
India offered to share its electronic expertise in managing elections with Egypt, including providing low-cost voting equipment. A delegation led by Indian Election Commission chief Shahabuddin Qureshi concluded talks with Egyptian officials, during which they presented India's electronic voting system and proposed cooperation to develop local Egyptian technology for manufacturing electronic voting equipment. Qureshi stated that India is ready to share all its electoral expertise, including small, easy-to-use electronic voting machines costing no more than 200 dollars, which allow voters, especially illiterate ones, to cast their ballots with ease.
```

---

## Article POLITICS_060

### Article body (Arabic)

```
أعلنت الأمم المتحدة والاتحاد الأوروبي وعدد من المسؤولين في العالم دعمهم للمفاوضات المباشرة التي افتتحت، أمس في واشنطن برعاية أمريكية .وطالب الأمين العام للأمم المتحدة بان كي مون، المتفاوضين بألا يتركوا مسار المفاوضات ينحرف بسبب هجمات تحريضية، في غشارة لعمليتي الخليل ورام الله ضد المتوطنين . وأعرب كي مون أيضا عن أمله في أن يخوض الجانبان الإسرائيلي والفلسطيني، محادثاتهما بحس عملي ومرونة . وأضاف أعلم أنها لن تكون عملية سهلة . ودعت وزيرة خارجية الاتحاد الأوروبي كاترين اشتون كل الأطراف إلى الامتناع عن أي استفزاز وذلك بهدف عدم تخريب المفاوضات . واعتبرت أن عملية الخليل تظهر أن هناك قوى في المنطقة مصممة على تخريب عملية السلام .وقال وزير الخارجية الألماني جيدو فيسترفيله في مؤتمر صحافي مشترك بعد لقائه نظيره البريطاني ويليام هيغ في لندن نناشد الأطراف المعنية توفير الظروف التي من شأنها أن تسمح بإنجاح محادثات السلام . وأشار إلى أن هذه المحادثات تمثل فرصة . وأكد هيغ أن بلاده ستفعل أقصى ما في وسعها لدعم المفاوضات .وأعرب وزير الخارجية الروسي سيرغي لافروف أثناء زيارة إلى بولندا، عن دعم بلاده للمفاوضات المباشرة، ولو أنها لا تضمن النجاح . وقال لافروف الذي يزور وارسو إننا ندعم المفاوضات على الرغم من معارضة بعض الأوساط الفلسطينية وداخل العالم العربي، ومن أنها لا تعطي ضمانة بالنجاح مئة في المئة، لكنها تقدم مع ذلك فرصة ينبغي عدم تجاهلها . (وكالات)
```

### NLI claims to label
1. دعا الأمين العام للأمم المتحدة بان كي مون الأطراف المتفاوضة إلى عدم السماح للأعمال التحريضية بإعاقة مسيرة المفاوضات
2. أكد وزير الخارجية البريطاني ويليام هيغ أن المملكة المتحدة ستبذل كل جهد ممكن لمساندة المفاوضات
3. أدلى وزير الخارجية الروسي سيرغي لافروف بتصريحاته حول دعم المفاوضات خلال زيارته إلى التشيك
4. شاركت الصين بشكل فعّال في رعاية المفاوضات المباشرة التي انطلقت في واشنطن

### English text to translate to Arabic
```
The United Nations, the European Union, and several world officials announced their support for the direct Israeli-Palestinian negotiations that were launched in Washington under American sponsorship. UN Secretary-General Ban Ki-moon urged negotiators not to let provocative attacks derail the talks, while EU foreign policy chief Catherine Ashton called on all parties to refrain from provocations that could undermine the peace process. German Foreign Minister Guido Westerwelle and British Foreign Secretary William Hague appealed for conditions conducive to successful peace talks, and Russian Foreign Minister Sergei Lavrov expressed his country's support for the negotiations despite acknowledging they do not guarantee success.
```

---

## Article POLITICS_022

### Article body (Arabic)

```
يتذكر خالد منصور من مخيم الفارعة للاجئين الفلسطينيين، شمال شرق مدينة نابلس بالضفة الغربية، قريته أم الزينات، الواقعة داخل الأراضي المحتلة عام ،1948 ويقول عندما كبرت ذهبت إلى هناك لزيارة أطلال البلدة برفقة أبي في عام ،1971 ودهشت كثيرا من جمالها وطبيعتها الفتانة، فأم الزينات هي الجنة بعينها، فيها الجبل الشامخ، جبل الكرمل وما أدراك ما الكرمل..!! وفيها الغابات والأحراش، وفيها الينابيع والآبار، فيها السهل المنبسط الخالي حتى من الحصى، وفيها الوعر وكروم الزيتون.كانت أم الزينات قرية بسيطة هادئة لم يتجاوز عدد سكانها في عام 1948 ال1750 نسمة، وأهلها فلاحون حقيقيون، جادون ومجتهدون، يحبون الأرض كحبّ أبنائهم، لم يفرّطوا في شبر منها، ولم يبيعوا حبّة تراب واحدة للغاصبين والسماسرة.. كانت وادعة وحصينة، فاستحقّت ما قاله عنها الثائر الفلسطيني الكبير أبو درّة بأنها البلد الأمين. إذ شكّلت هذه القرية الملاذ الأمين للثائرين على الاستعمار البريطاني، وللمقاومين للزّحف اليهودي الاستيطاني، خلال النصف الأول من القرن المنصرم، ولم يستطع المحتلون الإنجليز إلقاء القبض على أيّ من الثّوار في أراضيها، رغم أنها عرفت كقاعدة خلفية أساسية للثوار، وهو الأمر الذي أكّدته وقائع معركة أمّ الدّرج الشهيرة.ويقول منصور دخلت أم الزينات أول مرة بصحبة أبي، الذي عرّفني بكل معالمها، ورغم كبر سنّ والدي فإنه لم يكن يتعب من التجوال في البلدة، وكان يقضي ساعات وساعات، هائما على وجهه في دروبها القديمة، وكأنه يبحث عن شيء ما كان قد نسيه عند خروجه الأخير من البلدة. وعندما كان يحين موعد العودة، كان أبي يركب السيارة معنا متثاقلا، وكأنه يريد أن يقول لنا: اتركوني هنا في بلدتي، وعودوا أنتم إلى مخيمكم.ويصمت منصور قليلا ويضيف لقد مات أبي في عام ،1986 ولم تفارق لسانه سيرة أمّ الزينات، وأهل أمّ الزينات، وقد أوصانا أن ننقل رفاته إضافة إلى رفات صديق آخر عزيز عليه، هو داود الخالد، إلى أم الزينات، وذلك عندما نعود إليها، ونحررها من دنس الغاصبين.
```

### NLI claims to label
1. كان عدد سكان قرية أم الزينات نحو 1750 شخصاً في سنة 1948
2. وصف الثائر الفلسطيني أبو درّة قرية أم الزينات بأنها البلد الأمين
3. توفي والد خالد منصور في سنة 1988 دون أن ينسى ذكر قريته أم الزينات
4. عاد خالد منصور للعيش في قرية أم الزينات بشكل دائم بعد زيارته الأولى لها

### English text to translate to Arabic
```
Khaled Mansour, a Palestinian refugee from Al-Far'a camp near Nablus in the West Bank, recalls his ancestral village of Umm al-Zinat, located in the territories occupied in 1948, describing its stunning natural beauty including Mount Carmel, forests, springs, and olive groves. The village, home to about 1,750 people before 1948, was known as a safe haven for revolutionaries against British colonialism and Zionist settlement expansion, earning it the title 'the safe town' from the renowned Palestinian revolutionary Abu Durra. Mansour recounts how his father, who died in 1986, never stopped speaking about Umm al-Zinat and left instructions for his remains to be transferred back to the village upon its liberation.
```

---

## Article POLITICS_037

### Article body (Arabic)

```
أحس محمد هلال ونحو 100 آخرين من أفراد عشيرة البونمر العراقية بالأمان وهم مختبئون من مقاتلي تنظيم "داعش" الإرهابي وسط الحشائش الطويلة، حتى فضحت أضواء عشرات السيارات أمرهم .وصاح المتشددون "نحن نعرف أنكم هناك أيها الخونة" ثم فتحوا النار على المختبئين الذين قاتلوهم لأسابيع . مات أغلب المختبئين ووقع البعض في الأسر .أما هلال فقد نجا لكنه أصيب في الذراع والساق بعد أن غطى نفسه بالدم وتظاهر بالموت تحت الجثث بينما كان المتشددون يضربون الجرحى ويسبونهم . وأوضح أنه رصد جثثاً أخرى من بينها أطفال وشيوخ ملقاة على جانب الطريق أثناء فراره من المكان بعد الاختباء ساعات تحت القتلى . وقال هلال ل"رويترز" هاتفياً من مدينة حديثة التي تسيطر عليها القوات العراقية ومقاتلو العشائر، لكنها مازالت عرضة لهجمات مسلحي تنظيم "داعش": "أنا في انتظار أسرتي . فما من سبيل أمامي للوصول إليهم . هواتفهم النقالة مغلقة ولا حيلة لي" . ويواجه أفراد كثيرون من العشيرة موقفاً مماثلاً من الغموض بعد أن أعدم "داعش" المئات عقاباً للعشيرة التي قاومت التنظيم . فبعد الاستيلاء على القرية الرئيسية للعشيرة شرع مقاتلو "داعش" في تمشيط المنطقة بحثاً عمن انطلقوا سيراً على الأقدام على أمل الهروب من غضب الجماعة التي اشتهرت بقطع رأس من يعارض تفسيرها المتشدد للدين أو إطلاق النار عليه .ويبدو أن المجزرة جرى الإعداد لها إعداداً جيداً . فقد قال أفراد من العشيرة إن تنظيم "داعش" زرع قبل استيلائه على قرية زاوية البونمر مخبرين قدموا له في نهاية الأمر أسماء المقاتلين . وقال الحاج رديف الذي يمتلك متجراً: "في الليلة التي دخلوا فيها القرية تراجع الجيش عن الخط الأمامي وأخلى مواقعه . وهذا تركنا بلا ذخيرة ولم يبق سوى مقاتلين من القرى، ولذلك اضطررنا للاستسلام" . وفر كثير من أهالي القرى بما عليه من ملابس . فاتجه البعض إلى الطريق الرئيسي المؤدي إلى هيت فسقطوا في فخ تصديق وعود "داعش" بالملاذ الآمن . وعندها بدأت الدماء تسيل بإعدام 35 شخصاً . أما آخرون مثل أبو ابتسام (50 عاماً) فساروا نحو ستة كيلومترات إلى منطقة صحراوية غربي هيت بعد أن استولى الإرهابيون على ما بحوزتهم من ذهب ومال، بل إن أحد الإرهابيين انتزع العقد الذي كانت ابنته تتزين به من عنقها . وفي نقطة تفتيش أقامها مقاتلو "داعش" أخذ أحد الإرهابيين علبة حليب مجفف من زوجته وألقى بها في التراب . وحاولت الزوجة استعادة العلبة، لكنها تلقت وكزة لتتراجع . وقال أبو ابتسام إن الإرهابيين تركوهم يرحلون بعد أن سرقوهم . وأضاف: "قال واحد منهم حتى أولادنا لا يستحقون الحياة لأنهم سيكبرون يوماً ما ويقاتلونهم"،بعد أن تفرق أبناء العشيرة اتجه المقاتل ماجد عودة واثنان من أبناء عمومته صوب الصحراء، حيث اختبأوا خمسة أيام عاشوا خلالها على التمر والمياه غير النقية من بحيرة . وكلما كان هاتفه النقال يعمل كان يتصل بأمه . وفي أحد الأيام وجدها مصابة بالهلع حيث أخذ مقاتلو "داعش" شقيقه محمد الذي يبلغ من العمر 13 عاماً مع آخرين . وأضاف: "قلت لأمي ألا تقلق، إنه طفل فعلاً ولم يشارك حتى في القتال"، وتابع: "اتصلت بي عائلتي بعد يوم عندما وصلت إلى موقع للجيش، وقالت لي إن شقيقي و47 طالباً غيره قتلوا . . قتلوه لأنني شرطي" .ويعد أفراد عشيرة البونمر من أشد المقاتلين بأساً في العراق لا في الأنبار وحدها . ولا تزال العشيرة تحصي خسائرها . وقال حمدان النمراوي مساعد أحد زعماء العشيرة إن عدد القتلى بلغ ،540 وإن كثيرين مازالوا مفقودين . وكانت رحلة الهروب في غاية المشقة بالنسبة إلى البعض . وقال رجل يدعى أبو تكعة إنه نام مع أسرته المكونة من سبعة أفراد خلف تل رملي حتى لا يكتشف أمرهم . وأصيبت زوجته بجفاف ولم يعد بوسعها إرضاع طفلها الوليد . وأضاف "مات صغيري . لكن أمه ظلت تتشبث به ولم تتركه يومين" . وتابع أنه لم يكن هناك وقت للحداد وكان يخشى أن يقتفي عناصر "داعش" أثره . وقال: "دفنا الطفل هناك واستأمنا البدو على قبره وتحركنا" . (رويترز)
```

### NLI claims to label
1. نجا محمد هلال من الموت بعد أن تظاهر بأنه ميت مستخدماً الدماء لتغطية جسده واختبأ تحت جثث القتلى
2. أفاد حمدان النمراوي بأن عدد من لقوا حتفهم من أبناء العشيرة وصل إلى خمسمائة وأربعين شخصاً مع استمرار فقدان كثيرين
3. أعدم تنظيم داعش خمسة وأربعين شخصاً بعد أن صدقوا وعوده بتوفير ملاذ آمن لهم على الطريق المؤدي إلى هيت
4. تلقت عشيرة البونمر دعماً عسكرياً من التحالف الدولي أثناء مقاومتها لتنظيم داعش

### English text to translate to Arabic
```
Fighters of the ISIS terrorist organization massacred hundreds of members of Iraq's Albu Nimr tribe in Anbar province after seizing their main village, executing at least 540 people — including children and elderly — as punishment for the tribe's resistance against the group. Survivors recounted harrowing escapes: Muhammad Hilal survived by smearing himself with blood and playing dead under corpses, while others fled into the desert for days with their families, enduring dehydration, theft of their possessions at ISIS checkpoints, and the loss of loved ones including a newborn who died from lack of milk. The massacre appeared to have been carefully planned, with ISIS planting informants in the village beforehand to identify fighters, while the Iraqi army's withdrawal from frontline positions left tribal fighters without ammunition and forced many to surrender.
```

---
