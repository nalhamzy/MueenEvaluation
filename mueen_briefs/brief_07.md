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


## Article SPORTS_064

### Article body (Arabic)

```
خسر منتخب مصر للناشئين ، بهدف نظيف أمام الجزائر فى المباراة التى جرت اليوم فى ختام التصفيات المؤهلة لأمم أفريقيا للناشئين ، وجاء هدف منتخب الجزائر بتوقيع لاعبه عبدالرحمن زاوى فى الدقيقة 49.

كان منتخب مصر ضمن التأهل للنهائيات منذ الجولة السابقة بعد فوزه على المنتخب الليبي (2 – 1) حيث رفع رصيده إلى 6 نقاط بعد أن سبق له الفوز على تونس (1 – 1) ثم الخسارة أمام المغرب (1 – 2).

وأعلن حسين عبد اللطيف المدير الفني لمنتخب مصر للناشئين عن التشكيل الأساسي لمواجهة نظيره الجزائري على ملعب شهداء بنينا بمدينة بنغازي الليبية ويُديرها طاقم تونسي يقوده فرج عبد اللاوي، ضمن منافسات الجولة الختامية لتصفيات شمال أفريقيا (أوناف)، المؤهلة لكأس الأمم الأفريقية تحت 17 عاماً.

مالك عمرو (16) – ياسين تامر (4) - عادل علاء (6) - آدم يوسف (3)  - محمد جمال (7) - أحمد بشير (25) - عمر فودة (21) - أحمد صفوت (10) - عبد الله عمرو (20) - يوسف عثمان (13) – عبد العزيز خالد "إيفونا" (17).

ويجلس على دكة البدلاء كلاً من: محمد عبيد (1) - سيف تامر (5) – عاصم البيلي (8) - أحمد محروس "ميدو" (14) - عمر عبد الرحيم (15) - سيف كريم (18) – خالد مختار (19) – دانيال تامر "داني" (11) - زياد سعودي (24) .

طاقم حكام تونسى

أدار المباراة تحكيميا التونسي فرج عبدلاوي حكما للساحة، ويعاونه كلا من الليبي حسن التومي مساعد أول ، والتونسي ياسين السعداوي مساعد ثان، والمغربي هشام التمسماني حكما رابعا.
```

### NLI claims to label
1. سجل عبدالرحمن زاوى هدف الجزائر في الشوط الثاني من المباراة أمام مصر
2. أقيمت المباراة بين مصر والجزائر على ملعب شهداء بنينا في مدينة بنغازي
3. تأهل منتخب مصر للناشئين للنهائيات بعد تغلبه على ليبيا بنتيجة ثلاثة أهداف مقابل هدف
4. شهدت المباراة حضور جماهيري كبير من المشجعين المصريين والجزائريين في الملعب

### English text to translate to Arabic
```
Egypt's U-17 national team lost 1-0 to Algeria in the final round of the North African qualifiers for the African Cup of Nations for juniors, with Abdelrahman Zaoui scoring the only goal in the 49th minute. Egypt had already secured qualification in the previous round after beating Libya 2-1, bringing their tally to 6 points following earlier results against Tunisia and Morocco. The match was held at the Shuhada Benina Stadium in Benghazi, Libya, and was officiated by a Tunisian-led refereeing crew headed by Faraj Abdelaoui.
```

---

## Article SPORTS_013

### Article body (Arabic)

```
قدم تليفزيون اليوم السابع تغطية رياضية جديدة لمتابعة قضية أحمد سيد زيزو لاعب الأهلي الحالي مع ناديه السابق الزمالك.
	وتناول الزميل أحمد العدل تطورات جديدة في الأزمة حيث كشف عن وجود وسطات للصلح وإنهاء الأزمة وديا، على أن يتم التنازل عن الشكوي مقابل اصدار نادي الزمالك بيانا للتأكيد على احترام زيزو وتقديره لاسيما وان الأخير كان غاضبا من هجوم الجماهير البيضاء عليه وتصريحات مسئولو النادي ضده.

وشملت التغطية رد زيزو على هذه المبادرة حيث اصر على موقفه في استكمال القضية ضد الزمالك والحصول على المستحقات التي يطالب بها والتي تقدر بـ 83 مليون.

نادي الزمالك من جانبه رفض الصمت تجاه هذه التحركات لاسيما بعد التسريبات الأخيرة التي تؤكد أن الحكم في القضية سيكون لصالح اللاعب ، حيث تواصل مسئولو الزمالك مع مجلس إدارة اتحاد الكرة لإبلاغهم تحفظهم على هذه التسريبات والتأكيد على أن فريق الكرة متصدر المسابقة والنادي حاليا لا يتحمل اى أزمات جديدة خصؤصا وان المستشار القانوني للنادي تقدم بمستندات تدعم الموقف الأبيض في القضية.

وكان الزمالك قد تقدم بشكوى رسمية ضد اللاعب بسبب انقطاعه عن تدريبات ومباريات الفريق في توقيت حرج، وهو ما اعتبره النادي إخلالًا بالتزاماته التعاقدية، خاصة في ظل المنافسات المهمة التي كان يخوضها الفريق، وفي المقابل، تقدم زيزو بشكوى مضادة يطالب خلالها بالحصول على مستحقاته المالية المتأخرة، والتي تقدر بنحو 83 مليون جنيه.
```

