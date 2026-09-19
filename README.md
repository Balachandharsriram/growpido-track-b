# 🔍 Reputation Diagnostic – Growpido Track B

A professional reputation verification and claim-auditing system that analyzes public profiles, validates factual claims using open-web sources, and generates a structured verification report.

## 📌 Overview

This project was developed as part of the **Growpido Track B Assessment**.

The system performs claim-by-claim verification for public individuals by:

* Extracting factual claims from public profiles
* Cross-checking claims against multiple independent sources
* Classifying claims into:

  * ✅ Verified
  * ⚠️ Partially Verified
  * ❌ Unverified / Held
* Identifying inconsistencies and credibility gaps
* Generating a professional HTML report

---

## 🚀 Features

### Claim Verification Engine

* Validates factual statements using public web sources
* Detects repeated self-reported claims
* Distinguishes independent corroboration from copied content

### Reputation Analysis

* Identifies credibility risks
* Highlights conflicting public information
* Detects unsupported superlative claims such as:

  * "largest"
  * "first"
  * "leading"

### Report Generation

* Professional HTML dashboard
* Responsive design
* Verification summary cards
* Evidence-backed reasoning
* Source references

### Human Review Support

* Flags claims requiring manual verification
* Prevents publication of unsupported claims
* Maintains transparency in verification decisions

---

## 🏗️ Project Structure

```text
growpido-track-b/
│
├── index.html
├── styles/
│   └── style.css
├── assets/
│   └── screenshots/
├── data/
│   └── verified_claims.json
├── README.md
└── docs/
```

---

## 📊 Verification Categories

| Status                | Meaning                                                         |
| --------------------- | --------------------------------------------------------------- |
| ✅ Verified            | Confirmed by multiple independent sources                       |
| ⚠️ Partially Verified | Some evidence exists but does not fully support the exact claim |
| ❌ Unverified / Held   | Insufficient independent evidence or conflicting information    |

---

## 🎯 Example Analysis

### Subject

**Badr Jafar**

### Results

| Category           | Count |
| ------------------ | ----- |
| Verified           | 6     |
| Partially Verified | 2     |
| Unverified / Held  | 6     |

### Key Findings

* Multiple executive positions independently verified.
* Several "largest" and "first" claims lacked independent confirmation.
* Public biographies contained conflicting company statistics.
* Some educational credentials lacked primary-source validation.

---

## 💻 Technologies Used

* HTML5
* CSS3
* JavaScript
* Responsive Web Design
* Open Web Research Methodology

---

## 🖼️ Screenshots

Add project screenshots inside:

```text
assets/screenshots/
```

Then reference them:

```md
![Dashboard](assets/screenshots/dashboard.png)
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Balachandharsriram/growpido-track-b.git
```

Navigate to the project folder:

```bash
cd growpido-track-b
```

Open the HTML file:

```bash
start index.html
```

or simply open `index.html` in your browser.

---

## 📈 Future Improvements

* Automated web crawling
* Source credibility scoring
* AI-powered claim extraction
* PDF export
* Real-time reputation monitoring
* Multi-person batch analysis

---

## 🔒 Disclaimer

This project is intended for research, reputation auditing, and verification purposes only.

Verification results depend on publicly available information at the time of analysis. Human review is recommended before publishing any client-facing conclusions.

---

## 👨‍💻 Author

**Balachandharsriram M**

AI & Data Science Student

GitHub:
https://github.com/Balachandharsriram

---

## 📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and improve this project.
