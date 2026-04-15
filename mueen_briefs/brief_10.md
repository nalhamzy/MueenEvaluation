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


## Article TECH_023

### Article body (Arabic)

```
دبي: «الخليج»دفع تنامي التحوّل الذكي في المنازل حول العالم المراقبين إلى اعتبار 2017 «عام المنازل الذكية»، في وقت تشير التوقعات إلى أن أعدادها سوف تتضاعف خمس مرات من 90 مليوناً في العام 2016 إلى 463 مليون منزل ذكي في عام 2021. ويواكب «جيتكس شوبر»، أكبر معرض سنوي للإلكترونيات والتقنيات الاستهلاكية في الشرق الأوسط، هذا التحوّل بعرض تشكيلة واسعة من المنتجات المنزلية الذكية مع تواصل فعالياته حتى يوم السبت 30 سبتمبر الجاري في قاعات زعبيل 3، 4، 5، 6 بمركز دبي التجاري العالمي.وقال أفيناش شانبوج، المدير في إدارة المعارض بمركز دبي التجاري العالمي، إن «جيتكس شوبر» شهد هذا العام عرض نظم منزلية مثيرة للاهتمام يمكنها التحكّم بالأجهزة بنقرة زر واحدة، عبر تطبيق ذكي، أو حتى التخاطب مباشرة مع الأجهزة الذكية، وأضاف: «يتيح جيتكس شوبر لزواره العثور على ما يرغبون به من أجهزة منزلية ذكية كالثلاجات والسماعات، باعتباره أكبر معرض للإلكترونيات الاستهلاكية في الشرق الأوسط، ما يؤدي إلى إحداث ثورة في الروتين اليومي وتسهيل القيام بالمهام المنزلية».وتعرض شركة «شرف دي جي»، إحدى أكبر شركات التجزئة الإقليمية، خلال مشاركتها في جيتكس شوبر، تشكيلة واسعة من الأجهزة المنزلية الذكية، بينها سماعات «سمارت هوم» من «جوجل»، التي تعمل بنظام المساعدة الشخصية «أسيستنت» من «جوجل»، ونظام «ثيرموستات» من شركة «نيست» للتحكم الذكي بترشيد استهلاك الطاقة.من جانبها، تعرض شركة جمبو للإلكترونيات أحدث أجهزة الأمن المنزلي الذكية، مثل قفل «جرينز» للأبواب العامل بلوحة أرقام الذي يمكن فتحه ببصمة الإصبع، وجرس الباب المصوّر، الذي يتيح إلقاء نظرة مباشرة إلى خارج المنزل في أي وقت عبر تطبيق على الهاتف الذكي.وقد شهد العام الماضي تقديم العديد من النظم المنزلية الذكية، بما فيها النظام «إيكو» من «أمازون»، و«هوم كيت» من «أبل»، و«سمارت هوم» من «جوجل»، «سمارت ثينجز» من «سامسونج»، وغيرها. وتسمح الأنظمة الذكية للمستخدمين بالتحكم في مجموعة متنوعة من الأجهزة المنزلية لإدارة المنزل بسهولة، مثل قفل الباب الأمامي والتحكم في الإنارة ودرجة الحرارة وساعات التنبيه وستائر النوافذ.
```

### NLI claims to label
1. تشير التقديرات إلى أن عدد المنازل الذكية سيرتفع من 90 مليوناً في 2016 إلى نحو 463 مليوناً بحلول عام 2021
2. تقوم شركة جمبو للإلكترونيات بعرض أجهزة أمن منزلية ذكية تشمل قفلاً يُفتح عن طريق البصمة وجرس باب مزوداً بكاميرا
3. تستمر فعاليات جيتكس شوبر حتى يوم الجمعة 29 سبتمبر في مركز دبي التجاري العالمي
4. بلغ عدد الزوار الإجمالي لمعرض جيتكس شوبر في نسخة 2017 أكثر من مليون زائر

### English text to translate to Arabic
```
The growing global shift toward smart homes has led observers to label 2017 as the 'Year of Smart Homes,' with projections indicating that the number of smart homes will increase fivefold from 90 million in 2016 to 463 million by 2021. GITEX Shopper, the Middle East's largest annual consumer electronics exhibition, is showcasing a wide range of smart home products at the Dubai World Trade Centre, running through September 30, with major retailers like Sharaf DG and Jumbo Electronics presenting smart speakers, thermostats, and security devices. Smart home systems from companies such as Amazon, Apple, Google, and Samsung allow users to control various household functions including door locks, lighting, temperature, alarms, and window blinds with ease.
```

---

## Article TECH_048