### NLI claims to label
1. أصر زيزو على المضي قدماً في القضية ضد الزمالك والمطالبة بمستحقاته المالية المقدرة بـ 83 مليون جنيه
2. تواصل مسؤولو نادي الزمالك مع اتحاد الكرة للتعبير عن اعتراضهم على التسريبات التي تشير إلى صدور حكم لصالح اللاعب
3. تقدم نادي الأهلي بشكوى رسمية ضد زيزو بسبب تغيبه عن التدريبات والمباريات
4. تدخل اتحاد الكرة المصري بشكل مباشر لحل الأزمة بين زيزو ونادي الزمالك

### English text to translate to Arabic
```
Al-Ahly player Ahmed Sayed 'Zizo' is embroiled in an ongoing legal dispute with his former club Zamalek, with mediation efforts to settle the case amicably failing after Zizo insisted on pursuing his claim for 83 million Egyptian pounds in unpaid dues. Zamalek officials contacted the Egyptian Football Association board to express their objections to recent leaks suggesting the ruling would favor the player, emphasizing that the club's legal team has submitted supporting documents. The dispute originated when Zamalek filed a complaint against Zizo for missing training sessions and matches, while Zizo countered with a claim for his outstanding financial dues.
```

---

## Article SPORTS_065

### Article body (Arabic)

```
شهدت الرياضة المصرية اليوم الأحد 5 إبريل 2026 العديد من الأخبار الرياضية المهمة وأبرزها، الأهلي يكشف أسباب رفض عودة حمدى فتحى فى الميركاتو الصيفى لخلافة ديانج،منتخب مصر يحدد 29 مايو لخوض مباراة ودية بالقاهرة قبل السفر لأمريكا.

منتخب مصر يحدد 29 مايو لخوض مباراة ودية بالقاهرة قبل السفر لأمريكا

حدد الجهاز الفنى لمنتخب مصر بقيادة حسام حسن 29 مايو المقبل لخوض مباراة ودية باستاد العاصمة الجديدة، قبل السفر لأمريكا استعداداً لخوض منافسات كأس العالم 2026.

الأهلي يكشف أسباب رفض عودة حمدى فتحى فى الميركاتو الصيفى لخلافة ديانج

كشف مسئولو النادى الأهلى أسباب رفضهم فكرة عودة حمدى فتحى ، لاعب خط وسط الوكرة القطري، لتدعيم صفوف المارد الأحمر فى فترة الانتقالات الصيفية، لتعويض رحيل المالى أليو ديانج لاعب وسط الفريق الذى ينتهى تعاقده بنهاية الموسم الجاري، ووقع لصفوف فالنسيا الإسبانى.

هنا جودة تصل القاهرة بعد إنجازها التاريخي فى كأس العالم لتنس الطاولة

استقبل وزير الشباب والرياضة لاعبة المنتخب المصري لتنس الطاولة هنا جودة، وذلك بحضور رئيس الاتحاد، المصري لتنس الطاولة اللواء أشرف حلمي عقب تحقيقها إنجازًا تاريخيًا بالتأهل إلى الدور ربع النهائي لبطولة كأس العالم للسيدات لتنس الطاولة بالصين.

اتحاد الكرة يجهز اجتماعاً مع الأندية لحسم شكل المسابقات الموسم المقبل

يجهز اتحاد الكرة برئاسة هاني أبوريدة لعقد اجتماع مع أندية القسمين الثاني والثالث لمناقشة شكل المسابقات فى الموسم الجديد.

محمد شحاتة يتصدر قائمة غيابات الزمالك أمام المصري فى الدوري الليلة

يواجه فريق الكرة الأول بنادي الزمالك تحدياً قوياً بسبب الغيابات، وذلك عندما يلتقي المصري في المباراة التي تجمع الفريقين ضمن منافسات الجولة الأولى من الدور الثاني بمجموعة التتويج ببطولة دوري نايل ، حيث يبحث كل منهما عن حصد ثلاث نقاط ثمينة في مستهل مشواره بالدور الثاني من الدوري.

اتحاد الكرة يوافق على سفر إسلام عيسى لألمانيا لإجراء جراحة الصليبى

وافق اتحاد الكرة على سفر إسلام عيسى، لاعب نادى سيراميكا ومنتخب مصر، إلى ألمانيا لإجراء جراحة الرباط الصليبى، بالتنسيق مع الجهاز الطبى لمنتخب مصر.

آخر تطورات عودة رضا سليم للأهلي فى الميركاتو الصيفى

أكد مصدر في الأهلي أن المغربي رضا سليم ، لاعب الفريق المُعار لنادي الجيش الملكي المغربي، لن يعود للقلعة الحمراء الصيف المقبل، موضحاً أن هناك اتفاقاً على عدم عودة اللاعب المغربي للفريق.
```

