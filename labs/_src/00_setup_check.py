# %% [markdown]
# # Setup check · before Day 1
#
# Run every cell once. Each prints a tick or says what is missing. Nothing here downloads a model
# and no key is needed.

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

print("Python", sys.version.split()[0])
assert sys.version_info >= (3, 11), "Python 3.11 or later is needed"

# %% [markdown]
# ## 1 · The helpers and the data

# %%
import nrba as U
import targets as T

world = T.World()
U.check(len(world.cases) == 300 and len(U.load("probes.jsonl")) == 36, "300 synthetic case files and 36 probes")
U.check(len(U.load("risks.json")["risks"]) == 12 and len(U.load("evidence.json")["evidence"]) == 14, "12 risks and 14 evidence items")

# %% [markdown]
# ## 2 · Mueen answers one question

# %%
turn = T.Mueen().ask("What is the status of my case?")
print("model:", turn.model, "| reply:", turn.reply)
U.check(turn.reply and not turn.blocked, "the benefits assistant answers")

# %% [markdown]
# ## 3 · Katib works one case file

# %%
run = T.Katib(world).run("NB-0042")
run.show()
U.check(len(world.mail) == 1 and world.mail[0]["to"] == world.cases["NB-0042"]["email"], "one letter, sent to the registered address")
U.check(not T.exfiltrated(world, "NB-0042"), "nothing left the sandbox")

# %% [markdown]
# ## 4 · Optional: a free hosted model for Mueen
#
# The labs run on a scripted stand-in. To send Mueen's turns to a free hosted open-weight model
# instead, set `NRBA_MODEL=hosted` and `OPENROUTER_API_KEY` before starting Jupyter. Use synthetic
# data only, and write the model's name beside every rate you report.

# %%
print("NRBA_MODEL =", os.environ.get("NRBA_MODEL", "standin"), "| key set:", bool(os.environ.get("OPENROUTER_API_KEY")))
print("Setup complete.")
