import json,datetime as dt
TZ=dt.timezone(dt.timedelta(hours=10))
b=[-1.62,2.91,0.84,1.22,1.31,0.70,1.63,0.08,-1.40,0.39,-2.77,-1.37,-1.49,-2.15,13.27,4.58,-13.95,-24.00,-6.31,-1.01,1.35,-14.37,-22.84,-24.00,-6.44,0.49,0.94,-19.26,-7.92,-3.39,1.61,1.02,-0.05,0.13,-0.01,-0.10,-0.10,-0.18,-0.03,-0.05,-0.38,-1.58,-1.36,0.22,1.38,-1.64,-0.68,0.86,-0.65,-0.14,-1.09,-1.95,-2.84,-19.09,-23.94,-23.92,-23.91,-23.81,-23.22,-22.39,-7.05,-1.77,-6.77,-6.01,-3.03,-10.85,-5.61,-1.39,-1.41,-1.55,-3.26,-1.14,-0.87,-0.91,-0.94,-0.98,-0.96,-0.95,-0.76,-0.71]
g=[0.02,0.01,0.01,-0.03,0.01,0.01,0.01,0.02,0,0.01,0.01,0.01,-0.01,0.01,0.01,0.01,-10.80,-27.89,-8.14,-0.01,-0.03,-20.43,-26.32,-27.28,-7.07,0,0,-19.50,-7.22,0.01,0,0,0,0,0,0,0,0,0,0,0,0,0,-0.01,0,0,0,0,0.01,0,0,-0.01,0.01,-15.62,-20.41,-20.86,-20.87,-20.82,-19.87,-19.61,-5.23,0,-3.70,-1.98,0,-7.40,-2.85,0,0,0.01,0,0,0,0,0,0,0,0,0,0]
ev=[1.12,0.72,1.05,1.68,1.72,0.36,0.01,0,0.37,0.06,-0.17,0.72,0.75,-0.22,-15.00,-6.41,-1.21,-8.10,-5.58,-3.53,-4.43,-10.85,-9.44,-8.29,-5.96,-4.61,-4.09,-5.01,-1.85,0.06,-3.96,-2.95,-1.81,-1.85,-1.67,-1.60,-1.59,-1.60,-1.75,-1.72,-1.77,-1.72,-2.00,-3.24,-3.06,-0.69,-2.50,-3.15,-0.76,-1.20,-0.36,0,-0.02]+[0]*27
pv=[3.00,5.56,5.44,6.80,5.54,4.72,3.31,2.50,2.16,2.24,1.22,1.59,1.78,1.86,0.83,0.47,0.25,0.08]+[0]*62
soc=[80.0,80.19,80.53,80.69,80.98,81.18,81.49,81.71,81.41,81.44,81.20,80.73,80.48,80.10,80.74,83.49,82.54,78.03,74.26,74.07,74.07,73.11,68.93,63.87,60.17,59.96,60.16,58.58,54.86,54.16,53.83,54.27,54.3,54.3,54.3,54.3,54.3,54.3,54.2,54.2,54.2,54.0,53.68,53.54,53.73,53.79,53.41,53.44,53.56,53.4,53.33,53.05,52.50,50.60,45.60,40.52,35.43,30.33,25.27,20.37,16.77,16.30,15.46,13.93,13.03,11.78,9.52,9.04,8.74,8.43,7.91,7.43,7.23,7.05,6.84,6.63,6.42,6.21,6.04,5.87]
t0=dt.datetime(2026,10,27,16,0,tzinfo=TZ); T=[t0+dt.timedelta(minutes=5*i) for i in range(len(b))]
assert len(b)==len(g)==len(soc)==80, (len(b),len(g),len(ev),len(pv),len(soc))
P=json.load(open('realprice.json'))
def price(series,t):
    v=None
    for ts,x in series:
        if dt.datetime.fromisoformat(ts)<=t: v=x
    return v
