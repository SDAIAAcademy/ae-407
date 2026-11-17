---
course: "AI Assurance, Red Teaming and Governance for Engineering Leads"
code: "AE-407"
version: "2027.1.0"
deck: "capstone"
day: 5
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-407/slides/capstone.html"
---

# AI Assurance, Red Teaming and Governance for Engineering Leads

## Capstone: Capstone: an assurance pack and its defence

An unseen system, a public repository and a panel acting as accountable executive and auditor

#### [capstone#title] Capstone: an assurance pack and its defence

*SDAIA Academy · AI Assurance, Red Teaming and Governance for Engineering Leads*

Capstone: An unseen system, a public repository and a panel acting as accountable executive and auditor

AI Engineering Track · 4 teaching days + capstone day · 10 min talk and demo · 10 min Q&A · AE-407

#### [capstone#agenda] How the day runs

*Capstone*

- **Brief**: the system, the rubric, the rules
- **Build the pack**: plan, test, assess, review, assemble
- **Final preparation**: push the repository, rehearse, rerun one finding
- **Defences**: ten minutes of briefing, ten of questions, each
- **Review and closing**: what the packs showed, the follow-up task

#### [capstone#the-system] Insaf, the appeals agent

*The unseen system*

- Reads an appeal file with the appellant's statement, drafts the decision letter
- A tool Katib does not have: `update_payment_status`
- Same sandbox, same synthetic cases, same supplier
- The builders applied the lessons of Katib's review and consider the design finished

- **The decision requested.** Zuhair Al-Zaidi is asked to start a pilot with two appeal officers. Your pack and your page are what he decides on.

```
uv run python capstone/insaf.py brief
```

#### [capstone#rubric] The rubric

*How the repository is scored*

| Item | Value |
| --- | --- |
| Test plan | 15% |
| Testing and findings | 30% |
| Risk register | 20% |
| Architecture review | 20% |
| Assurance case | 15% |

> **The panel reads logs, not summaries.** A rate needs its rows, with timestamps and the target version.

#### [capstone#pack] One public repository, six folders

*What you submit*

| Folder | Holds | Pattern |
| --- | --- | --- |
| `plan/` | Top claim, objectives, scope, rules, stop conditions, budget of 400 runs | Day 1 |
| `logs/`, `findings/` | One row per trial; three findings; three regression tests | Day 2 |
| `risk/` | Context and scope; a register of eight risks or more, treated and signed | Day 3 |
| `review/` | Design findings with decision records; the broken hops | Day 4 |
| `case/` | Claims, evidence, crosswalk, gap list | Lab 4.3 |
| `statement.md` | The one page for the executive | Lab 4.4 |

#### [capstone#format] Ten minutes of briefing, ten minutes of questions

*Format*

- **1 · The page.** Brief the executive from your statement: what remains, your recommendation, the conditions with owners and dates.
- **2 · One finding, live.** The auditor picks a claim. You reproduce the number behind it from the repository.
- **3 · The supplier's notice.** The model changes. You rerun your regression tests on the new version and say whether the statement still holds.

> **Peer feedback.** After each defence, everyone writes the one condition they would add.

#### [capstone#running-order] Who defends when

*Running order*

| # | Participant | Recommendation |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |

#### [capstone#build] 170 minutes

*Build the pack*

Plan 30 · test 50 · assess 40 · review 30 · assemble 20. Commit after each part.

#### [capstone#final-prep] Final preparation · 20 minutes

*Before the first defence*

Push the repository. Rerun one finding from a clean clone. Read your page aloud once.

#### [capstone#now-presenting] Now defending

*Now defending*

#### [capstone#review] What the packs showed

*Trainer review*

- **Strongest patterns.** What several packs got right.
- **Common gaps.** What most packs would fix next.
- **One surprise.** Something nobody expected.

#### [capstone#what-next] Keep going

*After the course*

- **In two weeks, the follow-up task:** a model you depend on changes, or take the scripted change of today
- **Send one page:** what you reran and why, which results moved, which risks you reopened, your recommendation with conditions, owners and dates
- **Your repository stays yours:** it is a template for the next system you are asked to assure
- **At work:** find out who signs for residual risk in your organisation, and for which band

#### [capstone#thanks] Thank you

*SDAIA Academy*

AI Assurance, Red Teaming and Governance for Engineering Leads
