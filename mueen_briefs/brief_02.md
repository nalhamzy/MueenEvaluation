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


## Article CULTURE_062

### Article body (Arabic)

```
اجتمع مجلس إدارة اتحاد كتاب وأدباء الإمارات، وقرر قبول استقالة نجيب الشامسي نائب رئيس مجلس الإدارة، ووجه إليه الشكر على الجهود التي بذلها خلال الفترة الماضية . ثم استدعى عضو الاحتياط الأول القاصة باسمة يونس، وأعيد توزيع المهام على النحو التالي: حبيب الصايغ رئيساً لمجلس الإدارة، أسماء الزرعوني نائبة لرئيس مجلس الإدارة، إبراهيم الهاشمي أميناً عاماً، أحمد العسم أميناً للصندوق ورئيساً للهيئة الإدارية في فرع رأس الخيمة، محمد المزروعي مسؤولاً عن التأليف والنشر ورئيساً للهيئة الإدارية في فرع أبوظبي، وباسمة يونس مسؤولة ثقافية، وعبدالله السبب مسؤولاً للإعلام والعلاقات العامة .كما تمت تسمية حبيب الصايغ رئيساً لمجلس أمناء المؤتمر العام لكتاب وأدباء الإمارات، وباسمة يونس أمينة عامة للمؤتمر، فيما سميت أسماء الزرعوني أمينة عامة لملتقى الإمارات للإبداع الخليجي .
```

### NLI claims to label
1. تم قبول استقالة نجيب الشامسي من منصب نائب رئيس مجلس إدارة اتحاد كتاب وأدباء الإمارات
2. تولت أسماء الزرعوني منصب الأمينة العامة لملتقى الإمارات للإبداع الخليجي
3. عُيّن محمد المزروعي رئيساً للهيئة الإدارية في فرع رأس الخيمة
4. جاءت استقالة نجيب الشامسي بسبب خلافات داخلية في مجلس الإدارة

### English text to translate to Arabic
```
The board of directors of the UAE Writers and Authors Union convened and accepted the resignation of Najeeb Al Shamsi as vice chairman, thanking him for his past efforts. The board then called upon first reserve member, short story writer Basma Younes, and redistributed roles, with Habib Al Sayegh remaining as chairman, Asma Al Zaraouni appointed as vice chairwoman, and other members assigned various administrative and cultural responsibilities across branches in Abu Dhabi and Ras Al Khaimah. Additionally, Habib Al Sayegh was named chairman of the board of trustees of the General Conference of UAE Writers and Authors, Basma Younes was appointed as its secretary-general, and Asma Al Zaraouni was named secretary-general of the UAE Forum for Gulf Creativity.
```

---

## Article CULTURE_086

### Article body (Arabic)

```
أعلنت اللجنة الاجتماعية الفلسطينية في أبوظبي البيارة انها أنهت حصر المشاركات في مسابقة القدس للقصة القصيرة الدورة الثانية، حيث بلغ عدد المشاركات المستوفية للشروط 1338 عملاً جاءت من ثلاثين بلداً .وأعلن عبد المعز عودة مشرف المسابقة أن اللجنة قررت تخصيص 15 جائزة لهذه الدورة موزعة على خمس فئات عمرية، وذلك لمنح الفرصة كاملة للمتسابقين، وباشرت اللجنة عملية الفرز الأولى للقصص المشاركة بالتعاون مع لجان فرز مختصة في القصة القصيرة، ومن المتوقع أن يتم اعلان نتائج المسابقة منتصف شهر أكتوبر/ تشرين الأول المقبل .بدوره قال عمار الكردي رئيس اللجنة ان هذه المسابقة تهدف إلى تعزيز الوعي حول عروبة القدس وتسليط الضوء على دور المدينة الحضاري والثقافي باعتبارها رمزاً للسلام والمحبة .وأضاف الكردي ان اللجنة حرصت على التنسيق مع وزارتي التربية والتعليم في الإمارات وفلسطين وقامت بمخاطبة جميع السفارات العربية في الإمارات من أجل تعميم المشاركة في المسابقة في الوطن العربي .
```

### NLI claims to label
1. بلغ عدد الأعمال المستوفية لشروط مسابقة القدس للقصة القصيرة 1338 عملاً من ثلاثين دولة
2. تم تخصيص خمس عشرة جائزة موزعة على خمس فئات عمرية في الدورة الثانية من المسابقة
3. من المنتظر الإعلان عن نتائج المسابقة في منتصف شهر نوفمبر القادم
4. شارك في تحكيم المسابقة أدباء وكتّاب من عدة دول عربية

### English text to translate to Arabic
```
The Palestinian Social Committee in Abu Dhabi (Al-Bayara) announced the conclusion of submissions for the second edition of the Jerusalem Short Story Competition, receiving 1,338 qualifying entries from thirty countries. The committee decided to allocate 15 prizes distributed across five age categories, with initial screening of stories underway in collaboration with specialized panels, and results expected to be announced in mid-October. Committee chairman Ammar Al-Kurdi stated that the competition aims to raise awareness about the Arab identity of Jerusalem and highlight its civilizational and cultural role, noting that coordination was made with the ministries of education in both the UAE and Palestine, as well as Arab embassies in the UAE, to promote participation across the Arab world.
```

---

