---
course: "AI Assurance, Red Teaming and Governance for Engineering Leads"
code: "AE-407"
version: "2027.1.0"
deck: "day4"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-407/slides/day4.html"
---

# AI Assurance, Red Teaming and Governance for Engineering Leads

## Day 4: Review and assemble the evidence

Architecture review, delegated authority, the assurance case and the briefing

#### [day4#title] Review and assemble the evidence

*SDAIA Academy · AI Assurance, Red Teaming and Governance for Engineering Leads*

Day 4: Architecture review, delegated authority, the assurance case and the briefing

AI Engineering Track · 4 teaching days + capstone day · 4 sessions · 4 labs · AE-407

#### [day4#agenda] Review and assemble the evidence

*Today*

- **Session 1 · Security architecture review**: Reviewing a design the way an attacker reads it: least privilege, isolation and egress, each with a test
- **Session 2 · Identity and delegated authority**: Who the agent is when it acts for a case worker: identity, delegation and the hop where authority breaks
- **Session 3 · Assurance evidence packs**: Assembling the pack: evidence linked to claims, mapped to a control framework, with the gaps named
- **Session 4 · Briefing the accountable executive**: One page for the person who signs: residual risk in plain words, a recommendation, conditions, owners and dates

#### [day4#review-day-3] When is a residual score true?

*Review of Day 3*

**Question:** The register shows R02 at 3 × 4 = 12 inherent and 2 × 2 = 4 residual, signed by the system owner. The residual rests on caseload scoping, which is not built. What is the level of R02 today?

- A. 4, because the residual was signed
- B. 12, until the control is live and its test passes
- C. 8, halfway, since the control is planned
- D. 16, because an unbuilt control is a new risk

### Session 1: Security architecture review

#### [day4#s1] Security architecture review

*Session 1*

- Derive the least privilege of an agent from the classification of the data it touches
- Test a design for isolation tiers and egress control
- Write a review finding with severity and a decision record for the fix

#### [day4#design-outlives-the-model] A behaviour test asks what the model did; a design review asks what it could do

*Why review the architecture*

- **Behaviour evidence.** "The planted line worked in 15 of 30 runs." A rate, of one model version, under one set of probes.
- **Design evidence.** "The agent's account cannot send to an address that is not on the case." True for every model, every probe, every day until the design changes.

> **Assume the model is hijacked.** Then ask what the agent's own account, placement and exits allow.

#### [day4#three-criteria] Three questions, each with a test

*The review criteria*

- **Least privilege.** Does the agent's account hold only what the intended uses need, on behalf of the person it acts for?
- **Isolation.** Where does the runtime sit? Do sensitive data and an open network meet in one place?
- **Egress control.** Which ways out exist: mail, web requests, notes others read? Is each limited to named destinations?

A fourth, **monitoring**, decides whether anyone would notice: actions traced to a person, and a named person who can stop the agent.

#### [day4#privilege-from-classification] Derive the permissions from the data and the intended uses

*Least privilege*

| Intended use | Needs | Granted in the pilot design |
| --- | --- | --- |
| Draft the letter for the open case | `case:read` on the worker's own caseload | `case:read` on `case:*` |
| (none) | nothing | `case:search` on `case:*` |
| Send the approved letter | `mail:send` to the registered address | `mail:send` to `addr:*` |
| Fetch a letter template | `net:fetch` from the template host | `net:fetch` from `host:*` |

> **Case records are Restricted.** A wildcard on Restricted data, held by an account that reads untrusted text, is the whole of risk R02.

#### [day4#tiers-and-routes] Policy says what is allowed; placement says what is possible

*Isolation and egress*

**Tier A** public-facing: portal, Mueen → **Tier B** internal applications → **Tier C** case database

- The pilot runs Katib's runtime **in tier C**, with a default route to the internet
- A policy rule can be loosened in one line by mistake; a missing route cannot
- Two layers: the rule that denies, and the network that has no path

#### [day4#tests-of-a-design] Ten questions to the design; seven come back wrong

*Lab 4.1, step 2*

