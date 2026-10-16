import pathlib,shutil,hashlib,json,subprocess,zipfile
root=pathlib.Path(__file__).resolve().parents[2];out=root/'investigation/artifacts';stage=out/'stage';pkg=out/'windows-netclient-lab'
for sub in ['bin','sbin','etc','var/run','lab']: (pkg/sub).mkdir(parents=True,exist_ok=True)
for name in ['bin/nut.exe','bin/upsc.exe','sbin/upsmon.exe']:shutil.copy2(stage/name,pkg/name)
dll=list(stage.rglob('libupsclient-7.dll'));assert len(dll)==1,dll
for sub in ['bin','sbin']:shutil.copy2(dll[0],pkg/sub/dll[0].name)
for name in ['COPYING','LICENSE-GPL2','LICENSE-GPL3']:
 if (root/name).exists():shutil.copy2(root/name,pkg/name)
(pkg/'etc/nut.conf').write_text('MODE=netclient\n')
(pkg/'etc/upsmon.conf').write_text('''# LAB ONLY. Replace TEST-SERVER with an isolated synthetic NUT server.
MONITOR testups@TEST-SERVER 1 labmon lab-only-password secondary
MINSUPPLIES 1
SHUTDOWNCMD "cmd.exe /c C:\\NUT-Lab\\lab\\record-shutdown.cmd"
POWERDOWNFLAG C:\\NUT-Lab\\var\\run\\powerdown
POLLFREQ 5
POLLFREQALERT 2
DEADTIME 20
FINALDELAY 5
''')
(pkg/'lab/record-shutdown.cmd').write_bytes(b'@echo off\r\necho %DATE% %TIME% NUT shutdown requested>>C:\\NUT-Lab\\lab\\shutdown-requests.log\r\nexit /b 0\r\n')
(pkg/'README.txt').write_text('''WINDOWS X64 LAB PACKAGE - NOT PRODUCTION QUALIFIED

Unchanged upstream source, cross-compiled on ARM64 Linux/MinGW. Unsigned.
TLS disabled. Isolated synthetic test network only; no real UPS credentials.
No Windows execution or Hyper-V shutdown is claimed. No native ARM64 build.

Extract so bin, sbin, etc, lab and var are directly under C:\\NUT-Lab.
Preserve this layout; DLL is alongside each dependent executable.
Replace TEST-SERVER only with an isolated test NUT server and matching lab account.
SHUTDOWNCMD ONLY LOGS. It never calls Windows shutdown.
Review configuration before registering a service; do not install alongside an existing NUT service.

From elevated cmd.exe in C:\\NUT-Lab\\bin:
  nut.exe -V
  upsc.exe testups@TEST-SERVER
  nut.exe -I
  net start "Network UPS Tools"
  sc query "Network UPS Tools"
Confirm upsmon.exe is actually running, not only the service status.
Inspect Windows Event Log and lab\\shutdown-requests.log.
Use investigation/SUPERVISOR-VERIFICATION.md in the source repository for test cases.

Cleanup:
  net stop "Network UPS Tools"
  nut.exe -U
Confirm processes exited before removing the test folder.

Gate: prove config path resolution, unattended startup, disconnect/reconnect,
silent-server timeouts, child failure recovery and logging-only FSD behavior.
Actual shutdown and Hyper-V guest sequencing are later, separately controlled tests.

Source fork: https://github.com/ChrisMcGhan/nut
Exact upstream source revision is in manifest.json. Local build recipes and logs
are retained in investigation/. No patches are included in these binaries.
''')
manifest={'sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'target':'Windows x86-64','tls':False,'runtime_tested':False,'files':{str(p.relative_to(pkg)):hashlib.sha256(p.read_bytes()).hexdigest() for p in pkg.rglob('*') if p.is_file() and p.name!='manifest.json'}}
(pkg/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(out/'windows-netclient-lab-x64.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in pkg.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(pkg))
print(out/'windows-netclient-lab-x64.zip')