## Article CULTURE_091

### Article body (Arabic)

```
تشارك الإمارات في معرض الإسكندرية الدولي للكتاب، في الفترة من 23 مارس/آذار الجاري إلى 7 إبريل/نيسان المقبل، بالتنسيق مع اتحاد الناشرين المصريين، وبمشاركات عربية ودولية .وقال المشرف على المعرض، د . خالد عزب: إن مركز الإمارات للدراسات السياسية والاستراتيجية سيشارك في المعرض بأحدث إصداراته، وقدر عزب: إجمالي دور النشر التي سوف تشارك في معرض هذا العام بنحو 60 دار نشر، وتشارك لأول مرة فيه تايوان بمجموعة من أحدث ما أصدرته دور النشر التايوانية .كما أعلنت مكتبة الاسكندرية الجهة المنظمة للمعرض اختيارها المغرب لتحل ضيف شرف الدورة المقبلة للمعرض، التي ستقدم العديد من الأنشطة الثقافية، حيث يستضيف المعرض نخبة من كبار الكتاب والمثقفين والمفكرين المغاربة . وخصص المعرض قسما خاصا منه لسور الأزبكية وسور النبي دانيال، الذي يهتم بالكتاب المستعمل الذي يلقى إقبالا خاصا طوال فترة المعرض .ومن المقرر أن تشارك السعودية بجناح كبير سيقام في مقدمة المعرض ليتعرف رواده إلى الإنتاج الثقافي والمعرفي بالجامعات السعودية والمكتبات ومراكز الأبحاث . فيما يشارك المجلس الوطني للثقافة والفنون في الكويت بمطبوعاته وعلى رأسها سلسلة عالم المعرفة ومجلة عالم الفكر وسلسلة إبداعات وإصداراته من ذخائر التراث .وقد قررت مكتبة الاسكندرية تقديم خصومات خاصة على مطبوعاتها التي تلقى رواجا بين الجمهور، خاصة مجلة ذاكرة مصر المعاصرة، التي صدر منها حتى الآن 12 عددًا، حيث ستطرح الأعداد من الخامس إلى الثاني عشر في كميات إضافية لتلبية طلبات الجمهور من المجلة، كما ستعيد المكتبة طرح أعداد إضافية من سلسلة مراصد المتخصصة في علم الاجتماع الديني، وكذلك من سلسلة أوراق المتخصصة في الدراسات المستقبلية .
```

### NLI claims to label
1. تستمر فعاليات معرض الإسكندرية الدولي للكتاب لمدة ستة عشر يوماً تقريباً بدءاً من أواخر مارس وحتى أوائل إبريل
2. تم اختيار المغرب كضيف شرف للدورة القادمة من معرض الإسكندرية الدولي للكتاب الذي تنظمه مكتبة الإسكندرية
3. يبلغ إجمالي دور النشر المشاركة في المعرض هذا العام حوالي ثمانين دار نشر وفقاً لتقديرات المشرف على المعرض
4. تم تخصيص ميزانية إضافية من الحكومة المصرية لدعم معرض الإسكندرية الدولي للكتاب هذا العام

### English text to translate to Arabic
```
The UAE is participating in the Alexandria International Book Fair, held from March 23 to April 7, alongside approximately 60 publishing houses including first-time participant Taiwan, with the Emirates Center for Strategic and Political Studies showcasing its latest publications. The Bibliotheca Alexandrina, the fair's organizer, has selected Morocco as the guest of honor for this edition, hosting prominent Moroccan writers and intellectuals, while Saudi Arabia and Kuwait are also participating with major pavilions featuring their cultural and academic productions. The Bibliotheca Alexandrina has also announced special discounts on its popular publications, including additional copies of the magazine 'Memory of Contemporary Egypt' and specialized series in religious sociology and future studies.
```

---

## Article CULTURE_080

### Article body (Arabic)

```
نظم مركز الشارقة للشعر الشعبي مساء أمس الأول أولى أماسي الصالون الأدبي النسائي الذي يعتزم إقامته بشكل دوري، وضمت الشاعرات علياء جوهر وكلثم عبدالله وظبية الإمارات وهنادي المنصوري وفايزة الأسيرة وسلمى الشامسي وهمس الإمارات وشهناز محمد علي، وقدمت فقرات الأمسية الشاعرتان مريم النقبي ونوال سالم .خصصت الأمسية للحديث عن وضع الأديبة الإماراتية في مجتمعها خاصة الشاعرة الشعبية، وتطرق الحوار إلى ندرة المنابر المتاحة لها وقلة الملتقيات النسائية والنظرة الدونية التي ينظر المجتمع بها إلى الإبداع النسائي في مقابل إعلاء شأن الإبداع الرجالي، والنظرة إلى الشاعرة نفسها، كما تطرق إلى صعوبة إقامة مسابقات نسوية بحتة وعدم الاستمرار في الأنشطة والملتقيات النسائية، وعزوف الشاعرة الإماراتية عن المشاركة في برنامج شاعر المليون .وقدمت المشاركات مقترحات لتفعيل دور هذا الصالون وانطلاق الأقلام الشابة منه . وكان راشد شرار مدير المركز قد رحب بالشاعرات، وأكد لهن أن أبواب المركز مفتوحة لهن ولإبداعاتهن، ليكون مهد انطلاقة حقيقية للأقلام النسائية الشابة .ورداً على ذلك ألقت شاعرة البادية قصيدة عبرت فيها عن سعادتها بهذا التجمّع الذي كانت تتطلّع إليه منذ زمن، وقالت فيها:مركز للشعر يعنيناأوكل منا فز من صوبهمن دعيتو نحن لبينالجلسة ف الشعر مرغوبهونلتقي مع ناس ذربيناقولهم للوصف باعذوبهكلهم ع الدّرب ماشينافي وسط واديه باعجوبه
```

