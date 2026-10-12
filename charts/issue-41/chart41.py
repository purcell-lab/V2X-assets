src=open('plan/charts.py').read().split('\nfor fn in (')[0].replace('OUT = sys.argv[1]','OUT = "session/out"')
ns={'__file__':'plan/charts.py'}; exec(compile(src,'charts','exec'),ns)
Svg,Panel=ns['Svg'],ns['Panel']

# Measured 5-min means, 12 Oct 16:20-17:05 AEST (export positive, kW)
lab=['16:20','16:25','16:30','16:35','16:40','16:45','16:50','16:55','17:00','17:05']
ev=[1.42,4.95,16.79,25.03,25.06,20.14,17.20,19.24,11.14,7.27]
bs=[7.10,23.96,7.05,0.0,0.0,5.39,10.35,10.14,19.95,24.00]

# Projection 16:20-21:00, 1-min steps. Stores must supply 30 kW export.
def sim(ev_first):
    E,B=0.97*75,0.975*40.3; Ecap,Bcap=75,40.3; out=[]
    for m in range(0,281):
        out.append((100*E/Ecap,100*B/Bcap))
        need=30.0
        evmax=0 if E/Ecap<=0.16 else (25 if E/Ecap>0.30 else 7)
        bmax=0 if B/Bcap<=0.10 else 24
        if ev_first: e=min(evmax,need); b=min(bmax,need-e)
        else: b=min(bmax,need); e=min(evmax,need-b)
        E-=e/60; B-=b/60
    return out
A,Bf=sim(True),sim(False)

s=Svg(720,"Export priority: what the plant did vs EV-first and BESS-first over the evening peak",
      "12 Oct 2026 AEST · Model Y on the DC pile, Amber V2X `discharge`, 30 kW export cap · top: measured 5-min means · bottom: simple projection",
      "Top: stacked export from the EV pile and the home battery, 16:20 to 17:05, against the 30 kW export cap. Bottom: projected home-battery and EV state of charge to 21:00 under EV-first and BESS-first priority.")
# Panel A
p=Panel(s,64,84,770,230,len(lab),0,35,[0,10,20,30],"kW")
p.band(3,5)
s.text(p.cx(4),p.y0+14,"EV alone 25 kW · BESS idle · 5 kW cap unused",'tl',anchor='middle')
for i,(e,b) in enumerate(zip(ev,bs)):
    p.bar(i,e,'s1'); p.bar(i,e+b,'s2',base=e)
p.hline(30,'s3','',side='end')
s.text(p.cx(1),p.y(31.5),"BESS-first",'tl',anchor='middle')
s.text(p.cx(8.5),p.y(31.5),"BESS-first again",'tl',anchor='middle')
p.xlabels(lab,every=1)
s.legend(64,346,[("s1","EV pile export","bar"),("s2","home battery export","bar"),("s3","30 kW export cap","dash")])

# Panel B
x0,y0,w,h=64,410,770,230
X=lambda m: x0+w*m/280; Y=lambda v: y0+h*(100-v)/100
for v in (0,25,50,75,100):
    s.add(f'<line class="{"zero" if v==0 else "grid"}" x1="{x0}" y1="{Y(v):.1f}" x2="{x0+w}" y2="{Y(v):.1f}"/>'); s.text(x0-6,Y(v)+4,f"{v}",anchor="end")
s.text(x0-6,y0-8,"SoC %",anchor="end")
for m,l in ((0,'16:20'),(40,'17:00'),(100,'18:00'),(160,'19:00'),(220,'20:00'),(280,'21:00')):
    s.text(X(m),y0+h+16,l,anchor="middle")
mx=100
s.add(f'<line class="grid" x1="{X(mx):.1f}" y1="{y0}" x2="{X(mx):.1f}" y2="{y0+h}" stroke-dasharray="3 3"/>')
def pl(vals,idx,cls,dash):
    pts=' '.join(f'{X(m):.1f},{Y(v[idx]):.1f}' for m,v in enumerate(vals))
    d=' stroke-dasharray="5 4"' if dash else ''
    s.add(f'<polyline class="{cls}l" fill="none" stroke-width="2" points="{pts}"{d}/>')
pl(A,1,'s2',False); pl(Bf,1,'s2',True); pl(A,0,'s1',False); pl(Bf,0,'s1',True)
ba,bb=A[mx][1],Bf[mx][1]
s.text(X(mx)+6,y0+14,f"If the EV leaves at 18:00 the BESS holds {ba:.0f} % (EV-first) vs {bb:.0f} % (BESS-first)",'tl')
s.legend(64,672,[("s2","BESS SoC, EV-first","line"),("s2","BESS SoC, BESS-first","dash"),("s1","EV SoC, EV-first","line"),("s1","EV SoC, BESS-first","dash")])
s.text(64,696,"Projection: stores supply 30 kW · BESS 40.3 kWh, 24 kW, floor 10 % · EV 75 kWh, 25 kW (7 kW below 30 %, #21), floor 16 %",'t2')
s.save('session/out/issue-41/issue-41-export-priority.svg'); print(ba,bb,A[280],Bf[280])
