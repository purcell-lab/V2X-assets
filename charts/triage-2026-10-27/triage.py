import json,csv,os,sys,datetime as dt
src=open('plan/charts.py').read().split('\nLAB = ')[0].replace('OUT = sys.argv[1]','OUT = "tri/out"')
a=src.index('PLAN = os.path'); b=src.index('\nW = ')
src=src[:a]+src[b:]
ns={'__file__':'plan/charts.py'}; exec(compile(src,'charts','exec'),ns)
Svg,esc=ns['Svg'],ns['esc']
OUT='tri/out'
w=json.load(open('tri/w1s.json'))
T0=dt.datetime.fromisoformat(w['t0']); N=len(w['bess'])
def agg(a,step):
    out=[]
    for i in range(0,N,step):
        v=[x for x in a[i:i+step] if x is not None]; out.append(sum(v)/len(v) if v else None)
    return out
class TP:
    """time panel: x in seconds since T0"""
    def __init__(s,svg,x0,y0,wd,h,tmax,ymin,ymax,ticks,unit):
        s.s,s.x0,s.y0,s.w,s.h,s.tmax,s.ymin,s.ymax=svg,x0,y0,wd,h,tmax,ymin,ymax
        for t in ticks:
            svg.add(f'<line class="{"zero" if t==0 else "grid"}" x1="{x0}" y1="{s.y(t):.1f}" x2="{x0+wd}" y2="{s.y(t):.1f}"/>'); svg.text(x0-6,s.y(t)+4,f"{t:g}",anchor="end")
        svg.text(x0-6,y0-8,unit,anchor="end")
    def x(s,t): return s.x0+s.w*t/s.tmax
    def y(s,v): return s.y0+s.h*(s.ymax-max(s.ymin,min(s.ymax,v)))/(s.ymax-s.ymin)
    def line(s,ts,vals,cls,dash=False,width=2,step=False):
        pts=[];prev=None
        for t,v in zip(ts,vals):
            if v is None: continue
            if step and prev is not None: pts.append(f'{s.x(t):.1f},{s.y(prev):.1f}')
            pts.append(f'{s.x(t):.1f},{s.y(v):.1f}'); prev=v
        d=' stroke-dasharray="5 4"' if dash else ''
        s.s.add(f'<polyline class="{cls}l" fill="none" stroke-width="{width}" stroke-linejoin="round" points="{" ".join(pts)}"{d}/>')
    def xlabels(s,every_min=10):
        m0=(T0.minute*60+T0.second)
        first=(600-m0%600)%600
        t=first
        while t<=s.tmax:
            lab=(T0+dt.timedelta(seconds=t)).strftime('%H:%M')
            s.s.add(f'<line class="grid" x1="{s.x(t):.1f}" y1="{s.y0+s.h}" x2="{s.x(t):.1f}" y2="{s.y0+s.h+4}"/>')
            s.s.text(s.x(t),s.y0+s.h+16,lab,anchor="middle"); t+=every_min*60