### NLI claims to label
1. أقيمت الأمسية الأولى للصالون الأدبي النسائي في مركز الشارقة للشعر الشعبي وشارك فيها عدد من الشاعرات
2. تناولت الأمسية قضايا تتعلق بقلة الفرص المتاحة للشاعرة الإماراتية وصعوبة تنظيم مسابقات خاصة بالنساء
3. تولت تقديم فقرات الأمسية الشاعرتان علياء جوهر ونوال سالم
4. حضر الأمسية عدد من المسؤولين في هيئة الثقافة بالشارقة لدعم المبادرة

### English text to translate to Arabic
```
The Sharjah Center for Popular Poetry organized the first session of a women's literary salon, featuring eight female poets who discussed the challenges facing Emirati women writers, including the scarcity of platforms available to them, the lack of women's literary gatherings, and society's dismissive attitude toward women's creativity compared to men's. The participants proposed initiatives to activate the salon's role and support young female writers, while the center's director, Rashid Sharrar, affirmed that the center's doors are open to women poets and their creative works. In response, the poet known as 'Sha'irat al-Badiya' recited a poem expressing her long-awaited joy at the gathering and celebrating the union of talented female poets.
```

---

## Article CULTURE_098

### Article body (Arabic)

```
محمد ولد محمد سالم رحل محمد الفيتوري وبقي من عمره "ما لم يعشه، وما لم يقله وما لا يقال"، بقيت غصة الحزن في حلقه على ذلك الوطن الممتد من الخليج إلى رأس الرجاء الصالح الذي غنى له طوال سنين عمره الثمانين، بقصائد ثائرة تسعى إلى تحطيم كل الأغلال والقيود التي كبلت هذا الوطن واستعبدت سكانه، لكنّ الوطن خان شاعره مرتين، أولاهما عندما خان موبوتو سيسي سيكو الوطن، وتحالف مع أمريكا وقتل باتريس لومومبا رمز الثورة، وعندما تناحر رفقاء السلاح والثورة، واغتال كومباوري القائد الثوري توماس سنكارا، وعندما تخاذل الجميع وانفرد الصهاينة بشعب أعزل، فشردوا طليعته وقتلوها وأودعوها السجون، ولم يبق منها سوى ذلك الصبي الذي يحمل الحجارة في وجه الدبابة، وعندما دكّت قوات بوش الغازية بغداد وفتتت وطناً بحجم العراق وجعلته مسرحاً لتلاعب الأهواء الفاسدة .خان الوطن الفيتوري مرة أخرى عندما سحب منه النميري جواز سفره، وحرمه من أرض النيل التي سكنت روحه، وركع طويلاً لَدَى حَافَة نهرها، وبين شَجَرها، وفي دجاها الأبنوسي ونقوش تضاريسها ولامست شفتاه تماثيلها الشامخة، فعاش منفيا عن ذلك التراب الذي دخل في تشكيل وجدانه، وظل خياله يحمله إليه ليتوسده وترقد روحه فيه حتى ولو بقي جسده بعيداً عنه: (أرقد في كل شبر من الأرض/ أرقد كالماء في جسد النيل/ أرقد كالشمس فوق/ حقول بلادي/ مثلي أنا ليس يسكن قبرا)، وخانه الوطن عندما تركه للنسيان، رغم أنه هو لم ينس الوطن، ولم يغمض له جفن منذ حمل ريشته ليطرد عنه الذل والاستعباد والاستعمار والاستبداد، وكان حقيقاً به، وقد مالت شمس عمره للغروب، وارتعشت يده من طول ما حملت ذلك القلم الإفريقي العربي المصنوع من الأبنوس، أن يرد له ذلك الوطن شيئاً من جمائله الكثيرة، فيحتضنه في أواخر عمره بما احتضاناً يليق به، ويشيعه إلى قبره تشييعاً على قدر قلمه المناضل .لم يتنازل الفيتوري عن حلمه في أية لحظة، ولم يفقد الثقة في أرض السودان أن تنبت الجمال، وفي إفريقيا أن تثور وتتحرر إلى الأبد، وفي الوطن العربي أن يهزم الصهيونية ويصنع حضارة حديثة تليق به، ولم يفقد الثقة في قلمه أنه سوف يسعفه دائما بالجديد والبديع، وكان شعره في البداية قد ارتكز على الغنائية والإيقاع القوي والكلمة اللاذعة، لأن أحلام الثورة الإفريقية والعربية كانت كبيرة، ومواجهتها مع قوى التخلف والاستعمار كانت شديدة، فاحتاجت إلى الكلمة القوية والإيقاع المحمِّس، ولئن كانت تلك القوة قد خفتت في دواوينه الأخيرة، فإن ذلك لا يعني أنه تخلى عن قناعاته، ورمى أحلامه خلفه، بل ظل متمسكاً بها، لكنّ الانتكاسات الكثيرة أسلمته إلى نوع من التأمل والتفكير الحزين الذي يبحث عن تأويل لما حدث، ويحاول أن يستشف بصيص ضوء في المستقبل . dah_tah@yahoo.fr
```