### NLI claims to label
1. حدد الجهاز الفني للمنتخب المصري بقيادة حسام حسن إقامة مباراة ودية في استاد العاصمة الجديدة يوم 29 مايو تحضيراً لكأس العالم في أمريكا
2. وافق اتحاد الكرة المصري على انتقال إسلام عيسى لاعب سيراميكا إلى ألمانيا من أجل الخضوع لعملية جراحية في الرباط الصليبي
3. حققت هنا جودة إنجازاً تاريخياً بوصولها إلى الدور نصف النهائي في بطولة كأس العالم لتنس الطاولة للسيدات بالصين
4. يخطط اتحاد الكرة المصري لتعديل نظام الهبوط في الدوري الممتاز ضمن مناقشات شكل المسابقات للموسم القادم

### English text to translate to Arabic
```
On Sunday, April 5, 2026, Egypt's national football team, led by coach Hossam Hassan, scheduled a friendly match on May 29 at the New Administrative Capital Stadium before traveling to the United States to participate in the 2026 FIFA World Cup. Al-Ahly Club revealed the reasons behind rejecting the return of midfielder Hamdi Fathi from Qatar's Al Wakrah to replace Malian player Aliou Dieng, who signed with Spain's Valencia after his contract expires at the end of the current season. Additionally, the Egyptian Football Association approved the travel of Ceramica and national team player Islam Issa to Germany to undergo ACL surgery, while table tennis player Hana Goda was received by the Minister of Youth and Sports after her historic qualification to the quarterfinals of the Women's Table Tennis World Cup in China.
```

---

## Article SPORTS_014

### Article body (Arabic)

```
قررت الجهات المختصة، إخلاء سبيل 9 متهمين بضمان محل الإقامة احتياطياً علي ذمة التحقيقات التي تجري معهم بمعرفة النيابة العامة في عدد من القضايا المختلفة المتعلقة باتهامهم ببث أخبار كاذبة، وإساءة استخدام مواقع التواصل الاجتماعي .

وجاء ضمن المتهمين المخلي سبيلهم، كل من سيد مشاغب وشريف الروبي ونرمين حسين وسامي عبد الجواد وأحمد عزام وسامي الجندي.

وكانت أسندت النيابة العامة إليهم اتهامات بالاشتراك مع جماعة أنشئت على خلاف أحكام القانون الغرض منها الدعوة إلى تعطيل أحكام الدستور والقوانين ومنع مؤسسات الدولة والسلطات العامة من ممارسة أعمالها، ونشر أخبار ومعلومات وبيانات كاذبة - على نحو متعمد - عن الأوضاع السياسية والاقتصادية بالبلاد بقصد تكدير السلم العام وزعزعة الثقة في مؤسسات الدولة.

وكانت نيابة أمن الدولة العليا قد باشرت التحقيق مع المتهمين بالقضية في حضور عدد من المحامين الموكلين عنهم، وذلك في ضوء التحريات التي أجرتها أجهزة الأمن، والتي جاء بها ارتكابهم للجرائم موضوع الاتهامات، بعدما وجهت إليهم تهم نشر أخبار كاذبة عن الأوضاع السياسية والاقتصادية بالبلاد بقصد تكدير السلم العام في إطار أهداف جماعة الإخوان الإرهابية، والترويج لأغراض الجماعة التي تستهدف زعزعة الثقة في الدولة المصرية ومؤسساتها، والترويج لأغراض الجماعة التي تستهدف زعزعة الثقة في الدولة المصرية ومؤسساتها، ومشاركة جماعة ارهابية في تحقيق أهدافها، والاشتراك فى اتفاق جنائي، والتجمهر واستخدام حسابات خاصة علي شبكة المعلومات الدولية بهدف ارتكاب جريمة معاقب عليها في القانون بهدف الاخلال بالنظام العام.
```

### NLI claims to label
1. تم الإفراج عن تسعة متهمين بضمان محل إقامتهم بشكل احتياطي أثناء استمرار التحقيقات معهم
2. من بين الأشخاص الذين أُخلي سبيلهم سيد مشاغب وشريف الروبي ونرمين حسين
3. تولت نيابة أمن الدولة العليا التحقيق مع المتهمين دون حضور أي محامين
4. صدر قرار الإخلاء بناءً على طلب رسمي من منظمات حقوق الإنسان المحلية والدولية