# ---------- Chart 1: live Amber window ----------
def chart_live():
    st=30; ts=list(range(0,N,st))
    s=Svg(720,"Amber self-consume: pile limit up to 16 kW, EV takes 0.7 kW, BESS absorbs the PV",
          "27 Oct 2026 12:15:38–13:22:23 AEST · Remote EMS off (Amber V2X in control) · M3P on the DC pile at 72–73 %, car limit 95 % · 30-s means",
          "Top: PV, home battery and EV pile power with the DC pile charge limit written by Amber and the ESS max charging limit of 0. Bottom: EV pile power at 1 s with the running-state reversals.")
    tmax=N
    p=TP(s,64,84,770,300,tmax,-3,20,[0,5,10,15,20],"kW")
    lim=w['lim']
    p.line(ts,agg(lim,st),'s1',dash=True,width=2,step=True)
    p.line(ts,agg(w['pv'],st),'s3',width=2)
    p.line(ts,agg(w['bess'],st),'s2',width=2.2)
    p.line(ts,agg(w['ev'],st),'s1',width=2.4)
    s.add(f'<line class="critl" x1="{p.x0}" y1="{p.y(0)-1:.1f}" x2="{p.x0+p.w}" y2="{p.y(0)-1:.1f}" stroke-width="2" stroke-dasharray="2 3"/>')
    s.text(p.x0+6,p.y(0)+16,"ESS max charging limit = 0 kW since 12:10:26 (red dotted) — the BESS still charges at up to 17.8 kW",'tl')
    
    p.xlabels()
    s.legend(64,414,[("s3","PV","line"),("s2","home battery (+ charge)","line"),("s1","EV pile measured","line"),("s1","DC pile charge limit","dash"),("crit","ESS charge limit","dash")])
    # bottom
    q=TP(s,64,474,770,170,tmax,-1,2.5,[-1,0,1,2],"kW")
    ts1=list(range(0,N,5)); q.line(ts1,[w['ev'][i] for i in ts1],'s1',width=1.2)
    rs=w['rs']
    for i in range(1,N):
        if rs[i]!=rs[i-1] and rs[i]=='Discharging':
            s.add(f'<line class="critl" x1="{q.x(i):.1f}" y1="{q.y0+q.h-8}" x2="{q.x(i):.1f}" y2="{q.y0+q.h}" stroke-width="1"/>')
    s.text(q.x0+6,q.y0-10,"EV pile at 5 s · red ticks = switch to Discharging · 103 reversals in 66 min, median hold 10 s, DC discharge limit 0",'tl')
    q.xlabels()
    s.text(64,690,"Energy 12:15:38–13:22:23: PV 14.06 kWh · BESS +11.75 kWh · EV +0.80 / −0.03 kWh · grid +0.03 / −0.02 kWh",'t2'); s.text(64,708,"The DC pile charge limit Amber wrote would have allowed about 11.9 kWh into the EV over the same window.",'t2')
    s.save(f'{OUT}/issue-38/issue-38-amber-window-27oct.svg')

P=list(csv.DictReader(open('tri/plan1321.csv')))
for r in P:
    for k in r:
        if k not in('t','act'): r[k]=float(r[k])
LAB=[r['t'][3:] for r in P]
SUB="Amber V2X plan published 27 Oct 2026 13:21:07 AEST · 50 intervals, 13:00 27 Oct to 14:00 28 Oct AEST"
Panel=ns['Panel']
def chart_resid():
    s=Svg(420,"A · Site balance still leaves out the home battery: residual up to 13.7 kW in the current interval","Plan published 27 Oct 2026 13:21:07 AEST · residual = grid + solar − load − BESS − EV per interval, should be 0",
          "Bars per interval of the plan's site-balance residual; 42 of 50 intervals are non-zero, largest −13.67 kW in the current interval.")
    p=Panel(s,64,84,770,270,len(P),-14,2,[-14,-10,-6,-2,0,2],"kW")
    for i,r in enumerate(P):
        p.bar(i,r['resid'],'crit' if abs(r['resid'])>0.05 else 'muted',frac=0.7)
    p.xlabels(LAB,every=4)
    s.text(p.cx(1),p.y(-13.67)+4,"13:00 current interval: −13.67 kW = −batteryKw",'tl')
    s.text(p.cx(18),p.y(-5),"42 of 50 intervals non-zero (|r| > 0.05 kW)",'tl')
    s.legend(64,395,[("crit","residual ≠ 0","bar"),("muted","balanced","bar")])
    s.save(f'{OUT}/issue-31/issue-31-residual-27oct.svg')
