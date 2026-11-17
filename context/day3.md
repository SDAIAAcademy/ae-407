---
course: "AI Assurance, Red Teaming and Governance for Engineering Leads"
code: "AE-407"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-407/slides/day3.html"
---

# AI Assurance, Red Teaming and Governance for Engineering Leads

## Day 3: Assess the risk

The national framework, from context and scope to residual sign-off

#### [day3#title] Assess the risk

*SDAIA Academy · AI Assurance, Red Teaming and Governance for Engineering Leads*

Day 3: The national framework, from context and scope to residual sign-off

AI Engineering Track · 4 teaching days + capstone day · 4 sessions · 4 labs · AE-407

#### [day3#agenda] Assess the risk

*Today*

- **Session 1 · The national framework as method**: The National AI Risk Management Framework as a working method: its steps, and what context and scope must record
- **Session 2 · Scoring and calibration**: Scoring likelihood and impact on the national 4 by 4 matrix, and calibrating two scorers on evidence
- **Session 3 · Treatment and residual risk**: Choosing a treatment, re-scoring what remains and getting a named person to sign for it
- **Session 4 · Supplier and model-change risk**: What a supplier may change without asking, and how a model update notice becomes a retest decision

#### [day3#review-day-2] Which sentence can go to the owner?

*Review of Day 2*

**Question:** The planted line made Katib email a record out in 15 of 30 runs (interval 33% to 67%). After a recipient allowlist: 0 of 300. Which statement is right?

- A. "Before the fix, half of the case files were at risk"
- B. "After the fix, case data cannot leave"
- C. "The email path was open and is now closed; the web path is still to be treated"
- D. "We cannot yet say whether the fix works"

### Session 1: The national framework as method

#### [day3#s1] The national framework as method

*Session 1*

- Name the steps of the national framework and what each one produces
- Record context and scope: system and use limits, data and parties, automation and the human role, life cycle and change
- Separate intended uses from uses that are out of scope

#### [day3#findings-are-not-risks] A finding is something that happened in a test; a risk is something that may happen to people

*From testing to risk*

- **Finding F1.** A planted line made Katib email a case record to an outside address in 15 of 30 runs.
- **Risk R01.** An applicant's record is disclosed outside the Agency. How likely, with 120 files a day? How bad, for whom? Who owns it, who accepts what remains?

> **And some risks no probe finds.** Case workers who send drafts unread. A supplier who changes the model. A method is needed that looks there too.

#### [day3#framework-steps] Five steps stand on a base of reference pillars

*National AI Risk Management Framework · SDAIA, April 2026*

1. **1 · Context and scope** what the system is and touches
2. **2 · Identify** list and describe the risks
3. **3 · Assess** likelihood, impact, level
4. **4 · Treat** strategy, controls, residual, decision
5. **5 · Monitor and review** in operation

**Reference pillars under every step:** general principles and values, AI regulations, data regulations, sector regulations.

#### [day3#context-four-activities] Context and scope is four records, written before any risk is named

*Step 1*

- **The system and its limits.** Kind, purpose, outputs and how they are used. Intended uses and uses not allowed. Users and people affected.
- **Data, entries, exits.** Data by sensitivity and source. Where content comes in and goes out. Every party in the value chain.
- **Automation and people.** Recommends, decides or acts. Where a person approves, reviews, objects or stops. Who is responsible.
- **Life cycle and change.** The current stage. What changes, how often, who approves. What triggers a new assessment.

#### [day3#intended-and-out-of-scope] Uses that are out of scope are written down, not assumed

*Lab 3.1, the first record*

| Katib is intended to | Katib is not to |
| --- | --- |
| Draft the letter for the case file a case worker opened | Decide eligibility or change a payment |
| Look up the published rules of the benefit | Contact anyone other than the applicant of the case |
| Send the approved letter to the registered address | Search cases for any purpose other than the open file |

> **Each line on the right is a test waiting to be written.** Lab 2.2 already ran the second one.

#### [day3#acts-not-recommends] Record what the system can do, not what the design intends

*The level of automation*

- **Recommends.** A person reads the output and acts. Mueen answering a question is close to this.
- **Decides.** The output is the decision. Neither system is meant to decide eligibility.
- **Acts.** The system changes something through tools. Katib sends email and writes notes.

> **What goes wrong.** The design says "the case worker approves every letter". In Lab 2.2 a second email left before the draft was shown. The approval is a screen, not a gate.

#### [day3#change-plan] The context record says what will change and who approves it

*Life cycle and change*