### English text to translate to Arabic
```
Egyptian authorities decided to release nine defendants on bail, contingent on their place of residence, pending ongoing investigations by the Public Prosecution into charges of spreading false news and misusing social media platforms. Among those released were Sayed Moshagheb, Sherif El-Rouby, Nermeen Hussein, Sami Abdel-Gawad, Ahmed Azzam, and Sami El-Gendy. The defendants had been charged by the Supreme State Security Prosecution with participating in an unlawful organization, deliberately spreading false information about the country's political and economic conditions to disturb public peace, and promoting the goals of the Muslim Brotherhood, which is designated as a terrorist organization in Egypt.
```

---

## Article SPORTS_023

### Article body (Arabic)

```
تُختتم منافسات الجولة الثانية من الدور الثاني بمجموعة الهبوط في الدوري المصري، اليوم الإثنين، بمواجهة مرتقبة تجمع بين زد والمقاولون العرب في الساعة الثامنة مساءً باستاد القاهرة الدولي، فى لقاء يحمل أهمية كبيرة للفريقين في صراع البقاء.

ويدخل فريق زد المباراة بطموح تحقيق نتيجة إيجابية تعزز من موقفه في جدول ترتيب مجموعة الهبوط، خاصة أنه يتصدر جدول ترتيب مجموعة الهبوط برصيد 32 نقطة ، ويسعى الجهاز الفني للفريق إلى استغلال حالة التركيز لدى لاعبيه من أجل فرض السيطرة على مجريات اللقاء وتحقيق فوز يمنحه دفعة قوية في مشواره.

وفي المقابل، يطمح المقاولون العرب إلى الخروج بنتيجة إيجابية، سواء بالفوز أو التعادل على أقل تقدير، من أجل الحفاظ على حظوظه في الابتعاد عن مراكز الهبوط ، حيث يحتل الفريق المركز العاشر برصيد 19 نقطة ، ويعتمد الفريق على خبرة لاعبيه في مثل هذه المواقف الصعبة، بالإضافة إلى التنظيم الدفاعي الجيد واللعب على الهجمات المرتدة.

وتضم المجموعة الثانية المتنافسة على البقاء في مسابقة الدوري 14 فريقاً بداية من المركز الثامن وحتى الـ 21 وهم على الترتيب: زد ـ وادي دجلة ـ الجونة ـ البنك الأهلي ـ بتروجت ـ مودرن سبورت ـ طلائع الجيش ـ الاتحاد السكندري ـ غزل المحلة ـ المقاولون العرب ـ حرس الحدود ـ كهرباء الإسماعيلية ـ فاركو ـ  والإسماعيلي.
```

### NLI claims to label
1. يتواجد فريق زد في صدارة ترتيب مجموعة الهبوط بـ 32 نقطة
2. تضم مجموعة الهبوط في الدوري المصري أربعة عشر نادياً تتنافس على البقاء
3. يحتل المقاولون العرب المركز الحادي عشر في مجموعة الهبوط برصيد 19 نقطة
4. سبق لفريق زد أن فاز على المقاولون العرب في مباراة الدور الأول من البطولة

### English text to translate to Arabic
```
The second round of the relegation group in the Egyptian Premier League concludes on Monday with a crucial match between ZED FC and Al-Mokawloon Al-Arab at Cairo International Stadium at 8 PM, as both teams fight to secure their survival. ZED FC enters the match at the top of the relegation group standings with 32 points, aiming to strengthen their position, while Al-Mokawloon Al-Arab sit in tenth place with 19 points and seek at least a draw to distance themselves from the relegation zone. The relegation group comprises 14 teams ranked from 8th to 21st in the league, including teams such as Wadi Degla, El Gouna, Al-Ittihad Al-Sakandary, and Al-Ismaily.
```

---

## Article SPORTS_048

### Article body (Arabic)

