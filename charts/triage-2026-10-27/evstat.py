import json,datetime as dt
exec(open('ev.py').read().split("import sys")[0])
T0=dt.datetime.fromisoformat('2026-10-27T16:20:00+10:00'); T1=dt.datetime.fromisoformat('2026-10-27T18:36:00+10:00')
N=int((T1-T0).total_seconds())
def ser(k,num=True):
    s=S[k];out=[];i=0;v=None
    for n in range(N):
        t=T0+dt.timedelta(seconds=n)
        while i<len(s) and s[i][0]<=t: v=s[i][1];i+=1
        if num:
            try: out.append(float(v))
            except: out.append(None)
        else: out.append(v)
    return out
B=ser('sigen_plant_battery_power');G=ser('sigen_plant_grid_active_power');E=ser('sigen_inverter_dc_charger_output_power')
D=ser('amber_v2x_amber_purcell_id_au_optimiser_decision',False);X=ser('sigen_plant_grid_export_limitation')
SOC=ser('sigen_plant_battery_state_of_charge');ESOC=ser('m3p_t_battery_level');RS=ser('sigen_inverter_dc_charger_running_state',False)
json.dump({'t0':T0.isoformat(),'bess':B,'grid':G,'ev':E,'dec':D,'expl':X,'soc':SOC,'esoc':ESOC,'rs':RS},open('eve.json','w'))
# segments by decision
segs=[];cur=None;st=0
for n,d in enumerate(D):
    if d!=cur:
        if cur is not None: segs.append((st,n,cur))
        cur=d;st=n
segs.append((st,N,cur))
h=1/3600
tot={}
for a,b,d in segs:
    sl=lambda arr:[x for x in arr[a:b] if x is not None]
    exp=-sum(min(0,x) for x in sl(G))*h; evo=-sum(min(0,x) for x in sl(E))*h; bo=-sum(min(0,x) for x in sl(B))*h; bi=sum(max(0,x) for x in sl(B))*h
    v2b=sum(min(-e,bb) for e,bb in zip(E[a:b],B[a:b]) if e is not None and bb is not None and e<0 and bb>0)*h
    head=sum(max(0,30+g) for g in sl(G))*h if d=='discharge' else 0
    print(f"{(T0+dt.timedelta(seconds=a)).strftime('%H:%M:%S')}-{(T0+dt.timedelta(seconds=b)).strftime('%H:%M:%S')} {d:13} {(b-a)/60:5.1f}min expL={X[a]:.0f} export {exp:5.2f} EVout {evo:5.2f} BESSout {bo:5.2f} BESSin {bi:5.2f} EV->BESS {v2b:4.2f} unused<30 {head:5.2f} kWh")
    for k,v in (('exp',exp),('evo',evo),('bo',bo),('bi',bi),('v2b',v2b),('head',head)):
        tot.setdefault(d,{}).setdefault(k,0); tot[d][k]+=v
for d,v in tot.items(): print(d,{k:round(x,2) for k,x in v.items()})
