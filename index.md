---
course: "AI Assurance, Red Teaming and Governance for Engineering Leads"
code: "AE-407"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-407/index.html"
---

# AI Assurance, Red Teaming and Governance for Engineering Leads

ضمان أنظمة الذكاء الاصطناعي واختبارات الفريق الأحمر والحوكمة لقادة الفرق الهندسية

AI Engineering Track · 4 teaching days + capstone day · 26 hours · Level 400

Plan and run a bilingual red-team exercise, assess the risk with the national framework, review the architecture and brief the accountable executive on what remains

Participants lead the assurance of AI systems that act on an organisation's data. For the fictional Northern Region Benefits Agency (a bilingual benefits assistant and a case-worker agent that reads case files and drafts letters) they plan and run a red-team exercise in Arabic and English, manually and with automated probes, assess the risks with the National AI Risk Management Framework, review the security architecture for agent identity, least privilege, isolation and egress, and assemble an assurance case that ends in a residual-risk briefing. Targets run in a sandbox on synthetic case data. Hardening a single application is AE-308.

**Who it is for:** Specialists. Engineers who have completed the level 300 core and the practicum, or can show equivalent work: an AI system they built, operated and defended in review.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Northern Region Benefits Agency.** A fictional regional agency that pays family, disability and housing benefits. Its assurance team, led by Sulafa Al-Nashmi, examines two systems before the deputy governor signs for them: Mueen, the bilingual benefits assistant, and Katib, the case-worker agent that reads case files and drafts letters. Both run in a sandbox on 300 synthetic case files written with a fixed seed; no real person, case or address is described.

## The course

### Day 1: Plan the exercise

Slides: https://sdaiaacademy.github.io/ae-407/slides/day1.md