```
انتهى الشوط الأول بتقدم الزمالك بنتيجة 2 - 1 أمام المصرى، فى المباراة التي تجمعهما حاليًا على استاد برج العرب، في الجولة الأولى من المرحلة النهائية لحسم لقب الدوري.

سجل أسامة زمراوي هدف التقدم للمصري فى شباك الزمالك، بالدقيقة 12 من عمر المباراة، ثم نجح عدى الدباغ فى تسجيل هدف التعادل بعد صناعة من خوان بيزيرا فى الدقيقة 30، وسجل ناصر منسى الهدف الثاني للزمالك فى الدقيقة 44.

ـ حراسة المرمى : مهدي سليمان.

ـ خط الدفاع: محمود بنتايج – حسام عبد المجيد – محمد إسماعيل – عمر جابر.

ـ خط الوسط : أحمد ربيع – أحمد فتوح – عبد الله السعيد.

ـ خط الهجوم : خوان بيزيرا – ناصر منسي – عدي الدباغ.

ويتواجد على مقاعد البدلاء، محمد عواد ومحمود حمدي "الونش" ومحمد ابراهيم وأحمد عبد الرحيم "إيشو" ومحمود جهاد وآدم كايد وأحمد شريف وعمرو ناصر وسيف الجزيري.

-حراسة المرمى: عصام ثروت.

-خط الظهر: كريم العراقي، باهر المحمدي، خالد صبحي، مصطفى العش، أحمد أيمن منصور.

-خط الوسط: محمد مخلوف، محمود حمادة، أسامة زمراوي.

-الهجوم: منذر طمين، صلاح محسن.

البدلاء: محمد شحاته لحراسة المرمى، محمد الشامي، كريم بامبو، ميدو جابر، عمر الساعي، بونور موجيشا، مصطفى زيدان، عميد صوافطة، أحمد القرموطي.

ويتصدر نادي الزمالك جدول ترتيب المجموعة برصيد 43 نقطة، متساويًا مع بيراميدز صاحب المركز الثاني، لكن بفارق الأهداف لصالح الأبيض، ما يزيد من حدة المنافسة بين الفريقين.

ويأتي الأهلي في المركز الثالث برصيد 40 نقطة، ليبقى ضمن دائرة المنافسة بقوة، فيما يحتل سيراميكا المركز الرابع برصيد 38 نقطة.

وفي المراكز التالية، يتواجد المصري البورسعيدي في المركز الخامس برصيد 32 نقطة، يليه سموحة في المركز السادس بـ31 نقطة، ثم إنبي في المركز السابع برصيد 30 نقطة.
```

### NLI claims to label
1. سجل عدي الدباغ هدف التعادل للزمالك في الدقيقة الثلاثين بتمريرة من خوان بيزيرا
2. يحتل النادي الأهلي المرتبة الثالثة في جدول الترتيب بأربعين نقطة
3. افتتح أسامة زمراوي التسجيل لصالح المصري في الدقيقة العشرين من المباراة
4. شهدت المباراة حضور جماهيري كبير في استاد برج العرب

### English text to translate to Arabic
```
Zamalek took a 2-1 lead over Al-Masry at the end of the first half in their match at Borg El Arab Stadium, part of the opening round of the Egyptian league's final stage to decide the title. Osama Zamrawy opened the scoring for Al-Masry in the 12th minute, before Adi Al-Dabbagh equalized for Zamalek in the 30th minute and Nasser Mansi added a second in the 44th minute. Zamalek currently top the group standings with 43 points, level with Pyramids on points but ahead on goal difference, while Al-Ahly sit third with 40 points.
```

---

## Article SPORTS_001

### Article body (Arabic)