### NLI claims to label
1. عاش الشاعر محمد الفيتوري ثمانين عاماً قضاها في الكتابة والنضال من أجل وطنه الممتد من الخليج إلى أقصى أفريقيا
2. اتسم شعر الفيتوري في بداياته بالغنائية والإيقاع القوي نظراً لحجم التحديات التي واجهتها الثورات الإفريقية والعربية
3. قام الرئيس السوداني جعفر النميري بسحب الجنسية السودانية من الفيتوري ومنعه من النشر في الصحف
4. أقامت الحكومة السودانية حفل تكريم للفيتوري في الخرطوم قبل وفاته بفترة قصيرة

### English text to translate to Arabic
```
The article discusses the life and legacy of the renowned Afro-Arab poet Muhammad al-Fayturi, who passed away after dedicating his eighty years to revolutionary poetry aimed at liberating Africa and the Arab world from colonialism, oppression, and Zionism. Al-Fayturi was betrayed by his homeland twice: first through the political failures and betrayals across Africa and the Arab world, including the killing of Lumumba, the assassination of Sankara, and the invasion of Iraq; and second when Sudan's Nimeiry revoked his passport, forcing him into exile far from the Nile land that shaped his soul. Despite numerous setbacks and being consigned to oblivion by his homeland, al-Fayturi never abandoned his dreams of African liberation and Arab triumph, though his later poetry shifted from fiery revolutionary verse to a more contemplative and sorrowful tone searching for meaning amid repeated defeats.
```

---

## Article CULTURE_067

### Article body (Arabic)

```
تواصلت أنشطة الملتقى الرابع لفن الخط العربي الذي تنظمه إدارة الفنون في دائرة الثقافة والإعلام في الشارقة، حيث شهد متحف الحضارة الإسلامية في الشارقة صباح أمس تنظيم ورشة حول طريقة صناعة الورق يدوياً قدمها د . بسام داغستاني سوريا .بدأ داغستاني بالحديث عن تاريخ صناعة الورق يدوياً والتي كانت سائدة في العالم الإسلامي منذ ما يزيد على 1000 سنة، حيث عرف أصحابها بالوراقين، وأشار إلى أن هذا النوع من الورق عرف بالطلحي نسبة إلى صانع تخصص فيه يسمى طلحة، ويمتاز الورق المصنّع يدوياً بقدرته على مقاومة عوامل الزمن بعكس الورق المصنّع بالطرق الحديثة، وذلك لاحتواء المواد التي يصنع منها على نسبة مرتفعة من مادة السيليلوز، ولقلة نسبة الخشب فيه، وأما الورق المصنع بطرق حديثة فنسبة الخشب فيه مرتفعة جداً، والخشب معروف بضعف مقاومته لعوامل الزمن .وذكر داغستاني مراحل صناعة الورق والتي تبدأ باختيار المادة التي سيصنع منها، وهناك أربع مواد نباتية معروفة في تلك الصناعة، وهي القطن وهو أجودها وأكثرها نعومة، ثم الكتان وهو يماثل القطن، ويمتاز ورقه بالقوة والقدرة على مقاومة التشقق، وتعتبر مصر وسوريا من أكثر البلدان العربية إنتاجاً لهاتين المادتين قديماً وحديثاً، ويأتي بعد ذلك القنب وكان يستورد من بلاد الهند قديماً، وسعف النخيل وهو مجود في كل الأقطار العربية تقريباً، وهذه المواد تمتاز بالتوفر في الطبيعة مما يسهل على الإنسان اقتناءها واستخدامها، فلم يكن ذلك يكلف الوراق كبير عناء .وبعد اختيار المادة التي يريد الصانع أن ينتج منها الأوراق يغسلها بالماء، ثم يبيتها منقوعة في ماء فيه كلس، وفي الصباح يغسلها جيداً ثم ينشرها بعرضها للشمس طيلة النهار، ويكرر هذه العملية سبعة أيام متتالية، بعد ذلك يضع المادة في مهراس مع الماء ويدقها جيداً حتى تصير بنعومة الحرير، ثم يصبها في القوالب ليخرج منها بالأشكال والمقاسات التي يريد، وبعد تجفيفها يضعها في مكبس لتنبسط وتصبح جاهزة للاستعمال .ويضيف داغستاني: عند تلوين الورقة يقوم الصانع بتبييض المادة المستعملة في صناعة الورقة بالكلس حتى تكون ناصعة ثم يأخذ النباتات الصبغية وهي كثيرة متعددة الألوان، فيختار المادة المنتجة للّون الذي يريده وبعد غليها، يضع في المادة الماء الملون، ويتركها تتشبع باللون .الجدير بالذكر أن هذه الورشة استقطبت اهتمام فنانين وأساتذة جامعيين من كل الجنسيات وطلاب كليات الفنون، وبعد أن قدم المحاضر توضيحا عمليا لمراحل صناعة الورقة، اصطف الجميع كل يريد أن يأخذ دوره في تجريب هذه الصناعة التي قالت عنها إحدى الحاضرات إنها ساحرة، وقال الفنان التشكيلي باسل الساير بعد أنهى تجربة صناعة ورقة: إن على كل فنان أن يجرب العمل على هذا النوع من الورق لما له من خواص جمالية، وقدرة على عكس الألوان على حقيقتها، لذلك نحن هنا لتعلم هذه الطريقة، وأما الخطاط محمد قاسم الحداد فقد قال: إن هذا النوع من الورق، هو أجود أنواع الورق لكتابة اللوحة الخطية، فالألوان تظهر ناصعة جميلة، ولذلك فلا يمكن لخطاط أن يكتب لوحة بديعة من دون أن تكون على ورق مصنع بالطريقة التقليدية . واكتفى الخطاط محمد النوري بكتابة عبارة وكان فضل الله عليك عظيماً بخط أنيق جميل، على ورقته التي صنعها بيده.
```

