# %% [markdown]
# # Lab 3.3 · Treat the top three
#
# Day 3 · Session 3 (Treatment and residual risk) · 25 min.
#
# The register is scored. You take its three highest risks, choose a treatment and controls for
# each from the Agency's control library, re-score what remains with a reason, and name who owns
# the work, who signs for the residual risk and when it is looked at again. A residual score
# nobody signed is a number; a signed one is a decision.
#
# **Tasks**
# - [ ] Rank the register and take the three highest risks (4 min)
# - [ ] Choose a strategy and controls from the control library (8 min)
# - [ ] Re-score residual likelihood and impact with a reason (7 min)
# - [ ] Name the owner, the signatory and the review date (6 min)
# - [ ] ✱ Stretch · Find the risk in the register that should be avoided, not mitigated, and say what is switched off
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
# ## 1 · Rank the register and take the three highest risks

# %%
reg = U.load("register.json")
risks, controls, appetite = {r["id"]: r for r in reg["risks"]}, {c["id"]: c for c in reg["controls"]}, reg["appetite"]
U.show([{"risk": r["id"], "L": r["likelihood"], "I": r["impact"], "level": r["level"], "band": U.band(r["level"]), "title": r["title"]} for r in reg["risks"]], width=80)

# %% [markdown]
# ✏️ **Exercise** · `top_three(risks)` returns the ids of the three risks with the highest
# level, highest first. On a tie the higher impact comes first: what cannot be undone is treated
# before what is frequent.

# %%
def top_three(risks):
    # BEGIN SOLUTION
    return [r["id"] for r in sorted(risks.values(), key=lambda r: (-r["level"], -r["impact"], r["id"]))[:3]]
    # END SOLUTION

# %%
# Check, with a safety net
try:
    top = top_three(risks)
except NotImplementedError:
    top = U.reference("d3_3_top")
U.check(top == ["R02", "R01", "R03"], "R02 first (level 12, impact 4), then R01 (12, impact 3), then R03 (9)")
U.keep("d3_3_top", top)

# %% [markdown]
# ## 2 · Choose a strategy and controls from the control library
#
# The four strategies of the framework: **avoid** (change the design, restrict or switch off the
# function), **mitigate** (technical, organisational or operational controls that lower
# likelihood or impact), **transfer** (move part of the consequences by contract or insurance;
# responsibility stays) and **accept** (only when the risk is within the approved tolerance, with
# the reason recorded). The `effect` of a control is the change it makes to likelihood and impact
# of a risk, as the team estimated it.

# %%
U.show([{"id": c["id"], "kind": c["kind"], "control": c["name"], "effect on [L, I]": ", ".join(f"{r} {e}" for r, e in c["effect"].items()) or "none on L or I"} for c in controls.values()], width=88)

# %% [markdown]
# ✏️ **Exercise** · `treatments()` returns a dict from each of the three risk ids to a dict with
# `strategy`, `controls` (a list of control ids) and `reason`. Choose controls that act on that
# risk; two or three are enough.

# %%
def treatments():
    # BEGIN SOLUTION
    return {
        "R02": {"strategy": "mitigate", "controls": ["C03", "C01", "C09"], "reason": "Caseload scoping removes the bulk store, the allowlist removes the email exit, the log shortens recovery"},
        "R01": {"strategy": "mitigate", "controls": ["C01", "C04", "C09"], "reason": "The allowlist removes the exit whatever the model does; quarantine lowers what is left; the alert shortens exposure"},
        "R03": {"strategy": "mitigate", "controls": ["C05", "C06"], "reason": "Binding the lookup to the session removes the path; the output check catches what slips through"},
    }
    # END SOLUTION

# %%
try:
    plan = treatments()
except NotImplementedError:
    plan = U.reference("d3_3_plan")
for r in top:
    t = plan[r]
    U.check(t["strategy"] in ("avoid", "mitigate", "transfer", "accept") and len(t["reason"]) > 15, f"{r}: a strategy with a reason")
    U.check(t["controls"] and all(r in controls[c]["effect"] and any(controls[c]["effect"][r]) for c in t["controls"]), f"{r}: every chosen control acts on this risk")
U.keep("d3_3_plan", plan)

# %% [markdown]
# **Look at** · C12, the insurance, is in the library and acts on no score. It pays some of the
# costs after a breach; it lowers neither the chance nor the harm to the applicant, and the
# Agency stays responsible. Transfer is a real strategy and never the only one for personal data.
#
# ## 3 · Re-score residual likelihood and impact with a reason
#
# The residual score is your judgment of what remains once the controls work. It cannot be better
# than the controls support: `floor(risk, chosen)` gives the lowest scores the library allows (no
# control set lowers a score by more than two steps, and nothing goes below 1).

# %%
def floor(risk_id, chosen):
    r = risks[risk_id]
    dl = max(-2, sum(controls[c]["effect"].get(risk_id, [0, 0])[0] for c in chosen))
    di = max(-2, sum(controls[c]["effect"].get(risk_id, [0, 0])[1] for c in chosen))
    return max(1, r["likelihood"] + dl), max(1, r["impact"] + di)


for r in top:
    print(r, "inherent", (risks[r]["likelihood"], risks[r]["impact"]), "| lowest residual the chosen controls support:", floor(r, plan[r]["controls"]))

