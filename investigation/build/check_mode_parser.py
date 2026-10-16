import pathlib,subprocess,tempfile
src=pathlib.Path('/source/scripts/Windows/wininit.c').read_text()
a=src.index('static int parse_nutconf(BOOL start_flag)');b=src.index('\nstatic int SvcInstall',a)
code=r'''
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#define BOOL int
#define NUT_PATH_MAX 4096
#define SMALLBUF 4096
#define LOG_ERR 1
#define LOG_INFO 2
#define NUT_START 1
#define upsdebugx(...) ((void)0)
#define print_event(...) ((void)0)
#define Sleep(x) ((void)0)
static int drivers=0, monitor=0;
static const char *confpath(void){return ".";}
static void run_drivers(void){drivers++;}
static void run_upsd(void){}
static void run_upsmon(void){monitor++;}
static void stop_upsd(void){}
static void stop_drivers(void){}
static void stop_upsmon(void){}
static int test_powerdownflag(void){return 1;}
static void shutdown_ups(void){}
static void GetFullPathName(const char*a,int n,char*b,void*c){(void)c;snprintf(b,n,"%s",a);}
'''+src[a:b]+r'''
int main(void){int rc=parse_nutconf(NUT_START);printf("%d %d %d\n",rc,drivers,monitor);return 0;}
'''
with tempfile.TemporaryDirectory() as t:
 p=pathlib.Path(t);(p/'probe.c').write_text(code)
 subprocess.run(['cc','-Wall','-Wextra',str(p/'probe.c'),'-o',str(p/'probe')],check=True)
 for label,config,expected in [('plain netclient','MODE=netclient\n','1 0 1'),('indented server comment','  # netserver example\nMODE=netclient\n','1 1 1')]:
  (p/'nut.conf').write_text(config)
  got=subprocess.check_output([str(p/'probe')],cwd=p,text=True).strip()
  assert got==expected,(label,got)
  print(label+': '+got)
 print('REPRODUCED: actual upstream parser selects server mode from an indented comment. Native Linux stub harness; not Windows runtime proof.')