### NLI claims to label
1. أقيمت ورشة صناعة الورق اليدوي في متحف الحضارة الإسلامية بإمارة الشارقة
2. أوضح المحاضر أن الورق المصنوع يدوياً يتميز بمقاومته للزمن بسبب ارتفاع نسبة السيليلوز وانخفاض نسبة الخشب فيه
3. ذكر داغستاني أن المواد النباتية المستخدمة في صناعة الورق ثلاث وهي القطن والكتان وسعف النخيل
4. حصل الدكتور بسام داغستاني على شهادته الجامعية في مجال صناعة الورق التقليدي من إحدى الجامعات السورية

### English text to translate to Arabic
```
The Fourth Arabic Calligraphy Forum, organized by the Arts Department of the Sharjah Department of Culture and Information, held a workshop at the Sharjah Museum of Islamic Civilization on traditional handmade papermaking, presented by Dr. Bassam Daghestani from Syria. Daghestani explained the thousand-year history of handmade paper in the Islamic world, detailing the four plant-based materials used—cotton, linen, hemp, and palm fronds—and the multi-step production process involving washing, soaking in lime water, sun-drying, pounding, molding, and pressing. The workshop attracted artists, university professors, and art students of various nationalities, with participants such as artist Basel Al-Sayer and calligraphers Mohammed Qasim Al-Haddad and Mohammed Al-Nouri praising the aesthetic qualities of handmade paper for calligraphy and art.
```

---

## Article CULTURE_039

### Article body (Arabic)

```
انطلقت فعاليات الدورة العاشرة لأيام الشارقة المسرحية مساء 27 من مارس/آذار برعاية صاحب السمو الشيخ الدكتور سلطان بن محمد القاسمي عضو المجلس الأعلى حاكم الشارقة وبعرض القضية، إحدى أعماله المسرحية، واختتمت مساء 5 من أبريل/نيسان، حيث شاركت إحدى عشرة فرقة مسرحية قدمت اثني عشر عملاً مسرحياً في إطار التنافس على جوائز مسابقة المهرجان التي ارتفع عددها إلى ثلاث عشرة جائزة وهي: البانيو لفرقة مسرح الاتحاد في أبوظبي، والعارضة لفرقة مسرح دبا الفجيرة، وعنتر وعبلة لفرقة مسرح دبي الأهلي، وصرخة لفرقة مسرح الشارقة الوطني، وليلة عشاء باردة جدا لفرقة مسرح الفجيرة القومي، وألف باء لفرقة مسرح رأس الخيمة الوطني، والياثوم لفرقة مسرح أم القيوين الوطني، وشما لفرقة المسرح الحديث في الشارقة، وعائشة لفرقة مسرح رأس الخيمة الوطني، وحظوظ حنظلة الحنظلي لفرقة مسرح الشارقة الوطني، وآخر ليلة باردة لفرقة مسرح دبا الحصن، وما كان لأحمد بنت سليمان لفرقة المسرح القومي للشباب في دبي.وقد اشتمل الملتقى الفكري المصاحب للأيام على محورين، كان الأول منهما عبارة عن لقاء تداولي بين مديري المهرجانات المسرحية في المنطقة العربية وكذلك لقاء تداولي بين رؤساء تحرير الدوريات العربية المعنية بالشأن المسرحي والفنون المسرحية. بينما تعلق المحور الأخير بالفوارق بين عمل الدراماتورغ والمخرج في الفن المسرحي، في مسعى إلى إزالة الالتباس الذي يحيط بالمصطلح غير العربي وتعميق فحواه التي قد ترفد التجربة المسرحية العربية بعافية جديدة باعتبار أن الدراماتورغ هو ذلك الجهد والاشتغال على العرض المسرحي من نواحي النص والمفاهيم المسرحية.وقد عقدت لجنة التحكيم التي رأستها آنذاك الفنانة نضال الأشقر سلسلة اجتماعات جرى في إثرها اعتماد النتائج النهائية للجوائز على النحو التالي:حازت مسرحية البانيو من إخراج جواد الأسدي على جائزة أفضل ماكياج مسرحي، وحازت مسرحية عبلة وعنتر من إخراج جمال مطر جائزة أفضل ملابس، ومنحت جائزة أفضل مؤثرات صوتية وموسيقية لابراهيم الأميري عن اختياراته الموسيقية لمسرحية الياثوم من إخراج أحمد الأنصاري، أما جائزة الإضاءة فحازها محمد الطريفي عن تصميمه إضاءة مسرحية ليلة عشاء باردة جدا من إخراج حكيم جاسم، وحاز الممثل عبد الله الراشد جائزة أفضل ممثل لدور ثان رجالي عن أدائه في مسرحية العارضة من إخراج محمود أبو العباس، وذهبت جائزة أفضل ممثلة لدور ثان مناصفة بين الممثلتين مريم سلطان عن أدائها في مسرحية ما كان لأحمد بنت سليمان من إخراج ناجي الحاي وعائشة عبد الرحمن عن أدائها في مسرحية عنتر وعبلة من إخراج جمال مطر، وحاز الفنان أحمد الجسمي جائزة أفضل ممثل لدور أول عن أدائه في مسرحية حظوظ حنظلة الحنظلي من إخراج قاسم محمد، فيما ذهبت جائزة أفضل ممثلة لدور أول مناصفة بين الممثلتين هدى الخطيب عن أدائها في مسرحية الياثوم من إخراج أحمد الأنصاري وبدرية أحمد عن أدائها في مسرحية ما كان لأحمد بنت سليمان، أما أفضل تأليف مسرحي فحاز جائزته الكاتب والفنان ناجي الحاي، وحاز الفنان العراقي القدير قاسم محمد جائزة أفضل فنان عربي متميز، أما جائزة أفضل إخراج فكانت من نصيب أحمد الأنصاري الذي قدم إخراج مسرحية الياثوم، وأخيرا فقد حازت مسرحية ما كان لأحمد بنت سليمان جائزة أفضل عرض مسرحي متكامل.
```