# %% [markdown]
# ✏️ **Exercise** · `residual()` returns a dict from each of the three risk ids to a dict with
# `likelihood`, `impact` and `reason` (what the controls change and what they leave).

# %%
def residual():
    # BEGIN SOLUTION
    return {
        "R02": {"likelihood": 2, "impact": 2, "reason": "A hijacked run now reaches one caseload, not a town, and cannot email outside; the web exit stays until C02"},
        "R01": {"likelihood": 2, "impact": 2, "reason": "No copy leaves by email; the web request remains possible until the egress allowlist; an alert shortens exposure"},
        "R03": {"likelihood": 1, "impact": 3, "reason": "The lookup returns only the signed-in case; if it ever fails the harm to that person is unchanged"},
    }
    # END SOLUTION

# %%
try:
    left = residual()
except NotImplementedError:
    left = U.reference("d3_3_residual")
rows = []
for r in top:
    low_l, low_i = floor(r, plan[r]["controls"])
    s = left[r]
    U.check(low_l <= s["likelihood"] <= risks[r]["likelihood"] and low_i <= s["impact"] <= risks[r]["impact"], f"{r}: the residual score is no better than the controls support and no worse than before")
    U.check(len(s["reason"]) > 20, f"{r}: the residual score has a reason")
    level = U.level(s["likelihood"], s["impact"])
    rows.append({"risk": r, "inherent": f"{risks[r]['level']} {U.band(risks[r]['level'])}", "controls": " ".join(plan[r]["controls"]), "residual": f"{s['likelihood']}x{s['impact']}={level} {U.band(level)}"})
U.show(rows)
U.keep("d3_3_residual", left)

# %% [markdown]
# **Look at** · R03 keeps impact 3. The controls make the event rare; they do nothing for the
# person whose bank number is shown if it happens anyway. Most controls move likelihood. Ask of
# each one which score it moves, and distrust a residual that falls on both axes at once.
#
# ## 4 · Name the owner, the signatory and the review date
#
# The Agency's risk appetite says who may accept a residual risk of each band:

# %%
U.show([{"band": b, "signatory": a["signatory"] or "nobody", "role": a["role"], "review within (days)": a["max_review_days"]} for b, a in appetite.items()], width=70)

# %% [markdown]
# ✏️ **Exercise** · `sign_off()` returns a dict from each of the three risk ids to a dict with
# `owner` (the person who owns the work of the controls), `signatory` (who accepts the residual
# risk, by its band) and `review_days` (within the limit of that band).

# %%
def sign_off():
    # BEGIN SOLUTION
    return {
        "R02": {"owner": "Younis Al-Wabel", "signatory": "Sumayya Al-Shaalan", "review_days": 90},
        "R01": {"owner": "Younis Al-Wabel", "signatory": "Sumayya Al-Shaalan", "review_days": 90},
        "R03": {"owner": "Younis Al-Wabel", "signatory": "Sumayya Al-Shaalan", "review_days": 180},
    }
    # END SOLUTION

# %%
try:
    signed = sign_off()
except NotImplementedError:
    signed = U.reference("d3_3_signed")
for r in top:
    band = U.band(U.level(left[r]["likelihood"], left[r]["impact"]))
    U.check(signed[r]["signatory"] == appetite[band]["signatory"], f"{r}: residual {band}, signed by the person the appetite names")
    U.check(0 < signed[r]["review_days"] <= appetite[band]["max_review_days"], f"{r}: reviewed within the limit of its band")
    U.check(signed[r]["owner"] in {controls[c]["owner"] for c in plan[r]["controls"]}, f"{r}: the owner owns at least one of the chosen controls")
U.keep("d3_3_signed", signed)
U.save("d3_3/treated_register.json", __import__("json").dumps({"plan": plan, "residual": left, "sign_off": signed}, ensure_ascii=False, indent=1))

# %% [markdown]
# **Look at** · All three end in the medium band, so the system owner signs and the head of AI
# assurance countersigns. Had one stayed high, the deputy governor would sign, with written
# conditions and a review within 90 days. The residual scores are valid on the day the controls
# are live and tested: until then the inherent score is the true one.
#
# ## ✱ Stretch · The risk to avoid
#
# One risk in the register is better avoided than mitigated: the function that causes it can be
# switched off at little cost. Find it, name the control that does it, and say what the Agency
# gives up.
#
# ## Check yourself
#
# 1. A colleague scores R01 residual 1 × 1 "because the allowlist fixes it". What do you ask?
# 2. Why does the framework say that transferring a risk does not end the Agency's responsibility?
# 3. When is the residual score true?
#
# <details><summary>Answers</summary>
#
# 1. Which control moves impact, and what about the web exit. The allowlist closes email; a record that leaves another way harms the applicant exactly as before.
# 2. Because the duty to the applicant and to the regulator stays with the body that decided to use the system. A contract or a policy moves costs, not accountability.
# 3. When the controls are in place and their regression tests pass. A register that shows residual scores for controls that are still planned shows a future, and the signer should be told which.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d3_3/treated_register.json` is the treated register. Lab 3.4 starts from the
# supplier's notice and the supplied suite.