```
عاد اسم المرشد الأعلى في إيران مجتبى خامنئي للساحة السياسية من جديدة، بعد أن انتشر له فيديو بشكل كبير على وسائل التواصل الاجتماعي، وهو يدخل غرفة عمليات عسكرية محصنة وتظهر صورة مفعل ديمونة النووي الإسرائيلي.

وتظهر في خلفية المشهد الذى ظهر فيه المرشد الأعلى في إيران ، خريطة لمفاعل ديمونة الإسرائيلي مثبتة على الجدار الرئيسي داخل غرفة العمليات، في إشارة توحي بالاستعداد لاستهداف المفاعل، وهو ما عزز من انتشار الفيديو وتداوُله بوصفه مؤشرا على تصعيد عسكري محتمَل.

لكن بالفحص والتدقيق تشير إلى أن فيديو المرشد الأعلى في إيران مصنوع بالذكاء الاصطناعي، حيث تظهر التحولات الدرامية، التشويش على الخلفيات، والتأثيرات البصرية (مثل الوهج والانحناء) علامات واضحة على أدوات AI مثل Runway أو مشابهة.

كما لا توجد أي مصادر إعلامية موثوقة أو رسمية إيرانية تؤكده كلقطات حقيقية من غرفة حرب، وهو يتناسب مع حملة الدعاية الإيرانية التي تستخدم فيديوهات AI في الصراع الحالي.

وقال المرشد الأعلى في إيران مجتبى خامنئي إن خصوم إيران أخطأوا التقدير عندما ظنوا أن الشعب سيسقط النظام خلال أيام، مؤكدًا أن الحرب اندلعت بعد يأس "العدو" من تحرك داخلي لصالحه. وأضاف في رسالة بمناسبة عيد النيروز أن إيران واجهت ثلاث حروب خلال العام الماضي، معتبرًا أن الجبهة الداخلية أقوى مما يتصوره الخصوم، وأن الشعب شكّل "حصنًا منيعًا" ووجّه ضربات قوية.

وقد دعا المرشد الإيراني مجتبى خامنئي، في رسالة بمناسبة يوم الجمهورية الإسلامية، الشعب الإيراني إلى غرس الأشجار إحياءً لذكرى شهداء الحرب.

وتحمل الدعوة أبعاداً رمزية تجمع بين إحياء ذكرى الضحايا وتعزيز الوعي البيئي، في سياق رسائل داخلية تعكس التلاحم الوطني.

و تولي مجتبى خامنئي منصب المرشد الأعلى في إيران خلفا لوالده علي خامنئي، الذي قُتل في الهجوم الإسرائيلي الأمريكي على طهران يوم السبت 28 فبراير الماضي.

ويعد مجتبى خامنئي المرشد الأعلى في إيران  -المولود عام 1969- الابن الثاني للمرشد الراحل، ومن أبرز الشخصيات النافذة داخل الدوائر الضيقة المحيطة بمركز القرار في إيران.

وفي سياق تطورات الحرب خلال مارس 2026، أفادت مصادر إيرانية بأن مجتبى خامنئي نجا من الغارات الجوية الأمريكية والإسرائيلية التي استهدفت والده، وأسفرت عن مقتل عدد من أفراد عائلته ومسؤولين عسكريين، دون صدور تأكيد رسمي مستقل بشأن تلك المعطيات.

وتدخل الحرب الأمريكية الإسرائيلية المشتركة ضد إيران يومها الـ38 على التوالي، حيث يتواصل القصف المتبادل بين أطراف الصراع، وسط حديث عن مساعٍ حثيثة لوقف مؤقت لإطلاق النار قد يفضي إلى إنهاء الحرب، في الوقت الذي ظهرت فيه مساع حثيثة لوقف مؤقت لإطلاق النار قد يفضي لإنهاء الحرب؛ حيث قال مصدر ⁠مطلع لوكالة رويترز؛  إن إيران والولايات المتحدة تلقتا ⁠خطة لإنهاء الأعمال القتالية ربما تدخل ⁠حيز التنفيذ خلال ساعات وتؤدي إلى إعادة فتح مضيق هرمز.

وأضاف المصدر أن ‌باكستان أعدت إطارا لإنهاء القتال وتم تسليمه لإيران والولايات المتحدة، موضحا أنه يقوم على ⁠نهج من مرحلتين، ⁠ويبدأ بوقف فوري لإطلاق النار تعقبه اتفاقية شاملة.

وكشف المصدر أن مقترح الاتفاق النهائي يتضمن تخلي إيران عن الأسلحة النووية ورفع العقوبات والإفراج عن أصولها، موضحا أن الخطة ستقود لوقف فوري لإطلاق النار وفتح مضيق هرمز، ثم يتم التوصل لاتفاق نهائي خلال 15 إلى 20 يوما.

وفى السياق نفسه قالت مصادر أمريكية وإسرائيلية أن واشنطن وطهران ووسطاء إقليميين يبحثون وقف إطلاق نار محتملا لمدة 45 يوما قد يفضي لإنهاء دائم للحرب، وفق موقع أكسيوس.

من غرفة الحرب السيد مجتبى خامنئي . pic.twitter.com/ZeuUOQrFqe
```

### NLI claims to label
1. تبيّن أن مقطع الفيديو المنتشر لمجتبى خامنئي داخل غرفة عمليات عسكرية تم إنتاجه باستخدام تقنيات الذكاء الاصطناعي
2. أعدّت باكستان خطة من مرحلتين لإنهاء القتال بين إيران والولايات المتحدة تبدأ بوقف فوري لإطلاق النار ثم اتفاقية شاملة
3. قُتل علي خامنئي في الهجوم الإسرائيلي الأمريكي على طهران يوم الجمعة الثامن والعشرين من فبراير
4. أعلنت الحكومة الإيرانية رسمياً عن حجم الخسائر المادية الناجمة عن الغارات الأمريكية والإسرائيلية على طهران

### English text to translate to Arabic
```
A video widely circulated on social media appeared to show Iran's new Supreme Leader Mojtaba Khamenei entering a fortified military operations room with a map of Israel's Dimona nuclear reactor on the wall, but analysis indicated the video was fabricated using artificial intelligence tools. Mojtaba Khamenei, who assumed the position of Supreme Leader after his father Ali Khamenei was killed in a joint US-Israeli strike on Tehran on February 28, stated that Iran's adversaries miscalculated in believing the Iranian people would topple the regime, and called on citizens to plant trees in memory of war martyrs. As the joint US-Israeli war against Iran entered its 38th day with ongoing mutual bombardment, reports emerged that Pakistan had prepared a two-phase framework for ending hostilities, beginning with an immediate ceasefire and the reopening of the Strait of Hormuz, followed by a comprehensive agreement involving Iran's renunciation of nuclear weapons and the lifting of sanctions.
```

---

## Article SPORTS_058

### Article body (Arabic)

