<!-- academy:title -->
# AI Assurance, Red Teaming and Governance for Engineering Leads

ضمان أنظمة الذكاء الاصطناعي وتمارين الفرق الحمراء والحوكمة لقادة الفرق الهندسية

AI Engineering Track · SDAIA Academy · AE-407 · Level 400

REPLACE: one line under the title: what participants can do after the course

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
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Write the top claim for the benefits assistant and list evidence that would support or defeat it | [`D1_1_write_top_claim.ipynb`](labs/D1_1_write_top_claim.ipynb) |
| 1.2 | Day 1 · Session 2 | Review the agent's provided threat model, add missing paths where private data, untrusted content and an exit path meet, and rank them for testing | [`D1_2_review_agent_s.ipynb`](labs/D1_2_review_agent_s.ipynb) |
| 1.3 | Day 1 · Session 3 | Write a test plan with objectives tied to harms, stop conditions and handling of harmful outputs | [`D1_3_write_test_plan.ipynb`](labs/D1_3_write_test_plan.ipynb) |
| 1.4 | Day 1 · Session 4 | Map ten planned attacks to OWASP and ATLAS entries and drop two that serve no objective | [`D1_4_map_ten_planned.ipynb`](labs/D1_4_map_ten_planned.ipynb) |
| 2.1 | Day 2 · Session 1 | Attack the assistant in English, Arabic and transliterated Arabic and log every attempt | [`D2_1_attack_assistant_english.ipynb`](labs/D2_1_attack_assistant_english.ipynb) |
| 2.2 | Day 2 · Session 2 | Plant an instruction in a case file and try to make the agent send data out of the sandbox | [`D2_2_plant_instruction_case.ipynb`](labs/D2_2_plant_instruction_case.ipynb) |
| 2.3 | Day 2 · Session 3 | Run an automated probing campaign and report attack success with intervals | [`D2_3_run_automated_probing.ipynb`](labs/D2_3_run_automated_probing.ipynb) |
| 2.4 | Day 2 · Session 4 | Rate three provided findings for severity, likelihood and reproducibility and turn one into a regression test | [`D2_4_rate_three_provided.ipynb`](labs/D2_4_rate_three_provided.ipynb) |
| 3.1 | Day 3 · Session 1 | Set context, scope and stakeholders for the case-worker agent using the framework's phases | [`D3_1_set_context_scope.ipynb`](labs/D3_1_set_context_scope.ipynb) |
| 3.2 | Day 3 · Session 2 | Score twelve risks alone on the 4 by 4 matrix, then calibrate with a partner | [`D3_2_score_twelve_risks.ipynb`](labs/D3_2_score_twelve_risks.ipynb) |
| 3.3 | Day 3 · Session 3 | Choose controls for the three highest risks in a provided register and state residual scores and signatories | [`D3_3_choose_controls_three.ipynb`](labs/D3_3_choose_controls_three.ipynb) |
| 3.4 | Day 3 · Session 4 | Assess a supplier's model update notice and decide what must be retested before it goes live | [`D3_4_assess_supplier_s.ipynb`](labs/D3_4_assess_supplier_s.ipynb) |
| 4.1 | Day 4 · Session 1 | Review the agent design against least privilege, isolation and egress criteria and write three findings | [`D4_1_review_agent_design.ipynb`](labs/D4_1_review_agent_design.ipynb) |
| 4.2 | Day 4 · Session 2 | Find the broken hop in three delegation chains where the agent acts for a case worker | [`D4_2_find_broken_hop.ipynb`](labs/D4_2_find_broken_hop.ipynb) |
| 4.3 | Day 4 · Session 3 | Map a provided evidence set to a control framework and list the gaps an auditor would raise | [`D4_3_map_provided_evidence.ipynb`](labs/D4_3_map_provided_evidence.ipynb) |
| 4.4 | Day 4 · Session 4 | Draft a one-page residual-risk statement with conditions, owners and dates from a provided assurance pack | [`D4_4_draft_one_page.ipynb`](labs/D4_4_draft_one_page.ipynb) |
<!-- /academy:labs -->

## Capstone

An assurance pack for an unseen synthetic system (test plan, attack logs, findings with regression tests, risk register, architecture review, assurance case) in a public repository, defended before a panel acting as accountable executive and auditor

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

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

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- National AI Risk Management Framework (SDAIA, April 2026): REPLACE: the address of the official text
- SDAIA AI Ethics Principles: REPLACE: the address of the official text
- SDAIA Generative AI Guidelines: REPLACE: the address of the official text
- Personal Data Protection Law and its implementing regulations: REPLACE: the address of the official text
- NDMO Data Classification Policy: REPLACE: the address of the official text
- NCA Essential Cybersecurity Controls: REPLACE: the address of the official text
- NCA AI Cybersecurity Guidelines (consultation draft, 2026): REPLACE: the address of the official text