### NLI claims to label
1. بدأت فعاليات الدورة العاشرة لأيام الشارقة المسرحية في السابع والعشرين من مارس وانتهت في الخامس من أبريل
2. فاز الفنان أحمد الأنصاري بجائزة أفضل إخراج عن عمله في مسرحية الياثوم
3. حصل الممثل أحمد الجسمي على جائزة أفضل ممثل لدور أول عن أدائه في مسرحية الياثوم
4. شهدت الدورة العاشرة حضور وفود مسرحية من دول خليجية مجاورة خارج الإمارات

### English text to translate to Arabic
```
The 10th Sharjah Theatre Days, held under the patronage of His Highness Sheikh Dr. Sultan bin Muhammad Al Qasimi, Ruler of Sharjah, took place from March 27 to April 5, featuring twelve theatrical works performed by eleven troupes competing for thirteen awards. The accompanying intellectual forum addressed two main themes: deliberative meetings among Arab theater festival directors and journal editors, and a discussion on the distinctions between the roles of the dramaturg and the director in theater. The jury, chaired by artist Nidal Al-Ashqar, announced the final results, with the play 'Ma Kana li-Ahmad bint Sulayman' winning Best Integrated Performance, Ahmad Al-Ansari winning Best Director for 'Al-Yathum,' and Iraqi artist Qasim Muhammad receiving the Distinguished Arab Artist award.
```

---

## Article CULTURE_063

### Article body (Arabic)

```
القاهرة - "الخليج":أقرت لجنة المسرح في المجلس الأعلى للثقافة بمصر إنشاء مجلس أمناء للمسرح القومي وتغيير اسم "المسرح التجريبي" إلى اسم جديد هو "مهرجان القاهرة الدولي للمسرح المعاصر والتجريبي"، وذلك بعدما ظل هذا المهرجان لأكثر من عقدين على هذا الاسم .وأكد أعضاء اللجنة أن المهرجان التجريبي شكل نوعا من الحراك المسرحي المهم في مصر والعالم، وذلك لحضوره على المستوى العالمي، لافتين إلى أن المهرجان ظل طوال دوراته الماضية يؤسس لإرث ثقافي مهم من خلال كتب المهرجان والعروض المسجلة، مطالبين بضرورة تجنب الأخطاء خلال الدورة المقبلة .وناقش الحضور نوعية العروض التي ستقدم من خلال الدورة المرتقبة . ووصف د . جابر عصفور، وزير الثقافة، المسرح خلال الاجتماع بأنه "أهم روافد القوة الناعمة في مصر، فالمسارح بوجه عام تلعب دوراً أساسياً في الحراك الثقافي المصري"، مؤكداً أن المسرح القومي سيتم افتتاحه قريبا باعتباره درة المسارح في مصر .وقد وافقت اللجنة على إنشاء مجلس أمناء للمسرح القومي يتكون من كبار مثقفي وفناني مصر، ويختص ببرامج المسرح القومي، ويقوم بتحديد العروض التي ستعرض على خشبته، علاوة على كل ما يختص بالمسرح من ميزانيات .وخلال الاجتماع عرض عصفور على لجنة المسرح مراحل تطوير وترميم المسرح القومي كاملة، إيمانا منه بشفافية العمل داخل وزارة الثقافة، واستعرض مراحل الترميم والتطوير منذ الحريق الذي شب بالمسرح وحتى الآن .
```

