import json,datetime as dt
head=open('tri/triage.py').read().split('# ---------- Chart 1')[0]
exec(head)
w=json.load(open('tri/eve.json')); T0=dt.datetime.fromisoformat(w['t0']); N=len(w['bess'])
st=30; ts=list(range(0,N,st))
s=Svg(640,"Evening dispatch 27 Oct: no export until the export limit was raised, then BESS-first",
      "27 Oct 2026 16:20–18:36 AEST · Remote EMS off (Amber V2X in control) · M3P on the DC pile · 30-s means · shaded = Amber decision discharge",
      "Top: grid, home battery and EV pile power with the plan's grid export and Amber discharge windows. Bottom: home battery and EV state of charge.")
s.add('<style>.mutedl{stroke:#8f8e88}</style>')
p=TP(s,64,84,770,320,N,-32,24,[-30,-20,-10,0,10,20],"kW")
D=w['dec']; a=None
for n in range(N+1):
    d=D[n] if n<N else None
    if d=='discharge' and a is None: a=n
    if d!='discharge' and a is not None:
        s.add(f'<rect class="shade" x="{p.x(a):.1f}" y="{p.y0}" width="{p.x(n)-p.x(a):.1f}" height="{p.h}"/>'); a=None
for t in (-30,-20,-10,0,10,20):
    s.add(f'<line class="{"zero" if t==0 else "grid"}" x1="{p.x0}" y1="{p.y(t):.1f}" x2="{p.x0+p.w}" y2="{p.y(t):.1f}"/>')
sec=lambda hm:(dt.datetime.fromisoformat(f'2026-10-27T{hm}+10:00')-T0).total_seconds()
pl=[(sec('16:20:00'),0),(sec('17:00:00'),-11.68),(sec('17:30:00'),-23.07),(sec('18:00:00'),-22.89),(sec('18:30:00'),0),(N,0)]
p.line([x for x,_ in pl],[y for _,y in pl],'muted',dash=True,width=2,step=True)
s.add(f'<line class="critl" x1="{p.x0}" y1="{p.y(-30):.1f}" x2="{p.x0+p.w}" y2="{p.y(-30):.1f}" stroke-width="1" stroke-dasharray="2 3"/>')
p.line(ts,agg(w['grid'],st),'s3',width=2.2)
p.line(ts,agg(w['bess'],st),'s2',width=2.2)
p.line(ts,agg(w['ev'],st),'s1',width=2.2)
xl=p.x(sec('17:22:23'))
s.add(f'<line class="critl" x1="{xl:.1f}" y1="{p.y0}" x2="{xl:.1f}" y2="{p.y0+p.h}" stroke-width="1.5"/>')
s.text(xl+4,p.y0+14,"17:22:23 owner: export limit 0 → 35",'tl')
s.text(p.x(sec('16:52:00')),p.y(-6),"discharge, export limit 0:",'tl'); s.text(p.x(sec('16:52:00')),p.y(-6)+15,"no export",'tl')
s.text(p.x(sec('17:12:00'))-4,p.y(12),"EV → BESS",'tl',anchor='end'); s.text(p.x(sec('17:12:00'))-4,p.y(12)+15,"21 kW",'tl',anchor='end')
s.text(p.x(sec('18:15:10')),p.y(6),"18:15 DC session drop",'tl',anchor='middle')
p.xlabels()
s.legend(64,436,[("s3","grid (− export)","line"),("s2","home battery","line"),("s1","EV pile","line"),("muted","plan grid","dash"),("crit","−30 kW envelope","dash")])
q=TP(s,64,474,770,120,N,50,90,[50,60,70,80,90],"SoC %")
q.line(ts,agg(w['soc'],st),'s2',width=2); q.line(ts,agg(w['esoc'],st),'s1',width=2)
s.text(q.x(N*0.02),q.y(83),"home battery",'tl'); s.text(q.x(N*0.02),q.y(71),"M3P",'tl')
q.xlabels()
s.text(64,628,"Export 12.9 kWh vs 28.8 kWh planned · with the export limit at 35: BESS 10.9 kWh, EV 3.9 kWh (BESS-first, 74 %) · EV→BESS 2.3 kWh",'t2')
s.save('tri/out/issue-40/issue-40-evening-27oct.svg')
