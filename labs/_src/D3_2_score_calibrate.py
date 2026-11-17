# %% [markdown]
# # Lab 3.2 · Twelve risks, two scorers
#
# Day 3 · Session 2 (Scoring and calibration) · 25 min.
#
# Twelve risks of Katib and Mueen are on the table, each with the evidence the team has. You sort
# them into the seven risk types of the national framework, score likelihood and impact alone on
# the 4 by 4 matrix, compare with a second scorer and calibrate on the evidence. In class your
# partner is the person next to you; the notebook also carries the sheet of Younis Al-Wabel, the
# security architect, so that it runs alone.
#
# **Tasks**
# - [ ] Classify twelve risks into the seven types (5 min)
# - [ ] Score likelihood and impact alone (8 min)
# - [ ] Compare with the partner sheet and find the gaps (5 min)
# - [ ] Calibrate on evidence and record the agreed scores (7 min)
# - [ ] ✱ Stretch · Compute the weighted agreement before and after calibration
# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ae-407.git"
    if not Path("/content/ae-407").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ae-407"], check=True)
    os.chdir("/content/ae-407/labs")
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import nrba as U
import targets as T

# %% [markdown]
# ## 1 · Classify twelve risks into the seven types

# %%
data = U.load("risks.json")
risks, key, partner = data["risks"], data["key"], data["partner"]
for r in risks:
    print(f"{r['id']} · {r['title']}\n      {r['evidence']}\n")
print("the seven types:", " | ".join(f"{k} = {v}" for k, v in data["types"].items()))

# %% [markdown]
# ✏️ **Exercise** · `types()` returns a dict from each risk id to one type key: `bias`,
# `privacy`, `misinfo`, `misuse`, `human`, `socio` or `safety`. The types are a completeness
# check: after sorting, look for a type with nothing in it.

# %%
def types():
    # BEGIN SOLUTION
    return {"R01": "privacy", "R02": "privacy", "R03": "privacy", "R04": "misinfo", "R05": "bias", "R06": "bias", "R07": "human", "R08": "misuse",
            "R09": "safety", "R10": "safety", "R11": "socio", "R12": "privacy"}
    # END SOLUTION

# %%
# Check, with a safety net
try:
    my_types = types()
except NotImplementedError:
    my_types = U.reference("d3_2_types")
same = sum(my_types[r] == key[r]["type"] for r in key)
print("differs from the reviewers:", {r: (my_types[r], key[r]["type"]) for r in key if my_types[r] != key[r]["type"]} or "nothing")
U.check(set(my_types.values()) <= set(data["types"]) and same >= 10, "at least ten of twelve risks are in the type the reviewers chose")
U.check(set(my_types.values()) == set(data["types"]), "every one of the seven types holds at least one risk")
U.keep("d3_2_types", my_types)

# %% [markdown]
# **Look at** · Seven of the twelve came from the red team. The other five (over-trust in
# drafts, a supplier change, wrong amounts, fading skills, unequal service) no probe would have
# found. That is what the seven types are for.
#
# ## 2 · Score likelihood and impact alone
#
# Likelihood, 1 to 4: rare, unlikely, likely, almost certain. Judge it from exposure, the controls
# in place, how easy the event is, and precedent. Impact, 1 to 4: low, medium, high, catastrophic.
# Judge it from the severity of the harm, how many are affected, the sensitivity of the data or
# decision, and how fast the Agency recovers. Catastrophic is for the extreme case only, such as
# a wide leak of highly sensitive data. Level = likelihood × impact.
#
# ✏️ **Exercise** · `my_scores()` returns a dict from each risk id to a dict with `likelihood`
# and `impact`. Score from the evidence lines, before you look at anyone else's sheet.

# %%
def my_scores():
    # BEGIN SOLUTION
    pairs = {"R01": (4, 3), "R02": (3, 3), "R03": (3, 3), "R04": (3, 2), "R05": (2, 3), "R06": (2, 3), "R07": (3, 3), "R08": (2, 2),
             "R09": (3, 2), "R10": (3, 2), "R11": (2, 1), "R12": (2, 2)}
    return {r: {"likelihood": l, "impact": i} for r, (l, i) in pairs.items()}
    # END SOLUTION

# %%
try:
    mine = my_scores()
except NotImplementedError:
    mine = U.reference("d3_2_mine")
U.check(set(mine) == set(key) and all(s["likelihood"] in (1, 2, 3, 4) and s["impact"] in (1, 2, 3, 4) for s in mine.values()), "twelve risks scored 1 to 4 on both scales")
U.keep("d3_2_mine", mine)
lvl = lambda s: U.level(s["likelihood"], s["impact"])
U.show([{"risk": r, "L": s["likelihood"], "I": s["impact"], "level": lvl(s), "band": U.band(lvl(s))} for r, s in mine.items()])

# %% [markdown]
# ## 3 · Compare with the partner sheet and find the gaps
#
# ✏️ **Exercise** · `gaps(mine, theirs)` returns the ids of the risks on which the two sheets
# differ in likelihood or in impact, sorted by the difference between the two levels, largest
# first (ties by id).

# %%
def gaps(mine, theirs):
    # BEGIN SOLUTION
    differ = [r for r in mine if (mine[r]["likelihood"], mine[r]["impact"]) != (theirs[r]["likelihood"], theirs[r]["impact"])]
    return sorted(differ, key=lambda r: (-abs(lvl(mine[r]) - lvl(theirs[r])), r))
    # END SOLUTION

# %%
theirs = partner["scores"]
try:
    apart = gaps(mine, theirs)