### Article body (Arabic)

```
دبي ـ «الخليج»:أطلق سمو الشيخ حمدان بن محمد بن راشد آل مكتوم ولي عهد دبي رئيس المجلس التنفيذي لدبي، أمس أول، أيام معرض جيتكس 2015، أول منصة موحدة من نوعها للخدمات الحكومية الذكية (دبي الآن) تمكن المتعاملين من الوصول إلى كافة الخدمات وإجراء جميع المعاملات.تعد هذه المنصة الموحدة الأولى التي تم تصميمها بناء على إشراك المتعاملين من خلال مختبر تصميم تجربة المتعامل التابع للدائرة، الأكثر شمولية وسلاسة لتواصل الجمهور مع دوائر وجهات حكومة دبي، باعتبارها أحد الحلول الذكية المتميزة والشاملة لكونها تجمع في مكان واحد عدداً كبيراً من الخدمات الحكومية الذكية ل22جهة حكومية في دبي مشتركة في البوابة حتى الآن. وسيتمكن كل من لديه حساب في تطبيق الدفع عبر الهواتف الذكية mPay أو خدمة هويتي الإلكترونية MyID من الدخول إلى هذه البوابة بسهولة والاستفادة القصوى من مجموعة من الباقات الخدماتية التي بنيت بالكامل على رغبات المتعاملين، وجرى تجميعها ضمن باقات فرعية، مصنّفة بدورها تحت 11 فئة، وهي: الدفعات والفواتير، والإسكان والمواصلات العامة، والأمن والعدل، والصحة، وقيادة المركبات، وتأشيرات الإقامة، وخدمات التعليم، وخدمة إسلام، والأعمال، وخدمات عامة. وكشفت حكومة دبي الذكية أنه ولأول مرة أيضاً ستحتوي المنصة الموحدة على لوحة بيانات ذكية تفاعلية تجمع الخدمات الأكثر استخداماً في أقل عدد من الخطوات لتوفير وقت وجهد المتعاملين، مثال ذلك جمع الفواتير التي تستحق الدفع في مكان واحد، والقيام بدفعها مرة واحدة.وتعمل لوحة البيانات الذكية بأسلوب تفاعلي، حيث تحلل بيانات الخدمات التي يستخدمها المتعامل، ومن ثم تقوم بإظهار الوثائق التي تحتاج إلى تجديد قريباً، وكذلك التي انتهت في حال لم يقم المتعامل بتجديدها مع إظهار تنبيهات بذلك، كما تتميز المنصة بأنها تتيح للمتعاملين إمكان التحكم في الإعدادات الخاصة، ما يعطي الطابع الشخصي للمتعامل في اختيار الخدمات التي تهمه، ويرغب في إتاحتها على لوحة البيانات الذكية. تسديد رسوم وتبرع واستعلام وتحتوي البوابة الموحدة على مجموعة كبيرة ومتنوعة من الخدمات واسعة الانتشار بين المتعاملين، مثل: تسديد رسوم كل من: سالك ونول واتصالات ودو وهيئة كهرباء ومياه دبي والمخالفات المرورية والعديد من خدمات بلدية دبي وجمارك دبي، والتبرع لكل من مؤسسة الجليلة ودبي العطاء، وكذلك الحصول على معلومات عن الطيران، وخدمة حجز سيارات الأجرة، والخدمات الصحية مثل: عمل جداول التطعيم للمواليد الجدد، والتعرف إلى أقرب صيدلية، والاستعلام والحصول على خدمات الإدارة العامة للإقامة وشؤون الأجانب - دبي، والخدمات الدينية بما في ذلك أوقات الصلاة، ومواقع المساجد وحاسبة الزيادة الإيجارية التي توفرها مؤسسة التنظيم العقاري، والتعرف إلى أنواع الأنشطة التجارية، والاستعلام وتجديد الرخص التجارية، وحجز اسم تجاري، وخدمات الطوارئ، وخدمات الأعمال، والاستعلام عن الخدمات العامة مثل تقارير الطقس، والخدمات البريدية، والتعرف إلى الجامعات والمدارس، وتصنيفاتها وتقييمها، والمنهاج التعليمي، وغيرها الكثير.وقال أحمد بن حميدان، مدير عام دائرة حكومة دبي الذكية: «إن إطلاقنا لهذه المنصة الموحدة يأتي ضمن الخطوات التي نتخذها تنفيذاً لمبادرة صاحب السمو الشيخ محمد بن راشد آل مكتوم نائب رئيس الدولة رئيس مجلس الوزراء حاكم دبي، رعاه الله، في الانتقال إلى الحكومة الذكية والوصول بدبي إلى المدينة الأذكى عالمياً، واستجابةً لتوجيهات سمو الشيخ حمدان بن محمد بن راشد آل مكتوم ولي عهد دبي رئيس المجلس التنفيذي لدبي، بتوفير واجهة تطبيق واحدة، ورقم تعريفي واحد لتحقيق مزيد من الراحة والسعادة للمتعاملين».وأضاف بن حميدان قائلاً: «تماشياً مع استراتيجية الدائرة التي تسعى إلى تسهيل حياة الناس وتمكينهم من الوصول إلى الخدمات بمنتهى السهولة، وفي أي وقت، ولأننا نعمل كحكومة مترابطة ومتضافرة لتلبية احتياجات متعاملينا، وتعزيزاً لخدماتنا وسياساتنا بما يتوافق مع متطلباتهم، فإنه من دواعي سرورنا أن نعلن عن إطلاق هذه المنصة التي ستوفر كثيراً من الوقت والجهد على المتعاملين مع الجهات الحكومية في دبي، ما سيضفي على حياتهم اليومية مزيداً من الرضا والسعادة».
```