- **Session 1: Assurance is an argument with evidence**
  - State a top claim that evidence could show to be false
  - Separate a claim, its argument and its evidence
  - Name the evidence that defeats a claim and who is independent enough to produce it
  - [Lab 1.1: A top claim and its defeaters (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D1_1_top_claim.ipynb)
- **Session 2: Scoping from the threat model**
  - Read a threat model as a list of testable paths
  - Find the paths where private data, untrusted content and an exit path meet
  - Rank paths for testing by harm and by how little the attacker needs
  - [Lab 1.2: Missing paths in the threat model (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D1_2_threat_paths.ipynb)
- **Session 3: Objectives, scope and rules of engagement**
  - Write objectives that name a harm and a way to decide success
  - Set scope, rules of engagement and a budget of model calls
  - Write stop conditions and a procedure for harmful outputs
  - [Lab 1.3: A test plan a reviewer approves (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D1_3_test_plan.ipynb)
- **Session 4: Choosing techniques from catalogues**
  - Map a planned attack to an OWASP entry and a MITRE ATLAS technique
  - Tie every attack to a plan objective and drop those that serve none
  - Read coverage both ways: objectives without attacks and entries without tests
  - [Lab 1.4: Ten attacks, mapped and pruned (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D1_4_technique_map.ipynb)

### Day 2: Run the red team

Slides: https://sdaiaacademy.github.io/ae-407/slides/day2.md

- **Session 1: Manual probing in two languages**
  - Probe a target by hand and log every attempt, failed ones included
  - Carry one attack across English, Arabic and transliterated Arabic
  - Decide success from what happened, not from what the model said
  - [Lab 2.1: Three scripts, one log (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D2_1_manual_probing.ipynb)
- **Session 2: Indirect injection and goal hijack**
  - Plant an instruction in content the agent reads as part of its task
  - Tell a goal hijack from a data exfiltration by the evidence each leaves
  - Decide success from the exit log of the sandbox
  - [Lab 2.2: A planted line in a case file (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D2_2_indirect_injection.ipynb)
- **Session 3: Automated campaigns over repeated trials**
  - Plan a campaign that fits a fixed budget of model calls
  - Report attack success as a rate with an interval over repeated trials
  - Say which differences between techniques and scripts the intervals support
  - [Lab 2.3: A campaign within a budget (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D2_3_automated_campaign.ipynb)
- **Session 4: Findings people can act on**
  - Rate a finding for severity, likelihood and reproducibility from its evidence
  - Write a finding with the steps, the rate and the affected claim
  - Turn a finding into a regression test with a threshold over trials
  - [Lab 2.4: Three findings, one regression test (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D2_4_findings.ipynb)

### Day 3: Assess the risk

Slides: https://sdaiaacademy.github.io/ae-407/slides/day3.md

- **Session 1: The national framework as method**
  - Name the steps of the national framework and what each one produces
  - Record context and scope: system and use limits, data and parties, automation and the human role, life cycle and change
  - Separate intended uses from uses that are out of scope
  - [Lab 3.1: Context and scope for Katib (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D3_1_context_scope.ipynb)
- **Session 2: Scoring and calibration**
  - Classify a risk into the seven types of the national framework
  - Score likelihood and impact from stated evidence on the 4 by 4 matrix
  - Calibrate with a second scorer and record the reason for every changed score
  - [Lab 3.2: Twelve risks, two scorers (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D3_2_score_calibrate.ipynb)
- **Session 3: Treatment and residual risk**
  - Choose among avoid, mitigate, transfer and accept with a reason
  - Re-score residual likelihood and impact from what a control changes
  - Name the owner, the signatory and the review date of every residual risk
  - [Lab 3.3: Treat the top three (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D3_3_treat_residual.ipynb)
- **Session 4: Supplier and model-change risk**
  - Read a model update notice against the supplier contract
  - Decide which risks and which tests a model change reopens
  - Give a go, a go with conditions or a hold, with the evidence each needs
  - [Lab 3.4: A model update notice (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D3_4_supplier_change.ipynb)

### Day 4: Review and assemble the evidence

Slides: https://sdaiaacademy.github.io/ae-407/slides/day4.md

- **Session 1: Security architecture review**
  - Derive the least privilege of an agent from the classification of the data it touches
  - Test a design for isolation tiers and egress control
  - Write a review finding with severity and a decision record for the fix
  - [Lab 4.1: Three findings on the agent's design (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D4_1_architecture_review.ipynb)
- **Session 2: Identity and delegated authority**
  - Tell an agent identity from the person it acts for
  - Check a delegation hop: subject, actor, audience, scope and expiry
  - Say what a broken hop lets an attacker do
  - [Lab 4.2: The broken hop (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D4_2_delegation_chains.ipynb)
- **Session 3: Assurance evidence packs**
  - Map an evidence item to the controls it supports
  - Find controls with no evidence or with evidence too weak for the claim
  - Build the assurance case: claims, arguments, evidence and a gap list
  - [Lab 4.3: Evidence, controls and gaps (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D4_3_evidence_crosswalk.ipynb)
- **Session 4: Briefing the accountable executive**
  - State residual risk in words an executive can act on
  - Write a recommendation with conditions, owners and dates
  - Answer a challenge by reproducing the evidence, not by repeating the claim
  - [Lab 4.4: A one-page residual-risk statement (25 min)](https://sdaiaacademy.github.io/ae-407/labs/D4_4_residual_statement.ipynb)

### Capstone: Capstone: an assurance pack and its defence

Slides: https://sdaiaacademy.github.io/ae-407/slides/capstone.md

## Capstone

An assurance pack for an unseen synthetic system (test plan, attack logs, findings with regression tests, risk register, architecture review, assurance case) in a public repository, defended before a panel acting as accountable executive and auditor

**What you submit:** A link to a public GitHub repository that holds the assurance pack for Insaf, the appeals agent: the test plan, the attack logs with timestamps, the findings with three regression tests, the risk register, the architecture review, the assurance case with its gap list and the one-page residual-risk statement

**Rubric:**

- Test plan: 15%
- Testing and findings: 30%
- Risk register: 20%
- Architecture review: 20%
- Assurance case: 15%

## Outcomes

- **LO1** Plan a red-team exercise with objectives tied to harms, scope, rules of engagement and stop conditions, given a benefits assistant and a tool-using agent with their intended uses (Performance) Evidence: a test plan that a reviewer approves against a planning checklist
- **LO2** Conduct manual and automated adversarial testing in Arabic and English and quantify attack success over repeated trials, given sandboxed targets, technique catalogues and a fixed budget of model calls (Performance) Evidence: attack logs, a findings report with success rates, intervals and severity, and three regression tests
- **LO3** Assess the risks of an agent with the national framework, from context to treatment and residual sign-off, given the agent's design, its supplier contract and a control library (Performance) Evidence: a risk register with calibrated 4 by 4 scores, treatments, residual scores and named owners
- **LO4** Review a security architecture for agent identity, delegated authority, least privilege, isolation and egress control, given the agent's design documents and three delegation chains (Performance) Evidence: a review report with findings, severity and decision records for the proposed fixes
- **LO5** Build an assurance case that links each claim to evidence and maps the evidence to a control framework, given the test, risk and review outputs and a control framework (Performance) Evidence: an assurance case diagram and a gap list an auditor would accept as complete
- **LO6** Present residual risk and a recommendation with conditions to an accountable executive, given the assurance pack and a scripted supplier model change (Performance) Evidence: a one-page residual-risk statement and a briefing scored by the panel

## Tools

- **Automated probing:** garak, PyRIT, promptfoo
- **Technique catalogues and testing guides:** MITRE ATLAS, OWASP Top 10 for LLM Applications, OWASP Top 10 for Agentic Applications, OWASP AI Testing Guide, OWASP GenAI Red Teaming Manual
- **Target and attacker models:** locally served open-weight models, a hosted open-weight model
- **Policy engine for least-privilege tests:** Open Policy Agent, Cedar
- **Control frameworks:** NIST AI RMF with its generative AI profile, CSA AI Controls Matrix, ISO/IEC 42001 Annex A
- **Risk register and assurance case:** any spreadsheet, an open diagram tool such as draw.io

## Prerequisites

- AE-308 Securing Language Model and Agent Applications
- AE-303 Evaluation-Driven Development for Language Model Applications
- Has written a threat model for a system they built
- Reads a risk register and a likelihood and impact matrix

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

---

SDAIA Academy · AI Engineering Track · AI Assurance, Red Teaming and Governance for Engineering Leads

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-17 · commit f135e55
