import datetime as dt
src=open('plan/charts.py').read().split('\nfor fn in (')[0].replace('OUT = sys.argv[1]','OUT = "session/out"')
ns={'__file__':'plan/charts.py'}; exec(compile(src,'charts','exec'),ns)
Svg=ns['Svg']
T=lambda s: dt.datetime.fromisoformat('2026-10-12T'+s+'+10:00')
ev=[('11:10:00',0.943),('11:10:02',1.404),('11:10:07',1.51),('11:10:12',1.228),('11:10:17',1.496),('11:10:22',0.686),('11:10:27',0.918),('11:10:32',1.144),('11:10:37',-0.309),('11:10:42',1.309),('11:10:47',1.471),('11:10:52',1.542),('11:10:57',1.743),('11:11:02',2.004),('11:11:07',1.803),('11:11:13',0.799),('11:11:18',-0.502),('11:11:23',0.327),('11:11:28',0.01),('11:11:33',-0.583),('11:11:38',0.056),('11:11:43',0.0),('11:13:40',0.0)]
vv=[('11:10:00',352.0),('11:11:33',351.7),('11:11:48',1.7),('11:13:40',0.5)]
t0,t1=T('11:10:00'),T('11:13:00')
s=Svg(400,"I · Daemon switch to preserve ends the DC session instead of holding it",
      "12 Oct 2026 · Model Y at 18 % on the DC pile · Amber V2X in control · 5 s samples",
      "EV pile power before and after the 11:11:03 daemon cycle switched the strategy to preserveCharge, with the session state changes marked.")
x0,y0,w,h=64,84,770,230; ymin,ymax=-1,2.5
X=lambda t: x0+w*(t-t0).total_seconds()/(t1-t0).total_seconds()
Y=lambda v: y0+h*(ymax-v)/(ymax-ymin)
for v in (-1,0,1,2):
    s.add(f'<line class="{"zero" if v==0 else "grid"}" x1="{x0}" y1="{Y(v):.1f}" x2="{x0+w}" y2="{Y(v):.1f}"/>'); s.text(x0-6,Y(v)+4,f"{v}",anchor="end")
s.text(x0-6,y0-8,"kW",anchor="end")
for m in ('11:10:00','11:10:30','11:11:00','11:11:30','11:12:00','11:12:30','11:13:00'):
    s.text(X(T(m)),y0+h+16,m[:5] if m.endswith(':00') else m,anchor="middle")
s.add(f'<rect class="shade" x="{X(T("11:11:48")):.1f}" y="{y0}" width="{X(t1)-X(T("11:11:48")):.1f}" height="{h}"/>')
pts=' '.join(f'{X(T(a)):.1f},{Y(v):.1f}' for a,v in ev if T(a)<=t1)
s.add(f'<polyline class="s1l" fill="none" stroke-width="2" stroke-linejoin="round" points="{pts}"/>')
marks=[('11:11:03','daemon cycle: selfConsume → preserveCharge',2.35),('11:11:45','car: charging → stopped',1.7),('11:11:48','pile: Occupied, DC link 352 → 1.7 V',1.2),('11:11:51','pilot status: Finishing',0.7)]
for a,lab,yy in marks:
    s.add(f'<line class="critl" x1="{X(T(a)):.1f}" y1="{y0}" x2="{X(T(a)):.1f}" y2="{y0+h}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    s.text(X(T(a))+5,Y(yy),f"{a} {lab}",'tl')
s.text(X(T('11:12:10')),Y(-0.6),"session closed, cable still in",'t2')
s.legend(64,392,[("s1","EV pile power (dc_charger_output_power)","line"),("crit","event","dash")])
s.save('session/out/issue-39/issue-39-preserve-ends-session.svg'); print('ok')