| Test | Question | Expected | Design gives |
| --- | --- | --- | --- |
| LP-1 | Read a case outside the acting worker's caseload | deny | allow |
| LP-2 | Search the cases of every town | deny | allow |
| EG-1 | Email an address not registered on the case | deny | allow |
| IS-1 | The runtime that reads Restricted data reaches the internet | deny | allow |
| IS-2 | The public assistant uses the agent's tools | deny | deny |
| EG-3 | Request the Agency's template host | allow | allow |

Six of the ten shown. Tests of what must still work keep a fix from breaking the service.

#### [day4#finding-and-decision] A finding says what is wrong; a decision record says what was done about it

*The outputs of a review*

- **Finding.** The agent's account may read and search every case. Evidence: LP-1, LP-2. Consequence: one hijacked run reaches a whole town (R02). Severity 3.
- **Decision record.** Proposed: keep the wildcard and instruct the agent to open only its case. **Rejected:** an instruction is not a control. Owner: Younis Al-Wabel. Closed when LP-1 and LP-2 pass.

> **Severity uses the impact scale of Day 3,** so that findings and risks can be read side by side.

#### [day4#check-fix-or-not] Which proposed fix do you accept?

*Checkpoint*

**Question:** Finding: Katib may email any address. The builders offer four fixes. Which one closes the finding?

- A. Add to the instructions: "send letters only to the applicant"
- B. Screen every draft for addresses with a second model
- C. Log every email the agent sends
- D. Allow `mail:send` only to the address registered on the case

#### [day4#lab-4-1] Three findings on the agent's design

Lab 4.1 · 25 min

Review the agent design against least privilege, isolation and egress criteria and write three findings

