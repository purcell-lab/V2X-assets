import json,datetime as dt
head=open('tri/triage.py').read().split('# ---------- Chart 1')[0]
exec(head)
TZ=dt.timezone(dt.timedelta(hours=10))
n=json.load(open('tri/night5.json')); cf=json.load(open('tri/cf.json')); P=json.load(open('tri/realprice.json')); FC=json.load(open('tri/fc2025.json'))
T0=dt.datetime(2026,10,27,16,0,tzinfo=TZ); TEND=dt.datetime(2026,10,28,7,0,tzinfo=TZ); N=int((TEND-T0).total_seconds())
sec=lambda t:(t-T0).total_seconds()
s=Svg(716,"Evening 27 Oct: BESS exported to its floor at ~14 c, house then imports at ~21 c",
      "27 Oct 2026 16:00 → 28 Oct 07:00 AEST · Remote EMS off (Amber V2X in control) · actual to 22:40, counterfactuals from 20:26",
      "Top: home battery SoC actual and two counterfactuals. Bottom: import and feed-in prices with export intervals shaded.")
s.add('<style>.mutedl{stroke:#8f8e88}</style>')
p=TP(s,64,84,770,300,N,0,90,[0,20,40,60,80],"SoC %")
tt=[sec(dt.datetime.fromisoformat(x)) for x in n['t']]
# export shading
for x,g in zip(tt,n['grid']):
    if g<-1: s.add(f'<rect class="shade" x="{p.x(x):.1f}" y="{p.y0}" width="{p.x(x+300)-p.x(x):.1f}" height="{p.h}"/>')
for t in (0,20,40,60,80): s.add(f'<line class="{"zero" if t==0 else "grid"}" x1="{p.x0}" y1="{p.y(t):.1f}" x2="{p.x0+p.w}" y2="{p.y(t):.1f}"/>')
s.add(f'<line class="critl" x1="{p.x0}" y1="{p.y(5):.1f}" x2="{p.x0+p.w}" y2="{p.y(5):.1f}" stroke-width="1" stroke-dasharray="2 3"/>')
ct=[sec(dt.datetime.fromisoformat(x)) for x in cf['t']]
p.line(ct,cf['B'],'s3',dash=True,width=2.2); p.line(ct,cf['C'],'s1',dash=True,width=2.2)
p.line([x+150 for x in tt],n['soc'],'s2',width=2.6)
for hm,lab,dy in (('2026-10-27T20:22:10','20:22 EV session stopped by owner (target 50 % reached)',14),('2026-10-27T20:26:03','20:26 Amber "discharge": BESS → grid at 20.9 kW',30)):
    x=p.x(sec(dt.datetime.fromisoformat(hm+'+10:00')))
    s.add(f'<line class="critl" x1="{x:.1f}" y1="{p.y0}" x2="{x:.1f}" y2="{p.y0+p.h}" stroke-width="1.2"/>'); s.text(x+4,p.y0+dy,lab,'tl')
s.text(p.x(N-60),p.y(cf['B'][-1])-6,f"B: self-consume from 52 % → {cf['B'][-1]:.0f} % at 07:00",'tl',anchor='end')
s.text(p.x(N-60),p.y(12),"C: export surplus only, then self-consume",'tl',anchor='end')
s.text(p.x(sec(dt.datetime(2026,10,27,21,55,tzinfo=TZ))),p.y(29),"actual: 5.9 % at 22:40, then grid import",'tl')
xs=[]
t=T0
while t<=TEND:
    s.s=None if False else None
    t+=dt.timedelta(hours=2)
def xl(q):
    t=T0
    while t<=TEND:
        x=q.x(sec(t)); s.add(f'<line class="grid" x1="{x:.1f}" y1="{q.y0+q.h}" x2="{x:.1f}" y2="{q.y0+q.h+4}"/>'); s.text(x,q.y0+q.h+16,t.strftime('%H:%M'),anchor='middle'); t+=dt.timedelta(hours=1)
xl(p)
s.legend(64,414,[("s2","BESS SoC actual","line"),("s3","B: self-consume from 20:26","dash"),("s1","C: sell surplus only","dash"),("crit","5 % floor (assumed)","dash")])
q=TP(s,64,456,770,170,N,0,30,[0,10,20,30],"c/kWh")
for x,g in zip(tt,n['grid']):
    if g<-1: s.add(f'<rect class="shade" x="{q.x(x):.1f}" y="{q.y0}" width="{q.x(x+300)-q.x(x):.1f}" height="{q.h}"/>')
for t in (0,10,20,30): s.add(f'<line class="{"zero" if t==0 else "grid"}" x1="{q.x0}" y1="{q.y(t):.1f}" x2="{q.x0+q.w}" y2="{q.y(t):.1f}"/>')
gp=[(sec(dt.datetime.fromisoformat(a)),v*100) for a,v in P['gp']]; fi=[(sec(dt.datetime.fromisoformat(a)),v*100) for a,v in P['fi']]
q.line([a for a,_ in gp],[v for _,v in gp],'s2',width=2,step=True); q.line([a for a,_ in fi],[v for _,v in fi],'s3',width=2,step=True)
fg=sorted((sec(dt.datetime.fromisoformat(k+':00+10:00')),v*100) for k,v in FC['GF'].items() if dt.datetime.fromisoformat(k+':00+10:00')>dt.datetime(2026,10,27,22,40,tzinfo=TZ) and dt.datetime.fromisoformat(k+':00+10:00')<=TEND)
ff=sorted((sec(dt.datetime.fromisoformat(k+':00+10:00')),v*100) for k,v in FC['FF'].items() if dt.datetime.fromisoformat(k+':00+10:00')>dt.datetime(2026,10,27,22,40,tzinfo=TZ) and dt.datetime.fromisoformat(k+':00+10:00')<=TEND)
q.line([a for a,_ in fg],[v for _,v in fg],'s2',dash=True,width=2,step=True); q.line([a for a,_ in ff],[v for _,v in ff],'s3',dash=True,width=2,step=True)
xl(q)
s.legend(64,664,[("s2","import price (dashed = forecast known at 20:25)","line"),("s3","feed-in price","line"),("muted","shaded = grid export > 1 kW","bar")])
s.text(64,690,"Amber costAnalysis winner = Discharge in 82 of 82 daemon cycles, 15:56–22:36,",'t2'); s.text(64,707,"including at BESS 6.0 % with import 23.7 c against feed-in 12.9 c.",'t2')
s.save('tri/out/issue-new/overnight-27oct-bess-drain.svg')