### NLI claims to label
1. منصة دبي الآن تضم خدمات حكومية ذكية من اثنتين وعشرين جهة حكومية مشتركة في البوابة
2. يستطيع المستخدمون الدخول إلى البوابة عبر حساب تطبيق الدفع mPay أو خدمة هويتي الإلكترونية MyID
3. تم تصنيف الباقات الخدماتية في المنصة الموحدة تحت ثلاث عشرة فئة مختلفة
4. شهد معرض جيتكس 2015 إعلان شراكة بين حكومة دبي الذكية وشركات تقنية عالمية لتطوير المنصة

### English text to translate to Arabic
```
Sheikh Hamdan bin Mohammed bin Rashid Al Maktoum, Crown Prince of Dubai and Chairman of the Dubai Executive Council, launched 'DubaiNow,' the first unified platform for smart government services, on the opening day of GITEX 2015. The platform consolidates smart services from 22 government entities into a single portal, organized under 11 categories including payments, housing, health, transportation, and business, and features an interactive smart dashboard that aggregates frequently used services to save users time and effort. Ahmed bin Humaidan, Director General of Dubai Smart Government, stated that the launch aligns with Sheikh Mohammed bin Rashid Al Maktoum's initiative to transform Dubai into the world's smartest city and to enhance public satisfaction.
```

---

## Article TECH_028

### Article body (Arabic)

```
قال الرئيس لإدارة السياسات للتطبيقات الصناعية والتجارية في شركة إلكاتيل لوسنت الدولية لتطبيقات الاتصالات توماس برنز: إن الشركة تنافس عالمياً، وفي أسواق المنطقة على عمليات إنشاء شبكات اتصالات الجيل الرابع والتي تجري فيها حالياً عدة تجارب مع مشغلين للاتصالات من هذا النوع مع تنفيذها 3 شبكات في الأسواق الأمريكية خلال الفترة الماضية .وقال: إن انتشار الهواتف الذكية في المنطقة اسهم في رفع نسبة نمو تطبيقات الأعمال النقالة المخصصة للشركات في المنطقة بين 15-02% خلال 2010 في المنطقة، وأن تقديرات النمو للعام الجاري لتلك التطبيقات ستصل لنحو 20% مدعومة بتوقعات بدء عمليات شبكات الجيل الرابع في المنطقة والتي تسهم في توسع الشركات في استخدام تلك التطبيقات .
```

### NLI claims to label
1. صرّح توماس برنز بأن شركة إلكاتيل لوسنت قامت بتنفيذ ثلاث شبكات في الأسواق الأمريكية في الفترة السابقة
2. تراوحت نسبة نمو تطبيقات الأعمال النقالة للشركات في المنطقة بين 15 و20 بالمئة خلال عام 2010 بحسب ما ذكره برنز
3. توقّع برنز أن تبلغ نسبة نمو تطبيقات الأعمال النقالة للشركات نحو 30 بالمئة خلال العام الجاري
4. أبرمت إلكاتيل لوسنت عقوداً مع مشغلي اتصالات في دول الخليج العربي لإنشاء شبكات الجيل الرابع

### English text to translate to Arabic
```
Thomas Burns, head of industrial and commercial applications policy at Alcatel-Lucent, stated that the company is competing globally and in regional markets for the deployment of fourth-generation (4G) communication networks, having already implemented three networks in the American market while conducting several trials with regional telecom operators. He noted that the spread of smartphones in the region contributed to a 15-20% growth in enterprise mobile business applications during 2010. Burns added that growth estimates for the current year are expected to reach approximately 20%, supported by anticipated launches of 4G networks in the region, which would encourage companies to expand their use of such applications.
```

