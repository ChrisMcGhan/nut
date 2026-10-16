# Windows netclient: supervisor source verification

Revision fe4e6fec3807017418c6fbc19b007a660d8e409c. Static inspection on macOS only. No Windows binaries built or executed; no production changes. Local DeepSeek R1 32B receives the saved SOURCE-PACKET.txt directly through Ollama, with no tool access or claimed repository exploration. Its output is advisory, not acceptance evidence.

## Implemented behavior

- scripts/Windows/wininit.c:422 registers an automatic-start service under LocalSystem (account argument at 434). netclient branch at 370 starts only upsmon. docs/man/nut.exe.txt documents that architecture.
- clients/upsmon.c:1023 opens the service manager and requests service stop, waits two seconds, then at 1057 invokes the configured shutdown command using system(). This is not a built-in Hyper-V guest sequencing implementation; an external shutdown policy must be tested.

## Three bounded follow-ups

1. Child startup failure is not propagated: create_process returns 0 on failure (wininit.c:123), run_upsmon stores it (227), but netclient parsing returns success unconditionally (375). SvcMain then calls SvcReady, reporting RUNNING. Later recovery checks are conditional on a nonzero upsmon_pid (867). Source supports a false-healthy service state after launch failure; reproduce with a missing upsmon executable in a disposable VM before patching.
2. Mode parsing is substring-based (wininit.c:333-380), ignores comments only when # is the first character, and checks server modes before netclient. An indented comment containing netserver can select server behavior before the actual MODE line. Reproduce with synthetic config and inert child executables. No real UPS drivers should run in this test.
3. Daemon recovery is checked after an infinite WaitForMultipleObjects (775), whose handle list contains pipe events and a stop event, not child process handles. Recovery logic exists (867 onward), but prompt detection of a quiet child death is not demonstrated. Test terminating the monitor after traffic settles and measure restart latency. Do not claim recovery is entirely absent.

## Additional uncertainty

upsmon.c:1220 and 1237 mark Windows alarm helpers as potentially incomplete/not applicable. This alone does not prove network reads lack timeouts: inspect libupsclient and test a silent server before making that claim. The service stop requested before SHUTDOWNCMD also needs a runtime logging-stub test; source alone does not prove the monitor is killed before the command executes.

## Safe Windows validation plan

Use a disposable x64 Windows VM, fixed upstream build and snapshot. Keep it isolated from real UPS equipment. First substitute an absolute-path logging script for SHUTDOWNCMD, never host shutdown. Use a synthetic NUT server.

1. Reboot without login; verify service and upsmon are both running, then log out and repeat checks.
2. Missing executable and malformed/indented config tests: compare reported service state with actual child process and expected mode.
3. Kill monitor, stop/restart synthetic server, and simulate a silent accepted connection: measure recovery and bounded waits.
4. Simulate online, on-battery, recovery, low battery and forced-shutdown states independently; confirm expected stub invocations and no unintended trigger on ordinary communications loss according to documented policy.
5. Simulate shutdown-command failure and a slow logging script; verify logs, process lifetimes and deterministic behavior. Real VM/Hyper-V shutdown requires a later controlled test and is not accepted by these stub checks.

Recommendation: prioritize reproducing startup-failure reporting and mode parsing before broad port modernization. Preserve upstream contribution requirements, including human DCO sign-off; no automatic sign-off or PR publication.

## DeepSeek result review

The direct-source run completed normally: 13,612 input tokens and 920 generated tokens, approximately 202 seconds. The model correctly recognized that netclient starts only upsmon, but its proposed concrete concerns were not acceptable: duplicate upsdrvctl and POWERDOWNFLAG handling are outside the selected netclient path; claims of hangs or incorrect flag handling were not demonstrated; citations omitted file names and did not establish the alleged behavior. Its summary also conflated UPS power-off handling with local OS shutdown. Do not implement its recommendations. The three source-traced follow-ups above are the supervisor's independent findings, not validated DeepSeek findings. This model configuration has not demonstrated reliable autonomous repository investigation.
