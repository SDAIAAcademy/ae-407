<!-- academy:title -->
# AI Assurance, Red Teaming and Governance for Engineering Leads

ضمان أنظمة الذكاء الاصطناعي واختبارات الفريق الأحمر والحوكمة لقادة الفرق الهندسية

AI Engineering Track · SDAIA Academy · AE-407 · Level 400

Plan and run a bilingual red-team exercise, assess the risk with the national framework, review the architecture and brief the accountable executive on what remains

Participants lead the assurance of AI systems that act on an organisation's data. For the fictional Northern Region Benefits Agency (a bilingual benefits assistant and a case-worker agent that reads case files and drafts letters) they plan and run a red-team exercise in Arabic and English, manually and with automated probes, assess the risks with the National AI Risk Management Framework, review the security architecture for agent identity, least privilege, isolation and egress, and assemble an assurance case that ends in a residual-risk briefing. Targets run in a sandbox on synthetic case data. Hardening a single application is AE-308.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/ae-407/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Plan a red-team exercise with objectives tied to harms, scope, rules of engagement and stop conditions, given a benefits assistant and a tool-using agent with their intended uses | Performance | a test plan that a reviewer approves against a planning checklist |
| LO2 | Conduct manual and automated adversarial testing in Arabic and English and quantify attack success over repeated trials, given sandboxed targets, technique catalogues and a fixed budget of model calls | Performance | attack logs, a findings report with success rates, intervals and severity, and three regression tests |
| LO3 | Assess the risks of an agent with the national framework, from context to treatment and residual sign-off, given the agent's design, its supplier contract and a control library | Performance | a risk register with calibrated 4 by 4 scores, treatments, residual scores and named owners |
| LO4 | Review a security architecture for agent identity, delegated authority, least privilege, isolation and egress control, given the agent's design documents and three delegation chains | Performance | a review report with findings, severity and decision records for the proposed fixes |
| LO5 | Build an assurance case that links each claim to evidence and maps the evidence to a control framework, given the test, risk and review outputs and a control framework | Performance | an assurance case diagram and a gap list an auditor would accept as complete |
| LO6 | Present residual risk and a recommendation with conditions to an accountable executive, given the assurance pack and a scripted supplier model change | Performance | a one-page residual-risk statement and a briefing scored by the panel |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | Plan the exercise | Assurance is an argument with evidence; Scoping from the threat model; Objectives, scope and rules of engagement; Choosing techniques from catalogues | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Run the red team | Manual probing in two languages; Indirect injection and goal hijack; Automated campaigns over repeated trials; Findings people can act on | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Assess the risk | The national framework as method; Scoring and calibration; Treatment and residual risk; Supplier and model-change risk | [`slides/day3.html`](slides/day3.html) |
| Day 4 | Review and assemble the evidence | Security architecture review; Identity and delegated authority; Assurance evidence packs; Briefing the accountable executive | [`slides/day4.html`](slides/day4.html) |
| Capstone | Capstone: an assurance pack and its defence |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**Northern Region Benefits Agency.** A fictional regional agency that pays family, disability and housing benefits. Its assurance team, led by Sulafa Al-Nashmi, examines two systems before the deputy governor signs for them: Mueen, the bilingual benefits assistant, and Katib, the case-worker agent that reads case files and drafts letters. Both run in a sandbox on 300 synthetic case files written with a fixed seed; no real person, case or address is described.

