"""Generate Figure 1 (pathway matrix) and Figure 2 (MMAE exposure vs Section 7 guidance) from the coded data.
Writes PNG (300 dpi), TIFF (600 dpi), vector PDF, and JPG previews to ./fig. Run from the repository root."""
import os
os.makedirs("fig", exist_ok=True)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5})
# ---------------- Figure 1: matrix (15 ADCs) ----------------
rows=[("Brentuximab vedotin","MMAE","yes"),("Enfortumab vedotin","MMAE","yes"),("Polatuzumab vedotin","MMAE","yes"),
      ("Tisotumab vedotin","MMAE","yes"),("Telisotuzumab vedotin","MMAE","yes"),("Belantamab mafodotin","MMAF","no"),
      ("Ado-trastuzumab emtansine","DM1","yes"),("Mirvetuximab soravtansine","DM4","yes"),
      ("Fam-trastuzumab deruxtecan","DXd","no"),("Datopotamab deruxtecan","DXd","no"),("Sacituzumab govitecan","SN-38","yes"),
      ("Loncastuximab tesirine","SG3199","no"),("Pivekimab sunirine","FGN849","yes"),
      ("Inotuzumab ozogamicin","Calicheamicin","QT only"),("Gemtuzumab ozogamicin","Calicheamicin","no")]
cols=["CYP3A","P-gp","BCRP","OATP1B","UGT1A1"]
# 0 none, 1 12.3 only, 2 possible (12.3 only), 3 evaluated no change, 4 monitor, 5 avoid
S={"Brentuximab vedotin":[4,1,0,0,0],"Enfortumab vedotin":[4,4,0,0,0],"Polatuzumab vedotin":[4,1,0,0,0],"Tisotumab vedotin":[4,1,0,0,0],
   "Telisotuzumab vedotin":[4,1,0,0,0],"Belantamab mafodotin":[0,2,0,1,0],"Ado-trastuzumab emtansine":[5,1,0,0,0],
   "Mirvetuximab soravtansine":[4,1,0,0,0],"Fam-trastuzumab deruxtecan":[3,1,1,1,0],"Datopotamab deruxtecan":[3,1,1,1,0],
   "Sacituzumab govitecan":[0,0,0,0,5],"Loncastuximab tesirine":[1,1,0,0,0],"Pivekimab sunirine":[4,1,1,0,0],
   "Inotuzumab ozogamicin":[0,1,0,0,0],"Gemtuzumab ozogamicin":[0,0,0,0,0]}
# dagger: no clinical or model-based estimate of the effect of strong CYP3A inhibitors
DAG={"Ado-trastuzumab emtansine","Mirvetuximab soravtansine","Loncastuximab tesirine","Pivekimab sunirine"}
style={0:("white","",None,"black"),1:("#F6D7A7","12.3 only",None,"black"),2:("#F6D7A7","possible","////","black"),
       3:("#D9EAD3","no change",None,"black"),4:("#6FA8DC","monitor",None,"black"),5:("#1F4E79","avoid",None,"white")}
n=len(rows); cw,rh=1.0,1.0; x0=0
fig,ax=plt.subplots(figsize=(7.2,5.85),dpi=300)
for i,(adc,pl,s7) in enumerate(rows):
    y=n-1-i
    for j,c in enumerate(cols):
        code=S[adc][j]; fc,txt,hatch,tc=style[code]
        if j==0 and adc in DAG and txt: txt=txt+"\u2020"
        ax.add_patch(Rectangle((x0+j*cw,y),cw,rh,facecolor=fc,edgecolor="#9E9E9E",lw=0.6,hatch=hatch))
        if txt: ax.text(x0+j*cw+cw/2,y+rh/2,txt,ha="center",va="center",fontsize=6.6,color=tc)
    ax.add_patch(Rectangle((x0+len(cols)*cw+0.15,y),0.9,rh,facecolor="white",edgecolor="#9E9E9E",lw=0.6))
    col={"yes":"black","no":"#C0392B","QT only":"#555555"}[s7]
    ax.text(x0+len(cols)*cw+0.6,y+rh/2,s7,ha="center",va="center",fontsize=6.8 if s7=="QT only" else 7,color=col,
            fontweight="bold" if s7=="no" else "normal",style="italic" if s7=="QT only" else "normal")
    ax.text(-0.1,y+rh/2,adc,ha="right",va="center",fontsize=7.6)
    ax.text(x0+len(cols)*cw+1.25,y+rh/2,pl,ha="left",va="center",fontsize=7.2,color="#424242",style="italic")
for j,c in enumerate(cols): ax.text(x0+j*cw+cw/2,n+0.25,c,ha="center",va="bottom",fontsize=7.4,fontweight="bold")
ax.text(x0+len(cols)*cw+0.6,n+0.25,"Section 7\npresent",ha="center",va="bottom",fontsize=7.4,fontweight="bold")
ax.text(x0+len(cols)*cw+1.25,n+0.25,"Payload",ha="left",va="bottom",fontsize=8,fontweight="bold")
for yb in [n-5,n-6,n-8,n-10,n-11,n-12,n-13]:
    ax.plot([-4.2,x0+len(cols)*cw+3.6],[yb,yb],color="#616161",lw=0.8,clip_on=False)