```
تصل بعثة المنتخب الجزائري لكرة الصالات إلى القاهرة يوم التاسع من أبريل الجاري، وذلك تمهيداً لخوض مواجهتين وديتين أمام المنتخب الوطني المصري.

وتأتي هذه الزيارة فى إطار التعاون الرياضي بين الاتحادين، حيث يسعى الجانب الجزائري للدخول فى أجواء المنافسة مبكراً قبل انطلاق الاستحقاقات القارية، وسط ترتيبات إدارية رفيعة المستوى لضمان توفير كافة سبل الراحة للبعثة الشقيقة منذ لحظة وصولها وحتى موعد المغادرة.

ويستعد المنتخب الوطني لكرة الصالات لخوض المباراتين الوديتين يومي 12 و14 أبريل الحالي، ومن المقرر أن تستضيف صالة الدكتور حسن مصطفى بمدينة السادس من أكتوبر هاتين المواجهتين المرتقبتين.

وتأتي هذه الوديات ضمن البرنامج الإعدادي المكثف الذي وضعه الجهاز الفني للفراعنة بقيادة الكابتن نادر رشاد، لرفع الجاهزية الفنية والبدنية للاعبين قبل التوجه إلى المغرب للمشاركة في نهائيات كأس أمم أفريقيا، وهو التحدي الذي يعول عليه الجميع لاستعادة العرش الأفريقي.

يدخل المنتخب الوطني في معسكر تدريبي مغلق خلال الفترة من 7 حتى 14 أبريل الجارى، لفرض حالة من التركيز التام بين عناصر القائمة المختارة.

ويشرف على التحضيرات جهاز فني يضم نادر رشاد مديراً فنياً، والمعتز بالله سامي مدرباً عاماً، وأيمن عبد الرحمن مدرباً لحراس المرمى، بمرافقة جهاز إداري وطبي متكامل يضم نور الدين فرحان والدكتور مصطفى محمد، وذلك لضمان تهيئة المناخ المناسب للاعبين قبل الصدام القوي مع المنتخب الجزائري الذي يعد اختباراً حقيقياً لقدرات الفراعنة.
```

### NLI claims to label
1. من المقرر أن تُقام المباراتان الوديتان بين مصر والجزائر في صالة الدكتور حسن مصطفى بمدينة السادس من أكتوبر
2. يتولى نادر رشاد قيادة الجهاز الفني للمنتخب المصري لكرة الصالات بصفته مديراً فنياً
3. يدخل المنتخب المصري لكرة الصالات معسكراً تدريبياً مغلقاً خلال الفترة من 7 حتى 16 أبريل
4. سبق للمنتخب المصري لكرة الصالات أن فاز بلقب كأس أمم أفريقيا في النسخة الأخيرة من البطولة

### English text to translate to Arabic
```
The Algerian futsal national team is set to arrive in Cairo on April 9 to play two friendly matches against Egypt's national futsal team on April 12 and 14 at the Dr. Hassan Moustafa Hall in the Sixth of October City. These friendlies are part of an intensive preparation program led by head coach Nader Rashad to enhance the Egyptian team's technical and physical readiness ahead of the Africa Cup of Nations finals in Morocco. The Egyptian team will enter a closed training camp from April 7 to 14, supervised by a full coaching, administrative, and medical staff to ensure optimal preparation for the upcoming continental competition.
```

---

## Article SPORTS_052

### Article body (Arabic)

```
ألغى التسلل هدف تقدم الزمالك الذى سجله أحمد ربيع فى شباك المصرى، بالدقيقة 8 من عمر المباراة التي تجمعهما حاليًا على استاد برج العرب، في الجولة الأولى من المرحلة النهائية لحسم لقب الدوري.

ـ حراسة المرمى : مهدي سليمان.

ـ خط الدفاع: محمود بنتايج – حسام عبد المجيد – محمد إسماعيل – عمر جابر.

ـ خط الوسط : أحمد ربيع – أحمد فتوح – عبد الله السعيد.

ـ خط الهجوم : خوان بيزيرا – ناصر منسي – عدي الدباغ.

ويتواجد على مقاعد البدلاء، محمد عواد ومحمود حمدي الونش" ومحمد ابراهيم وأحمد عبد الرحيم "إيشو" ومحمود جهاد وآدم كايد وأحمد شريف وعمرو ناصر وسيف الجزيري.

-حراسة المرمى: عصام ثروت.

-خط الظهر: كريم العراقي، باهر المحمدي، خالد صبحي، مصطفى العش، أحمد أيمن منصور.

-خط الوسط: محمد مخلوف، محمود حمادة، أسامة زمراوي.

-الهجوم: منذر طمين، صلاح محسن.

البدلاء: محمد شحاته لحراسة المرمى، محمد الشامي، كريم بامبو، ميدو جابر، عمر الساعي، بونور موجيشا، مصطفى زيدان، عميد صوافطة، أحمد القرموطي.

ويتصدر نادي الزمالك جدول ترتيب المجموعة برصيد 43 نقطة، متساويًا مع بيراميدز صاحب المركز الثاني، لكن بفارق الأهداف لصالح الأبيض، ما يزيد من حدة المنافسة بين الفريقين.

ويأتي الأهلي في المركز الثالث برصيد 40 نقطة، ليبقى ضمن دائرة المنافسة بقوة، فيما يحتل سيراميكا المركز الرابع برصيد 38 نقطة.

وفي المراكز التالية، يتواجد المصري البورسعيدي في المركز الخامس برصيد 32 نقطة، يليه سموحة في المركز السادس بـ31 نقطة، ثم إنبي في المركز السابع برصيد 30 نقطة.
```

