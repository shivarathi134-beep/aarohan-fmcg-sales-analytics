"""Create illustrative dashboard design previews from calculated synthetic outputs.
These PNGs are not Power BI screenshots and do not demonstrate interactivity.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'powerbi'; OUT.mkdir(exist_ok=True)
NAVY='#15243A'; TEAL='#087E8B'; BLUE='#3772FF'; VIOLET='#7455D9'; AMBER='#F4A259'; RED='#D94F4F'; GREEN='#169873'
BG='#F3F6FA'; PALE=BG; WHITE='#FFFFFF'; TXT='#1C2838'; MUTED='#6C7A8B'; GRID='#E6EBF2'

def load(name): return pd.read_csv(ROOT/'outputs'/name)
def rounded(ax, xy, w, h, fc=WHITE, ec=None, radius=0.02, lw=0.8):
    p=FancyBboxPatch(xy,w,h,boxstyle=f"round,pad=0.008,rounding_size={radius}",facecolor=fc,edgecolor=ec or fc,linewidth=lw)
    ax.add_patch(p); return p

def setup_page(title, subtitle, tag):
    fig=plt.figure(figsize=(16,9),dpi=120,facecolor=BG)
    base=fig.add_axes([0,0,1,1]); base.set_xlim(0,1); base.set_ylim(0,1); base.axis('off')
    base.add_patch(Rectangle((0,0.86),1,0.14,color=NAVY))
    base.text(0.035,0.944,title,fontsize=21,fontweight='bold',color=WHITE,va='center')
    base.text(0.036,0.897,subtitle,fontsize=10,color='#D1DBE7',va='center')
    rounded(base,(0.79,0.905),0.17,0.045,fc='#253A56',radius=0.014)
    base.text(0.875,0.927,tag,ha='center',va='center',fontsize=9,color=WHITE,fontweight='bold')
    base.text(0.965,0.874,'SYNTHETIC DATA',fontsize=7.5,color='#F4C27A',ha='right',va='center',fontweight='bold')
    return fig,base

def panel(base,x,y,w,h,title,sub=None):
    rounded(base,(x,y),w,h,fc=WHITE,radius=0.014)
    base.text(x+0.018,y+h-0.036,title,fontsize=10.5,color=TXT,fontweight='bold',va='center')
    if sub: base.text(x+0.018,y+h-0.064,sub,fontsize=7.5,color=MUTED,va='center')

def axis(fig, x,y,w,h):
    ax=fig.add_axes([x,y,w,h]); ax.set_facecolor(WHITE)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(axis='both',colors=MUTED,labelsize=8,length=0,pad=4)
    ax.grid(axis='y',color=GRID,linewidth=0.7); ax.set_axisbelow(True)
    return ax

def metric(base,x,label,value,sub,accent):
    rounded(base,(x,0.738),0.225,0.094,fc=WHITE,radius=0.014)
    base.add_patch(Rectangle((x,0.738),0.006,0.094,color=accent))
    base.text(x+0.018,0.805,label.upper(),fontsize=8,color=MUTED,fontweight='bold',va='center')
    base.text(x+0.018,0.769,value,fontsize=18,color=NAVY,fontweight='bold',va='center')
    base.text(x+0.018,0.748,sub,fontsize=7.4,color=MUTED,va='center')

# Page 1: executive overview
monthly=load('monthly_summary.csv'); region=load('region_summary.csv'); category=load('category_summary.csv')
discount=load('discount_band_summary.csv'); product=load('product_summary.csv'); returns=load('return_reason_summary.csv')
kpi=load('executive_summary.csv').set_index('metric')['value']
fig,base=setup_page('AAROHAN  /  FMCG CONTROL TOWER','Sales performance  •  Profitability  •  Distribution health  •  FY2024–FY2025','01  EXECUTIVE OVERVIEW')
metric(base,0.035,'Net Sales (After Returns)',f"{kpi['Estimated net sales after returns']/1e6:.2f}M",'estimated • currency units',TEAL)
metric(base,0.267,'Estimated Profit',f"{kpi['Estimated profit']/1e6:.2f}M",'net sales less estimated COGS',BLUE)
metric(base,0.499,'Profit Margin',f"{kpi['Estimated profit margin']*100:.2f}%",'weighted • estimated',VIOLET)
metric(base,0.731,'Unit Return Rate',f"{kpi['Unit return rate']*100:.2f}%",'returned units / ordered units',AMBER)
# Monthly trends panel
panel(base,0.035,0.405,0.565,0.305,'MONTHLY NET SALES TREND','Net sales after estimated return-value adjustment')
ax=axis(fig,0.068,0.438,0.505,0.192)
ax.grid(axis='x',visible=False)
ax.plot(range(len(monthly)),monthly['net_sales_after_returns_est']/1e6,color=TEAL,linewidth=2.7,marker='o',markersize=2.5)
ax.fill_between(range(len(monthly)),monthly['net_sales_after_returns_est']/1e6,alpha=0.12,color=TEAL)
ax.set_ylabel('Millions',fontsize=8,color=MUTED)
ax.set_xticks(range(0,len(monthly),3)); ax.set_xticklabels(monthly['year_month'].iloc[::3],rotation=0,fontsize=7)
ax.set_ylim(0,monthly['net_sales_after_returns_est'].max()/1e6*1.2)
# Region panel
panel(base,0.615,0.405,0.35,0.305,'REGIONAL CONTRIBUTION','Net sales after returns')
ax=axis(fig,0.64,0.438,0.28,0.19)
r=region.sort_values('net_sales_after_returns_est')
ax.barh(r['region_name'],r['net_sales_after_returns_est']/1e6,color=[BLUE,TEAL,VIOLET,AMBER][:len(r)],height=0.55)
ax.set_xlabel('Millions',fontsize=8,color=MUTED); ax.grid(axis='x',visible=False); ax.grid(axis='y',visible=False)
for i,v in enumerate(r['net_sales_after_returns_est']/1e6): ax.text(v+0.08,i,f'{v:.2f}',va='center',fontsize=7.5,color=TXT)
ax.set_xlim(0,r['net_sales_after_returns_est'].max()/1e6*1.22)
# Category panel
panel(base,0.035,0.065,0.38,0.31,'CATEGORY PROFITABILITY','Estimated profit • margin at right')
ax=axis(fig,0.095,0.105,0.26,0.18)
c=category.sort_values('profit_est')
barcols=[AMBER if x=='Staples' else TEAL for x in c['category']]
ax.barh(c['category'],c['profit_est']/1e6,color=barcols,height=0.56)
ax.set_xlabel('Profit (millions)',fontsize=8,color=MUTED); ax.grid(axis='x',visible=False); ax.grid(axis='y',visible=False)
for i,(_,row) in enumerate(c.iterrows()): ax.text(row['profit_est']/1e6+0.04,i,f"{row['profit_est']/1e6:.2f}  •  {row['profit_margin_pct_est']:.1%}",va='center',fontsize=7,color=TXT)
ax.set_xlim(0,c['profit_est'].max()/1e6*1.65)
# Discount panel
panel(base,0.43,0.065,0.26,0.31,'DISCOUNT MIX CHECK','Margin by observed discount band')
ax=axis(fig,0.455,0.105,0.21,0.205)
disc_order=['0–4.9%','5–9.9%','10–19.9%','20%+']
d=discount.set_index('discount_band').reindex(disc_order).reset_index()
colors=[TEAL,BLUE,VIOLET,RED]
ax.bar(d['discount_band'],d['profit_margin_pct_est']*100,color=colors,width=0.62)
ax.set_ylabel('Margin %',fontsize=8,color=MUTED); ax.tick_params(axis='x',labelrotation=0,labelsize=7)
ax.set_ylim(0,max(d['profit_margin_pct_est']*100)*1.22); ax.grid(axis='x',visible=False)
for i,v in enumerate(d['profit_margin_pct_est']*100): ax.text(i,v+1.2,f'{v:.1f}%',ha='center',fontsize=7,color=TXT)
# Top profit products panel
panel(base,0.705,0.065,0.26,0.31,'TOP PROFIT CONTRIBUTORS','Top 5 SKUs by estimated profit')
base.text(0.73,0.302,'PRODUCT',fontsize=7,color=MUTED,fontweight='bold')
base.text(0.94,0.302,'PROFIT',fontsize=7,color=MUTED,fontweight='bold',ha='right')
top=product.sort_values('profit_est',ascending=False).head(5).reset_index(drop=True)
for i,row in top.iterrows():
    yy=0.267-i*0.039
    base.text(0.73,yy,row['product_name'],fontsize=8.2,color=TXT,va='center')
    base.text(0.94,yy,f"{row['profit_est']/1e6:.2f}M",fontsize=8.2,color=TEAL,fontweight='bold',va='center',ha='right')
    base.plot([0.73,0.94],[yy-0.018,yy-0.018],color=GRID,lw=0.6)
base.text(0.035,0.025,'DESCRIPTIVE ANALYSIS ONLY  •  Discounts do not establish causation  •  Profit and return values use stated assumptions',fontsize=7.2,color=MUTED)
fig.savefig(OUT/'dashboard_preview.png',bbox_inches='tight',facecolor=BG)
plt.close(fig)

# Page 2: product / returns review
fig,base=setup_page('AAROHAN  /  PROFIT & RETURNS REVIEW','SKU economics  •  Promotional discount bands  •  Return-reason monitoring','02  PRODUCT & RISK')
low=product.sort_values('profit_est').head(5); high=product.sort_values('profit_est',ascending=False).head(5)
metric(base,0.035,'Highest Profit SKU',high.iloc[0]['product_name'],f"{high.iloc[0]['profit_est']/1e6:.2f}M estimated profit",TEAL)
metric(base,0.267,'Lowest Profit SKU',low.iloc[0]['product_name'],f"{low.iloc[0]['profit_est']/1e6:.2f}M • still positive",AMBER)
metric(base,0.499,'Average Line Discount',f"{kpi['Average line discount']*100:.2f}%",'unweighted average discount',BLUE)
metric(base,0.731,'Return Value',f"{kpi['Estimated return value']/1e6:.2f}M",'estimated discounted selling value',RED)
panel(base,0.035,0.39,0.46,0.32,'TOP AND BOTTOM SKUS BY ESTIMATED PROFIT','All products show positive estimated profit in the supplied synthetic data')
ax=axis(fig,0.11,0.435,0.34,0.205)
rank=pd.concat([low,high]).sort_values('profit_est')
ax.barh(rank['product_name'],rank['profit_est']/1e6,color=[AMBER if x in set(low['product_name']) else TEAL for x in rank['product_name']],height=0.55)
ax.set_xlabel('Estimated profit (millions)',fontsize=8,color=MUTED); ax.grid(axis='x',visible=False); ax.grid(axis='y',visible=False)
panel(base,0.51,0.39,0.455,0.32,'RETURN VALUE BY RECORDED REASON','Estimate = returned units × discounted unit price')
ax=axis(fig,0.595,0.435,0.32,0.205)
rr=returns.sort_values('estimated_return_value')
ax.barh(rr['return_reason'],rr['estimated_return_value']/1000,color=[RED if 'Damaged' in x else VIOLET for x in rr['return_reason']],height=0.55)
ax.set_xlabel('Thousands of currency units',fontsize=8,color=MUTED); ax.grid(axis='x',visible=False); ax.grid(axis='y',visible=False)
for i,v in enumerate(rr['estimated_return_value']/1000): ax.text(v+4,i,f'{v:,.0f}',va='center',fontsize=7.4,color=TXT)
ax.set_xlim(0,rr['estimated_return_value'].max()/1000*1.28)
panel(base,0.035,0.065,0.45,0.295,'DISCOUNT BAND: OBSERVED MARGIN','Relationship, not proof of discount impact')
ax=axis(fig,0.075,0.11,0.37,0.18)
ax.bar(d['discount_band'],d['profit_margin_pct_est']*100,color=colors,width=0.62)
ax.set_ylabel('Estimated margin %',fontsize=8,color=MUTED); ax.grid(axis='x',visible=False)
for i,v in enumerate(d['profit_margin_pct_est']*100): ax.text(i,v+1.1,f'{v:.1f}%',ha='center',fontsize=8,color=TXT)
ax.set_ylim(0,max(d['profit_margin_pct_est']*100)*1.23)
panel(base,0.505,0.065,0.46,0.295,'MANAGEMENT INVESTIGATION QUEUE','Prioritise validation, not automatic policy changes')
queue=[
 ('01','Investigate transit damage','Review carrier, packaging and distributor patterns.'),
 ('02','Review Staples economics','High sales coexist with lower estimated margin.'),
 ('03','Test deep-discount promotions','Use controlled tests before changing offers.'),
 ('04','Check monthly seasonality','Compare like-for-like periods and product mix.')]
for i,(num,head,sub) in enumerate(queue):
 yy=0.265-i*0.052
 rounded(base,(0.525,yy-0.016),0.037,0.037,fc=PALE,radius=0.009)
 base.text(0.543,yy+0.002,num,ha='center',va='center',fontsize=8,color=TEAL,fontweight='bold')
 base.text(0.575,yy+0.008,head,fontsize=8.3,color=TXT,fontweight='bold',va='center')
 base.text(0.575,yy-0.012,sub,fontsize=7.2,color=MUTED,va='center')
base.text(0.035,0.025,'Not a Power BI screenshot • Static preview for design reference • All source values are synthetic',fontsize=7.2,color=MUTED)
fig.savefig(OUT/'dashboard_product_returns_preview.png',bbox_inches='tight',facecolor=BG)
plt.close(fig)
print('Generated illustrative preview images:', OUT/'dashboard_preview.png', OUT/'dashboard_product_returns_preview.png')