---

## Article TECH_086

### Article body (Arabic)

```
دبي "الخليج":أعلنت شركة لينوفو أمس عن تدشين أول منتجاتها من عائلة الخوادم "ثينك سيرفر" (ThinkServer) للمرة الأولى في الإمارات، وقطر ومصر معززة بذلك محفظتها من المنتجات والخدمات لتصبح محطة واحدة لتقديم الحلول لعملاء المؤسسات والشركات المتوسطة الصغيرة . وأوضحت الشركة أن خوادم ThinkServer سيتم إطلاقها في الشرق الأوسط وإفريقيا خلال الشهور القليلة القادمة .وتتضمن مجموعة خوادم ThinkServer خوادم الرفوف التي تناسب النشر على السحابة وقواعد البيانات، أو أعباء الأحمال الافتراضية، إلى جانب الخوادم البرجية المصممة لإدارة أعمال الملفات والطباعة ومنافذ البيع .وقال لي ألكورن، مدير مجموعة أعمال المؤسسات في لينوفو الشرق الأوسط وإفريقيا: "لينوفو في وضع جيد كمنافس عالمي قوي في سوق المؤسسات والشركات المتوسطة الصغيرة، تقدم للعملاء حلولاً متكاملة من البداية وحتى النهاية، بما في ذلك التخزين، والخوادم، والشبكات، والبرمجيات والخدمات ذات الصلة . يأتي إطلاق خوادم ThinkServer في المنطقة دليلاً على التزامنا تجاه عملائنا الذين يرغبون بالحصول على الأداء الاستثنائي، والموثوقية، والأدوات سهلة الاستخدام والحلول التي تناسبهم" .وتتمتع هذه الخوادم بتصميم متوازن يجعلها قادرة على تلبية متطلبات الأعمال الحالية والمستقبلية .
```

### NLI claims to label
1. أعلنت شركة لينوفو عن إطلاق خوادم ثينك سيرفر لأول مرة في كل من الإمارات وقطر ومصر
2. تشمل مجموعة خوادم ثينك سيرفر خوادم رفوف ملائمة للحوسبة السحابية وقواعد البيانات بالإضافة إلى خوادم برجية مخصصة لإدارة الملفات والطباعة ومنافذ البيع
3. صرّح لي ألكورن بصفته المدير التنفيذي لشركة لينوفو في منطقة الشرق الأوسط وشمال إفريقيا بأن الشركة تسعى لتقديم حلول شاملة للعملاء
4. تخطط لينوفو لافتتاح مراكز بيانات جديدة في دول الخليج العربي لدعم خدمات خوادم ثينك سيرفر

### English text to translate to Arabic
```
Lenovo announced the launch of its ThinkServer product line for the first time in the UAE, Qatar, and Egypt, aiming to provide end-to-end solutions for enterprises and small-to-medium businesses. The company stated that the ThinkServer range, which includes rack and tower servers designed for cloud deployment, databases, virtualization, file management, and point-of-sale operations, will be rolled out across the Middle East and Africa in the coming months. Lee Alcorn, Director of Enterprise Business at Lenovo Middle East and Africa, emphasized the company's commitment to delivering exceptional performance, reliability, and user-friendly solutions to its customers in the region.
```

---

## Article TECH_093

### Article body (Arabic)

```
أعلنت شركة إكستريم نتووركس، أمس، عن تعيين أوسكار رودريغز في منصب الرئيس التنفيذي والمدير العام للشركة . وينضم رودريغز إلى إكستريم نتووركس وفي رصيده ما يزيد على 20 عاماً من الخبرة في مجال المبيعات والتسويق .صرّح غوردون ستيت، رئيس مجلس إدارة الشركة قائلاً: ينضم رودريغز إلى إكستريم نتووركس حاملاً معه إرثاً غنياً والخبرة المطلوبة في مجال تسويق التقنيات فضلاً عن الصفات القيادية المناسبة لإدارة الشركة، وتابع ستيت قائلاً: ونحن بحاجة لشخص بحجم خبرته وعلاقاته لكي يساعدنا على تطوير الشركة وتوسيع آفاقها وتحريك عجلة نموّها .وصرّح رودريغز قائلاً: جُلّ ما لفتني في إكستريم نتووركس العمل الدؤوب الذي أنجزته الشركة في الأشهر الأخيرة، حيث واظبت على تطوير فعاليتها وتجنيد طاقاتها بما أعاد إحياء المنافسة في السوق وجعلها رائدة في مجالها .
```