The people in the case: Zuhair Al-Zaidi, deputy governor for benefits and the accountable executive; Sulafa Al-Nashmi, head of AI assurance; Sumayya Al-Shaalan, case-work supervisor and owner of both systems; Younis Al-Wabel, security architect; Zakiya Al-Buraik, internal auditor; Tuqa Al-Mishaal, data protection officer. The hosted model comes from Lisan Language Systems, a fictional supplier. The models in the labs are a scripted stand-in, so that every rate can be reproduced; its rates are its own and say nothing about any real model.

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | A top claim and its defeaters | [`D1_1_top_claim.ipynb`](labs/D1_1_top_claim.ipynb) |
| 1.2 | Day 1 · Session 2 | Missing paths in the threat model | [`D1_2_threat_paths.ipynb`](labs/D1_2_threat_paths.ipynb) |
| 1.3 | Day 1 · Session 3 | A test plan a reviewer approves | [`D1_3_test_plan.ipynb`](labs/D1_3_test_plan.ipynb) |
| 1.4 | Day 1 · Session 4 | Ten attacks, mapped and pruned | [`D1_4_technique_map.ipynb`](labs/D1_4_technique_map.ipynb) |
| 2.1 | Day 2 · Session 1 | Three scripts, one log | [`D2_1_manual_probing.ipynb`](labs/D2_1_manual_probing.ipynb) |
| 2.2 | Day 2 · Session 2 | A planted line in a case file | [`D2_2_indirect_injection.ipynb`](labs/D2_2_indirect_injection.ipynb) |
| 2.3 | Day 2 · Session 3 | A campaign within a budget | [`D2_3_automated_campaign.ipynb`](labs/D2_3_automated_campaign.ipynb) |
| 2.4 | Day 2 · Session 4 | Three findings, one regression test | [`D2_4_findings.ipynb`](labs/D2_4_findings.ipynb) |
| 3.1 | Day 3 · Session 1 | Context and scope for Katib | [`D3_1_context_scope.ipynb`](labs/D3_1_context_scope.ipynb) |
| 3.2 | Day 3 · Session 2 | Twelve risks, two scorers | [`D3_2_score_calibrate.ipynb`](labs/D3_2_score_calibrate.ipynb) |
| 3.3 | Day 3 · Session 3 | Treat the top three | [`D3_3_treat_residual.ipynb`](labs/D3_3_treat_residual.ipynb) |
| 3.4 | Day 3 · Session 4 | A model update notice | [`D3_4_supplier_change.ipynb`](labs/D3_4_supplier_change.ipynb) |
| 4.1 | Day 4 · Session 1 | Three findings on the agent's design | [`D4_1_architecture_review.ipynb`](labs/D4_1_architecture_review.ipynb) |
| 4.2 | Day 4 · Session 2 | The broken hop | [`D4_2_delegation_chains.ipynb`](labs/D4_2_delegation_chains.ipynb) |
| 4.3 | Day 4 · Session 3 | Evidence, controls and gaps | [`D4_3_evidence_crosswalk.ipynb`](labs/D4_3_evidence_crosswalk.ipynb) |
| 4.4 | Day 4 · Session 4 | A one-page residual-risk statement | [`D4_4_residual_statement.ipynb`](labs/D4_4_residual_statement.ipynb) |
<!-- /academy:labs -->

## Capstone

An assurance pack for an unseen synthetic system (test plan, attack logs, findings with regression tests, risk register, architecture review, assurance case) in a public repository, defended before a panel acting as accountable executive and auditor

**Submission:** A link to a public GitHub repository that holds the assurance pack for Insaf, the appeals agent: the test plan, the attack logs with timestamps, the findings with three regression tests, the risk register, the architecture review, the assurance case with its gap list and the one-page residual-risk statement

The unseen system is Insaf, the appeals agent of the same Agency; its brief is in [`labs/capstone/README.md`](labs/capstone/README.md). The defence takes 10 minutes of presentation and 10 minutes of questions, in which the participant reproduces one finding the panel selects.

## Prerequisites

- AE-308 Securing Language Model and Agent Applications
- AE-303 Evaluation-Driven Development for Language Model Applications
- Has written a threat model for a system they built
- Reads a risk register and a likelihood and impact matrix

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Automated probing:** garak, PyRIT, promptfoo
- **Technique catalogues and testing guides:** MITRE ATLAS, OWASP Top 10 for LLM Applications, OWASP Top 10 for Agentic Applications, OWASP AI Testing Guide, OWASP GenAI Red Teaming Manual
- **Target and attacker models:** locally served open-weight models, a hosted open-weight model
- **Policy engine for least-privilege tests:** Open Policy Agent, Cedar
- **Control frameworks:** NIST AI RMF with its generative AI profile, CSA AI Controls Matrix, ISO/IEC 42001 Annex A
- **Risk register and assurance case:** any spreadsheet, an open diagram tool such as draw.io
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

