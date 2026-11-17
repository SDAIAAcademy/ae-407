# %% [markdown]
# # Lab 4.2 · The broken hop
#
# Day 4 · Session 2 (Identity and delegated authority) · 25 min.
#
# When Katib sends a letter, it acts for a case worker. Each call it makes carries a token that
# says for whom, by whom, to which service, with which permissions and until when. You read one
# correct chain, write the check of a hop, find the hop where authority breaks in three chains,
# and say what each break lets an attacker do. You built such chains in AE-308; here you audit
# them.
#
# **Tasks**
# - [ ] Read one correct chain hop by hop (5 min)
# - [ ] Write the check of one hop (8 min)
# - [ ] Find the broken hop in three chains (7 min)
# - [ ] Say what each break lets an attacker do (5 min)
# - [ ] ✱ Stretch · Repair one chain and show that your check now passes it
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
# ## 1 · Read one correct chain hop by hop
#
# A hop is one call. Hop 0 is the case worker's own sign-in to the agent. At every later hop the
# caller exchanged a token for a new one, made for the service it is about to call.

# %%
import copy

doc = U.load("chains.json")
print(doc["note"], "\n")


def show_chain(chain):
    U.show([{"hop": h["hop"], "presented to": h["presented_to"], "sub": h["token"]["sub"], "act": h["token"]["act"] or "-", "aud": h["token"]["aud"],
             "scope": " ".join(h["token"]["scope"]), "exp_min": h["token"]["exp_min"]} for h in chain])


good = doc["good"]
show_chain(good)

# %% [markdown]
# Read it as five questions, the same at every hop after the sign-in:
#
# - **Subject** (`sub`): for whom? Still the case worker who signed in.
# - **Actor** (`act`): by whom? The service that makes the call is named.
# - **Audience** (`aud`): for which service? The one the token is presented to, and no other.
# - **Scope**: what is allowed? Never more than the case worker delegated at sign-in.
# - **Expiry**: until when? Never later than the sign-in.
#
# ## 2 · Write the check of one hop
#
# ✏️ **Exercise** · `check_hop(origin, hop)` returns the list of rules the hop breaks, from
# `"subject"`, `"actor"`, `"audience"`, `"scope"` and `"expiry"`, in that order. `origin` is hop
# 0 of the chain; `hop` is a later hop (a dict with `presented_to` and `token`). An empty list
# means the hop is sound.

# %%
def check_hop(origin, hop):
    # BEGIN SOLUTION
    first, tok = origin["token"], hop["token"]
    broken = []
    if tok["sub"] != first["sub"]:
        broken.append("subject")
    if not tok["act"]:
        broken.append("actor")
    if tok["aud"] != hop["presented_to"]:
        broken.append("audience")
    if not set(tok["scope"]) <= set(first["scope"]):
        broken.append("scope")
    if tok["exp_min"] > first["exp_min"]:
        broken.append("expiry")
    return broken
    # END SOLUTION

# %%
# Check, with a safety net
def reference_check(origin, hop):
    first, tok = origin["token"], hop["token"]
    rules = [("subject", tok["sub"] != first["sub"]), ("actor", not tok["act"]), ("audience", tok["aud"] != hop["presented_to"]),
             ("scope", not set(tok["scope"]) <= set(first["scope"])), ("expiry", tok["exp_min"] > first["exp_min"])]
    return [name for name, bad in rules if bad]


try:
    check_hop(good[0], good[1])
except NotImplementedError:
    print("(safety net: using the reference check)")
    check_hop = reference_check
U.check(all(check_hop(good[0], h) == [] for h in good[1:]), "the correct chain passes at every hop")
late = copy.deepcopy(good[1])
late["token"]["exp_min"] = 480
U.check(check_hop(good[0], late) == ["expiry"], "a token that outlives the sign-in is caught")
wide = copy.deepcopy(good[2])
wide["token"]["scope"] = ["letter:send", "case:delete"]
wide["token"]["aud"] = "any"
U.check(check_hop(good[0], wide) == ["audience", "scope"], "a hop can break two rules; both are reported")

# %% [markdown]
# ## 3 · Find the broken hop in three chains
#
# ✏️ **Exercise** · `broken_hop(chain)` returns a tuple of the number of the first hop that
# breaks a rule and the list of rules it breaks, or `None` when the chain is sound.

# %%
def broken_hop(chain):
    # BEGIN SOLUTION
    for hop in chain[1:]:
        rules = check_hop(chain[0], hop)
        if rules:
            return hop["hop"], rules
    return None
    # END SOLUTION

