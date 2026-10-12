import datetime as dt
src=open('plan/charts.py').read().split('\nfor fn in (')[0].replace('OUT = sys.argv[1]','OUT = "session/out"')
ns={'__file__':'plan/charts.py'}; exec(compile(src,'charts','exec'),ns)
Svg=ns['Svg']
T=lambda s: dt.datetime.fromisoformat('2026-10-11T'+s+'+10:00')
ev=[('21:43:00',0),('21:43:10',-2.57),('21:43:25',-4.87),('21:43:36',-6.49),('21:43:46',-5.22),('21:44:01',-2.76),('21:44:07',-3.62),('21:45:00',-3.5),('21:46:09',-3.58),('21:46:15',-7.07),('21:46:30',-6.88),('21:47:30',-6.89),('21:48:16',-6.88),('21:48:24',-0.81),('21:49:00',-0.91),('21:50:00',-0.95),('21:51:00',-0.96)]
bs=[('21:43:00',0.0),('21:43:10',-2.80),('21:43:20',-2.49),('21:43:25',-0.77),('21:43:31',0.0),('21:44:01',-1.03),('21:44:07',0.0),('21:46:09',0.0),('21:46:15',2.72),('21:46:30',3.04),('21:46:35',5.59),('21:47:00',5.75),('21:48:16',5.77),('21:48:19',5.76),('21:48:24',0.02),('21:51:00',0.0)]
gr=[('21:43:00',0.94),('21:43:10',-3.92),('21:43:31',-2.03),('21:43:46',-1.57),('21:44:01',-0.01),('21:51:00',0.0)]
t0,t1=T('21:43:00'),T('21:51:00')
s=Svg(420,"J · Under Amber V2X control the EV discharges ~6.9 kW into the home battery",
      "11 Oct 2026, 21:43–21:51 AEST · PV 0 · vehicle at 28 % on the DC pile · 5 s samples · kW",
      "EV pile, home battery and grid power. While the remote EMS switch is off (Amber V2X in control) the EV discharges at its low-SoC limit and the home battery charges from it.")
x0,y0,w,h=64,84,770,250; ymin,ymax=-8,8
X=lambda t: x0+w*(t-t0).total_seconds()/(t1-t0).total_seconds()
Y=lambda v: y0+h*(ymax-v)/(ymax-ymin)
s.add(f'<rect class="shade" x="{X(T("21:46:10")):.1f}" y="{y0}" width="{X(T("21:48:19"))-X(T("21:46:10")):.1f}" height="{h}"/>')
s.text(X(T("21:46:10"))+4,y0+14,"Amber V2X in control (switch off) 21:46:10–21:48:19",'tl')
for v in (-8,-4,0,4,8):
    s.add(f'<line class="{"zero" if v==0 else "grid"}" x1="{x0}" y1="{Y(v):.1f}" x2="{x0+w}" y2="{Y(v):.1f}"/>'); s.text(x0-6,Y(v)+4,f"{v}",anchor="end")
s.text(x0-6,y0-8,"kW",anchor="end")
for m in range(43,52):
    s.text(X(T(f'21:{m}:00')),y0+h+16,f'21:{m}',anchor="middle")
def poly(pts,cls):
    p=' '.join(f'{X(T(a)):.1f},{Y(v):.1f}' for a,v in pts)
    s.add(f'<polyline class="{cls}l" fill="none" stroke-width="2" stroke-linejoin="round" points="{p}"/>')
poly(gr,'s3'); poly(bs,'s2'); poly(ev,'s1')
s.text(X(T('21:47:10')),Y(-6.88)+16,"EV −6.9 kW",'tl',anchor='middle')
s.text(X(T('21:47:10')),Y(5.76)+16,"home battery +5.8 kW",'tl',anchor='middle')
s.text(X(T('21:49:30')),Y(-0.95)+16,"EV −0.9 kW (HA Remote EMS)",'t2',anchor='middle')
s.legend(64,404,[("s1","EV pile (+ charge)","line"),("s2","home battery (+ charge)","line"),("s3","grid (+ import)","line")])
s.save('session/out/issue-40/issue-40-v2b-transfer.svg'); print('ok')
