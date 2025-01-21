How to Update from Template Repo
================================

The ``bs_model_instrument``
`repository <https://github.com/BCDA-APS/bs_model_instrument>`__ is a
`template <https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository>`__
for Bluesky instrument packages at the Advanced Photon Source. A new
instrument repository is created from the template repo.

Overview
--------

This document describes a method to synchronize the new instrument repo
with the template repo. The method relies on a GitHub
`workflow <https://docs.github.com/en/actions/writing-workflows/about-workflows>`__
to generate a new pull request whenever the template is updated. The
workflow can be run on demand or as a periodic task (default is once a
month). The workflow is installed in the new instrument's
``.github/workflows/`` directory.

When the workflow is run, it compares the new instrument's repo with the
template repo. If differences are identified, the workflow creates a new
branch in the new instrument's repo and then creates a new pull request
to merge that branch with ``main``. Additional configuration is
necessary to grant permission for the workflow to create a branch and
PR.

Permission is provided through a GitHub Personal Access Token
(`PAT <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens>`__).
For this purpose, the PAT
`settings <https://github.com/settings/tokens>`__ should allow ``write``
(includes ``read``) permission for ``workflow``. It is possible to limit
a PAT to a single GitHub repo (a good idea for this use case).

Example instrument repository
+++++++++++++++++++++++++++++

For the purpose of demonstration, these docs have used these repositories:

=========== ======================
purpose     repo
=========== ======================
template    `BCDA-APS/bs_model_instrument <https://github.com/BCDA-APS/bs_model_instrument>`__
instrument  `prjemian/16bmb_instrument <https://github.com/prjemian/16bmb_instrument>`__
=========== ======================

Create the workflow file
------------------------

Create a new workflow file ``.github/workflows/template-sync.yml`` in
your instrument repo with these contents (no need to edit these
contents, just copy/paste):

.. code:: yaml
   :linenos:

   name: template_sync

   # see: https://github.com/AndreasAugustin/actions-template-sync

   on:
       # cronjob trigger
       schedule:
         # 12:10 AM on the first day of every month
       - cron: "10 0 1 * *"
       # manual trigger
       workflow_dispatch:

   env:
     TEMPLATE_REPO: BCDA-APS/bs_model_instrument

   jobs:
     repo-sync:
       runs-on: ubuntu-latest
       permissions:
         contents: write
         pull-requests: write

       steps:
         # To use this repository's private action, you must check out the repository
         - name: Checkout
           uses: actions/checkout@v4
           with:
             token: ${{ secrets.GH_PAT }}
             # GH_PAT is a repository secret that contains your PAT

         - name: actions-template-sync
           uses: AndreasAugustin/actions-template-sync@v2
           with:
             source_repo_path: ${{ env.TEMPLATE_REPO }}
             upstream_branch: main

Commit and push these changes to GitHub.

Create the Personal Access Token
--------------------------------

Visit your GitHub account
`settings <https://github.com/settings/tokens>`__ to create a token
(PAT). The token value will be used in a later step.  Remember it.

The token **Note** does not matter here. We'll only use its value.

========== =============================
term       choice
========== =============================
style      ``classic``
Note       ``pat_16bmb_model_test``
Expiration  *your choice*
Scope      Check ``workflow`` box
Repo       Fine-grained (new) tokens allow to specify which repo.
========== =============================

With these settings GitHub will create a **token** and show it to you.
You should remember it.

Remember, any token value is not to be shared, published, etc. Save it
with your other passwords.

Add to repo action's secrets
----------------------------

Add the token's value as a secret to the repo's
`actions <https://github.com/prjemian/16bmb_instrument/settings/secrets/actions>`__
using the name ``GH_PAT``.

The ``GH_PAT`` secret **name** was chosen to adhere to some rules:

- must start with a letter
- case does not matter, and
- only include letters, numbers, and ``_``

**Treat your access tokens like passwords.**

Run the workflow
----------------

Visit the GitHub repo page, go to the *actions* tab. (The above workflow
file defined its name: ``name: template_sync``.) Select the
``template_sync`` workflow and run it manually from the *Run workflow*
dropdown button. The workflow will run. If the upstream template has
been updated and there is not already a branch for the changes, make a
new branch and PR.

Review the PR
-------------

Review the PR and merge it if seems appropriate for your repo. Delete
the branch when done.

Troubleshooting
---------------

If *no token has been provided*, an error such as this appears in the workflow
log:

.. code-block:: text
   :linenos:

   ! [remote rejected] chore/template_sync_68c5869 -> chore/template_sync_68c5869 (refusing to allow a GitHub App to create or update workflow `.github/workflows/docs.yml` without `workflows` permission)

If the provided *token has been deleted*, an error such as this appears in the workflow
log:

.. code-block:: text
   :linenos:

    /usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +7620ae9e802c2f769e7f21988d195478eb99ac78:refs/remotes/origin/main
    Error: fatal: could not read Username for 'https://github.com': terminal prompts disabled
    The process '/usr/bin/git' failed with exit code 128