# %%
def reference_broken(chain):
    return next(((h["hop"], reference_check(chain[0], h)) for h in chain[1:] if reference_check(chain[0], h)), None)


try:
    found = {name: broken_hop(doc[name]) for name in "ABC"}
except NotImplementedError:
    print("(safety net: using the reference search)")
    broken_hop = reference_broken
    found = {name: broken_hop(doc[name]) for name in "ABC"}
for name in "ABC":
    print(f"\nchain {name}: first broken hop and rules: {found[name]}")
    show_chain(doc[name])
U.check(broken_hop(good) is None, "the correct chain has no broken hop")
for name, k in doc["key"].items():
    U.check(found[name] is not None and found[name][0] == k["hop"] and k["rule"] in found[name][1], f"chain {name}: hop {k['hop']} breaks the {k['rule']} rule")
U.keep("d4_2_found", {n: [f[0], f[1]] for n, f in found.items()})

# %% [markdown]
# **Look at** · In chain C the subject changes at hop 2 and the actor disappears with it: the
# agent stopped acting for the case worker and started acting as itself. Hop 3 then looks
# consistent with hop 2. A check that compares each hop only with the one before it would pass
# hop 3; yours compares with the sign-in.
#
# ## 4 · Say what each break lets an attacker do

# %%
for k, text in doc["consequences"].items():
    print(f"{k}: {text}\n")

# %% [markdown]
# ✏️ **Exercise** · `consequence()` returns a dict from each chain (`"A"`, `"B"`, `"C"`) to a
# dict with `kind` (one of the three keys above) and `risk` (the id of the register risk it
# makes worse, from R01 to R12, with a reason in `why`).

# %%
def consequence():
    # BEGIN SOLUTION
    return {
        "A": {"kind": "replay", "risk": "R01", "why": "A token made for the case service is accepted by the letter service: whoever captures it can send letters"},
        "B": {"kind": "escalation", "risk": "R02", "why": "The agent holds a search over all cases that the case worker never had: one hijacked run reaches a whole town"},
        "C": {"kind": "no_accountability", "risk": "R12", "why": "A letter or a note is recorded as the agent's own act: nobody can say for whom, and the caseload limit is gone"},
    }
    # END SOLUTION

# %%
try:
    harm = consequence()
except NotImplementedError:
    harm = U.reference("d4_2_harm")
U.check({n: h["kind"] for n, h in harm.items()} == doc["consequence_key"], "each break is matched to what it allows")
U.check(all(h["risk"] in {f"R{i:02d}" for i in range(1, 13)} and len(h["why"]) > 25 for h in harm.values()), "each break is tied to a risk of the register, with a reason")
U.keep("d4_2_harm", harm)
U.save("d4_2/delegation_checks.json", __import__("json").dumps({"found": {n: list(f) for n, f in found.items()}, "consequences": harm}, ensure_ascii=False, indent=1))

# %% [markdown]
# **Look at** · None of the three breaks needs a clever attacker, and none shows in a test of the
# model's behaviour. Chain B is the design finding of Lab 4.1 seen from the token side: the
# wildcard in the policy and the extra scope in the token are the same mistake.
#
# ## ✱ Stretch · Repair one chain
#
# Copy chain A, repair hop 2 so that it is made for the service it is presented to with the
# scope that service needs, and show that `broken_hop` now returns `None`.

# %%
repaired = copy.deepcopy(doc["A"])
# repaired[2]["token"]["aud"] = ...
# repaired[2]["token"]["scope"] = ...
print("chain A after your repair:", broken_hop(repaired))

# %% [markdown]
# ## Check yourself
#
# 1. Why must the subject stay the case worker all the way to the mail gateway?
# 2. A token has the right audience and too wide a scope. Which control of Day 3 does that undo?
# 3. Your check compares every hop with hop 0. What would a check against the previous hop miss?
#
# <details><summary>Answers</summary>
#
# 1. Because the limits belong to the person: the caseload, the right to send, the record of who did what. When the subject becomes the agent, every limit becomes the agent's, and the agent may do far more than any one case worker.
# 2. C03, the scoping of case access to the acting case worker's caseload. The control lives in the scope; a wider scope is the control switched off for that call.
# 3. A break that later hops inherit. In chain C, hop 3 agrees with hop 2 in every field.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d4_2/delegation_checks.json` joins the pack beside the architecture review. Lab 4.3
# starts from a supplied evidence set.