### NLI claims to label
1. تم تعيين أوسكار رودريغز رئيساً تنفيذياً ومديراً عاماً لشركة إكستريم نتووركس
2. يمتلك رودريغز خبرة تتجاوز عقدين من الزمن في مجالي المبيعات والتسويق
3. أشار غوردون ستيت، نائب رئيس مجلس إدارة الشركة، إلى أن رودريغز يحمل خبرة واسعة في تسويق التقنيات
4. عمل أوسكار رودريغز سابقاً في شركة سيسكو قبل انتقاله إلى إكستريم نتووركس

### English text to translate to Arabic
```
Extreme Networks announced the appointment of Oscar Rodriguez as its new CEO and General Manager, bringing over 20 years of experience in sales and marketing. Gordon Stitt, the company's Chairman of the Board, stated that Rodriguez possesses the rich legacy, technology marketing expertise, and leadership qualities needed to develop and expand the company. Rodriguez expressed that he was most impressed by the diligent work Extreme Networks has accomplished in recent months, enhancing its effectiveness and competitiveness to become a leader in its field.
```

---

## Article TECH_088

### Article body (Arabic)

```
أعلنت شركة أوبتوما لأنظمة العرض الرقمية، عن نمو حصتها السوقية حيث أصبحت تحتل المركز الثاني في قائمة مزودي أجهزة العرض الرقمية في الربع الثالث، والرابع في سوق أجهزة العرض بشكل عام في منطقة الشرق الأوسط.جاء أداء الشركة القوي في الربع الثالث ليؤكد على مكانة أوبتوما المتقدمة بين شركات أجهزة العرض في المنطقة. حيث اقتربت من السيطرة على 7% من هذه السوق في جميع أرجاء الشرق الأوسط وإفريقيا في الربع الثالث من عام ،2008 بينما تتوقع الشركة تحقيق مزيد من النمو في الربع الرابع والمستقبل القريب.وقال آدم دينت، مدير منطقة في أوبتوما الشرق الأوسط وإفريقيا: إن هذا النمو المدهش في مبيعاتنا إنما يعكس زيادة الطلب على منتجاتنا في الأسواق المحلية بشكل عام، وسوق المملكة العربية السعودية بشكل خاص، والتي تشهد أعمالنا فيها نموا كبيرا حيث نهيمن على حصة سوقية فيها تقدر بأكثر من 15%. وتشهد أجهزة عرض أوبتوما المبتكرة وعالية الدقة اهتماما متزايدا خصوصا أجهزة عرض السينما المنزلية التي تحظى بشعبية هائلة وزيادة مطردة في الطلب.
```

### NLI claims to label
1. احتلت أوبتوما المرتبة الثانية بين مزودي أجهزة العرض الرقمية في الربع الثالث في منطقة الشرق الأوسط
2. صرّح آدم دينت بأن السوق السعودي يشهد نمواً ملحوظاً لأعمال الشركة مع حصة سوقية تتجاوز 15%
3. استحوذت أوبتوما على نحو 12% من سوق أجهزة العرض في الشرق الأوسط وإفريقيا خلال الربع الثالث من 2008
4. أطلقت أوبتوما خطاً جديداً من أجهزة العرض الرقمية المخصصة لقطاع التعليم في المنطقة خلال عام 2008

### English text to translate to Arabic
```
Optoma, a digital display systems company, announced that it has grown its market share to become the second-largest digital projector provider in the third quarter and fourth overall in the Middle East projector market. The company captured nearly 7% of the Middle East and Africa projector market in Q3 2008, with particularly strong performance in Saudi Arabia where it holds over 15% market share. Adam Dent, Optoma's regional manager for the Middle East and Africa, attributed the growth to increasing demand for the company's products, especially its innovative high-definition home cinema projectors.
```

---

## Article TECH_032

### Article body (Arabic)

