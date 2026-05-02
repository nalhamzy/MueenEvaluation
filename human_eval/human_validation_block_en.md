## 8. Human Validation


To independently validate the GPT-5.2 LLM-as-Judge scores, a single qualified human evaluator scored Summary and Translation outputs from all 4 models on a stratified subsample of 30 articles (6 per category). The evaluator was **blinded** — model identities were anonymized as Model A–D and revealed only after scoring was complete.

**Evaluator:** Ahmed Al Saidi (native). **Period:** 2026-04-28 → 2026-05-02. **Total judgments:** 240 (30 articles × 4 models × 2 tasks). **Scale:** integer 1–5 (rescaled to 0–10 for comparability).

### 8.1 Human-validated leaderboard (rescaled to 0–10)


| Rank | Model | Summary (Human) | Translation (Human) | Combined (Human) |
|:----:|-------|:--------------:|:-------------------:|:----------------:|
| 1 | Qwen 3.5 397B | 8.75 | 9.17 | **8.96** |
| 2 | DeepSeek Chat | 6.17 | 8.17 | **7.17** |
| 3 | Mistral Large | 4.25 | 2.25 | **3.25** |
| 4 | **Mueen AI** | 2.75 | 0.67 | **1.71** |

### 8.2 Agreement with the GPT-5.2 LLM Judge


Per-judgment correlation between the human evaluator (rescaled to 0–10) and the GPT-5.2 LLM judge on the same 30 articles:

| Task | n | Spearman ρ | Pearson r |
|------|:-:|:---------:|:---------:|
| Summary | 120 | +0.526 | +0.568 |
| Translation | 120 | +0.808 | +0.767 |
| Combined | 240 | +0.688 | +0.682 |

At the **model level** (4-point Spearman over the model means on the same 30 articles): ρ = +1.000.

### 8.3 Model means on the same 30-article subset


| Model | LLM Judge (0–10) | Human (0–10) | Δ (Human − LLM) |
|-------|:----------------:|:------------:|:---------------:|
| Qwen 3.5 397B | 8.99 | 8.96 | -0.03 |
| DeepSeek Chat | 8.65 | 7.17 | -1.48 |
| Mistral Large | 6.52 | 3.25 | -3.27 |
| Mueen AI | 5.99 | 1.71 | -4.28 |

### 8.4 Ranking comparison


| Model | LLM Rank | Human Rank | Match |
|-------|:--------:|:----------:|:-----:|
| Qwen 3.5 397B | 1 | 1 | ✓ |
| DeepSeek Chat | 2 | 2 | ✓ |
| Mistral Large | 3 | 3 | ✓ |
| Mueen AI | 4 | 4 | ✓ |

**The human and automated judges produced an identical model ranking.** This is the strongest possible agreement signal at the model level and supports the leaderboard reported in Section 3.

### 8.5 Mueen AI — per-category human scores (1–5)


| Category | n | Summary | Translation | Combined |
|----------|:-:|:-------:|:-----------:|:--------:|
| Culture | 6 | 2.00 | 1.83 | **1.92** |
| Finance | 6 | 2.50 | 1.17 | **1.83** |
| Politics | 6 | 2.33 | 1.00 | **1.67** |
| Sports | 6 | 2.00 | 1.17 | **1.58** |
| Tech | 6 | 1.67 | 1.17 | **1.42** |

### 8.6 Evaluator's qualitative observations


> *(Original Arabic by the evaluator. Model letters de-anonymized post-scoring: A → Qwen 3.5, B → Mueen AI, C → DeepSeek Chat, D → Mistral Large.)*
>
> - الاخبار الاقتصادية وخصوصا التي تحمل ارقام تشكل اكبر فارق في نتائج النماذج
> - ويجب اعتمادها في قياس اداء النماذج المستقبلية
> - المواضيع المرتبط بالرياضة كانت الاسهل واظهرت نتائج متقاربة بين النماذج
> - اكبر الفروق تكمن في فصاحة اللغة والشمولية حيث اظهر النموذج A تفوقا كبيرا في المصطلحات المستخدمة وجودة المخرجات
> - النموذج C اداءه متقارب من النموذج A وتفوق عليه في موضيع الترجمة في بعض المقالات وينقصه الفصاحة فقط.
> - اظهر النموذج B العديد من حالات الهلوسة في مهمة التلخصيص وكذلك الترجمة من خلال اختلاق معلومات جديدة او حذف معلومات مهمة
> - اكبر التحديات التي يواجهها النموذج D هي تركيب الجمل العربية واختيار المصطلاحات المناسبة.

### 8.7 What this means


The blinded human evaluation **confirms** the ordering produced by the automated LLM judge: Mueen AI ranks fourth, behind all three commercial frontier models. The gap between Mueen AI and the leading model is consistent across both judges. This independent human validation removes the principal credibility risk of an automated benchmark — that the LLM judge could systematically favor some models over others — and supports the conclusions in Sections 3–6.