### NLI claims to label
1. وصف وزير الثقافة جابر عصفور المسرح بأنه من أبرز روافد القوة الناعمة في مصر
2. وافقت اللجنة على تشكيل مجلس أمناء للمسرح القومي يضم نخبة من المثقفين والفنانين المصريين
3. تم تغيير اسم المهرجان التجريبي بعد مرور أكثر من ثلاثة عقود على تأسيسه
4. من المقرر أن تُقام الدورة المقبلة للمهرجان في شهر أكتوبر من العام الجاري

### English text to translate to Arabic
```
The Theater Committee of Egypt's Supreme Council of Culture approved the establishment of a board of trustees for the National Theater and renamed the 'Experimental Theater Festival' to the 'Cairo International Festival for Contemporary and Experimental Theater,' after the festival had carried its original name for over two decades. Egypt's Minister of Culture, Dr. Gaber Asfour, described theater as one of the most important tributaries of Egypt's soft power and confirmed that the National Theater would be reopened soon. During the meeting, Asfour also presented the full stages of the National Theater's renovation and restoration since the fire that had struck it.
```

---

## Article CULTURE_073

### Article body (Arabic)

```
خورفكان: «الخليج»اختتمت مساء أمس الأول في المركز الثقافي في خورفكان فعاليات مهرجان الشارقة للشعر الشعبي في دورته الثالثة عشرة بأمسية شارك فيها الشعراء فلاح بن ذروة الهاجري (الكويت)، وطلال النشير (قطر)، وسعيد آل هطلا(السعودية)، وأدارها الإعلامي معجب جابر ومحمد بن قذلة الأحبابي (الإمارات)، وقدمت فرقة الفنون الشعبية «الحربية» مجموعة من الأغاني الحماسية، حضر الأمسية الشيخ سعيد بن صقر القاسمي نائب رئيس مكتب سمو الحاكم في خورفكان وراشد شرار مدير المهرجان.قرأ فلاح بن ذروة الهاجري قصائد متنوعة، منها قصيدة «يا كاتب التاريخ» التي قرأ منها: «يا كاتب التاريخ انحت حضارات/ نهضة وبيبان الفخر طارقتها/ أبو ظبي تزهى بنور الإمارات/ بدبيّها وعجمانها وشارقتها»، وعلى مثل هذا المنوال ظلّ هذا الشاعر ينحت قصائده بتحدٍ وثقة وهدوء وسط تفاعل الجمهور. الشاعر محمد بن قذلة أبدع صوراً فنية متطرقاً إلى مواضيع جديدة لفتت حضوره، وفي قصيدة «غدير من سرابي»، يقول: «أرى الأيام ما هي حسب ظني/ أحاسبها ولا تحسب حسابي/ تذكرني بشطرٍ مذهلني/ تصور لك غديرٍ من سرابي/ أنا عنّيت من كثر التمني/ ومن كثر الأماني يا عذابي». الشاعر طلال النشير امتازت قصائده بالفكرة اللماحة والذائقة العالية مجدداً في صوره بصفته أحد فرسان شاعر المليون في موسمه السابع، ومن قصيدة «يا غناتي» قرأ النشير: «صارحيني بكل شيٍّ في نهايات الطريق/ واعذريني بكل جرحٍ دام قلت المعذرة/ كنتي أغلى من طموح السير في عين العويق/ وما رحلتي من حياتي لين صارت بعثرة/ ما به اقسى من طعونك كون طعنات الرفيق/ وما به أوضح من غموضك كون صدق المحبرة».أما سعيد آل هطلا، فقد بدت عليه الثقة بمقطوعات ذكية ومختارة، وذات جزالة، حيث قرأ قصائد لافتة، منها «حياة القلوب» التي قال فيها: «أنا بخير ياللي خيرك إن جا يجي بعدين/ ماني بناقص من يدينك إلا سلامتها/ معي وجه واحد ما اقدر أتصور بوجهين/ ولو حاجتي بتموت من كثر حاجتها/ إذا عاد قلبك حي وتشوف بالثنتين/ ترى أغلى من النفس العزيزة كرامتها».
```

### NLI claims to label
1. شارك الشاعر طلال النشير القادم من قطر في الأمسية الختامية لمهرجان الشارقة للشعر الشعبي
2. أقيمت فعاليات الأمسية الختامية للمهرجان في المركز الثقافي بمدينة خورفكان
3. كان طلال النشير أحد فرسان برنامج شاعر المليون في موسمه الثامن
4. تم تكريم الشعراء المشاركين في الأمسية الختامية بجوائز مالية من إدارة المهرجان

### English text to translate to Arabic
```
The thirteenth edition of the Sharjah Festival for Popular Poetry concluded at the Cultural Center in Khorfakkan, featuring an evening of performances by poets from Kuwait, Qatar, Saudi Arabia, and the UAE, along with traditional folk songs by the Al-Harbiya troupe. The event was attended by Sheikh Saeed bin Saqr Al Qasimi, Deputy Head of the Ruler's Office in Khorfakkan, and festival director Rashid Sharar, and was moderated by media professionals Moajab Jaber and Mohammed bin Qathla Al Ahbabi. The participating poets — Falah bin Tharwa Al Hajri, Talal Al Nashir, Saeed Al Hatla, and Mohammed bin Qathla — presented diverse poems covering themes of civilization, love, longing, and dignity, drawing enthusiastic audience engagement.
```

---

## Article CULTURE_085

