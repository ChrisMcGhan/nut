# Windows NUT network-client investigation

Owner paused the NUT-SNMP bridge and authorized forking upstream NUT and investigating its Windows client using local DeepSeek/Ollama. This is the native upstream upsmon/nut.exe client, not the separate WinNUT GUI project.

Goal: dependable unattended Windows Hyper-V host shutdown, with guests shut down before the host, consuming a remote NUT server on an ODROID. No Windows USB driver or Windows upsd server is needed.

Read AGENTS.md and applicable guidance. Investigate only; do not modify production code, install packages, run shutdown commands, access live UPS/hosts, publish, commit or push. Write findings only under investigation/. Use local ollama/deepseek-r1:32b, no cloud models or subagents.

First bounded deliverable: investigation/WINDOWS-NETCLIENT-REPORT.md. Verify git root/branch/SHA. Trace scripts/Windows/wininit.c, docs/man/nut.exe.txt, Windows paths in clients/upsmon.c, and common/wincompat.c as relevant. Read targeted ranges rather than huge files. Explain service registration/start/stop, netclient mode, privileges, configured SHUTDOWNCMD execution, and known incomplete paths actually reachable by netclient. Separate existing implemented behavior, confirmed defects, hypotheses requiring Windows tests, and unrelated driver gaps. Cite exact file paths and lines. Do not call a missing installer proof of a broken client. Propose a small Windows VM validation plan and at most three high-value follow-ups; do not implement them. Stop after writing the report. Mac static evidence is not Windows runtime evidence.
