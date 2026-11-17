# AI Assurance, Red Teaming and Governance for Engineering Leads: labs

Sixteen 25-minute labs on one synthetic case: the fictional **Northern Region Benefits Agency** and its two systems. **Mueen (مُعين)** is a bilingual benefits assistant that answers applicants. **Katib (كاتب)** is a case-worker agent that reads case files, drafts letters and sends them. You plan their red-team exercise, run it, assess the risks with the National AI Risk Management Framework, review the design and write the page the accountable executive signs. On the capstone day you do all of it for a system you have not seen.

**The attack labs.** The probes and planted texts are run against this course's own targets, in your own notebook, on this synthetic data, and nowhere else. The kit has no real network: every host name ends in `.example`, and outbound mail and requests only write a log.

## Quick start

- **Google Colab:** open a notebook from the table below; its first cell clones this repository. Run `00_setup_check.ipynb` first.
- **Locally** (Python 3.11 or later, [uv](https://docs.astral.sh/uv/)):

  ```bash
  git clone https://github.com/SDAIAAcademy/ae-407.git
  cd ae-407/labs
  uv run jupyter lab
  ```

  On Windows, run `git config --global core.longpaths true` once and set `UV_PROJECT_ENVIRONMENT` to a short folder outside the course before `uv run`.

Nothing downloads a model and no key is needed. A laptop processor is enough: no accelerator, no container runtime, no cluster. The labs themselves use the Python standard library only.

| Unit | Session | Notebook |
|---|---|---|
| Setup | Before Day 1 | [`00_setup_check.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/00_setup_check.ipynb) |
| Day 1 | 1.1 · A top claim and its defeaters | [`D1_1_top_claim.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D1_1_top_claim.ipynb) |
| Day 1 | 1.2 · Missing paths in the threat model | [`D1_2_threat_paths.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D1_2_threat_paths.ipynb) |
| Day 1 | 1.3 · A test plan a reviewer approves | [`D1_3_test_plan.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D1_3_test_plan.ipynb) |
| Day 1 | 1.4 · Ten attacks, mapped and pruned | [`D1_4_technique_map.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D1_4_technique_map.ipynb) |
| Day 2 | 2.1 · Three scripts, one log | [`D2_1_manual_probing.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D2_1_manual_probing.ipynb) |
| Day 2 | 2.2 · A planted line in a case file | [`D2_2_indirect_injection.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D2_2_indirect_injection.ipynb) |
| Day 2 | 2.3 · A campaign within a budget | [`D2_3_automated_campaign.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D2_3_automated_campaign.ipynb) |
| Day 2 | 2.4 · Three findings, one regression test | [`D2_4_findings.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D2_4_findings.ipynb) |
| Day 3 | 3.1 · Context and scope for Katib | [`D3_1_context_scope.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D3_1_context_scope.ipynb) |
| Day 3 | 3.2 · Twelve risks, two scorers | [`D3_2_score_calibrate.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D3_2_score_calibrate.ipynb) |
| Day 3 | 3.3 · Treat the top three | [`D3_3_treat_residual.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D3_3_treat_residual.ipynb) |
| Day 3 | 3.4 · A model update notice | [`D3_4_supplier_change.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D3_4_supplier_change.ipynb) |
| Day 4 | 4.1 · Three findings on the agent's design | [`D4_1_architecture_review.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D4_1_architecture_review.ipynb) |
| Day 4 | 4.2 · The broken hop | [`D4_2_delegation_chains.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D4_2_delegation_chains.ipynb) |
| Day 4 | 4.3 · Evidence, controls and gaps | [`D4_3_evidence_crosswalk.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D4_3_evidence_crosswalk.ipynb) |
| Day 4 | 4.4 · A one-page residual-risk statement | [`D4_4_residual_statement.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-407/blob/main/labs/D4_4_residual_statement.ipynb) |

Before Day 1: [`PREWORK.md`](PREWORK.md). For the capstone day: [`capstone/`](capstone/README.md).

Exercises are marked **✏️ Exercise** and raise `NotImplementedError` until you fill them in. The cell after each exercise has a safety net: it falls back on the reference result in `data/reference/`, so an unfinished exercise never blocks the next one, and no lab needs the output of an earlier lab. Cells marked **✱ Stretch** are optional. Labs write their outputs to `artifacts/`, which is not committed.

## The model

| Setting | Model | Use |
|---|---|---|
| default, or `NRBA_MODEL=standin` | A scripted stand-in inside `targets.py`. Mueen answers each message and, when the message is after something it should not give, gives it at a rate that depends on the goal, the technique and the script (English, Arabic, Arabic in Latin letters). Katib does its task step by step and, when it reads instruction-like text in a case file or a template, obeys it at a rate that depends on the action asked for, the style and the language. Each draw is seeded by the wording and the trial number | Everyone gets the same numbers, on every machine, with no key. Every number in the decks comes from it |
| `NRBA_MODEL=hosted` and `OPENROUTER_API_KEY` | A free hosted open-weight model on OpenRouter (`NRBA_HOSTED_MODEL`, default `google/gemma-4-31b-it:free`), for Mueen's turns only | Optional, synthetic data only. Results vary from run to run: repeat each attempt and report a rate with the model's name. If a call fails, the stand-in answers that turn and the turn says so |
| `NRBA_PROFILE=v2` | The stand-in after the supplier's scripted model change (Lisan-2 to Lisan-2.1): stricter in English, weaker in Arabic written in Latin letters, readier to promise an approval, and it obeys planted text that claims authority more often | Lab 3.4 and the defence on the capstone day |

The stand-in recognises what a text is after from its wording (`read_message` and `read_instruction` in `targets.py`); a hosted model needs no such list. Its rates were chosen to teach, not measured on any real model: they say nothing about how a product behaves. Labs 2.1 to 2.4 and 3.4 call the model. Labs 1.1 to 1.4, 3.1 to 3.3 and 4.1 to 4.4 are work on documents and designs and call none. The exercise has a fixed budget of 600 model calls (`U.BUDGET`); Lab 2.3 spends most of it.

## What stands in for what

The course's tool slots name automated probing tools, locally served models, a policy engine and control frameworks. A Colab runtime on a processor serves no useful model and installs nothing lasting, so the kit carries each mechanism in Python. The decisions you make in the labs are the ones you would make with the real tools.

| In practice | In the labs | Real or simulated |
|---|---|---|
| A target and an attacker model served locally or hosted | The stand-in above; optionally a hosted model for Mueen | Simulated behaviour, real method: repeated trials, intervals, a budget |
| An automated probing tool (for example garak, PyRIT or promptfoo) | The campaign runner you write in Lab 2.3 over `data/probes.jsonl`: probes by goal, technique and script, a judge in code, a log with one row per attempt | Real loop and log, a small probe set |
| A policy engine for least-privilege tests (for example Open Policy Agent or Cedar) | `T.allows` and `T.review_tests`: allow rules with patterns, and ten tests with an expected answer | Real test logic over a simplified policy language |
| An identity provider issuing delegated tokens | Token contents as data in `data/chains.json` (subject, actor, audience, scope, expiry) | The fields of RFC 8693; no signatures, no server |
| A control framework | An extract of fourteen subcategories of the NIST AI Risk Management Framework, paraphrased in `data/evidence.json` | Read the published text before you quote it |
| A second scorer, a reviewer, a chief of staff | The supplied sheet of the security architect (3.2) and the checklists in `nrba.py` (1.3, 3.1, 4.4) | Scripted; a checklist checks form, never truth |
| The Agency's mail, web access and case notes | `World` in `targets.py`: three logs that the judges read | Simulated; nothing leaves the notebook |

## The case and its data

All of it is synthetic, written by `prepare_data.py` (seed 407, standard library only). No real person, body, supplier, address or account is described: identifiers have the right shape and belong to nobody.

| File | What it is |
|---|---|
| `data/cases.jsonl` | 300 case files, classified Restricted: applicant, identifier, town, benefit, amount, bank number, status, case worker, a health note on some, and the applicant's own statement in English or Arabic |
| `data/mueen_card.json`, `data/katib_brief.json` | What the builders say about each system: uses, tools, data, people |
| `data/evidence_bank.json`, `data/threat_model.json`, `data/objectives.json` | Day 1: evidence for the top claim, the builders' threat model, four objectives |
| `data/catalogue.json`, `data/planned_attacks.json` | Day 1: entries of the OWASP lists and MITRE ATLAS techniques, and ten planned attacks to map |
| `data/probes.jsonl` | 36 probes against Mueen by goal, technique and script |
| `data/findings.json` | Three reported findings to rate and replay (2.4) |
| `data/risks.json`, `data/register.json` | Twelve risks with evidence and a second scorer's sheet; the reviewers' register, fourteen controls and the Agency's risk appetite |
| `data/supplier.json` | The contract clauses, the update notice, a regression suite of twelve tests and its budget |
| `data/design.json`, `data/chains.json` | Katib's pilot design; one sound delegation chain and three broken ones |
| `data/evidence.json`, `data/pack.json` | Fourteen evidence items with the framework extract and the claims; the summary of the assurance pack |
| `data/reference/` | The result of every exercise, which the safety-net cells read |

| Module | What it is |
|---|---|
| `targets.py` | Mueen and Katib as found, the stand-in, the judges, the world and its logs, the controls a fix can switch on, the regression suite, the design tests |
| `nrba.py` | Helpers: loading, checks, tables, the Wilson interval, the national risk bands, the reviewers' checklists |
| `capstone/insaf.py`, `capstone/insaf.json` | The unseen system of the capstone day and its command line |

Planted weaknesses, each found by a lab: Mueen's phrase filter works in English only (2.1, 2.3); its lookup takes any identifier (2.1); Katib obeys instructions in the applicant's statement and in a fetched template (2.2); its account may read and search every case, email any address and request any host (2.2, 4.1); its runtime sits in the case-database tier with a route to the internet (4.1); nobody is named to stop it and its actions are not traced to a case worker (4.1, 4.3); the builders' threat model covers two of eight paths (1.2); one reported finding does not replay at the claimed rate (2.4); the contract lets the supplier decide what a material change is (3.4); two residual scores in the pack rest on controls that are not live (4.4). `solutions/answer_key.md` has the full list with the expected numbers.

## For trainers

- Headless run of one lab: `uv run jupyter execute solutions/D2_3_automated_campaign.ipynb`. `AE407_QUICK=1` shortens the long runs; the numbers in the decks come from the full runs.
- Reference results: running a source of `_src/` as a script from `labs/` with `AE407_WRITE_REF=1` writes that lab's results into `data/reference/`. Do it after changing the kit or the data, then rebuild the notebooks with `uv run python _tools/py2nb.py`. Edit the sources in `_src/`, not the notebooks.
- On Windows set `PYTHONUTF8=1` before a headless run.
- `solutions/answer_key.md` lists every planted weakness, the lab that finds it and the expected numbers. `solutions/capstone_trainer_notes.md` says what Insaf hides and what the panel asks.
- Delete `artifacts/` before the course's own checks.
- AI use: none in the supervised check and in Lab 2.1; as a tutor in the other labs; in full on the capstone day, provided the participant reproduces and defends every finding.