```
تشارك هيئة الصحة بدبي بمعرض أسبوع جيتكس للتقنية في دورته ال33 بمركز دبي الدولي للمؤتمرات والمعارض بعدد من الفعاليات التي تعزز توجهها نحو الحكومة الذكية . أكد أحمد العمري مدير إدارة تقنية المعلومات بالإنابة بهيئة الصحة بدبي أهمية هذه المشاركة التي تهدف إلى تعريف الجمهور من الأطباء والمهنيين الصحيين وأفراد المجتمع المحلي بمشاريعها وتطبيقاتها الذكية التي تطلقها الهيئة لأول مرة ضمن خطتها الاستراتيجية المتماشية مع مبادرة الحكومة الذكية التي أطلقها صاحب السمو الشيخ محمد بن راشد آل مكتوم نائب رئيس الدولة رئيس مجلس الوزراء حاكم دبي، رعاه الله، وتوجيهات سمو الشيخ حمدان بن محمد بن راشد آل مكتوم، ولي عهد دبي، رئيس المجلس التنفيذي بالانتقال نحو الحكومة الذكية وتفعيل جميع المبادرات والأنشطة في مجال الخدمات الذكية .التفتيش الإلكترونيوأوضح العمري أن مشاركة الهيئة في معرض جيتكس ركزت على تعريف الزوار بأحدث خدماتها في مجال التطبيقات الذكية والمستشفيات الذكية والعمليات الإدارية الذكية كالتفتيش الإلكتروني وحملات التوعية الصحية الذكية وغيرها من الخدمات التي تلبي احتياجات كل فئات وشرائح المجتمع . وقال العمري إن جناح الهيئة يشكل فرصة مثالية للجمهور من المتعاملين الحاليين أو المحتملين مع هيئة الصحة بدبي للتعرف على أحدث الخدمات والتطبيقات والحلول الذكية والمبتكرة التي توفرها الهيئة لعملائها .وأكد حرص الهيئة والتزامها بتبني مبدأ الإبداع والابتكار للارتقاء بمستوى خدماتها المتنوعة والوصول بها إلى المتعاملين مباشرة عبر تطبيقات الهواتف الذكية وفق إجراءات تتسم بالمرونة وسهولة الاستخدام .رضا العملاءوأوضح العمري أن التطبيقات الذكية التي ستطلقها هيئة الصحة بدبي خلال فعاليات معرض جيتكس ستساهم بشكل فاعل في تحقيق رضا العملاء وتقديم خدمات تفوق توقعاتهم، وهو ما ترتكز عليه مبادرات الاستراتيجية العامة لهيئة الصحة في دبي لعام 2013-2025 .ودعا مدير إدارة تقنية المعلومات بالإنابة زوار المعرض من مختلف شرائح المجتمع ومن المستثمرين إلى التعرف على خدمات الهيئة الذكية التي سيتم عرضها بشكل مفصل طيلة أيام المعرض التي ستستمر حتى الرابع والعشرين من أكتوبر/تشرين الأول الجاري .وشهد جناح هيئة الصحة بدبي إقبالاً واسعاً من مختلف فئات ورموز المجتمع للتعرف على الخدمات الذكية التي اطلقتها الهيئة، حيث زار جناح الهيئة كل من اللواء محمد المري مدير الإدارة العامة للإقامة وشؤون الأجانب بدبي وسامي القمزي نائب رئيس مجلس الإدارة والعضو المنتدب لمؤسسة دبي للإعلام، وسلطان بطي بن مجرن المدير العام لدائرة الأراضي والأملاك بدبي .مسابقة يوميةولفت غانم لوتاه مدير إدارة التسويق والاتصال المؤسسي بهيئة الصحة بدبي إلى المسابقة اليومية التي تطرحها الهيئة طيلة أيام المعرض لعملائها من المتابعين على حساب الهيئة على تويتر DHA_DUBAI بهدف وضع متابعيها في قلب الحدث وتعريفهم بأحدث المستجدات والخدمات والتطبيقات الذكية التي تقدمها الهيئة، مشيراً إلى الجوائز القيمة التي ستقدمها الهيئة للفائزين في مسابقاتها اليومية .العيادة الذكيةتواصل العيادة الذكية لهيئة الصحة بدبي تقديم خدماتها لمتابعيها على تويتر طيلة أيام أسبوع جيتكس للتقنية من الساعة الواحدة حتى الثانية بعد الظهر للاجابة على كل أسئلتهم واستفساراتهم المتعلقة بمختلف المواضيع الصحية، حيث خصصت الهيئة عيادتها أمس للحديث عن أضرار التدخين .
```

### NLI claims to label
1. أحمد العمري يشغل منصب مدير إدارة تقنية المعلومات بالإنابة في هيئة الصحة بدبي
2. العيادة الذكية لهيئة الصحة بدبي تقدم خدماتها على تويتر يومياً لمدة ساعة واحدة خلال أسبوع جيتكس
3. معرض جيتكس للتقنية كان في دورته الثانية والثلاثين عند مشاركة هيئة الصحة بدبي
4. هيئة الصحة بدبي خصصت ميزانية خاصة لتطوير تطبيقاتها الذكية المعروضة في جيتكس