ax.set_xlim(-4.3,x0+len(cols)*cw+3.7); ax.set_ylim(-0.2,n+1.3); ax.axis("off")
leg=[Patch(facecolor="#1F4E79",edgecolor="#9E9E9E",label="Section 7: avoid"),Patch(facecolor="#6FA8DC",edgecolor="#9E9E9E",label="Section 7: monitor"),
     Patch(facecolor="#D9EAD3",edgecolor="#9E9E9E",label="Section 12.3: evaluated, no clinically significant change"),
     Patch(facecolor="#F6D7A7",edgecolor="#9E9E9E",label="Section 12.3 only: substrate, no Section 7 guidance"),
     Patch(facecolor="#F6D7A7",edgecolor="#9E9E9E",hatch="////",label="Section 12.3 only: possible substrate"),
     Patch(facecolor="white",edgecolor="#9E9E9E",label="Not stated")]
ax.legend(handles=leg,loc="upper center",bbox_to_anchor=(0.5,-0.0),ncol=2,fontsize=6.8,frameon=False)
plt.tight_layout()
for ext,kw,dpi in [("png",{},300),("tiff",{"pil_kwargs":{"compression":"tiff_lzw"}},600),("pdf",{},300)]:
    plt.savefig(f"fig/Figure1.{ext}",dpi=dpi,bbox_inches="tight",**kw)
plt.close()
# ---------------- Figure 2 (unchanged content) ----------------
mm=[("Brentuximab vedotin","clinical",34,-46,"Monitor","Noted, no action","None"),
    ("Enfortumab vedotin","PBPK",38,-53,"Monitor","None","Monitor (dual P-gp/CYP3A4)"),
    ("Polatuzumab vedotin","PBPK",45,-63,"Monitor","Noted, no action","None"),
    ("Tisotumab vedotin","extrapolated",34,-46,"Monitor","None","None"),
    ("Telisotuzumab vedotin","PBPK",40,-70,"Monitor","None","None")]
mk={"clinical":"o","PBPK":"s","extrapolated":"^"}
fig,ax=plt.subplots(figsize=(7.4,3.2),dpi=300)
fig.subplots_adjust(right=0.52)
for i,(n_,ev,ki,ri,a,b,c) in enumerate(mm):
    y=len(mm)-1-i
    ax.plot([ri,ki],[y,y],color="#BDBDBD",lw=1,zorder=1)
    ax.scatter(ki,y,marker=mk[ev],s=46,color="#E67E22",edgecolor="black",lw=0.5,zorder=3)
    ax.scatter(ri,y,marker=mk[ev],s=46,color="#2E86C1",edgecolor="black",lw=0.5,zorder=3)
    ax.text(ki+3,y,f"+{ki}%",va="center",fontsize=7.2); ax.text(ri-3,y,f"{ri}%".replace("-","\u2212"),va="center",ha="right",fontsize=7.2)
    ax.text(1.03,y,f"Inhibitors: {a}\nInducers: {b}  |  P-gp: {c}",va="center",fontsize=6.6,transform=ax.get_yaxis_transform(),clip_on=False)
ax.axvline(0,color="black",lw=0.8)
ax.set_yticks(range(len(mm))); ax.set_yticklabels([m[0] for m in mm][::-1],fontsize=7.8)
ax.set_xlim(-100,70); ax.set_xticks([-80,-60,-40,-20,0,20,40,60])
ax.set_xlabel("Change in unconjugated MMAE exposure (%)",fontsize=8)
ax.text(1.03,len(mm)-0.45,"Section 7 guidance",fontsize=7.6,fontweight="bold",transform=ax.get_yaxis_transform(),clip_on=False)
for s in ["top","right"]: ax.spines[s].set_visible(False)
leg=[Line2D([],[],marker="o",ls="",color="#E67E22",markeredgecolor="black",label="Ketoconazole (strong CYP3A inhibitor)"),
     Line2D([],[],marker="o",ls="",color="#2E86C1",markeredgecolor="black",label="Rifampin (strong CYP3A inducer)"),
     Line2D([],[],marker="o",ls="",color="white",markeredgecolor="black",label="Clinical study"),
     Line2D([],[],marker="s",ls="",color="white",markeredgecolor="black",label="PBPK prediction"),
     Line2D([],[],marker="^",ls="",color="white",markeredgecolor="black",label="Extrapolated from another MMAE ADC")]
ax.legend(handles=leg,loc="upper left",bbox_to_anchor=(-0.35,-0.22),ncol=3,fontsize=6.6,frameon=False)
for ext,kw,dpi in [("png",{},300),("tiff",{"pil_kwargs":{"compression":"tiff_lzw"}},600),("pdf",{},300)]:
    plt.savefig(f"fig/Figure2.{ext}",dpi=dpi,bbox_inches="tight",**kw)
plt.close()
from PIL import Image
for nme in ["Figure1","Figure2"]:
    im=Image.open(f"fig/{nme}.png"); print(nme,im.size)
    im.convert("RGB").save(f"fig/ADC_DDI_{nme}.jpg","JPEG",quality=95,dpi=(300,300))