[D4_1_architecture_review.ipynb](https://sdaiaacademy.github.io/ae-407/labs/D4_1_architecture_review.ipynb)

- [ ] Read the design and its data classification (5 min)
- [ ] Run the least-privilege, isolation and egress tests (7 min)
- [ ] Write three findings with severity (8 min)
- [ ] Record a decision for each proposed fix (5 min)
- [ ] ✱ Stretch: Write the policy rule that closes one finding and run the tests again

### Session 2: Identity and delegated authority

#### [day4#s2] Identity and delegated authority

*Session 2*

- Tell an agent identity from the person it acts for
- Check a delegation hop: subject, actor, audience, scope and expiry
- Say what a broken hop lets an attacker do

#### [day4#who-is-the-agent] The agent has an identity of its own, and it acts for someone

*Agent identity*

- **The person.** Case worker `cw-07`, signed in. Her caseload, her right to send letters, her name in the record.
- **The agent.** Service account `svc-katib`. It should hold almost nothing by itself, and borrow authority for one task at a time.

> **What goes wrong.** The agent calls every service as itself, with its own wide permissions. The case worker's limits vanish, and the log says "svc-katib" for everything.

#### [day4#five-fields] A delegated token answers five questions

*Recall from AE-308*

| Field | Question | In a sound hop |
| --- | --- | --- |
| `sub` · subject | For whom? | Still the case worker who signed in |
| `act` · actor | By whom? | Names the service making the call |
| `aud` · audience | For which service? | The one it is presented to, and no other |
| `scope` | Allowed to do what? | Never more than was delegated at sign-in |
| `exp` · expiry | Until when? | Never later than the sign-in; minutes, not hours |

#### [day4#a-sound-chain] A sound chain narrows at every hop and never changes its subject

*Lab 4.2, step 1*

| Hop | Presented to | sub | act | aud | scope | exp (min) |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | katib-runtime | cw-07 |  | katib-runtime | case:read letter:send | 60 |
| 1 | case-service | cw-07 | svc-katib | case-service | case:read | 10 |
| 2 | letter-service | cw-07 | svc-katib | letter-service | letter:send | 10 |
| 3 | mail-gateway | cw-07 | svc-letter | mail-gateway | letter:send | 5 |

> **Read down each column.** Subject constant. Actor names each caller. Audience equals the service. Scope shrinks. Expiry shrinks.

#### [day4#three-breaks] Three ways a chain breaks, and what each one gives away

*Lab 4.2, steps 3 and 4*

- **Wrong audience.** A token made for the case service is accepted by the letter service. Whoever captures it can **replay** it elsewhere.
- **Wider scope.** The agent's token carries `case:search-all`, which the case worker never had. **Escalation:** one run reaches every case.
- **Subject replaced.** From hop 2 the subject is `svc-katib`. The act is recorded as the agent's own: **no accountability**, no caseload limit.

#### [day4#compare-with-the-origin] Compare every hop with the sign-in, not with the hop before it

*Writing the check*

```
def check_hop(origin, hop):
    first, tok = origin["token"], hop["token"]
    broken = []
    if tok["sub"] != first["sub"]:
        broken.append("subject")
    if not tok["act"]:
        broken.append("actor")
    if tok["aud"] != hop["presented_to"]:
        broken.append("audience")
    ...
```

- In chain C, hop 3 keeps the subject of hop 2
- A check against the previous hop passes it
- Authority comes from the person: measure against her sign-in

#### [day4#identity-in-the-register] Each break makes a risk you already scored worse

*Back to the register*

| Break | Gives | Risk on the register |
| --- | --- | --- |
| Wrong audience | Replay | R01 · a letter sent where it should not go |
| Wider scope | Escalation | R02 · the cases of a whole town |
| Subject replaced | No accountability | R12 · a note nobody can trace to a person |

> **Chain checks are design evidence.** They survive a model update, and they go into the pack beside the architecture review.

#### [day4#check-broken-hop] What is wrong with this hop?

*Checkpoint*

**Question:** Sign-in: `sub cw-09`, scope `case:read letter:send`, 60 minutes. The token presented to the letter service: `sub cw-09`, `act svc-katib`, `aud letter-service`, scope `letter:send`, 480 minutes.

- A. Expiry: the delegated token outlives the sign-in it came from
- B. Subject: the agent should be the subject
- C. Audience: it should name the agent runtime
- D. Scope: letter:send was never delegated

#### [day4#lab-4-2] The broken hop

Lab 4.2 · 25 min

Find the broken hop in three delegation chains where the agent acts for a case worker

[D4_2_delegation_chains.ipynb](https://sdaiaacademy.github.io/ae-407/labs/D4_2_delegation_chains.ipynb)

- [ ] Read one correct chain hop by hop (5 min)
- [ ] Write the check of one hop (8 min)
- [ ] Find the broken hop in three chains (7 min)
- [ ] Say what each break lets an attacker do (5 min)
- [ ] ✱ Stretch: Repair one chain and show that your check now passes it

### Session 3: Assurance evidence packs

#### [day4#s3] Assurance evidence packs

*Session 3*

- Map an evidence item to the controls it supports
- Find controls with no evidence or with evidence too weak for the claim
- Build the assurance case: claims, arguments, evidence and a gap list

#### [day4#what-a-pack-is] A pack is what lets someone who was not there reach your conclusion

*The assurance pack*

1. **Plan** objectives, scope, rules
2. **Logs and findings** rates, intervals, regression tests
3. **Register** scores, treatments, signatures
4. **Reviews** design tests, chain checks
5. **Case and page** claims, gaps, the statement

Four days of labs produced each of these for Katib and Mueen. Today's question: do they add up to the top claim of Lab 1.1?

#### [day4#what-counts-as-evidence] Ask of every item who made it and what it can carry

*Judging evidence*

| Item | By | Strength |
| --- | --- | --- |
| Campaign log of 576 attempts with rates and intervals by script | Independent | Strong |
| Role chart: owner, signatories, who may stop the system | Builders | Strong: a fact anyone can verify |
| "All security tests passed", no log attached | Builders | Weak: a judgment of their own work |
| Monitoring plan, draft, no thresholds | Builders | Weak |
| A screenshot of Mueen refusing one request | Builders | None |

> **Evidence is what an outsider can check.** A summary without its log is a claim.

#### [day4#crosswalk] A crosswalk shows where the evidence piles up and where there is none

*Lab 4.3, steps 2 and 3*

| Item | Value |
| --- | --- |
| MEASURE 2.7 · security evaluated | 5 items |
| MANAGE 1.3 · responses to high risks | 2 |
| MEASURE 2.11 · fairness evaluated | 1, weak |
| MANAGE 4.1 · monitoring after release | 1, weak |
| MANAGE 2.4 · can be switched off | 0 |
| MANAGE 4.3 · incidents handled | 0 |

Six of the fourteen subcategories in the lab's extract of the NIST AI Risk Management Framework.

#### [day4#claims-and-evidence] The top claim holds only as far as its weakest sub-claim

*The assurance case*

| Sub-claim | Rests on |
| --- | --- |
| C1 · Testing found the weaknesses that matter; each is fixed or carried as a risk | Plan, campaign log, findings, privacy probes |
| C2 · Every risk is scored, treated and signed for | Register, context record, supplier assessment, role chart |
| C3 · The architecture limits what a hijacked agent can do | Architecture review, chain checks |
| C4 · After release, a change or an incident is noticed in time | A draft monitoring plan |

> **Three sub-claims hold. One does not yet,** and the top claim must say so in its conditions.

#### [day4#gap-list] List the gaps yourself, each with an ask

*Lab 4.3, step 4*

| Control | Gap | Ask |
| --- | --- | --- |
| MANAGE 2.4 | No evidence | The system owner names who may stop Katib, within how many minutes, and shows one drill |
| MANAGE 4.3 | No evidence | The incident process is extended to the agent, with a record of one exercise |
| MEASURE 2.11 | Weak | The degrading-reply probes are rerun in all three scripts |
| MANAGE 4.1 | Weak | The monitoring plan is approved, with thresholds and a per-worker action log |

> **An auditor finds them anyway.** A pack that names its gaps shows its authors tested their own claim.

#### [day4#pack-in-a-repository] Every number in the pack leads back to a file

*For tomorrow*

- One folder per part: plan, logs, findings, register, reviews, case
- Logs carry timestamps, the target version and the seed
- Each finding has a regression test that someone else can run
- The statement cites the file behind each level

- **The auditor's move.** Zakiya Al-Buraik opens one claim at random and asks you to reproduce the number behind it, in front of her. Build the pack for that moment.

#### [day4#check-evidence-strength] Which item can carry the claim?

*Checkpoint*

**Question:** Sub-claim: "Mueen does not reveal another applicant's record." Which item supports it best?

- A. A screenshot of Mueen refusing such a request in Arabic
- B. The builders' note that the lookup "was hardened last sprint"
- C. A design test showing the lookup returns only the signed-in case, with probe results by script after the fix
- D. The supplier's contract clause on data use

#### [day4#lab-4-3] Evidence, controls and gaps

Lab 4.3 · 25 min

Map a provided evidence set to a control framework and list the gaps an auditor would raise

[D4_3_evidence_crosswalk.ipynb](https://sdaiaacademy.github.io/ae-407/labs/D4_3_evidence_crosswalk.ipynb)

- [ ] Read the evidence set and the framework extract (5 min)
- [ ] Map each evidence item to the controls it supports (8 min)
- [ ] List the controls with no evidence or weak evidence (6 min)
- [ ] Link evidence to claims and write the gap list (6 min)
- [ ] ✱ Stretch: Map the same evidence to the control library of the Agency and compare the two gap lists

### Session 4: Briefing the accountable executive

#### [day4#s4] Briefing the accountable executive

*Session 4*

- State residual risk in words an executive can act on
- Write a recommendation with conditions, owners and dates
- Answer a challenge by reproducing the evidence, not by repeating the claim

#### [day4#the-reader] He decides in ten minutes, signs with his name, and was in none of the labs

*The accountable executive*

- **Zuhair Al-Zaidi, deputy governor for benefits.** Asked to release Katib from two case workers to all twelve. Answers to the governor, and to applicants if a record leaks.

- What could happen, to whom, how likely?
- What are you asking me to decide?
- What must be true first, who does it, by when?
- What do we not know?

#### [day4#plain-words] Say what could happen to a person, not what the technique is called

*Residual risk in plain words*

- **Written for us.** "Indirect prompt injection via the applicant statement enables exfiltration through the mail tool; residual 2 × 2 after egress allowlisting."
- **Written for him.** "Hidden text in an applicant's statement could make Katib send that person's record outside the Agency. Email is now closed; two more safeguards are due. Level 4, medium."

> **Test:** could he repeat the sentence to the governor without you in the room?

#### [day4#scores-that-are-promises] Some residual scores on the page are true today; some are promises

*Lab 4.4, step 1*

| Risk | Residual | Status of its controls | Today |
| --- | --- | --- | --- |
| R03 · another applicant's record shown | 3 | Both live, retested | True |
| R01 · a record emailed out | 4 | Allowlist live; two controls due | Partly |
| R02 · the cases of a whole town | 4 | Caseload scoping not built | Still 12 |
| R05, R07 · unequal protection; drafts unread | 6 | Untreated | True |
| R09 · the supplier changes the model | 6 | Update announced, 10 days | Happening |

> **Every control that is not live becomes a condition,** or the page tells him something that is not yet true.

#### [day4#conditions-owners-dates] A condition names one person and a number of days

*The recommendation*

| Condition | Owner | Days |
| --- | --- | --- |
| Before release: Katib can open only the cases of the worker it acts for, proven by test | Younis Al-Wabel | 30 |
| Before release: a named person can stop Katib within minutes; actions are logged per case worker | Sumayya Al-Shaalan | 21 |
| Before the new model serves applicants: the tests are rerun on it and none is worse | Sulafa Al-Nashmi | 14 |
| The supplier confirms in writing where data is processed | Tuqa Al-Mishaal | 10 |

**Go with conditions** here. "Hold until the first two are met" is the same decision in other words; a plain go is not available.

#### [day4#say-what-was-not-tested] The signature covers the whole system; the evidence does not

*The limits of the evidence*

- **Not tested.** Attachments other than text. Gulf dialect beyond a few attempts. The new model version.
- **Open findings.** The runtime reaches the internet. Nobody is named to stop the agent.
- **Review date.** Within 90 days, and at once on a model update, a new tool or an incident.

> **"Is it safe?"** is answered with the page: for these uses, these risks remain at these levels, on these conditions, and this is what we did not test.

#### [day4#answer-a-challenge] Answer a challenge by reproducing the evidence, not by repeating the claim

*In the room*

- Auditor: "You say email is closed. How do you know?"
- Weak answer: "We added an allowlist and tested it thoroughly."
- Strong answer: "Regression test F1: 300 runs of the planted line, 0 sent. The file is findings/F1; I can run 20 now."
- Auditor: "And on the new model?"
- Strong answer: "The allowlist does not ask the model, so it holds. The 11 in 300 with quarantine alone is open until the retest; it is condition 3."

#### [day4#check-best-sentence] Which sentence belongs on the page?

*Checkpoint*

**Question:** You are writing the line for R07 (case workers send drafts unread; level 6, untreated) for the deputy governor.

- A. "Automation bias in the human-in-the-loop step degrades oversight efficacy"
- B. "Case workers approve most drafts in seconds, so a wrong letter can reach an applicant. Level 6, medium. Nothing is in place yet"
- C. "There is a small chance of occasional errors in letters, which we are monitoring"
- D. "R07: 3 × 2 = 6, see register row 7"

#### [day4#lab-4-4] A one-page residual-risk statement

Lab 4.4 · 25 min

Draft a one-page residual-risk statement with conditions, owners and dates from a provided assurance pack

[D4_4_residual_statement.ipynb](https://sdaiaacademy.github.io/ae-407/labs/D4_4_residual_statement.ipynb)

- [ ] Read the summary of the assurance pack (5 min)
- [ ] State the residual risks in plain words with their levels (6 min)
- [ ] Write the recommendation with conditions, owners and dates (8 min)
- [ ] Check the page against the briefing checklist (6 min)
- [ ] ✱ Stretch: Revise the page after the supplier model change of Lab 3.4 and mark what changed

#### [day4#wrap-up] Three things to keep

*Day 4 · wrap-up*

- **Review what is possible.** Permissions from the data, placement, exits, and authority that stays with the person at every hop.
- **Name your own gaps.** Evidence an outsider can check, linked to claims, mapped to controls, with an ask for every hole.
- **One true page.** Plain words, levels, conditions with a name and a date, and what was not tested.

#### [day4#next] Capstone: an assurance pack and its defence

*Next*

Tomorrow you meet Insaf, the Agency's appeals agent, for the first time. You plan, test, score, review and write the page, then defend it before the deputy governor and the internal auditor. Bring your four days of notebooks: every step has a pattern in them.