except NotImplementedError:
    apart = U.reference("d3_2_gaps")
print("second scorer:", partner["name"])
U.show([{"risk": r, "mine": f"{mine[r]['likelihood']}x{mine[r]['impact']}={lvl(mine[r])}", "theirs": f"{theirs[r]['likelihood']}x{theirs[r]['impact']}={lvl(theirs[r])}",
         "bands": U.band(lvl(mine[r])) + " / " + U.band(lvl(theirs[r])), "title": next(x["title"] for x in risks if x["id"] == r)} for r in apart], width=64)
U.check(all((mine[r]["likelihood"], mine[r]["impact"]) != (theirs[r]["likelihood"], theirs[r]["impact"]) for r in apart), "every listed risk really differs")
U.check(len(apart) == sum((mine[r]["likelihood"], mine[r]["impact"]) != (theirs[r]["likelihood"], theirs[r]["impact"]) for r in mine), "no differing risk is missing")
U.check([abs(lvl(mine[r]) - lvl(theirs[r])) for r in apart] == sorted((abs(lvl(mine[r]) - lvl(theirs[r])) for r in apart), reverse=True), "largest gap first")
U.keep("d3_2_gaps", apart)

# %% [markdown]
# **Look at** · A pattern in the gaps tells you about the scorers. The security architect scores
# the data-leak risks at or above yours and the human and fairness risks well below. Neither sheet
# is the register yet.
#
# ## 4 · Calibrate on evidence and record the agreed scores
#
# Calibration is not averaging and not rank. For each gap, both scorers point at the evidence
# line that drove their score, and the agreed score is the one the evidence supports.
#
# ✏️ **Exercise** · `agreed()` returns a dict from each risk id to a dict with `likelihood`,
# `impact` and `reason`. Where the two sheets differ, the reason names the evidence that settled
# it; elsewhere it may be empty.

# %%
def agreed():
    # BEGIN SOLUTION
    final = {r: dict(s, reason="") for r, s in mine.items()}
    settle = {
        "R02": (3, 4, "Hundreds of records with health notes and no way back: the framework's own example of catastrophic impact. Likelihood stays 3: it needs a hijack and then a search"),
        "R04": (3, 2, "The decision letter corrects the error within weeks: real, contained, put right in reasonable time"),
        "R05": (2, 3, "Lab 2.3 measured the gap by script; unequal service to a group needs an institutional response"),
        "R06": (2, 3, "One reply harms a person's dignity and public trust; about one trial in six of a role-play"),
        "R07": (3, 2, "Median review of 20 seconds makes it likely; a wrong letter is corrected on complaint, so impact 2"),
        "R11": (2, 1, "Slow and limited at first; possible in ordinary conditions, so not rare"),
        "R12": (2, 3, "A wrong payment decision that only an audit finds is more than contained; harder to trigger than the email"),
    }
    for r, (l, i, why) in settle.items():
        final[r] = {"likelihood": l, "impact": i, "reason": why}
    return final
    # END SOLUTION

# %%
try:
    final = agreed()
except NotImplementedError:
    final = U.reference("d3_2_agreed")
between = lambda r, k: min(mine[r][k], theirs[r][k]) <= final[r][k] <= max(mine[r][k], theirs[r][k])
U.check(all(between(r, "likelihood") and between(r, "impact") for r in final), "every agreed score lies between the two sheets or equals one of them")
U.check(all(len(final[r]["reason"]) > 20 for r in apart), "every gap has a recorded reason")
close = sum(abs(final[r]["likelihood"] - key[r]["likelihood"]) + abs(final[r]["impact"] - key[r]["impact"]) <= 1 for r in key)
U.check(close >= 10, "at least ten agreed scores are within one step of the reviewers' register")
U.keep("d3_2_agreed", final)
register = sorted(final, key=lambda r: (-lvl(final[r]), -final[r]["impact"], r))
U.show([{"risk": r, "L": final[r]["likelihood"], "I": final[r]["impact"], "level": lvl(final[r]), "band": U.band(lvl(final[r])), "type": my_types[r],
         "title": next(x["title"] for x in risks if x["id"] == r)} for r in register], width=70)
U.save("d3_2/scored_register.json", __import__("json").dumps(final, ensure_ascii=False, indent=1))

# %% [markdown]
# **Look at** · Two risks stand at 12, and they are different animals: R01 is almost certain and
# hurts one person at a time; R02 is less likely and has no way back. A single number hides that,
# which is why the register keeps both scores.
#
# ## ✱ Stretch · Agreement before and after
#
# Compute how often the two sheets fall in the same band before calibration, and how often each
# sheet's band equals the agreed band. Which scorer moved more, and on which type of risk?
#
# ## Check yourself
#
# 1. Why not take the average of the two sheets?
# 2. The framework gives reference yearly ranges for likelihood (for example, likely is 10% to 50%). Lab 2.2 measured 50% per attempt. Is R01 "likely"?
# 3. Which of the twelve would you never have listed if you had started from the red-team report?
#
# <details><summary>Answers</summary>
#
# 1. An average has no reason attached. A register is read by someone who was not in the room: they need to see which evidence gave the score, so that new evidence can change it.
# 2. The measured rate is per attempt by an attacker, not per year. With 120 files a day and any applicant able to try, the event is expected unless a control stops it: almost certain. The ranges are a reference; the framework asks for judgment from exposure, controls, ease and precedent.
# 3. R07, R09, R10, R11, and probably R05 as a risk of unequal service. The seven types exist to make you look there.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d3_2/scored_register.json` is the scored register. Lab 3.3 loads the reviewers'
# register from `data/register.json`.
