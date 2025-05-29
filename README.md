# 🧠 Vanguard A/B Test Analysis – Funnel Optimization

## 🧩 Business Context

> Vanguard, a global investment management leader, recently launched a **digital redesign** of its customer onboarding experience. To assess the true impact of this redesign, the company conducted an **A/B test**.  
Users were randomly assigned to either the **control group** (original user journey) or the **treatment group** (newly redesigned flow). The objective:  
> **Measure if the redesign leads to a higher funnel completion rate, fewer drop-offs, and better user experience.**

> [!NOTE]
> This project simulates a real-life product experiment. It was developed during a Data Analysis Bootcamp to replicate decision-making scenarios based on real A/B testing data.

---

<details>
<summary>📦 <strong>Dataset Overview</strong></summary>

The dataset consists of user navigation events throughout the onboarding funnel:

- `user_id`: Unique identifier per user.
- `group`: A/B group label – `control` or `treatment`.
- `step`: Funnel step (e.g., `step_1`, `step_2`, ..., `confirm`).
- `timestamp`: Timestamp of the event.
- Derived fields (created in preprocessing):
  - `time_diff`: Time difference between steps.
  - `final_step`: Last recorded step per user.
  - `error_flags`: Indicators for anomalies.

</details>

---

<details>
<summary>🧹 <strong>Data Cleaning & Wrangling</strong></summary>

To ensure valid insights, we applied rigorous data preprocessing steps:

- Chronologically sorted user steps.
- Removed sessions with:
  - Repeated steps (e.g., multiple `step_2`s).
  - Backward jumps (e.g., `step_3` to `step_1`).
  - Zero-second step transitions.
- Labeled sessions that did **not** end in `confirm` as **abandonments**.
- Engineered features for:
  - Time spent per step.
  - Funnel depth reached.
  - Navigation consistency.

> These cleaning rules were based on domain assumptions. In a production setting, more session metadata and UX feedback would further guide this logic.

</details>

---

<details>
<summary>📊 <strong>Exploratory Data Analysis</strong></summary>

The EDA compared control vs. treatment groups on multiple dimensions:

- **Completion Rate** – % of users reaching the `confirm` step.
- **Drop-off Points** – Common exit steps.
- **Navigation Errors** – Frequency of repeated or reversed steps.
- **Time Metrics** – Total and per-step time comparisons.

Key visualizations:
- Funnel diagrams by group
- Step-wise conversion rates
- Session length distributions

</details>

---

<details>
<summary>🧪 <strong>Hypothesis Testing</strong></summary>

We ran statistical tests to validate whether differences observed were statistically significant:

- ✅ **Z-test for proportions** (completion rate comparison).
- ✅ **T-test** / **Mann-Whitney U test** (time differences).
- ✅ **Chi-squared test** (distribution of final steps and errors).
- ✅ **Sanity checks** for group balance and random assignment.

Assumptions tested:
- Normality (Shapiro-Wilk, histograms).
- Equal variances (Levene's test).

> Statistical significance ≠ business impact. All insights were contextualized with user experience and operational considerations.

</details>

---

<details>
<summary>📈 <strong>Key Insights</strong></summary>

- ✅ **Higher completion rate** in the treatment group (statistically significant).
- 🔄 **Fewer navigation errors** post-redesign, especially backward transitions.
- ⏱️ **Time efficiency** slightly improved but not statistically conclusive.
- 🧩 Users followed a more linear path in the redesigned flow.

</details>

---

<details>
<summary>🧭 <strong>Recommendations</strong></summary>

- ✅ **Roll out the redesign** to the broader user base.
- 📊 Monitor funnel metrics continuously to detect regressions.
- 🔬 Run additional segmented tests (e.g., new vs. returning users).
- 🧠 Gather qualitative UX insights (e.g., via surveys, heatmaps).
- ⚙️ Improve experiment design with longer run times and controlled traffic splits.

</details>

---

## 👥 Authors

[![Xavi](https://img.shields.io/badge/@xavistem-GitHub-181717?logo=github&style=flat-square)](https://github.com/xavistem)  
[![Rocío Jiménez](https://img.shields.io/badge/@JimenezRoDA-GitHub-181717?logo=github&style=flat-square)](https://github.com/JimenezRoDA)


## 🧑‍🏫 Educational Context

This analysis was developed as part of a Data Analytics Bootcamp.  
It reflects industry-standard approaches to experimentation, data cleaning, and interpretation of A/B tests within digital products.