### Article body (Arabic)

```
يرث الناس من أصولهم الكثير من الأشياء مثل المال والعقارات إضافة إلى الصفات والخصائص الجسدية وحتى الأمراض، وتتوارث الأجيال الثقافة كذلك بحكم التنشئة والتفكير والبيئة التي يعيشون فيها . ولا شك بأن الميراث يختلف من عصر إلى عصر ومن زمن إلى زمن في ما يتعلق بالمال أو الثقافة ومتغيراتهم، ويمكن أن يتغير بشكل أقل في ما يخص الصفات الجسمانية والمرضية مع اختلاط الأنساب والانفتاح على المجتمعات الأخرى للتزاوج منها .أما عن الثقافة، فهي تعتبر جزءاً مهماً من الميراث، وتعني الكثير فيه، بل ربما هي أصل تطور الإنسان ونجاحه وما يحظى به من تعليم ومناصب مستقبلاً، على الرغم من عدم التفات الكثير لها أو طغيان مفهوم الميراث المادي على ساحة تفكير الإنسان في هذه الأزمنة، ومع ذلك فإن مفهوم الميراث الثقافي يحتاج إلى أن يتم تعزيزه، بشكل أو بآخر وعبر أكثر من وسيلة وأداة، من منطلق كونه الجزء المهم من الهوية الوطنية الثقافية لكل دولة ولكل جيل .إضافة إلى كون الميراث الثقافي هو الأصل في نمو الدول وفي قدرتها على الوقوف في محاذاة البلدان المتقدمة، من خلال مفاهيم ومبادئ وقيم، تسهم في صقل الشخصية، وتساعد على بناء إنسان ملتزم قادر على التفكير واثق من ذاته، ويعرف تماماً ماهي الخطوة المقبلة باتجاه الهدف والحياة .وبما أن الميراث الثقافي يتضمن اللغة المحكية ليست فقط بحروفها، ولكن بأساليب التعبير والألفاظ التي يتداولها الشخص بناء على محفوظاته السابقة، ويجمع المبادئ والقيم التي يتربى عليها الطفل في بيته وبيئته من أساليب التعامل مع الآخرين وطرق التواصل مع الغير بدءاً من التواصل مع الزملاء في المدرسة، وانتهاء إلى كيفية التعامل مع الزوج أو الزوجة في بيت الزوجية، وصولاً إلى العادات والممارسات الأخرى المتبعة في بيته وبيئته ليمارسها تماماً كما كان يفعل والداه أو أجداده، فهو أكبر حجماً وتأثيراً من الميراث المادي، ويعول عليه لأجل مستقبل هادف ومتطور فكرياً وإنسانياً .وفي جعبة الذاكرة أكثر من نموذج حول تعلق أغلب المثقفين بالكتاب وتثقيف الذات من خلال المكتبات المنزلية التي توارثوها من أجدادهم أو حتى من خلال الجلسات الاجتماعية التي كانت تقام في الصالونات وتدور فيها الحوارات حول أهم القضايا المجتمعية والسياسية والثقافية وغيرها مما يؤثر تأثيراً كبيراً في مفاهيم الطفل، ويزرع في أعماقه التوجهات الفكرية والثقافية التي يتطلع للسير عليها مستقبلاً .إن الثقافة التي تصل إلى الأجيال الجديدة، حتى لو كانت ثقافة مختلفة عن الأخرى التي عاشها آباؤهم وأجدادهم بحكم التغيرات الزمنية، لا تأتيهم بمعزل عن المجتمع أو عن العادات والممارسات المتداولة فيه وبين أسرهم وبقية الأشخاص المتعاملين معهم، ولا تصل إليهم من الفضاء الخارجي، وإن كانت الوسائل الإعلامية ذات تأثير كبير فيهم، لكن الثقافة الإنسانية والمجتمعية المتداولة بشكل يومي وممارسات طبيعية، هي بدورها ذات تأثير جذري في تشكيل الشخصية ومفاهيمها، وفي الترويج للقيم الثقافية التي تقولب الأجيال الشابة اعتماداً عليها .
```

### NLI claims to label
1. يُعد الميراث الثقافي عنصراً جوهرياً في تشكيل الهوية الوطنية لكل بلد ولكل جيل من الأجيال
2. كثير من المثقفين ارتبطوا بالقراءة وتطوير أنفسهم عبر المكتبات البيتية الموروثة والجلسات الحوارية في الصالونات الاجتماعية
3. يرى المقال أن الميراث المادي أعظم أثراً وأكبر حجماً من الميراث الثقافي في حياة الإنسان
4. أجرت منظمة اليونسكو دراسة حديثة تؤكد تراجع الاهتمام بالميراث الثقافي في الدول العربية

### English text to translate to Arabic
```
The article discusses how cultural inheritance, encompassing language, values, principles, and social practices, is passed down through generations and is arguably more influential than material inheritance in shaping individuals' identities, intellectual growth, and national development. It highlights that many intellectuals trace their passion for knowledge to home libraries and social salons inherited from their ancestors, where discussions on societal, political, and cultural issues profoundly shaped children's intellectual orientations. The article emphasizes that even though new generations live in different times with evolving media influences, the daily cultural and social practices within families and communities remain the most fundamental force in forming personalities and promoting cultural values among youth.
```

---
