import json,pathlib,urllib.request,subprocess
root=pathlib.Path(__file__).resolve().parents[1]
selections={'scripts/Windows/wininit.c':[(1,800)],'clients/upsmon.c':[(940,1100)],'docs/man/nut.exe.txt':[(1,150)]}
chunks=[]
for name,ranges in selections.items():
 lines=(root/name).read_text().splitlines()
 for a,b in ranges: chunks.append('\nFILE '+name+'\n'+'\n'.join(f'{i}: {lines[i-1]}' for i in range(a,min(b,len(lines))+1)))
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
prompt='''Investigate native Windows NUT netclient only. You have NO TOOLS. The exact source excerpts below are your only evidence. Do not claim you read any other files, ran tests, or wrote files. Produce a concise report with: implemented service and shutdown flow; at most 3 concrete source-backed concerns; hypotheses requiring Windows runtime tests; five safe validation cases using a disposable VM and logging shutdown stub. Cite supplied path:line. Clearly distinguish inference from demonstrated defect. Do not discuss USB driver problems unrelated to netclient. Never invent paths. Source SHA: '''+sha+'\n'+''.join(chunks)
(root/'investigation/SOURCE-PACKET.txt').write_text(prompt)
req=urllib.request.Request('http://127.0.0.1:11434/api/chat',data=json.dumps({'model':'deepseek-r1:32b','messages':[{'role':'user','content':prompt}],'stream':False,'options':{'num_ctx':32768,'num_predict':8192,'temperature':0.1}}).encode(),headers={'Content-Type':'application/json'})
with urllib.request.urlopen(req,timeout=1200) as r: data=json.load(r)
(root/'investigation/DEEPSEEK-SOURCE-REVIEW.md').write_text('# DeepSeek source review - unverified model output\n\nRevision: '+sha+'\n\n'+data['message']['content'])
(root/'investigation/REVIEW-METRICS.json').write_text(json.dumps({k:v for k,v in data.items() if k!='message'},indent=2))
print('Report saved. Completion reason:',data.get('done_reason'))
