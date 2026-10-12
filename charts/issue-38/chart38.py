import json,sys,datetime as dt,importlib.util
spec=importlib.util.spec_from_file_location('c','plan/charts.py')
src=open('plan/charts.py').read().split('\nfor fn in (')[0]
src=src.replace('OUT = sys.argv[1]','OUT = "session/out"')
ns={'__file__':'plan/charts.py'}; exec(compile(src,'charts','exec'),ns)
Svg,STYLE,esc=ns['Svg'],ns['STYLE'],ns['esc']
F=dt.datetime.fromisoformat
E={e['entity_id'].split('.')[1]:e['states'] for e in json.load(open('session/h1.json'))['data']['entities']}
def ser(k): return [(F(x['last_changed']),float(x['state'])) for x in E[k] if x['state'] not in('unknown','unavailable')]
ev=ser('sigen_inverter_dc_charger_output_power'); b=ser('sigen_plant_battery_power')
t0=F('2026-10-12T10:22:00+10:00'); t1=F('2026-10-12T10:37:00+10:00')
s=Svg(420,"H · Plan sets the EV to 8.9–15.4 kW; the DC pile delivers about 0.6 kW",
      "12 Oct 2026, Model Y plugged in 10:23:12 at 17 % · Amber V2X in control · 5 s samples · kW",
      "Measured EV pile power and home battery power, with the plan's EV setpoint for the current interval as steps.")
x0,y0,w,h=64,84,770,260; ymin,ymax=-2,18
X=lambda t: x0+w*(t-t0).total_seconds()/(t1-t0).total_seconds()
Y=lambda v: y0+h*(ymax-v)/(ymax-ymin)
for v in (0,4,8,12,16):
    s.add(f'<line class="{"zero" if v==0 else "grid"}" x1="{x0}" y1="{Y(v):.1f}" x2="{x0+w}" y2="{Y(v):.1f}"/>'); s.text(x0-6,Y(v)+4,f"{v}",anchor="end")
s.text(x0-6,y0-8,"kW",anchor="end")
for m in range(22,38,2):
    t=F(f'2026-10-12T10:{m:02d}:00+10:00'); s.text(X(t),y0+h+16,t.strftime('%H:%M'),anchor="middle")
ts=F('2026-10-12T10:24:20+10:00')
s.add(f'<rect class="shade" x="{X(t0):.1f}" y="{y0}" width="{X(ts)-X(t0):.1f}" height="{h}"/>')
s.text(X(t0)+6,y0+16,"plug-in, handshake",'t2')
def poly(pts,cls,dash=''):
    p=' '.join(f'{X(t):.1f},{Y(v):.1f}' for t,v in pts if t0<=t<=t1)
    s.add(f'<polyline class="{cls}l" fill="none" stroke-width="2" stroke-linejoin="round" points="{p}"{dash}/>')
poly(b,'s2'); poly(ev,'s1')
# setpoint steps
steps=[(F('2026-10-12T10:26:06+10:00'),F('2026-10-12T10:31:06+10:00'),8.94,'10:26 plan'),
       (F('2026-10-12T10:36:05+10:00'),t1,15.35,'10:36 plan')]
for a,c,v,lab in steps:
    s.add(f'<line class="critl" x1="{X(a):.1f}" y1="{Y(v):.1f}" x2="{X(c):.1f}" y2="{Y(v):.1f}" stroke-width="2.5" stroke-dasharray="6 4"/>')
    if c==t1: s.text(X(c)-2,Y(v)+16,f"{lab}: EV setpoint +{v:.2f}",'tl',anchor='end')
    else: s.text(X(a)+2,Y(v)-6,f"{lab}: EV setpoint +{v:.2f}",'tl')
s.text(X(F('2026-10-12T10:31:30+10:00')),Y(10.6),"10:31 plan not captured",'t2')
s.text(X(F('2026-10-12T10:30:00+10:00')),Y(15.6),"home battery 13–15 kW",'tl')
s.text(X(F('2026-10-12T10:30:00+10:00')),Y(2.0),"EV mean 0.60 kW, 16 reversals, 13 samples < 0",'tl')
s.legend(64,404,[("s1","EV pile measured (dc_charger_output_power)","line"),("s2","home battery measured","line"),("crit","plan EV setpoint, current interval","dash")])
s.save('session/out/issue-38/issue-38-setpoint-not-delivered.svg')
print('ok')