### NLI claims to label
1. تم إلغاء هدف سجله أحمد ربيع لصالح الزمالك في مرمى المصري بسبب التسلل
2. يحتل النادي الأهلي المرتبة الثالثة في جدول الترتيب بأربعين نقطة
3. يتصدر الزمالك جدول الترتيب برصيد 43 نقطة متقدمًا على بيراميدز بفارق النقاط
4. شهدت المباراة حضورًا جماهيريًا كبيرًا على مدرجات استاد برج العرب

### English text to translate to Arabic
```
In the opening round of the Egyptian Premier League's final stage at Borg El Arab Stadium, Zamalek had an early goal by Ahmed Rabie against Al-Masry disallowed for offside in the 8th minute. Zamalek currently lead the standings with 43 points, level with Pyramids in second place but ahead on goal difference, while Al-Ahly sit third with 40 points. Al-Masry occupy fifth place with 32 points, trailing behind fourth-placed Ceramica on 38 points.
```

---

## Article SPORTS_020

### Article body (Arabic)

```
حدد قانونيون مجموعة من النصائح المهمة التي يجب مراعاتها عند كتابة عقود البيع، لتفادي أي نزاعات قانونية مستقبلية وضمان سلامة الإجراءات بين البائع والمشتري، مؤكدين أن دقة صياغة العقد تعد الضمان الأول لحماية الحقوق.

وجاءت أبرز النصائح التي يجب الانتباه إليها عند تحرير عقد البيع كالتالي:

1. عدم شراء نماذج عقود البيع الجاهزة من المكتبات.

2. الحرص على أن يقوم محامٍ بتحرير العقد وصياغته قانونيًا.

3. ضرورة النص على تاريخ ويوم تحرير العقد بشكل واضح.

4. التأكد من أهلية المتعاقدين للتصرف والتعاقد وإقرارهم بذلك.

5. كتابة بيانات المتعاقدين كاملة، وتشمل الاسم بالكامل ورقم البطاقة والعنوان بالتفصيل.

6. في حال وجود وكالة، يجب كتابة رقم التوكيل ومكان توثيقه والتأكد من سلامته.

7. عند وجود ورثة، يتم ذكر رقم إعلام الوراثة، وإذا كان هناك قاصر يجب كتابة رقم قرار الوصاية وموافقة النيابة الحسبية على البيع.

8. وصف المبيع وصفًا تفصيليًا دقيقًا يشمل الحدود والمساحة ورقم وتاريخ رخصة البناء، بما لا يترك مجالًا للشك أو التأويل.

9. تحديد الحصة المشاعة المرتبطة بالمبيع وكتابتها بالنسبة المئوية.

10. توضيح أيلولة الملكية وتسلسلها مع التأكد من صحة المستندات واستلامها.

11. كتابة الثمن الحقيقي بالأرقام والحروف.

12. في حالة السداد بالتقسيط، يجب تحديد قيمة الأقساط ومواعيد استحقاقها مع النص على الشرط الجزائي.

13. إقرار البائع بعدم التصرف في العين المبيعة سابقًا، مع ضمان عدم تعرضه أو تعرض الغير للمشتري.

14. إقرار البائع بضمان العيوب الخفية وتحمله المسؤولية حال ظهور أي عيب بالمبيع، مع تحديد عدد صفحات العقد وبنوده وعدد النسخ ويفضل أن تكون ثلاث نسخ، إضافة إلى التأكد من صحة التوقيعات والبصمات.
```

### NLI claims to label
1. أكد خبراء في القانون أن الصياغة الدقيقة للعقد هي الضمانة الأساسية لصون حقوق الأطراف المتعاقدة
2. من بين التوصيات المذكورة ضرورة تدوين المبلغ الفعلي للبيع بالأرقام والحروف معاً
3. أوصى القانونيون بأن يكون عدد نسخ العقد نسختين فقط لكل من البائع والمشتري
4. نصح القانونيون بتسجيل العقد في الشهر العقاري خلال مدة لا تتجاوز ثلاثين يوماً من تاريخ تحريره

### English text to translate to Arabic
```
Legal experts have outlined a set of essential guidelines for drafting sales contracts to prevent future legal disputes and ensure the protection of both buyers' and sellers' rights. The recommendations include having a lawyer draft the contract, clearly stating the date, verifying the legal capacity of all parties, providing detailed descriptions of the sold property, and specifying the real price in both numbers and words. Additional advice covers cases involving power of attorney, inheritance, installment payments, the seller's guarantee against hidden defects, and ensuring the contract is signed in three copies with verified signatures and fingerprints.
```

---