FC=json.load(open('fc2025.json'))
load=[pv[i]+g[i]-b[i]-ev[i] for i in range(80)]
json.dump({'t':[x.isoformat() for x in T],'bess':b,'grid':g,'ev':ev,'pv':pv,'soc':soc,'load':load},open('night5.json','w'))
i0=T.index(dt.datetime(2026,10,27,20,25,tzinfo=TZ))
h=5/60
E=sum(-min(0,g[i])*h for i in range(i0,80)); Erev=sum(-min(0,g[i])*h*price(P['fi'],T[i]+dt.timedelta(minutes=2)) for i in range(i0,80))
H=sum(load[i]*h for i in range(i0,80))
print('20:25-22:40: export %.2f kWh, revenue $%.2f (avg %.1f c), house load %.2f kWh (mean %.2f kW), BESS %.1f%%->%.1f%%'%(E,Erev,100*Erev/E,H,H/(len(b)-i0)/h,soc[i0],soc[-1]))
# earlier evening exports 16:00-20:25
E0=sum(-min(0,g[i])*h for i in range(0,i0)); R0=sum(-min(0,g[i])*h*price(P['fi'],T[i]+dt.timedelta(minutes=2)) for i in range(0,i0))
print('16:00-20:25 export %.2f kWh revenue $%.2f avg %.1f c'%(E0,R0,100*R0/E0))
# rest of night 22:40-07:00 using plan load_kw (22:41 plan) and 20:25 forecast import price
plan=[('22:30',0.70),('23:00',0.76),('23:30',0.62),('00:00',0.58),('00:30',0.52),('01:00',0.57),('01:30',0.56),('02:00',0.54),('02:30',0.53),('03:00',0.52),('03:30',0.48),('04:00',0.47),('04:30',0.43),('05:00',0.52),('05:30',0.54),('06:00',0.46-0.26),('06:30',max(0,0.46-0.53))]
L=0;C=0
for hm,kw in plan:
    day='27' if hm>='12' else '28'
    hrs=0.5 if hm!='22:30' else (60-40)/60*0.5/0.5*0.5*2/2  # 22:40-23:00 = 1/3 h
    if hm=='22:30': hrs=20/60
    p=FC['GF'].get(f'2026-10-{day}T{hm}')
    L+=kw*hrs; C+=kw*hrs*p
print('rest of night 22:40-07:00 load (plan load_kw, conservative) %.2f kWh, import cost at 20:25 forecast $%.2f (avg %.1f c)'%(L,C,100*C/L))
FLOOR=5.0; cap=40.3
usable0=(soc[i0]-FLOOR)/100*cap; usable_now=(soc[-1]-FLOOR)/100*cap
need=H+L
print('usable BESS at 20:25 above %.0f%%: %.2f kWh; night need 20:25-07:00: %.2f kWh; usable now %.2f'%(FLOOR,usable0,need,usable_now))
REF=0.075/0.9  # refill tomorrow 09:00 at 7.5c, 90% RTE
imp_actual=max(0,L-usable_now)
cost_imp_actual=C*imp_actual/L
endA=0.0 if L>=usable_now else usable_now-L
A=Erev-cost_imp_actual+endA*REF
endB=usable0-need
B=0+endB*REF
avgfit=Erev/E
S=max(0,usable0-need-1.0)
# sell surplus at the best realised FiT intervals after 20:25
fits=sorted([price(P['fi'],T[i]+dt.timedelta(minutes=2)) for i in range(i0,i0+12)],reverse=True)
Crev=S*sum(fits[:6])/6
endC=1.0
Cv=Crev+endC*REF
print(f'A actual: export ${Erev:.2f} - overnight import {imp_actual:.2f} kWh ${cost_imp_actual:.2f} + BESS@07:00 {endA:.2f} kWh x {REF*100:.1f}c = ${A:.2f}')
print(f'B self-consume from 20:25: BESS@07:00 {endB:.2f} kWh ({FLOOR+endB/cap*100:.1f}%) x {REF*100:.1f}c = ${B:.2f}')
print(f'C export surplus only {S:.2f} kWh at {100*sum(fits[:6])/6:.1f}c then self-consume, 1 kWh reserve: ${Cv:.2f}')
print('A-B $%.2f, C-A $%.2f'%(A-B,Cv-A))

print('\n=== final, start SoC 52.3% at 20:26 (plan bsoc) ===')
S0=52.3; usable0=(S0-FLOOR)/100*cap
for name,val in (('refill 7.5c/0.9',REF),('next-evening import ~21.3c',C/L)):
    A=Erev-cost_imp_actual
    endB=usable0-need; B=endB*val
    S=max(0,usable0-need-1.0); Cv=S*sum(fits[:6])/6+1.0*val
    best=max(B,Cv)
    print(f'{name}: A=${A:.2f}  B=${B:.2f} (BESS@07:00 {FLOOR+endB/cap*100:.1f}%)  C=${Cv:.2f} (export {S:.2f} kWh)  A vs best ${A-best:+.2f}')
# counterfactual SoC traces 20:25 -> 07:00 at 5-min
tr={'t':[], 'B':[], 'C':[]}
t=dt.datetime(2026,10,27,20,25,tzinfo=TZ); sB=S0; sC=S0; exportedC=0
Sx=usable0-need-1.0
planload=dict(plan)
while t<=dt.datetime(2026,10,28,7,0,tzinfo=TZ):
    tr['t'].append(t.isoformat()); tr['B'].append(round(sB,2)); tr['C'].append(round(sC,2))
    if t<T[-1]+dt.timedelta(minutes=5):
        k=T.index(t) if t in T else None; ld=load[k] if k is not None else 0.9
    else:
        hm=t.strftime('%H:')+('00' if t.minute<30 else '30'); ld=planload.get(hm,0.5)
    sB-=ld*h/cap*100
    x=0
    if exportedC<Sx: x=min(20.9*h,Sx-exportedC); exportedC+=x
    sC-=(ld*h+x)/cap*100
    t+=dt.timedelta(minutes=5)
json.dump(tr,open('cf.json','w')); print('B end %.1f C end %.1f'%(tr['B'][-1],tr['C'][-1]))