### National references

- [National AI Risk Management Framework, full text in Arabic (SDAIA, April 2026)](https://sdaia.gov.sa/ar/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryAr.pdf)
- [National AI Risk Management Framework, English executive summary (SDAIA, April 2026)](https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryEn.pdf)
- [Principles of AI Ethics (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf)
- [Generative AI Guideline for Government (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Files/GenAIGuidelinesForGovernmentENCompressed.pdf)
- [Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [Data Classification Policy (National Data Management Office, SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf)
- [National Cybersecurity Authority: controls list (Essential Cybersecurity Controls; AI Cybersecurity Guidelines, consultation draft)](https://nca.gov.sa/en/regulatory-documents/controls-list/)
- [Essential Cybersecurity Controls (National Cybersecurity Authority)](https://nca.gov.sa/en/regulatory-documents/controls-list/ecc/)

### Risk lists, technique catalogues and testing guides

- [OWASP Top 10 for LLM Applications 2026 (OWASP GenAI Security Project)](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications for 2026 (OWASP GenAI Security Project)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP GenAI Red Teaming Guide (OWASP GenAI Security Project)](https://genai.owasp.org/resource/genai-red-teaming-guide/)
- [OWASP AI Testing Guide](https://owasp.org/projects/ai-testing-guide)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [MITRE ATLAS data, version 2026.10](https://github.com/mitre-atlas/atlas-data)
- [Simon Willison: The lethal trifecta for AI agents (June 2025)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)

### Assurance cases

- [Bloomfield and Rushby: Assurance 2.0, a manifesto (2020)](https://arxiv.org/abs/2004.10474)
- [Goal Structuring Notation community standard (Safety-Critical Systems Club)](https://scsc.uk/gsn)
- [AI Security Institute: Safety cases at AISI](https://www.aisi.gov.uk/blog/safety-cases-at-aisi)

### Control frameworks

- [NIST AI Risk Management Framework (AI RMF 1.0), NIST AI 100-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [NIST AI RMF: Generative Artificial Intelligence Profile, NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [NIST AI Risk Management Framework: overview page](https://www.nist.gov/itl/ai-risk-management-framework)
- [CSA AI Controls Matrix (Cloud Security Alliance)](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix)

### Identity and delegated authority

- [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)

### Tools named as examples

- [garak, the LLM vulnerability scanner](https://github.com/NVIDIA/garak)
- [PyRIT, the Python Risk Identification Tool for generative AI](https://github.com/Azure/PyRIT)
- [promptfoo: red teaming guide](https://www.promptfoo.dev/docs/red-team/)
- [Open Policy Agent: documentation](https://www.openpolicyagent.org/docs)
- [Cedar policy language](https://www.cedarpolicy.com/)
- [OpenRouter models list](https://openrouter.ai/models)
<!-- /academy:sources -->

### National references

- National AI Risk Management Framework (SDAIA, April 2026): https://sdaia.gov.sa/ar/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryAr.pdf (full text, Arabic) and https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryEn.pdf (executive summary, English)
- SDAIA AI Ethics Principles: https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf
- SDAIA Generative AI Guidelines: https://sdaia.gov.sa/en/SDAIA/about/Files/GenAIGuidelinesForGovernmentENCompressed.pdf
- Personal Data Protection Law and its implementing regulations: https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf and https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf
- NDMO Data Classification Policy: https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf
- NCA Essential Cybersecurity Controls: https://nca.gov.sa/en/regulatory-documents/controls-list/ecc/
- NCA AI Cybersecurity Guidelines (consultation draft, 2026): listed by the National Cybersecurity Authority at https://nca.gov.sa/en/regulatory-documents/controls-list/ ; the course cites the draft by name and states nothing about its content