def chart_comp():
    rows=[r for r in P if abs(r['ev'])>5 and r['act']!='selfConsume']
    s=Svg(360,"E · Grid-side EV energy still booked as home-side: 63.8 kWh of g2v/v2g booked as 1.43 kWh",SUB,
          "Grouped bars for the six EV dispatch intervals: grid-implied EV energy versus booked g2v or v2g.")
    p=Panel(s,64,84,770,210,len(rows),0,14,[0,4,8,12],"kWh")
    for i,r in enumerate(rows):
        h=r['dur']/60; imp=min(abs(r['grid']),abs(r['ev']))*h
        bk=abs(r['g2v'] if r['ev']>0 else r['v2g'])
        p.bar(i,imp,'s3',frac=0.3,off=-0.17); p.bar(i,max(bk,0.06),'crit',frac=0.3,off=0.17)
        s.text(p.cx(i)-0.17*p.slot,p.y(imp)-4,f"{imp:.1f}",'ax',anchor='middle'); s.text(p.cx(i)+0.17*p.slot,p.y(bk)-4,f"{bk:.2f}",'ax',anchor='middle')
    p.xlabels([f"{r['t']} {'v2g' if r['ev']<0 else 'g2v'}" for r in rows],every=1)
    s.legend(64,338,[("s3","grid-side EV energy implied by the plan's own grid figure","bar"),("crit","booked g2v / v2g","bar")])
    s.save(f'{OUT}/issue-35/issue-35-components-27oct.svg')
def chart_cost():
    costs=[("discharge",-26.33),("preserve",0.0),("selfConsume",18.47),("charge",38.94)]
    s=Svg(300,"F · The cost analysis still picks discharge; the plan still selects self-consume",
          "Plan 27 Oct 2026 13:21:07 AEST, current interval 13:00 · marginal cost in cents · lower is better · gridNoEV −14.28 kW, import 12.91 c, export 8.73 c",
          "Horizontal bars: discharge −26.33 c is the winner, selfConsume +18.47 c is selected.")
    x0,wd,y0=170,560,80; lo,hi=-30,45
    X=lambda v:x0+wd*(v-lo)/(hi-lo)
    for t in(-30,-15,0,15,30,45):
        s.add(f'<line class="{"zero" if t==0 else "grid"}" x1="{X(t):.1f}" y1="{y0-6}" x2="{X(t):.1f}" y2="{y0+4*42}"/>'); s.text(X(t),y0+4*42+16,f"{t} c",anchor="middle")
    for k,(n,v) in enumerate(costs):
        y=y0+k*42; cls="s3" if n=="discharge" else("s1" if n=="selfConsume" else "muted")
        a,b=sorted((X(0),X(v)))
        if b-a>0.5: s.add(f'<rect class="{cls}" x="{a:.1f}" y="{y:.1f}" width="{b-a:.1f}" height="24" rx="3"/>')
        s.text(x0-10,y+16,n,'tl',anchor='end')
        tag={"discharge":"  ← costAnalysis winner","selfConsume":"  ← selectedAction"}.get(n,"")
        s.text(max(X(v),X(0))+6,y+16,f"{v:+.2f} c{tag}",'tl')
    s.save(f'{OUT}/issue-36/issue-36-cost-vs-action-27oct.svg')
def chart_solar():
    S=dict(l.strip().split(',') for l in open('tri/solcast.csv'))
    A=json.load(open('tri/pv30.json'))
    rows=[r for r in P if r['t'] in S or r['pv']>0]
    s=Svg(400,"G · Plan solar forecast is 23 % of Solcast: 18.9 kWh planned vs 81.1 kWh forecast",SUB+" · solar per 30-min interval",
          "Bars of plan solar_kw per interval beside the Solcast estimate and measured PV.")
    p=Panel(s,64,84,770,240,len(rows),0,18,[0,5,10,15],"kW")
    for i,r in enumerate(rows):
        p.bar(i,r['pv'],'s2',frac=0.32,off=-0.17); p.bar(i,float(S.get(r['t'],0)),'muted',frac=0.32,off=0.17)
    act=[A.get(r['t']) for r in rows]
    for i,v in enumerate(act):
        if v is not None: p.dot(i,v,'s3')
    p.xlabels([r['t'] for r in rows],every=3)
    s.text(p.cx(len(rows)-2)-10,p.y(0)-6,"plan 0.0 →",'tl',anchor='end')
    s.legend(64,368,[("s2","plan solar_kw","bar"),("muted","Solcast pv_estimate","bar"),("s3","measured PV, 13:00–13:25 mean","bar")])
    s.save(f'{OUT}/issue-37/issue-37-solar-forecast-27oct.svg')
for f in sys.argv[1:]: globals()['chart_'+f]()
