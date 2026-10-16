# Pre-Windows preparation result

Source revision: fe4e6fec3807017418c6fbc19b007a660d8e409c. Branch codex/windows-netclient-investigation. Production source unchanged; no commits or pushes.

## Completed

- Native ARM64 Debian container with MinGW x86-64 cross compiler built on the Mac. Docker base pinned in recipe; installed package versions recorded in artifacts/toolchain-packages.txt. Apt versions are recorded, not snapshot-pinned.
- Bootstrap, configure, build and staged install passed for unchanged upstream. Configure flags: --host=x86_64-w64-mingw32 --build=aarch64-linux-gnu --prefix=/ --with-all=no --without-ssl --without-doc --with-confdir=/etc. Full logs retained under artifacts/. An initial ignored --with-client option was removed and the complete build rerun successfully.
- Selected installed nut.exe, upsc.exe and upsmon.exe are Windows PE32+ x86-64. Packaged libupsclient-7.dll next to dependent executables. Recursive package import inspection showed only that bundled DLL plus ADVAPI32, KERNEL32, WS2_32 and msvcrt Windows system DLLs. This is static dependency verification, not execution.
- windows-netclient-lab-x64.zip passes ZIP integrity checking and includes per-file SHA256 manifest, source revision, licensing, layout instructions and a shutdown command that only appends a log entry. Sample server is a placeholder; no production credentials.
- Extracted actual upstream parse_nutconf function into a native C harness with inert process stubs. Plain netclient selects monitor only. An indented comment containing netserver before MODE=netclient selects server behavior. Reproduction and compiler warnings saved in artifacts/parser-check.txt. This demonstrates parser logic, not WinAPI behavior.

## Build limits

TLS disabled: use only an isolated synthetic test environment. Binaries are unsigned and not production-qualified. No Windows runtime, Windows service, shutdown privilege or Hyper-V behavior has been tested. Cross-compiled tests were not executed. The build generated additional upstream tools, but the ZIP deliberately contains only the three network-client programs and their DLL. No native ARM64 executable is provided.

Libtool emitted nonfatal host-path conversion messages for uninstalled executables, while make and staged install exited successfully. The package uses installed executables, but only Windows execution can confirm the staged layout works. Full log is retained; this is not a warning-free build claim.

## Reproduce on Mac

From repository root:

```
docker build -t nut-windows-cross:local investigation/build
mkdir -p investigation/artifacts
docker run --rm --network none --cpus 4 --memory 4g -v "$PWD:/source:ro" -v "$PWD/investigation/artifacts:/out" nut-windows-cross:local sh /source/investigation/build/compile.sh
docker run --rm --network none -v "$PWD:/source:ro" nut-windows-cross:local python3 /source/investigation/build/check_mode_parser.py
python3 investigation/build/package.py
```

Source remains read-only to containers; builds use their disposable filesystem. All configuration sample paths need verification on Windows. Next required platform gate is an isolated Windows VM running the logging-only baseline tests in SUPERVISOR-VERIFICATION.md. Do not infer safe host shutdown from successful compilation.