### English text to translate to Arabic
```
Dubai Health Authority (DHA) participated in the 33rd GITEX Technology Week at the Dubai International Convention and Exhibition Centre, showcasing its smart government initiatives including smart applications, smart hospitals, electronic inspection, and smart health awareness campaigns. Acting IT Director Ahmad Al Amri emphasized that the new smart applications, launched in line with Sheikh Mohammed bin Rashid Al Maktoum's smart government initiative and the DHA's 2013-2025 strategic plan, aim to enhance customer satisfaction and deliver services exceeding expectations. The DHA's pavilion attracted prominent visitors including Major General Mohammed Al Marri and other senior officials, while the authority also ran daily Twitter competitions and continued its Smart Clinic service addressing health topics such as smoking hazards.
```

---

## Article TECH_070

### Article body (Arabic)

```
دبي «الخليج»: كشفت «دو» عن إطلاق عرضها الجديد «العرض الكبير» الذي يمكن العملاء من الحصول على بيانات إضافية مضاعفة صالحة لغاية انتهاء العام الجاري. وتسهم هذه البيانات في تلبية احتياجات العملاء المتنوعة في مجال خدمات إنترنت الهاتف المتحرك التي تشمل البريد الإلكتروني ووسائل التواصل الاجتماعي ومشاهدة مقاطع الفيديو. كما يمتاز العرض بكونه يلبي احتياجات العملاء الفردية وذلك حسب نمط استخدام كل منهم، مما يعني أن العرض يخدم كل من العملاء ذوي الاستخدام المكثف والاستخدام القليل للبيانات. وقال فهد الحساوي، الرئيس التنفيذي للشؤون التجارية في دو: «نعمل دوماً على إيجاد سبل مبتكرة لمفاجئة عملائنا، وخاصة من خلال العروض التي تثري حياتهم اليومية بالطرق الأكثر إثارة. وسيتخلص عملاؤنا عبر «العرض الكبير» من القلق على إمكانية انتهاء رصيدهم من البيانات أو عناء الحاجة للبحث عن شبكات الواي فاي، وذلك انطلاقاً من قناعتنا بحق العميل في تجربة ما نسمّيه «حرية البيانات».
```

### NLI claims to label
1. أعلنت شركة دو عن عرض جديد يحمل اسم «العرض الكبير» يوفر للعملاء بيانات إضافية مضاعفة تستمر حتى نهاية السنة الحالية
2. صرّح فهد الحساوي بأن العرض الجديد سيغني العملاء عن القلق بشأن نفاد رصيد البيانات أو البحث عن شبكات الواي فاي
3. فهد الحساوي يشغل منصب الرئيس التنفيذي للشؤون التقنية في شركة دو
4. يتضمن العرض الكبير من دو خصومات على أسعار المكالمات الدولية للعملاء

### English text to translate to Arabic
```
Dubai-based telecom operator 'du' has launched a new promotion called 'The Big Offer,' which provides customers with doubled additional data valid until the end of the current year. The offer is designed to meet diverse mobile internet needs, including email, social media, and video streaming, and caters to both heavy and light data users. Fahd Al Hassawi, du's Chief Commercial Officer, stated that the promotion aims to free customers from worrying about running out of data or searching for Wi-Fi networks, embodying what the company calls 'data freedom.'
```

---

## Article TECH_043

### Article body (Arabic)

```
أعلنت ئي مارين ش .م .خ المتخصصة في تمديد وصيانة الكابلات البحرية في المنطقة، أمس عن اتمامها المرحلة الأولى من تمديد مشروع كابل TEAMS، الذي يمتد ل 4900 كيلومتر، ويصل بين مومباسا في كينيا وسواحل مدينة الفجيرة في دولة الإمارات .يهدف المشروع الذي أطلقته الحكومة الكينية إلى ربط كينيا ببقية العالم عن طريق كابل بحري للألياف الضوئية . ويعمل المشروع على الربط بين مدينة مومباسا في كينيا وسواحل الفجيرة في دولة الإمارات . وتصل سعة الكابل إلى 2 .1 تيرا بت، ما يعادل وحدتين من الألياف الضوئية لكل 640 جيجابت .وبدأت سفينة الكوابل البحرية نيوا، التي تعد إحدى السفن المتطورة التي تمتلكها ئي مارين، بتمديد الكابل البحري الشهر الماضي على أن يتم الانتهاء من المشروع بمرحلتيه الأولى والثانية خلال شهر يونيو/ حزيران المقبل . ويعمل فريق ئي مارين حالياً على تنفيذ المرحلة الثانية من المشروع .وقال عمر جاسم بن كلبان، الرئيس التنفيذي والعضو المنتدب لشركة ئي مارين: يعمل طاقم سفينة الكوابل البحرية نيوا حالياً على تنفيذ مشروع (تيمز)، حيث غادرت السفينة دولة الإمارات إلى مومباسا في وقت سابق من الشهر الماضي بهدف اتمام المرحلة الأولى من المشروع، ونحن سعداء اليوم بالاعلان عن اتمام المرحلة الاولى من هذا المشروع .وأضاف ابن كلبان: نحن ندرك مخاطر القرصنة البحرية التي تتعرض لها السواحل الإفريقية مؤخراً إلا أننا نتخذ كافة الاحتياطات اللازمة لحماية طاقمنا وسفينتنا .ومن الجدير ذكره أن الحكومة الكينية تمتلك 45في المائة من المشروع، واتصالات 15في المائة، وتعود ملكية بقية المشروع إلى شركات اتصالات إقليمية أخرى ومجموعة من مزودي خدمات الانترنت وشركات أخرى .
```

