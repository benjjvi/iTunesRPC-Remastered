Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') and Improper Encoding or Escaping of Output in server.py

### Impact
_What kind of vulnerability is it? Who is impacted?_
This vulnerability is a XSS and Improper Encoding vulnerability. AFAIK, only servers are impacted.

### Patches
_Has the problem been patched? What versions should users upgrade to?_
_~No patches have been released yet.~_ 
As of commit 24f43aa, the issue **has** been fixed. No official releases are affected. Commits 7f9dd665e39f03e068ceb68a40ef257cd2e04b14, b39ad023a08e513205870c10823c2c67f7d768ca, 96cc9f2af75c5ecd846e0eb055230462d063c623, 4d0f88be6598277208af626684b9cda9629e830d, c29b3c842d7dd6ab97a7ad12882a545c6a320051, 953fd83326b1956e8b446a1cc3033bf310711840, 355a474ecfcb44e197a00a749001f8573c8ae647, and 54b02d9f3a94de94e4fb471908b8cf798e62e411 are all still vulnerable.

### Workarounds
_Is there a way for users to fix or remediate the vulnerability without upgrading?_
Users can manually add escaping to the server and client, or upgrade to commit 24f43aa.

### For more information
If you have any questions or comments about this advisory:
* Email us at [report.app.vulnerability@bildsben.tech](mailto:report.app.vulnerability@bildsben.tech)