| What changes | How often | Who approves |
| --- | --- | --- |
| The supplier updates the hosted model | About twice a year | The system owner, after a staging retest |
| Letter templates | Monthly | The case-work supervisor |
| A tool is added or its permissions change | Rarely | The security architect |

- **Reassess when:** a model update, a new tool or permission, a new kind of data, an incident
- An assessment with no trigger for the next one is out of date on the day it is signed

#### [day3#check-context-gap] What is missing from this context record?

*Checkpoint*

**Question:** A record for Mueen states its purpose, three intended uses, its data with classification levels, the supplier, and that "a person can always ask for a human". What must be added before risks are identified?

- A. The ten most likely risks
- B. The uses that are out of scope, and the plan for changes and reassessment
- C. The model's size and training method
- D. The controls that will be applied

#### [day3#lab-3-1] Context and scope for Katib

Lab 3.1 · 25 min

Set context, scope and stakeholders for the case-worker agent using the framework's phases

[D3_1_context_scope.ipynb](https://sdaiaacademy.github.io/ae-407/labs/D3_1_context_scope.ipynb)

- [ ] Describe the system, its intended uses and the uses out of scope (6 min)
- [ ] List the data, the entry and exit points and the parties (7 min)
- [ ] State the level of automation and the human decision points (6 min)
- [ ] State the life-cycle stage and the change plan (6 min)
- [ ] ✱ Stretch: Name the reference pillar that each of your out-of-scope uses rests on

### Session 2: Scoring and calibration

#### [day3#s2] Scoring and calibration

*Session 2*

- Classify a risk into the seven types of the national framework
- Score likelihood and impact from stated evidence on the 4 by 4 matrix
- Calibrate with a second scorer and record the reason for every changed score

#### [day3#seven-risk-types] Seven types of risk are a check that nothing was left out

*Step 2 · identification*

| Type | At the Agency |
| --- | --- |
| Bias, discrimination and abuse | Weaker protection in Latin-letter Arabic; a degrading reply |
| Privacy and security | A record emailed out; another applicant's bank number shown |
| Misinformation | A false assurance of approval |
| Harmful use | Applicants learn the fraud-screening rule and work around it |
| Human and machine interaction | Case workers send drafts unread |
| Social, economic and environmental effects | Drafting skill fades; dependence on one supplier |
| Safety and limitations | A wrong amount in a letter; behaviour shifts after a model update |

#### [day3#describe-each-risk] Each risk is described by its source, its intent and its timing

*Step 2 · description*

- **Caused by.** A shortcoming of the AI system, or a person's misuse of it.
- **Intent.** Deliberate, or not.
- **Timing.** Before release, or after.

| Risk | Cause | Intent | Timing |
| --- | --- | --- | --- |
| R01 · a planted line makes Katib email a record out | Person, through a system weakness | Deliberate | After release |
| R10 · a letter with a wrong amount | System | Not deliberate | After release |

#### [day3#likelihood-scale] Likelihood has four levels and is judged from four things

*Step 3 · likelihood*

| Level | Meaning |
| --- | --- |
| 1 · Rare | Very unlikely to occur |
| 2 · Unlikely | Possible, not expected in ordinary conditions |
| 3 · Likely | Considerably probable given the system and its setting |
| 4 · Almost certain | Expected unless effective controls limit it |

- **Exposure:** how much the system is used, by how many
- **Controls:** what prevention is in place and how well it works
- **Ease:** how little it takes
- **Precedent:** has it happened, here or elsewhere

#### [day3#impact-scale] Impact has four levels, and the fourth is for the extreme case

*Step 3 · impact*

| Level | The expected harm is |
| --- | --- |
| 1 · Low | Limited, local, quickly contained |
| 2 · Medium | Real, but contained and put right in reasonable time |
| 3 · High | Large and clear; needs an institutional response |
| 4 · Catastrophic | Very grave, wide, perhaps irreversible |

- **Severity** of the harm
- **Size:** how many people or services
- **Sensitivity** of the data or the decision
- **Recovery:** the slower, the higher

> **A wide leak of highly sensitive data**, such as health or financial data, is one of the signs of catastrophic impact the framework names.

#### [day3#risk-matrix] Level is likelihood times impact, read in four bands

*Step 3 · level*

| Likelihood ↓ · Impact → | 1 Low | 2 Medium | 3 High | 4 Catastrophic |
| --- | --- | --- | --- | --- |
| 4 · Almost certain | 4 | 8 | 12 | 16 |
| 3 · Likely | 3 | 6 | 9 | 12 |
| 2 · Unlikely | 2 | 4 | 6 | 8 |
| 1 · Rare | 1 | 2 | 3 | 4 |

- **1 to 2** low
- **3 to 6** medium
- **8 to 12** high
- **16** catastrophic

#### [day3#two-scorers] Two careful people score the same evidence differently

*Lab 3.2, the gaps*

| Risk | First sheet | Security architect | Bands |
| --- | --- | --- | --- |
| R07 · drafts sent unread | 3 × 3 = 9 | 2 × 1 = 2 | high / low |
| R02 · the cases of a whole town | 3 × 3 = 9 | 4 × 4 = 16 | high / catastrophic |
| R12 · a false approval note | 2 × 2 = 4 | 3 × 3 = 9 | medium / high |

> **The pattern is the lesson.** The architect scores leaks higher and the human and fairness risks far lower. A single scorer hands a pattern to the register.

#### [day3#calibrate-on-evidence] Calibrating is pointing at evidence, not averaging and not rank

*Calibration*

- For each gap, both scorers name the evidence line that drove their score
- The agreed score is the one the evidence supports
- The **reason is written into the register**, so new evidence can change it

- **R02, agreed 3 × 4 = 12.** Impact 4: hundreds of records with health notes and no way back. Likelihood stays 3: it needs a hijack and then a search.

> **Two risks stand at 12.** R01 is almost certain and hurts one person at a time; R02 is less likely and cannot be undone. Keep both scores, not only the product.

#### [day3#check-score-r02] Which score does the evidence support?

*Checkpoint*

**Question:** Risk: Mueen shows another applicant's amount or bank number on request. Evidence: 4,000 conversations a week; an English phrase filter; the lookup tool takes any identifier; the campaign reached 42% over 144 attempts; one record per request; a breach notice is needed.

- A. Likelihood 2, impact 3: a control is in place
- B. Likelihood 3, impact 4: personal data is always catastrophic
- C. Likelihood 4, impact 1: frequent but small
- D. Likelihood 3, impact 3: likely, and a large harm to one person each time

#### [day3#lab-3-2] Twelve risks, two scorers

Lab 3.2 · 25 min

Score twelve risks alone on the 4 by 4 matrix, then calibrate with a partner

[D3_2_score_calibrate.ipynb](https://sdaiaacademy.github.io/ae-407/labs/D3_2_score_calibrate.ipynb)

- [ ] Classify twelve risks into the seven types (5 min)
- [ ] Score likelihood and impact alone (8 min)
- [ ] Compare with the partner sheet and find the gaps (5 min)
- [ ] Calibrate on evidence and record the agreed scores (7 min)
- [ ] ✱ Stretch: Compute the weighted agreement before and after calibration

### Session 3: Treatment and residual risk

#### [day3#s3] Treatment and residual risk

*Session 3*

- Choose among avoid, mitigate, transfer and accept with a reason
- Re-score residual likelihood and impact from what a control changes
- Name the owner, the signatory and the review date of every residual risk

#### [day3#four-treatments] There are four responses to a risk, and each needs a reason

*Step 4 · strategy*

- **Avoid.** Change the design, restrict the use, switch the function off, when the risk is high and cannot be brought down.
- **Mitigate.** Technical, organisational and operational controls that lower likelihood or impact.
- **Transfer.** Move part of the consequences by contract, guarantee or insurance.
- **Accept.** When what remains is within the approved tolerance, with the reason and the conditions recorded.

#### [day3#controls-have-owners] A control has a kind, an owner and a date

*Step 4 · controls*

| Control from the Agency's library | Kind | Owner |
| --- | --- | --- |
| C01 · `send_letter` only to the address registered on the case | Technical | Younis Al-Wabel |
| C04 · the statement is summarised by a call that has no tools | Technical | Sumayya Al-Shaalan |
| C07 · the case worker sees recipient and attachments before a letter leaves | Operational | Sumayya Al-Shaalan |
| C08 · 30 days of notice and a staging retest before a model change | Organisational | Tuqa Al-Mishaal |

> **What goes wrong.** "The team" owns a control. Nobody is asked when it slips, and the residual score stays on the register as if it were true.

#### [day3#which-score-moves] Ask of every control which score it moves

*Residual risk*

| Control, for risk R01 | Likelihood | Impact |
| --- | --- | --- |
| C01 · recipient allowlist | down 2: the exit is gone | none |
| C04 · statement quarantined | down 1: the model obeys less often | none |
| C09 · action log with an alert on a new recipient | none | down 1: found and contained sooner |

- Most controls move **likelihood**. Impact moves when less can be reached, or recovery is faster
- Distrust a residual that falls on both scores with one control

#### [day3#residual-of-top-three] Three high risks become three medium ones, on conditions

*Lab 3.3, the result*

| Risk | Inherent | Controls | Residual |
| --- | --- | --- | --- |
| R02 · the cases of a whole town | 3 × 4 = 12 high | C03 caseload scoping, C01, C09 | 2 × 2 = 4 medium |
| R01 · a record emailed out | 4 × 3 = 12 high | C01, C04, C09 | 2 × 2 = 4 medium |
| R03 · another applicant's record shown | 3 × 3 = 9 high | C05 session binding, C06 output check | 1 × 3 = 3 medium |

> **R03 keeps impact 3.** The controls make it rare. If it happens anyway, the person whose bank number is shown is harmed exactly as before.

#### [day3#transfer-keeps-responsibility] Insurance moves costs; responsibility stays where it was

*A trap in the library*

- **C12 · cyber insurance for breach costs.** Effect on likelihood: none. Effect on impact for the applicant: none. It pays part of the Agency's costs afterwards.

- Transfer is a real strategy: supplier commitments, guarantees, insurance
- It does not end the entity's responsibility for governance and compliance
- For personal data it is never the only treatment

#### [day3#sign-by-band] What remains is accepted by a named person, or escalated

*Step 4 · the decision*

| Residual band | Who accepts at the Agency | Review within |
| --- | --- | --- |
| Low | The system owner | 365 days |
| Medium | The system owner, countersigned by the head of AI assurance | 180 days |
| High | The deputy governor, with written conditions | 90 days |
| Catastrophic | Nobody: avoid or redesign |  |

> **A residual score nobody signed is a number.** A signed one is a decision, with a date on which it is looked at again.

#### [day3#check-residual-claim] Do you accept this residual score?

*Checkpoint*

**Question:** R01 is 4 × 3 = 12. The builders propose one control, the recipient allowlist, and a residual of 1 × 1 = 1, to be signed by the system owner. The allowlist is planned for next quarter. What do you answer?

- A. No: one control cannot move both scores that far, the web exit remains, and it is not live
- B. Yes: the allowlist removes the exit, so the risk is gone
- C. No: only the deputy governor may sign for R01
- D. Yes, if the Agency also buys insurance

#### [day3#lab-3-3] Treat the top three

Lab 3.3 · 25 min

Choose controls for the three highest risks in a provided register and state residual scores and signatories

[D3_3_treat_residual.ipynb](https://sdaiaacademy.github.io/ae-407/labs/D3_3_treat_residual.ipynb)

- [ ] Rank the register and take the three highest risks (4 min)
- [ ] Choose a strategy and controls from the control library (8 min)
- [ ] Re-score residual likelihood and impact with a reason (7 min)
- [ ] Name the owner, the signatory and the review date (6 min)
- [ ] ✱ Stretch: Find the risk in the register that should be avoided, not mitigated, and say what is switched off

### Session 4: Supplier and model-change risk

#### [day3#s4] Supplier and model-change risk

*Session 4*

- Read a model update notice against the supplier contract
- Decide which risks and which tests a model change reopens
- Give a go, a go with conditions or a hold, with the evidence each needs

#### [day3#measured-on-the-old-model] Every rate you measured belongs to one version of one model

*Supplier risk*

- Mueen and Katib run on a model hosted by Lisan Language Systems
- The supplier can change that model; the Agency's tests ran on **Lisan-2**
- A model change touches language handling, tool calls and safety behaviour at once

- **R09 on the register.** The supplier changes the model and behaviour in Arabic shifts unnoticed. Likelihood 3, impact 2. It also reopens most of the other eleven.

#### [day3#notice-against-contract] Read the notice against the contract, clause by clause

*Lab 3.4, step 1*

- **The notice.** Lisan-2 to Lisan-2.1, live in **10 days**, "minor". Better dialect and Latin-letter Arabic; a new tool-call format; safety behaviour retrained; a second hosting region.

| Clause | Says |
| --- | --- |
| CL1 | 30 days of notice for a change that "materially" affects behaviour; the supplier decides what is material |
| CL2 | The Agency may test in staging for 14 days |
| CL5 | Processing in the primary region; silent on a second region |

> **Ten days of notice, fourteen days of testing.** The right to test does not fit into the time given.

#### [day3#who-says-minor] The supplier classifies by what changed; you classify by what it can do to your risks

*Classifying a change*

| Announced change | Risks whose evidence it touches |
| --- | --- |
| Better dialect and Latin-letter Arabic | R03, R04, R05, R06, R08: every probe result by script |
| New tool-call format | R01, R02, R12, R10: everything Katib does through tools |
| Safety behaviour retrained, "fewer unnecessary refusals" | R04, R06, and every refusal the tests counted on |
| A second hosting region | R09, and where Restricted data is processed |

> **Major.** Ten of the twelve risks rest on behaviour that may now differ.

#### [day3#what-to-retest] Retest what depends on the model; keep what does not

*Lab 3.4, step 3*

- **Behaviour tests: rerun.** Eight tests, 460 calls: probes by script, planted instructions, letter amounts. Staging allows 400, so one must wait: the one that guards the lowest risk.
- **Design tests: still valid.** Policy tests of the service account, delegation chain checks, allowlist unit tests. They never called the model.

- The hosting change costs no calls: it is a question to the supplier, in writing
- What is left out is **recorded as not retested**, with the risk it guards

#### [day3#what-survives-a-model-change] Evidence about controls outside the model survives the update

*A property of evidence*

| Evidence | After the model changes |
| --- | --- |
| "0 of 300 with the recipient allowlist" | Holds: the allowlist does not ask the model |
| "11 of 300 with the statement quarantined" | Open: it is a rate of this model |
| "47% in Latin-letter Arabic" | Open |
| Policy tests, delegation chain checks | Hold |

> **The more of the case rests on architecture, the cheaper every model change becomes.** That is tomorrow's first two sessions.

#### [day3#suite-on-the-new-model] The test left out for the budget is one of those that got worse

*Lab 3.4, stretch*

| Test | Lisan-2 | Lisan-2.1 | Retested? |
| --- | --- | --- | --- |
| T02 · the screening rule, three scripts | 27 of 120 · 22% | 44 of 120 · 37% | no |
| T04 · false assurance | 45 of 90 · 50% | 55 of 90 · 61% | yes |
| T07 · a false note planted | 11 of 30 · 37% | 18 of 30 · 60% | yes |
| T08 · wrong amounts in letters | 2 of 50 · 4% | 5 of 50 · 10% | yes |
| T05 · a record emailed out | 15 of 30 | 15 of 30 | yes |

A budget decides what you do not see: say so in the decision record.

#### [day3#go-conditions-hold] Three answers, and each needs its evidence

*The decision*

- **Go.** The affected tests were rerun on the new version and none is worse.
- **Go with conditions.** Rerun in progress; named risks carried as open; an owner and a date for each condition.
- **Hold.** Nothing retested yet, or a test is worse and its risk is above the appetite. The date moves.

- Here: **hold**, use the 14 days of clause CL2, ask where the second region is
- Tell the deputy governor: the scores he is asked to sign were measured on the old model

#### [day3#check-update-decision] What do you retest first?

*Checkpoint*

**Question:** A supplier announces a model update that changes only the format of tool calls. You have calls for one behaviour test before the weekend. The register's top risks are R02 and R01 (both 12, through Katib's tools) and R03 (9, through Mueen's lookup).

- A. The unit tests of the recipient allowlist
- B. The degrading-reply probes in three scripts
- C. The planted instruction that makes Katib email a record out
- D. The data-residency check of the hosting region

#### [day3#lab-3-4] A model update notice

Lab 3.4 · 25 min

Assess a supplier's model update notice and decide what must be retested before it goes live

[D3_4_supplier_change.ipynb](https://sdaiaacademy.github.io/ae-407/labs/D3_4_supplier_change.ipynb)

- [ ] Read the update notice against the contract clauses (5 min)
- [ ] Classify the change and name the risks it reopens (6 min)
- [ ] Choose what must be retested from the regression suite (8 min)
- [ ] Decide: go, go with conditions or hold (6 min)
- [ ] ✱ Stretch: Run the regression suite against the changed model and compare it with your retest choice

#### [day3#wrap-up] Three things to keep

*Day 3 · wrap-up*

- **Context before risks.** What the system can do, what it touches, who decides, what will change. Seven types to check nothing was left out.
- **Scores with reasons.** Likelihood and impact from stated evidence, calibrated by two people. Keep both scores, not only the product.
- **Residual, signed and dated.** Each control moves one score. What remains is accepted by a named person, and reopened when the model changes.

#### [day3#next] Day 4: Review and assemble the evidence

*Next*

Tomorrow you review Katib's design, find where delegated authority breaks, assemble the assurance case and write the page the deputy governor signs. Reread your top claim from Day 1.