### NLI claims to label
1. يبلغ طول كابل TEAMS حوالي 4900 كيلومتر ويربط بين مومباسا الكينية وسواحل الفجيرة الإماراتية
2. تمتلك الحكومة الكينية نسبة 45 بالمائة من مشروع كابل تيمز بينما تمتلك اتصالات 15 بالمائة منه
3. تبلغ سعة الكابل البحري 2.1 تيرا بت أي ما يعادل ثلاث وحدات من الألياف الضوئية لكل 640 جيجابت
4. حصلت سفينة نيوا على حراسة عسكرية أثناء عملها قبالة السواحل الأفريقية لحمايتها من القرصنة

### English text to translate to Arabic
```
E Marine, a UAE-based submarine cable installation and maintenance company, announced the completion of the first phase of the TEAMS cable project, a 4,900-kilometer fiber-optic submarine cable connecting Mombasa, Kenya, to the coast of Fujairah in the UAE, with a capacity of 1.2 terabits. The project, initiated by the Kenyan government to link Kenya to the rest of the world, is being carried out by E Marine's advanced cable ship Niwa, with both phases expected to be completed by the following June. The Kenyan government holds 45 percent ownership of the project, Etisalat owns 15 percent, and the remainder is held by regional telecommunications companies, internet service providers, and other firms.
```

---

## Article TECH_026

### Article body (Arabic)

```
أعلنت أمس شركة لينوفو، عن مجموعة جديدة متعددة أنماط الاستخدام من حواسيب المفكرة والحواسيب اللوحية والهواتف الذكية والتي تعرض للمرة الأولى في المنطقة خلال معرض جايتكس شوبر 2013 .وتتمتع مفكرات فليكس متعددة نمط التشغيل بمرونة كبيرة تمكنها من الدوران حتى 300 درجة، وتقدم طريقة جديدة وأكثر طبيعية للتفاعل مع الحواسيب وتوفر تجربة لمس مريحة . وإلى جانب القيمة الكبيرة لحواسيب فليكس فإنها تتمتع بمرونة عالية وشاشة خلفية عصرية تعمل باللمس ومصممة بشكل متناغم مع اللون البرتقالي الجذاب . وتبدو الصور الظاهرة على شاشة حواسيب فليكس حيوية وطبيعية بفضل الشاشة عالية الوضوح، ويمكن الانتقال إلى شاشة فائقة الوضوح الكامل بشكل اختياري . وبفضل شاشة لمس بعشر نقاط ونظام التشغيل ويندوز 8 وبطارية تعمل لمدة 9 ساعات فإن حواسيب فليكس تقدم إنتاجية عالية مع سهولة في الانتقال في آن معاً .
```

### NLI claims to label
1. حواسيب فليكس مزودة بشاشة لمس تدعم عشر نقاط وتعمل بنظام ويندوز 8
2. كشفت لينوفو عن منتجاتها الجديدة لأول مرة في المنطقة ضمن فعاليات جايتكس شوبر 2013
3. تستطيع مفكرات فليكس الدوران حتى 360 درجة مما يمنحها مرونة استثنائية
4. تعمل حواسيب فليكس بمعالجات إنتل من الجيل الرابع

### English text to translate to Arabic
```
Lenovo announced a new multimode collection of notebooks, tablets, and smartphones, showcased for the first time in the region at GITEX Shopper 2013. The Flex notebooks feature a flexible design that rotates up to 300 degrees, offering a natural and comfortable touch experience. Equipped with a 10-point touchscreen, Windows 8, and a battery lasting up to 9 hours, the Flex devices deliver high productivity and seamless usability.
```

---
