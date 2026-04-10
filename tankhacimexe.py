"""TANK HACIM HESABI - Kivy APK"""
import json,os,shutil
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color,Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp,sp

def _dd():
    try:
        from android.storage import app_storage_path
        return app_storage_path()
    except: return os.path.dirname(os.path.abspath(__file__))
DD=_dd()
SF=os.path.join(DD,"sludge_ayar.json")
HF=os.path.join(DD,"sludge_gecmis.json")
TF=os.path.join(DD,"tank_data.json")
CF=os.path.join(DD,"custom_tanks.json")

L_TR={"app":"TANK HACIM HESABI","trim":"TRIM (m):","dt":"Tarih:","calc":"HESAPLA","exp":"CIKTI AL","set":"SET","back":"< Geri","sett":"Ayarlar","thm":"TEMA","thl":"Acik","thd":"Koyu","lng":"DIL","hist":"GECMIS","save":"KAYDET","err":"HATA","noh":"Kayit yok.","ds":"Secilenleri Sil","da":"Tumunu Sil","ht":"Gecmis","eok":"Kaydedildi!","cda":"Tum kayitlari sil?","y":"Evet","n":"Hayir","rec":"Kayit","ts":"Trim","cm":"cm","pe":"PDF","po":"PDF OK!","pf":"PDF hata!","pg":"Sf","lj":"Gemi Yukle","jt":"Sounding Table","jo":"Yuklendi!","je":"JSON hata!","nj":"JSON yok.","nd":"Tank verisi yok!","sd":"---","cn":"Iptal","sh":"Gemi:","at":"+ Tank Ekle","tn":"Tank Adi:","fh":"m3=cm (orn: 1.4=115)","ad":"Ekle","tv":"TANKLAR","cu":"(M)","prv":"GERI","nxt":"ILERI","nq":"Not eklemek ister misiniz?","nt":"Not","nl":"Not:","ed":"Duzenle","rm":"Sil","dsq":"Bu kayitlari silmek istediginizden emin misiniz?","dsa":"Tum kayitlari silmek istediginizden emin misiniz?","edt":"Tank Duzenle","rmq":"Bu tanki silmek istediginizden emin misiniz?","no_sel":"Kayit secilmedi.","tot":"TOPLAMLAR","chrt":"Tank Delta Grafigi (ilk kayda gore)"}
L_EN={"app":"TANK VOLUME CALC","trim":"TRIM (m):","dt":"Date:","calc":"CALCULATE","exp":"EXPORT","set":"SET","back":"< Back","sett":"Settings","thm":"THEME","thl":"Light","thd":"Dark","lng":"LANG","hist":"HISTORY","save":"SAVE","err":"ERROR","noh":"No records.","ds":"Del Sel","da":"Del All","ht":"History","eok":"Saved!","cda":"Delete all?","y":"Yes","n":"No","rec":"Record","ts":"Trim","cm":"cm","pe":"PDF","po":"PDF saved!","pf":"PDF error!","pg":"Pg","lj":"Load Ship","jt":"Sounding Table","jo":"Loaded!","je":"JSON error!","nj":"No JSON.","nd":"No data!","sd":"---","cn":"Cancel","sh":"Ship:","at":"+ Add Tank","tn":"Tank Name:","fh":"m3=cm (ex: 1.4=115)","ad":"Add","tv":"TANKS","cu":"(M)","prv":"PREV","nxt":"NEXT","nq":"Add a note?","nt":"Note","nl":"Note:","ed":"Edit","rm":"Del","dsq":"Delete these records?","dsa":"Delete ALL records?","edt":"Edit Tank","rmq":"Delete this tank?","no_sel":"No records selected.","tot":"TOTALS","chrt":"Tank Delta Chart (from 1st record)"}
LANG={"tr":L_TR,"en":L_EN}

C_L={"BG":"f0f4f8","CD":"ffffff","C2":"e8f0fe","EN":"f0f0f0","EA":"dbeafe","TT":"1565c0","LB":"1e3a5f","MU":"607080","RC":"0277bd","BB":"1976d2","BF":"ffffff","TB":"e8f5e9","TF":"2e7d32","IB":"e3f2fd","IF":"0d47a1","NB":"dce8f8","NF":"1e3a5f","DB":"ffcccc","DF":"c62828","KB":"ffe0b2","KF":"e65100","EB":"bbdefb","EF":"0d47a1","VB":"c8e6c9","VF":"2e7d32","MB":"e3edf7","MF":"1565c0","XB":"c8e6c9","XF":"2e7d32","HB":"fff3e0","HF":"e65100","WF":"f57f17","OB":"c8e6c9","OF":"2e7d32","JB":"e1bee7","JF":"6a1b9a","AB":"fff3e0","AF":"e65100","ZB":"fce4ec","ZF":"c62828"}
C_D={"BG":"1a1a2e","CD":"16213e","C2":"0f3460","EN":"1a1a3e","EA":"1b4070","TT":"4fc3f7","LB":"b0c4de","MU":"7890a0","RC":"4dd0e1","BB":"0288d1","BF":"ffffff","TB":"1b3a1b","TF":"66bb6a","IB":"0d2137","IF":"64b5f6","NB":"1e2d50","NF":"b0c4de","DB":"4a1a1a","DF":"ef9a9a","KB":"4a3a1a","KF":"ffcc80","EB":"0d3060","EF":"64b5f6","VB":"1b3a1b","VF":"66bb6a","MB":"0f3460","MF":"4fc3f7","XB":"1b3a1b","XF":"66bb6a","HB":"2e1a00","HF":"ffcc80","WF":"ffee58","OB":"1b3a1b","OF":"66bb6a","JB":"2e1a3e","JF":"ce93d8","AB":"2e1a00","AF":"ffcc80","ZB":"2e0a0a","ZF":"ef9a9a"}
CS={"light":C_L,"dark":C_D}

TD,TB,CI={},{},{}
AK,AC=[],[]
VK=set();SN="---";CT={}

def _bt(raw):
    t={}
    for r in raw: t[r[0]]={-1:r[1],0:r[2],1:r[3],2:r[4],3:r[5],4:r[6],5:r[7],6:r[8],7:r[9]}
    return t
def lc():
    global CT
    try:
        with open(CF,"r") as f: CT=json.load(f)
    except: CT={}
def sc2():
    try:
        with open(CF,"w") as f: json.dump(CT,f,indent=2,ensure_ascii=False)
    except: pass
def ac():
    for k,v in CT.items():
        if k not in TD:
            TD[k]={"name":v.get("name",k),"cat":v.get("cat","sludge"),"tip":"cf"}
            if k not in AK: AK.append(k)
            VK.add(k)
def lj(path=None):
    global TD,TB,CI,AK,VK,AC,SN
    if path is None: path=TF
    if not os.path.exists(path): return False
    try:
        with open(path,"r") as f: jd=json.load(f)
    except: return False
    TD.clear();TB.clear();CI.clear();AK.clear();VK.clear();AC.clear()
    SN=jd.get("ship_name","---")
    for ck,cd in jd.get("categories",{}).items():
        CI[ck]={"lt":cd.get("label_tr",ck),"le":cd.get("label_en",ck),"c":cd.get("clr","TOT")}
        AC.append(ck)
    for tk,td in jd.get("tanks",{}).items():
        TD[tk]={"name":td.get("name",tk),"cat":td.get("cat","sludge"),"tip":td.get("tip","table")}
        raw=td.get("data",[])
        if raw and td.get("tip","table")=="table": TB[tk]=_bt([tuple(r) for r in raw])
        AK.append(tk);VK.add(tk)
    ac()
    if path!=TF:
        try: shutil.copy2(path,TF)
        except: pass
    return True
lc();lj();ac()

def _df(): return {"theme":"light","lang":"tr","order":AK[:],"vis":{k:True for k in AK},"co":AC[:],"vc":{c:True for c in AC},"trim":"2","last_cm":{}}
def ls2():
    try:
        with open(SF,"r") as f: s=json.load(f)
        if "order" not in s: s["order"]=AK[:]
        if "vis" not in s: s["vis"]={}
        if "co" not in s: s["co"]=AC[:]
        if "vc" not in s: s["vc"]={}
        if "trim" not in s: s["trim"]="2"
        if "last_cm" not in s: s["last_cm"]={}
        s["order"]=[k for k in s["order"] if k in VK]
        for k in AK:
            if k not in s["order"]: s["order"].append(k)
        for k in VK:
            if k not in s["vis"]: s["vis"][k]=True
        for c in AC:
            if c not in s["co"]: s["co"].append(c)
            if c not in s["vc"]: s["vc"][c]=True
        return s
    except: return _df()
def ss2(s):
    try:
        with open(SF,"w") as f: json.dump(s,f,indent=2)
    except: pass
def lh():
    try:
        with open(HF,"r") as f: return json.load(f)
    except: return []
def sh2(h):
    try:
        with open(HF,"w") as f: json.dump(h,f,indent=2,ensure_ascii=False)
    except: pass

def lu(table,cm,trim):
    tc=[-1,0,1,2,3,4,5,6,7];t1,t2=tc[0],tc[-1]
    for i in range(len(tc)-1):
        if tc[i]<=trim<=tc[i+1]: t1,t2=tc[i],tc[i+1]; break
    rows=sorted(table.keys());r1,r2=rows[0],rows[-1]
    for i in range(len(rows)-1):
        if rows[i]<=cm<=rows[i+1]: r1,r2=rows[i],rows[i+1]; break
    def li(a,b,x,x0,x1): return a if x0==x1 else a+(b-a)*(x-x0)/(x1-x0)
    if r1==r2: return round(li(table[r1][t1],table[r1][t2],trim,t1,t2),1)
    va=li(table[r1][t1],table[r1][t2],trim,t1,t2);vb=li(table[r2][t1],table[r2][t2],trim,t1,t2)
    return round(va+(vb-va)*(cm-r1)/(r2-r1),1)

def cv(key,cs,trim):
    v=cs.strip().replace(",",".")
    if not v: return None
    try:
        c=float(v);d=TD[key];t=d.get("tip","table")
        if t=="cf":
            ct=CT.get(key,{});m=ct.get("m3",1.4);x=ct.get("cm_max",115)
            return round((m*c)/x,1) if x else 0.0
        elif t=="formula": return round((1.4*c)/115,1)
        else:
            if key not in TB: return None
            return lu(TB[key],c,trim)
    except: return None

def hx(h,a=1.0):
    h=h.lstrip('#')
    return [int(h[i:i+2],16)/255.0 for i in (0,2,4)]+[a]

def mb(w,c):
    r=hx(c)
    with w.canvas.before:
        Color(*r)
        w._r=Rectangle(pos=w.pos,size=w.size)
    w.bind(pos=lambda w,v:setattr(w._r,'pos',v),size=lambda w,v:setattr(w._r,'size',v))

class TankApp(App):
    def build(self):
        self.title="Tank Hacim Hesabi"
        self.S=ls2();self.fk=None;self.ti=None
        self.ew={};self.rl={};self.cl={}
        self.R=BoxLayout(orientation='vertical')
        self._m()
        return self.R

    def c(self,k):
        th=self.S.get("theme","light")
        return '#'+CS.get(th,C_L).get(k,"ffffff")
    def l(self,k):
        return LANG.get(self.S.get("lang","tr"),L_TR).get(k,k)
    def catl(self,ck):
        ci=CI.get(ck,{})
        return ci.get("le",ci.get("lt",ck)) if self.S.get("lang")=="en" else ci.get("lt",ck)
    def _sn(self): return SN if SN!="---" else "---"

    def _m(self,*a):
        self.R.clear_widgets();self.ew={};self.rl={};self.cl={};mb(self.R,self.c("BG"))
        # Header
        top=BoxLayout(orientation='vertical',size_hint_y=None,padding=[dp(8),dp(4),dp(8),dp(2)])
        top.bind(minimum_height=top.setter('height'))
        h=BoxLayout(size_hint_y=None,height=dp(36))
        h.add_widget(Label(text=self.l("app"),color=hx(self.c("TT")),font_size=sp(15),bold=True,size_hint_x=.8))
        sb=Button(text=self.l("set"),background_normal='',background_color=hx(self.c("MB")),color=hx(self.c("MF")),font_size=sp(11),bold=True,size_hint_x=.2,size_hint_y=None,height=dp(32))
        sb.bind(on_release=lambda x:self._st());h.add_widget(sb);top.add_widget(h)
        top.add_widget(Label(text=self.l("sh")+" "+self._sn(),color=hx(self.c("MU")),font_size=sp(10),size_hint_y=None,height=dp(20),halign='left',text_size=(Window.width-dp(20),None)))
        if not TD:
            top.add_widget(Label(text=self.l("nd"),color=hx(self.c("WF")),font_size=sp(13),bold=True,size_hint_y=None,height=dp(60)))
            self.R.add_widget(top);return
        # Trim (restore saved)
        tr=BoxLayout(size_hint_y=None,height=dp(40),spacing=dp(6));mb(tr,self.c("C2"))
        tr.add_widget(Label(text=self.l("trim"),color=hx(self.c("TT")),font_size=sp(12),bold=True,size_hint_x=.28))
        self.ti=TextInput(text=self.S.get("trim","2"),multiline=False,readonly=True,font_size=sp(15),halign='center',background_color=hx(self.c("EA")),foreground_color=hx(self.c("LB")),size_hint_x=.22,size_hint_y=None,height=dp(34))
        def _tt(inst,touch):
            if inst.collide_point(*touch.pos):
                self.fk=None
                if inst.text: inst.text=""
                self._hl(None)
        self.ti.bind(on_touch_down=_tt)
        tr.add_widget(self.ti)
        tr.add_widget(Label(text=self.l("dt")+" "+datetime.now().strftime('%d.%m.%Y'),color=hx(self.c("MU")),font_size=sp(9),size_hint_x=.5))
        top.add_widget(tr);self.R.add_widget(top)
        # Scrollable tank list ONLY
        sv=ScrollView(do_scroll_x=False,bar_width=dp(4),scroll_type=['bars','content'])
        inn=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(2),padding=[dp(8),dp(2),dp(8),dp(2)])
        inn.bind(minimum_height=inn.setter('height'));self.fk=None
        lcm=self.S.get("last_cm",{})
        for key in self.S.get("order",AK):
            if key not in TD or not self.S.get("vis",{}).get(key,True): continue
            d=TD[key];row=BoxLayout(size_hint_y=None,height=dp(38),spacing=dp(3));mb(row,self.c("CD"))
            row.add_widget(Label(text=d["name"],color=hx(self.c("LB")),font_size=sp(9),halign='left',size_hint_x=.42,text_size=(None,None)))
            saved_cm=lcm.get(key,"")
            ei=TextInput(text=saved_cm,multiline=False,readonly=True,halign='center',font_size=sp(14),background_color=hx(self.c("EN")),foreground_color=hx(self.c("LB")),size_hint_x=.2,size_hint_y=None,height=dp(30))
            row.add_widget(ei)
            row.add_widget(Label(text=self.l("cm"),color=hx(self.c("MU")),font_size=sp(10),size_hint_x=.1))
            rl=Label(text='--',color=hx(self.c("RC")),font_size=sp(13),bold=True,size_hint_x=.28)
            row.add_widget(rl)
            def _ft(inst,touch,k=key):
                if inst.collide_point(*touch.pos):
                    self.fk=k;self._hl(k)
                    if k in self.ew and self.ew[k].text:
                        self.ew[k].text=""
                        if k in self.rl: self.rl[k].text="--"
                        self.S.setdefault("last_cm",{}).pop(k,None);ss2(self.S)
                        self._refresh_totals()
            row.bind(on_touch_down=_ft);self.ew[key]=ei;self.rl[key]=rl;inn.add_widget(row)
            if self.fk is None: self.fk=key
            # initial calc from restored value
            if saved_cm:
                try:
                    trim=float(self.ti.text.replace(",","."))
                    vol=cv(key,saved_cm,trim)
                    if vol is not None: rl.text=f"{vol:.1f} m\u00b3"
                except: pass
        inn.add_widget(Widget(size_hint_y=None,height=dp(6)))
        sv.add_widget(inn);self.R.add_widget(sv)
        # Fixed: Calc + Export
        br=BoxLayout(size_hint_y=None,height=dp(42),spacing=dp(6),padding=[dp(8),dp(2),dp(8),dp(2)])
        c1=Button(text=self.l("calc"),background_normal='',background_color=hx(self.c("BB")),color=hx(self.c("BF")),font_size=sp(13),bold=True)
        c1.bind(on_release=lambda x:self._fc());br.add_widget(c1)
        e1=Button(text=self.l("exp"),background_normal='',background_color=hx(self.c("XB")),color=hx(self.c("XF")),font_size=sp(13),bold=True)
        e1.bind(on_release=lambda x:self._ex());br.add_widget(e1)
        self.R.add_widget(br)
        # Fixed: Category totals
        tot_box=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(2),padding=[dp(8),dp(2),dp(8),dp(2)])
        tot_box.bind(minimum_height=tot_box.setter('height'))
        for ck in self.S.get("co",AC):
            if ck not in CI or not self.S.get("vc",{}).get(ck,True): continue
            ci=CI[ck];cbg="TB";cfg="TF"
            if ci["c"]=="CAT1": cbg,cfg="AB","AF"
            elif ci["c"]=="CAT2": cbg,cfg="ZB","ZF"
            elif ci["c"]=="BIL": cbg,cfg="IB","IF"
            cr=BoxLayout(size_hint_y=None,height=dp(30));mb(cr,self.c(cbg))
            cr.add_widget(Label(text=self.catl(ck)+":",color=hx(self.c(cfg)),font_size=sp(11),bold=True,size_hint_x=.6))
            cl=Label(text="0.0  m\u00b3",color=hx(self.c(cfg)),font_size=sp(14),bold=True,size_hint_x=.4)
            cr.add_widget(cl);self.cl[ck]=cl;tot_box.add_widget(cr)
        self.R.add_widget(tot_box)
        # Numpad (GERI / ILERI instead of triangles)
        np=GridLayout(cols=4,size_hint_y=None,height=dp(215),spacing=dp(2),padding=[dp(6),dp(2),dp(6),dp(4)])
        mb(np,self.c("BG"))
        prv=self.l("prv");nxt=self.l("nxt")
        pad=[("7","NB","NF"),("8","NB","NF"),("9","NB","NF"),("-","DB","DF"),
             ("4","NB","NF"),("5","NB","NF"),("6","NB","NF"),("C","KB","KF"),
             ("1","NB","NF"),("2","NB","NF"),("3","NB","NF"),("ENT","EB","EF"),
             (".","NB","NF"),("0","NB","NF"),(prv,"VB","VF"),(nxt,"VB","VF")]
        for lb,bg,fg in pad:
            if lb==prv: cmd=lambda x:self._nv(-1)
            elif lb==nxt: cmd=lambda x:self._nv(1)
            else: cmd=lambda x,v=lb:self._pr(v)
            fsz=sp(13) if lb in (prv,nxt) else sp(18)
            b=Button(text=lb,background_normal='',background_color=hx(self.c(bg)),color=hx(self.c(fg)),font_size=fsz,bold=True,size_hint_y=None,height=dp(52))
            b.bind(on_release=cmd);np.add_widget(b)
        self.R.add_widget(np)
        self._refresh_totals()
        if self.fk: self._hl(self.fk)

    def _refresh_totals(self):
        if not self.ti or not self.cl: return
        try: trim=float(self.ti.text.replace(",","."))
        except: return
        tots={c:0.0 for c in AC}
        for k,ti in self.ew.items():
            v=ti.text.strip()
            if not v: continue
            vol=cv(k,v,trim)
            if vol is not None:
                cat=TD[k]["cat"]
                if cat in tots: tots[cat]+=vol
        for ck,cl in self.cl.items(): cl.text=f"{tots.get(ck,0):.1f}  m\u00b3"

    def _hl(self,k):
        for key,ti in self.ew.items(): ti.background_color=hx(self.c("EA")) if key==k else hx(self.c("EN"))

    def _pr(self,v):
        if v=="-":
            if self.ti:
                t=self.ti.text;self.ti.text=t[1:] if t.startswith("-") else "-"+t
                if self.fk is None:
                    self.S["trim"]=self.ti.text;ss2(self.S);self._refresh_totals()
            return
        if v=="C":
            if self.fk and self.fk in self.ew:
                self.ew[self.fk].text=""
                if self.fk in self.rl: self.rl[self.fk].text="--"
                self.S.setdefault("last_cm",{}).pop(self.fk,None);ss2(self.S)
                self._refresh_totals()
            elif not self.fk and self.ti:
                self.ti.text=""
                self.S["trim"]="";ss2(self.S)
            return
        if v=="ENT": self._sc();return
        tgt=self.ew.get(self.fk) if self.fk else self.ti
        if not tgt: return
        if v=="." and "." in tgt.text: return
        tgt.text+=v
        if self.fk is None and tgt is self.ti:
            self.S["trim"]=self.ti.text;ss2(self.S);self._refresh_totals()

    def _nv(self,d):
        ks=[k for k in self.S.get("order",AK) if k in self.ew]
        if not ks: return
        if self.fk is None or self.fk not in ks: self.fk=ks[0]
        else:
            self._sk(self.fk);i=ks.index(self.fk)+d
            if 0<=i<len(ks): self.fk=ks[i]
        # Clear value of newly focused tank
        if self.fk in self.ew and self.ew[self.fk].text:
            self.ew[self.fk].text=""
            if self.fk in self.rl: self.rl[self.fk].text="--"
            self.S.setdefault("last_cm",{}).pop(self.fk,None);ss2(self.S)
            self._refresh_totals()
        self._hl(self.fk)

    def _sc(self):
        if self.fk is None:
            ks=[k for k in self.S.get("order",AK) if k in self.ew]
            if ks: self.fk=ks[0];self._hl(self.fk)
            return
        self._sk(self.fk);self._nv(1)

    def _sk(self,k):
        try: trim=float(self.ti.text.replace(",","."))
        except: return
        ti=self.ew.get(k);rl=self.rl.get(k)
        if not ti or not rl: return
        v=ti.text.strip()
        if not v:
            rl.text="--"
            self.S.setdefault("last_cm",{}).pop(k,None)
            self.S["trim"]=self.ti.text;ss2(self.S);self._refresh_totals();return
        vol=cv(k,v,trim)
        rl.text=f"{vol:.1f} m\u00b3" if vol is not None else self.l("err")
        self.S.setdefault("last_cm",{})[k]=v
        self.S["trim"]=self.ti.text;ss2(self.S)
        self._refresh_totals()

    def _fc(self):
        try: trim=float(self.ti.text.replace(",","."))
        except: return
        tots={c:0.0 for c in AC}
        lcm=self.S.setdefault("last_cm",{})
        for k,ti in self.ew.items():
            rl=self.rl.get(k)
            if not rl: continue
            v=ti.text.strip()
            if not v:
                rl.text="--";lcm.pop(k,None);continue
            vol=cv(k,v,trim)
            if vol is not None:
                rl.text=f"{vol:.1f} m\u00b3";cat=TD[k]["cat"]
                if cat in tots: tots[cat]+=vol
                lcm[k]=v
            else: rl.text=self.l("err")
        for ck,cl in self.cl.items(): cl.text=f"{tots.get(ck,0):.1f}  m\u00b3"
        self.S["trim"]=self.ti.text;ss2(self.S)

    def _ex(self):
        self._fc()
        # Yes/No/Cancel note dialog
        ct=BoxLayout(orientation='vertical',spacing=dp(10),padding=dp(15))
        ct.add_widget(Label(text=self.l("nq"),font_size=sp(13),color=hx(self.c("LB"))))
        br=BoxLayout(size_hint_y=None,height=dp(42),spacing=dp(8))
        yb=Button(text=self.l("y"),background_normal='',background_color=hx(self.c("BB")),color=hx(self.c("BF")),font_size=sp(12),bold=True)
        nb=Button(text=self.l("n"),background_normal='',background_color=hx(self.c("XB")),color=hx(self.c("XF")),font_size=sp(12),bold=True)
        cb=Button(text=self.l("cn"),background_normal='',background_color=hx(self.c("DB")),color=hx(self.c("DF")),font_size=sp(12),bold=True)
        br.add_widget(yb);br.add_widget(nb);br.add_widget(cb);ct.add_widget(br)
        pp=Popup(title='',content=ct,size_hint=(.85,.28),auto_dismiss=False,separator_height=0)
        def _save(note=""):
            now=datetime.now()
            rec={"datetime":now.strftime("%d.%m.%Y %H:%M"),"ship":self._sn(),"trim":self.ti.text if self.ti else "","tanks":{},"totals":{},"note":note}
            for k,ti in self.ew.items():
                rl=self.rl.get(k);rec["tanks"][k]={"name":TD[k]["name"],"cm":ti.text,"vol":rl.text if rl else "--"}
            for ck,cl in self.cl.items(): rec["totals"][ck]={"label":self.catl(ck),"val":cl.text}
            h=lh();h.insert(0,rec);sh2(h);self._toast(self.l("eok"))
        def _yes(x): pp.dismiss();self._note_input(_save)
        def _no(x): pp.dismiss();_save("")
        def _cn(x): pp.dismiss()
        yb.bind(on_release=_yes);nb.bind(on_release=_no);cb.bind(on_release=_cn)
        pp.open()

    def _note_input(self,cb_save):
        ct=BoxLayout(orientation='vertical',spacing=dp(8),padding=dp(12))
        ct.add_widget(Label(text=self.l("nl"),font_size=sp(12),color=hx(self.c("LB")),size_hint_y=None,height=dp(22)))
        ni=TextInput(text='',multiline=True,font_size=sp(13),size_hint_y=None,height=dp(110))
        ct.add_widget(ni)
        br=BoxLayout(size_hint_y=None,height=dp(40),spacing=dp(8))
        sb=Button(text=self.l("save"),background_normal='',background_color=hx(self.c("BB")),color=hx(self.c("BF")),font_size=sp(12),bold=True)
        cbn=Button(text=self.l("cn"),background_normal='',background_color=hx(self.c("MB")),color=hx(self.c("MF")),font_size=sp(12),bold=True)
        br.add_widget(sb);br.add_widget(cbn);ct.add_widget(br)
        pp=Popup(title=self.l("nt"),content=ct,size_hint=(.9,.55),auto_dismiss=False)
        def _ok(x): pp.dismiss();cb_save(ni.text.strip())
        def _c(x): pp.dismiss()
        sb.bind(on_release=_ok);cbn.bind(on_release=_c)
        pp.open()
        Clock.schedule_once(lambda dt:setattr(ni,'focus',True),0.3)

    def _toast(self,msg):
        p=Popup(title='',content=Label(text=msg,font_size=sp(15),bold=True,color=hx(self.c("OF"))),size_hint=(.7,.12),background_color=hx(self.c("OB")),auto_dismiss=True,separator_height=0)
        p.open();Clock.schedule_once(lambda dt:p.dismiss(),1.5)

    # ═══ SETTINGS ═══
    def _st(self):
        self.R.clear_widgets();mb(self.R,self.c("BG"))
        hdr=BoxLayout(size_hint_y=None,height=dp(40),padding=[dp(6),0,dp(6),0])
        bb=Button(text=self.l("back"),background_normal='',background_color=hx(self.c("MB")),color=hx(self.c("MF")),font_size=sp(12),bold=True,size_hint_x=.3)
        bb.bind(on_release=lambda x:self._m());hdr.add_widget(bb)
        hdr.add_widget(Label(text=self.l("sett"),color=hx(self.c("TT")),font_size=sp(15),bold=True,size_hint_x=.7))
        self.R.add_widget(hdr)
        sv=ScrollView(do_scroll_x=False,bar_width=dp(4))
        inn=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(6),padding=[dp(10),dp(6),dp(10),dp(20)])
        inn.bind(minimum_height=inn.setter('height'))
        # Load JSON
        jb=Button(text=self.l("lj"),background_normal='',background_color=hx(self.c("JB")),color=hx(self.c("JF")),font_size=sp(13),bold=True,size_hint_y=None,height=dp(42))
        jb.bind(on_release=lambda x:self._jp());inn.add_widget(jb)
        if SN!="---": inn.add_widget(Label(text=self.l("sh")+" "+SN,color=hx(self.c("MU")),font_size=sp(10),size_hint_y=None,height=dp(20)))
        # Theme+Lang
        td=BoxLayout(size_hint_y=None,height=dp(70),spacing=dp(8))
        for grp,lk,opts in[("theme","thm",[("light","thl"),("dark","thd")]),("lang","lng",[("tr","TR"),("en","EN")])]:
            f=BoxLayout(orientation='vertical',size_hint_x=.5);mb(f,self.c("CD"))
            f.add_widget(Label(text=self.l(lk),color=hx(self.c("TT")),font_size=sp(11),bold=True,size_hint_y=None,height=dp(22)))
            for val,lbl in opts:
                txt=self.l(lbl) if lbl in LANG.get(self.S.get("lang","tr"),{}) else lbl
                b=ToggleButton(text=txt,group=grp,state='down' if self.S.get(grp)==val else 'normal',size_hint_y=None,height=dp(24),font_size=sp(10))
                b.bind(on_press=lambda x,g=grp,v=val:self.S.update({g:v}))
                f.add_widget(b)
            td.add_widget(f)
        inn.add_widget(td)
        # Tank visibility + reorder + edit/delete
        if TD:
            inn.add_widget(Label(text=self.l("tv"),color=hx(self.c("TT")),font_size=sp(11),bold=True,size_hint_y=None,height=dp(26)))
            self._vc={}
            ordered=[k for k in self.S.get("order",AK) if k in TD]
            for k in ordered:
                row=BoxLayout(size_hint_y=None,height=dp(34),spacing=dp(2));mb(row,self.c("CD"))
                cb=CheckBox(active=self.S.get("vis",{}).get(k,True),size_hint_x=.10);self._vc[k]=cb;row.add_widget(cb)
                nm=TD[k]["name"]+(f" {self.l('cu')}" if k in CT else "")
                row.add_widget(Label(text=nm,color=hx(self.c("LB")),font_size=sp(9),halign='left',size_hint_x=.44,text_size=(None,None)))
                is_custom=k in CT
                if is_custom:
                    eb=Button(text=self.l("ed"),background_normal='',background_color=hx(self.c("IB")),color=hx(self.c("IF")),font_size=sp(8),bold=True,size_hint_x=.12)
                    eb.bind(on_release=lambda x,kk=k:self._edct(kk));row.add_widget(eb)
                    rb=Button(text=self.l("rm"),background_normal='',background_color=hx(self.c("DB")),color=hx(self.c("DF")),font_size=sp(8),bold=True,size_hint_x=.12)
                    rb.bind(on_release=lambda x,kk=k:self._rmct(kk));row.add_widget(rb)
                else:
                    row.add_widget(Widget(size_hint_x=.12))
                    row.add_widget(Widget(size_hint_x=.12))
                ub=Button(text="^",background_normal='',background_color=hx(self.c("VB")),color=hx(self.c("VF")),font_size=sp(14),bold=True,size_hint_x=.11)
                ub.bind(on_release=lambda x,kk=k:self._mv(kk,-1));row.add_widget(ub)
                db=Button(text="v",background_normal='',background_color=hx(self.c("VB")),color=hx(self.c("VF")),font_size=sp(14),bold=True,size_hint_x=.11)
                db.bind(on_release=lambda x,kk=k:self._mv(kk,1));row.add_widget(db)
                inn.add_widget(row)
            ab=Button(text=self.l("at"),background_normal='',background_color=hx(self.c("XB")),color=hx(self.c("XF")),font_size=sp(11),bold=True,size_hint_y=None,height=dp(36))
            ab.bind(on_release=lambda x:self._at());inn.add_widget(ab)
        # Category totals visibility + reorder (for calc page display)
        if CI:
            inn.add_widget(Label(text=self.l("tot"),color=hx(self.c("TT")),font_size=sp(11),bold=True,size_hint_y=None,height=dp(26)))
            self._vcc={}
            co_ordered=[c for c in self.S.get("co",AC) if c in CI]
            for ck in co_ordered:
                row=BoxLayout(size_hint_y=None,height=dp(34),spacing=dp(2));mb(row,self.c("CD"))
                cb=CheckBox(active=self.S.get("vc",{}).get(ck,True),size_hint_x=.10);self._vcc[ck]=cb;row.add_widget(cb)
                row.add_widget(Label(text=self.catl(ck),color=hx(self.c("LB")),font_size=sp(10),halign='left',size_hint_x=.44,bold=True,text_size=(None,None)))
                # Spacer widgets to keep up/down arrows aligned with tank rows
                row.add_widget(Widget(size_hint_x=.12))
                row.add_widget(Widget(size_hint_x=.12))
                ub=Button(text="^",background_normal='',background_color=hx(self.c("VB")),color=hx(self.c("VF")),font_size=sp(14),bold=True,size_hint_x=.11)
                ub.bind(on_release=lambda x,kk=ck:self._mvc(kk,-1));row.add_widget(ub)
                db=Button(text="v",background_normal='',background_color=hx(self.c("VB")),color=hx(self.c("VF")),font_size=sp(14),bold=True,size_hint_x=.11)
                db.bind(on_release=lambda x,kk=ck:self._mvc(kk,1));row.add_widget(db)
                inn.add_widget(row)
        # History + Save
        hb=Button(text=self.l("hist"),background_normal='',background_color=hx(self.c("HB")),color=hx(self.c("HF")),font_size=sp(13),bold=True,size_hint_y=None,height=dp(42))
        hb.bind(on_release=lambda x:self._hi());inn.add_widget(hb)
        sb=Button(text=self.l("save"),background_normal='',background_color=hx(self.c("BB")),color=hx(self.c("BF")),font_size=sp(14),bold=True,size_hint_y=None,height=dp(46))
        sb.bind(on_release=lambda x:self._sv());inn.add_widget(sb)
        inn.add_widget(Widget(size_hint_y=None,height=dp(40)));sv.add_widget(inn);self.R.add_widget(sv)

    def _sv(self):
        if hasattr(self,'_vc'):
            for k,cb in self._vc.items(): self.S.setdefault("vis",{})[k]=cb.active
        if hasattr(self,'_vcc'):
            for k,cb in self._vcc.items(): self.S.setdefault("vc",{})[k]=cb.active
        ss2(self.S);self._m()

    def _jp(self):
        dirs=["/storage/emulated/0/Download","/sdcard/Download",os.path.expanduser("~/Download"),os.path.expanduser("~/Downloads"),DD]
        jfs=[];seen=set()
        for d in dirs:
            if not os.path.isdir(d): continue
            for f in os.listdir(d):
                if f.lower().endswith(".json") and f not in("sludge_ayar.json","sludge_gecmis.json","custom_tanks.json"):
                    fp=os.path.join(d,f)
                    if fp not in seen: seen.add(fp);jfs.append((f,fp))
        ct=BoxLayout(orientation='vertical',spacing=dp(6),padding=dp(10))
        if not jfs: ct.add_widget(Label(text=self.l("nj"),font_size=sp(12)))
        else:
            for fn,fp in jfs:
                b=Button(text=fn,size_hint_y=None,height=dp(36),font_size=sp(11))
                b.bind(on_release=lambda x,p=fp:self._dj(p));ct.add_widget(b)
        self._jpp=Popup(title=self.l("jt"),content=ct,size_hint=(.85,.5),auto_dismiss=True);self._jpp.open()

    def _dj(self,p):
        if hasattr(self,'_jpp'): self._jpp.dismiss()
        if lj(p):
            self.S["order"]=AK[:];self.S["vis"]={k:True for k in AK};self.S["co"]=AC[:];self.S["vc"]={c:True for c in AC}
            ss2(self.S);self._toast(self.l("jo"));self._st()
        else: self._toast(self.l("je"))

    def _at(self):
        ct=BoxLayout(orientation='vertical',spacing=dp(8),padding=dp(12))
        ct.add_widget(Label(text=self.l("tn"),font_size=sp(11),size_hint_y=None,height=dp(20)))
        ni=TextInput(text='',multiline=False,font_size=sp(13),size_hint_y=None,height=dp(34));ct.add_widget(ni)
        ct.add_widget(Label(text=self.l("fh"),font_size=sp(9),size_hint_y=None,height=dp(18)))
        fi=TextInput(text='',multiline=False,font_size=sp(13),size_hint_y=None,height=dp(34));ct.add_widget(fi)
        br=BoxLayout(size_hint_y=None,height=dp(38),spacing=dp(8))
        def ds(x):
            nm=ni.text.strip();fm=fi.text.strip()
            if not nm: return
            m3,cmv=1.4,115.0
            if "=" in fm:
                pts=fm.split("=")
                try: m3=float(pts[0].replace(",","."));cmv=float(pts[1].replace(",","."))
                except: pass
            base="custom_"+nm.lower().replace(" ","_")[:20];k=base;cn=1
            while k in TD: k=f"{base}_{cn}";cn+=1
            CT[k]={"name":nm,"m3":m3,"cm_max":cmv,"cat":"sludge"}
            TD[k]={"name":nm,"cat":"sludge","tip":"cf"};AK.append(k);VK.add(k)
            self.S.setdefault("order",[]).append(k);self.S.setdefault("vis",{})[k]=True
            sc2();pp.dismiss();self._st()
        sb=Button(text=self.l("ad"),background_normal='',background_color=hx(self.c("BB")),color=hx(self.c("BF")),font_size=sp(12),bold=True)
        sb.bind(on_release=ds);br.add_widget(sb)
        cb=Button(text=self.l("cn"),background_normal='',background_color=hx(self.c("MB")),color=hx(self.c("MF")),font_size=sp(12),bold=True)
        br.add_widget(cb);ct.add_widget(br)
        pp=Popup(title=self.l("at"),content=ct,size_hint=(.85,.5),auto_dismiss=True)
        cb.bind(on_release=lambda x:pp.dismiss());pp.open()

    def _save_vis_state(self):
        if hasattr(self,'_vc'):
            for k,cb in self._vc.items(): self.S.setdefault("vis",{})[k]=cb.active
        if hasattr(self,'_vcc'):
            for k,cb in self._vcc.items(): self.S.setdefault("vc",{})[k]=cb.active

    def _mvc(self,k,d):
        self._save_vis_state()
        order=self.S.setdefault("co",AC[:])
        if k not in order: return
        i=order.index(k);j=i+d
        if j<0 or j>=len(order): return
        order[i],order[j]=order[j],order[i]
        ss2(self.S);self._st()

    def _mv(self,k,d):
        self._save_vis_state()
        order=self.S.setdefault("order",AK[:])
        if k not in order: return
        i=order.index(k);j=i+d
        if j<0 or j>=len(order): return
        order[i],order[j]=order[j],order[i]
        ss2(self.S);self._st()

    def _edct(self,k):
        if k not in CT: return
        info=CT[k]
        ct=BoxLayout(orientation='vertical',spacing=dp(8),padding=dp(12))
        ct.add_widget(Label(text=self.l("tn"),font_size=sp(11),size_hint_y=None,height=dp(20),color=hx(self.c("LB"))))
        ni=TextInput(text=info.get("name",k),multiline=False,font_size=sp(13),size_hint_y=None,height=dp(34));ct.add_widget(ni)
        ct.add_widget(Label(text=self.l("fh"),font_size=sp(9),size_hint_y=None,height=dp(18),color=hx(self.c("MU"))))
        fi=TextInput(text=f"{info.get('m3',1.4)}={info.get('cm_max',115)}",multiline=False,font_size=sp(13),size_hint_y=None,height=dp(34));ct.add_widget(fi)
        br=BoxLayout(size_hint_y=None,height=dp(38),spacing=dp(8))
        def do_save(x):
            nm=ni.text.strip();fm=fi.text.strip()
            if not nm: return
            m3,cmv=info.get("m3",1.4),info.get("cm_max",115.0)
            if "=" in fm:
                pts=fm.split("=")
                try: m3=float(pts[0].replace(",","."));cmv=float(pts[1].replace(",","."))
                except: pass
            CT[k]["name"]=nm;CT[k]["m3"]=m3;CT[k]["cm_max"]=cmv
            TD[k]["name"]=nm
            sc2();self._save_vis_state();pp.dismiss();self._st()
        sb=Button(text=self.l("save"),background_normal='',background_color=hx(self.c("BB")),color=hx(self.c("BF")),font_size=sp(12),bold=True)
        sb.bind(on_release=do_save);br.add_widget(sb)
        cbn=Button(text=self.l("cn"),background_normal='',background_color=hx(self.c("MB")),color=hx(self.c("MF")),font_size=sp(12),bold=True)
        br.add_widget(cbn);ct.add_widget(br)
        pp=Popup(title=self.l("edt"),content=ct,size_hint=(.85,.5),auto_dismiss=True)
        cbn.bind(on_release=lambda x:pp.dismiss());pp.open()

    def _rmct(self,k):
        if k not in CT: return
        ct=BoxLayout(orientation='vertical',spacing=dp(10),padding=dp(15))
        ct.add_widget(Label(text=self.l("rmq"),font_size=sp(12),color=hx(self.c("LB")),size_hint_y=None,height=dp(26)))
        ct.add_widget(Label(text=TD[k]["name"],font_size=sp(13),bold=True,color=hx(self.c("DF")),size_hint_y=None,height=dp(28)))
        br=BoxLayout(size_hint_y=None,height=dp(40),spacing=dp(10))
        yb=Button(text=self.l("y"),background_normal='',background_color=hx(self.c("DB")),color=hx(self.c("DF")),font_size=sp(13),bold=True)
        nb=Button(text=self.l("n"),background_normal='',background_color=hx(self.c("MB")),color=hx(self.c("MF")),font_size=sp(13),bold=True)
        br.add_widget(yb);br.add_widget(nb);ct.add_widget(br)
        pp=Popup(title='',content=ct,size_hint=(.85,.32),auto_dismiss=False,separator_height=0)
        def do_del(x):
            self._save_vis_state()
            CT.pop(k,None);TD.pop(k,None)
            if k in AK: AK.remove(k)
            VK.discard(k)
            if k in self.S.get("order",[]): self.S["order"].remove(k)
            self.S.get("vis",{}).pop(k,None)
            self.S.get("last_cm",{}).pop(k,None)
            sc2();ss2(self.S);pp.dismiss();self._st()
        yb.bind(on_release=do_del);nb.bind(on_release=lambda x:pp.dismiss())
        pp.open()

    # ═══ HISTORY ═══
    def _hi(self):
        self.R.clear_widgets();mb(self.R,self.c("BG"));hist=lh()
        hdr=BoxLayout(size_hint_y=None,height=dp(40),padding=[dp(6),0,dp(6),0])
        bb=Button(text=self.l("back"),background_normal='',background_color=hx(self.c("MB")),color=hx(self.c("MF")),font_size=sp(12),bold=True,size_hint_x=.3)
        bb.bind(on_release=lambda x:self._st());hdr.add_widget(bb)
        hdr.add_widget(Label(text=self.l("ht"),color=hx(self.c("TT")),font_size=sp(15),bold=True,size_hint_x=.7))
        self.R.add_widget(hdr)
        if not hist: self.R.add_widget(Label(text=self.l("noh"),color=hx(self.c("MU")),font_size=sp(13)));return
        sv=ScrollView(do_scroll_x=False,bar_width=dp(4))
        inn=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(4),padding=[dp(8),dp(4),dp(8),dp(4)])
        inn.bind(minimum_height=inn.setter('height'));self._hc=[]
        for idx,rec in enumerate(hist):
            cd=BoxLayout(orientation='vertical',size_hint_y=None,padding=dp(6),spacing=dp(2))
            cd.bind(minimum_height=cd.setter('height'));mb(cd,self.c("CD"))
            tr=BoxLayout(size_hint_y=None,height=dp(24))
            cb=CheckBox(active=False,size_hint_x=.1);self._hc.append((idx,cb));tr.add_widget(cb)
            tr.add_widget(Label(text=f"{self.l('rec')} #{idx+1}",color=hx(self.c("TT")),font_size=sp(11),bold=True,size_hint_x=.5))
            tr.add_widget(Label(text=rec.get("datetime","?"),color=hx(self.c("MU")),font_size=sp(9),size_hint_x=.4,halign='right'))
            cd.add_widget(tr)
            cd.add_widget(Label(text=f"{self.l('ts')}: {rec.get('trim','?')} m",color=hx(self.c("LB")),font_size=sp(9),size_hint_y=None,height=dp(16),halign='left',text_size=(Window.width-dp(30),None)))
            for tk,td in rec.get("tanks",{}).items():
                if isinstance(td,dict) and td.get("cm"):
                    cd.add_widget(Label(text=f"  {td.get('name',tk)}: {td['cm']} cm > {td.get('vol','--')}",color=hx(self.c("LB")),font_size=sp(8),size_hint_y=None,height=dp(14),halign='left',text_size=(Window.width-dp(30),None)))
            for ck,cd2 in rec.get("totals",{}).items():
                if isinstance(cd2,dict):
                    cd.add_widget(Label(text=f"  {cd2.get('label',ck)}: {cd2.get('val','0.0')}",color=hx(self.c("RC")),font_size=sp(9),bold=True,size_hint_y=None,height=dp(16),halign='left',text_size=(Window.width-dp(30),None)))
            nt=rec.get("note","")
            if nt:
                cd.add_widget(Label(text=f"  {self.l('nl')} {nt}",color=hx(self.c("HF")),font_size=sp(9),bold=True,size_hint_y=None,height=dp(16),halign='left',text_size=(Window.width-dp(30),None)))
            inn.add_widget(cd)
        inn.add_widget(Widget(size_hint_y=None,height=dp(20)));sv.add_widget(inn);self.R.add_widget(sv)
        bot=BoxLayout(size_hint_y=None,height=dp(76),orientation='vertical',spacing=dp(3),padding=[dp(8),dp(2),dp(8),dp(4)])
        pe=Button(text=self.l("pe"),background_normal='',background_color=hx(self.c("XB")),color=hx(self.c("XF")),font_size=sp(11),bold=True,size_hint_y=None,height=dp(32))
        pe.bind(on_release=lambda x:self._pdf(hist));bot.add_widget(pe)
        br=BoxLayout(size_hint_y=None,height=dp(32),spacing=dp(6))
        ds=Button(text=self.l("ds"),background_normal='',background_color=hx(self.c("DB")),color=hx(self.c("DF")),font_size=sp(10),bold=True)
        ds.bind(on_release=lambda x:self._dsl(hist));br.add_widget(ds)
        da=Button(text=self.l("da"),background_normal='',background_color=hx(self.c("KB")),color=hx(self.c("KF")),font_size=sp(10),bold=True)
        da.bind(on_release=lambda x:self._dal());br.add_widget(da);bot.add_widget(br);self.R.add_widget(bot)

    def _dsl(self,hist):
        td2=sorted({i for i,cb in self._hc if cb.active})
        if not td2:
            self._toast(self.l("no_sel"));return
        # Build list of record names to confirm
        names=[f"#{i+1} - {hist[i].get('datetime','?')}" for i in td2]
        self._confirm_delete(self.l("dsq"),names,lambda: (sh2([r for i,r in enumerate(hist) if i not in set(td2)]),self._hi()))

    def _dal(self):
        hist=lh()
        if not hist:
            self._toast(self.l("noh"));return
        names=[f"#{i+1} - {r.get('datetime','?')}" for i,r in enumerate(hist)]
        self._confirm_delete(self.l("dsa"),names,lambda: (sh2([]),self._hi()))

    def _confirm_delete(self,question,names,action):
        ct=BoxLayout(orientation='vertical',spacing=dp(8),padding=dp(12))
        ct.add_widget(Label(text=question,font_size=sp(12),bold=True,color=hx(self.c("LB")),size_hint_y=None,height=dp(26)))
        # scrollable list of names
        sv=ScrollView(do_scroll_x=False,bar_width=dp(3),size_hint_y=1)
        inn=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(2))
        inn.bind(minimum_height=inn.setter('height'))
        for nm in names:
            inn.add_widget(Label(text=nm,font_size=sp(10),color=hx(self.c("DF")),size_hint_y=None,height=dp(20),halign='left',text_size=(Window.width*.75,None)))
        sv.add_widget(inn);ct.add_widget(sv)
        br=BoxLayout(size_hint_y=None,height=dp(40),spacing=dp(10))
        yb=Button(text=self.l("y"),background_normal='',background_color=hx(self.c("DB")),color=hx(self.c("DF")),font_size=sp(13),bold=True)
        nb=Button(text=self.l("n"),background_normal='',background_color=hx(self.c("MB")),color=hx(self.c("MF")),font_size=sp(13),bold=True)
        br.add_widget(yb);br.add_widget(nb);ct.add_widget(br)
        pp=Popup(title='',content=ct,size_hint=(.88,.6),auto_dismiss=False,separator_height=0)
        def dd(x): pp.dismiss();action()
        yb.bind(on_release=dd);nb.bind(on_release=lambda x:pp.dismiss());pp.open()

    def _pdf(self,hist):
        if not hist: return
        fn=f"sludge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        dirs=["/storage/emulated/0/Download","/sdcard/Download",DD]
        sd=DD
        for d in dirs:
            if os.path.isdir(d): sd=d;break
        fp=os.path.join(sd,fn)
        try: self._wp(hist,fp);self._toast(f"{self.l('po')}\n{fp}")
        except: self._toast(self.l("pf"))

    def _wp(self,hist,path):
        PW,PH=595.28,841.89;M=28;CO,RO=2,3
        CW=(PW-2*M-10)/CO;CH=(PH-2*M-60)/RO;GX,GY=10,6
        def e(t):
            for a,b in[("\\","\\\\"),("(","\\("),(")","\\/"),("\u00b3","3"),("\u0130","I"),("\u0131","i"),("\u015f","s"),("\u015e","S"),("\u011f","g"),("\u011e","G"),("\u00fc","u"),("\u00dc","U"),("\u00f6","o"),("\u00d6","O"),("\u00e7","c"),("\u00c7","C")]: t=t.replace(a,b)
            return t
        def pv(vs):
            # Parse "12.5 m³" or "12.5 m3" -> 12.5
            try: return float(vs.replace("m\u00b3","").replace("m3","").replace("m","").strip())
            except: return None
        cks=[hist[i:i+6] for i in range(0,len(hist),6)]
        n_data=len(cks)
        has_chart=False
        tp=n_data
        def ps(recs,pn):
            s=[]
            ship_title=e(self._sn()+' - '+self.l('ht'))
            pg_txt=e(self.l("pg")+" "+str(pn)+"/"+str(tp))
            s.append(f"BT /F1 11 Tf {M} {PH-M-14} Td ({ship_title}) Tj ET")
            s.append(f"BT /F1 8 Tf {PW-M-50} {PH-M-14} Td ({pg_txt}) Tj ET")
            s.append(f"{M} {PH-M-22} m {PW-M} {PH-M-22} l S");ty=PH-M-40
            for idx,rec in enumerate(recs):
                col=idx%CO;row=idx//CO;cx=M+col*(CW+GX);cy=ty-row*(CH+GY)
                s.append(f"0.85 0.85 0.85 rg {cx} {cy-CH} {CW} {CH} re f")
                s.append(f"0 0 0 rg {cx} {cy-CH} {CW} {CH} re S")
                ly=cy-14
                rec_title=e(self.l("rec")+" - "+rec.get("datetime","?"))
                s.append(f"BT /F2 9 Tf {cx+6} {ly} Td ({rec_title}) Tj ET")
                ly-=4;s.append(f"{cx+4} {ly} m {cx+CW-4} {ly} l S");ly-=12
                trim_txt=e(self.l("ts")+": "+rec.get("trim","?")+" m")
                s.append(f"BT /F1 8 Tf {cx+6} {ly} Td ({trim_txt}) Tj ET");ly-=11
                # Önceki kayıt (kronolojik olarak): hist yeniden eskiye, recs bu sayfanın dilimi
                # Global index: bu rec'in hist içindeki yeri
                global_idx=hist.index(rec)
                prev_rec=hist[global_idx+1] if global_idx+1<len(hist) else None
                for tk,td in rec.get("tanks",{}).items():
                    if isinstance(td,dict) and td.get("cm"):
                        if ly<cy-CH+30: break
                        cur_v=pv(td.get("vol",""))
                        diff_str="";diff_color=None
                        if prev_rec is not None:
                            ptd=prev_rec.get("tanks",{}).get(tk)
                            if isinstance(ptd,dict) and ptd.get("cm"):
                                pv_=pv(ptd.get("vol",""))
                                if cur_v is not None and pv_ is not None:
                                    d=cur_v-pv_
                                    if abs(d)>=0.05:
                                        diff_str=f" ({d:+.1f})"
                                        diff_color=(1,0,0) if d>0 else (0,0.55,0)
                        base_txt=f"{td.get('name',tk)}: {td['cm']} cm > {td.get('vol','--')}"
                        # Siyah ana metin
                        s.append(f"0 0 0 rg BT /F1 7 Tf {cx+8} {ly} Td ({e(base_txt)}) Tj ET")
                        # Renkli fark (varsa) — ana metnin yaklaşık genişliği kadar sağa kaydır
                        if diff_str and diff_color:
                            off=len(base_txt)*3.6  # Helvetica 7pt için kaba karakter genişliği
                            r,g,b=diff_color
                            s.append(f"{r} {g} {b} rg BT /F2 7 Tf {cx+8+off} {ly} Td ({e(diff_str)}) Tj ET")
                            s.append("0 0 0 rg")
                        ly-=10
                for ck,cd in rec.get("totals",{}).items():
                    if isinstance(cd,dict):
                        if ly<cy-CH+8: break
                        tot_txt=e(cd.get('label',ck)+": "+cd.get('val','0.0'))
                        s.append(f"BT /F2 8 Tf {cx+6} {ly} Td ({tot_txt}) Tj ET");ly-=11
                nt=rec.get("note","")
                if nt and ly>=cy-CH+8:
                    note_txt=e(self.l("nl")+" "+nt)
                    maxc=int((CW-12)/3.5)
                    if len(note_txt)>maxc: note_txt=note_txt[:maxc]+"..."
                    s.append(f"BT /F2 7 Tf {cx+6} {ly} Td ({note_txt}) Tj ET");ly-=10
            return "\n".join(s)
        def cs(pn):
            # Chart page: tank volume deltas from first record
            recs=list(reversed(hist))  # chronological: oldest first
            s=[]
            ship_title=e(self._sn()+' - '+self.l('chrt'))
            pg_txt=e(self.l("pg")+" "+str(pn)+"/"+str(tp))
            s.append(f"BT /F2 12 Tf {M} {PH-M-14} Td ({ship_title}) Tj ET")
            s.append(f"BT /F1 8 Tf {PW-M-50} {PH-M-14} Td ({pg_txt}) Tj ET")
            s.append(f"0 0 0 RG 1 w {M} {PH-M-22} m {PW-M} {PH-M-22} l S")
            # Parse tank volumes across records
            tank_data={};tank_names={}
            for rec in recs:
                for tk,td in rec.get("tanks",{}).items():
                    if not isinstance(td,dict): continue
                    v=pv(td.get("vol",""))
                    tank_data.setdefault(tk,[]).append(v)
                    tank_names[tk]=td.get("name",tk)
            n_recs=len(recs)
            for tk in tank_data:
                while len(tank_data[tk])<n_recs: tank_data[tk].append(None)
            # Only tanks with a valid baseline
            usable=[(tk,vals) for tk,vals in tank_data.items() if vals[0] is not None]
            if not usable:
                s.append(f"BT /F1 10 Tf {M+20} {PH/2} Td (No chart data) Tj ET")
                return "\n".join(s)
            # Deltas from first record
            deltas={}
            for tk,vals in usable:
                base=vals[0]
                deltas[tk]=[(v-base) if v is not None else None for v in vals]
            # Max absolute delta for scaling
            max_abs=0.001
            for vals in deltas.values():
                for v in vals:
                    if v is not None and abs(v)>max_abs: max_abs=abs(v)
            # Chart area
            cx_l=60.0;cx_r=PW-30.0;cy_b=200.0;cy_t=PH-70.0
            cw=cx_r-cx_l;chh=cy_t-cy_b
            cy_mid=(cy_b+cy_t)/2;half_h=chh/2
            # Chart background + border
            s.append(f"0.97 0.97 0.97 rg {cx_l} {cy_b} {cw} {chh} re f")
            s.append(f"0 0 0 RG 0.5 w {cx_l} {cy_b} {cw} {chh} re S")
            # Grid lines + Y axis labels
            for frac in [-1.0,-0.5,0.0,0.5,1.0]:
                y=cy_mid+half_h*frac
                val=max_abs*frac
                if frac==0:
                    s.append(f"0 0 0 RG 0.9 w {cx_l} {y} m {cx_r} {y} l S")
                else:
                    s.append(f"0.75 0.75 0.75 RG 0.3 w {cx_l} {y} m {cx_r} {y} l S")
                lbl=f"{val:+.1f}" if frac!=0 else "0.0"
                s.append(f"0 0 0 rg BT /F1 7 Tf {cx_l-32} {y-2} Td ({lbl}) Tj ET")
            # Y axis unit label (rotated would be complex, place top-left)
            s.append(f"BT /F2 7 Tf {cx_l-32} {cy_t+6} Td (m3) Tj ET")
            # X axis: record labels
            group_w=cw/max(n_recs,1)
            n_tanks=len(usable)
            bar_group=group_w*0.8
            bar_w=bar_group/max(n_tanks,1)
            for ri in range(n_recs):
                gx=cx_l+ri*group_w+group_w/2
                s.append(f"BT /F2 7 Tf {gx-6} {cy_b-12} Td (R{ri+1}) Tj ET")
                dt=recs[ri].get("datetime","")[:10]
                if dt:
                    s.append(f"BT /F1 5 Tf {gx-15} {cy_b-20} Td ({e(dt)}) Tj ET")
            # Colors for tanks (cycle)
            colors=[(0.20,0.45,0.85),(0.85,0.25,0.25),(0.25,0.70,0.30),(0.95,0.60,0.10),
                    (0.55,0.25,0.75),(0.15,0.70,0.70),(0.80,0.45,0.60),(0.50,0.55,0.20),
                    (0.35,0.55,0.35),(0.75,0.40,0.15),(0.30,0.30,0.65),(0.65,0.20,0.45)]
            # Draw bars: grouped by record, one bar per tank
            for ti,(tk,_) in enumerate(usable):
                r,g,b=colors[ti%len(colors)]
                for ri,dv in enumerate(deltas[tk]):
                    if dv is None: continue
                    bx=cx_l+ri*group_w+group_w*0.1+ti*bar_w
                    h=(dv/max_abs)*half_h
                    if h>=0: by=cy_mid;bh=h
                    else: by=cy_mid+h;bh=-h
                    if bh<0.8: bh=0.8
                    bww=bar_w-0.4
                    if bww<0.5: bww=0.5
                    s.append(f"{r:.2f} {g:.2f} {b:.2f} rg {bx:.2f} {by:.2f} {bww:.2f} {bh:.2f} re f")
                    # Small value label above/below bar for readability
                    if abs(dv)>=0.1:
                        lv=f"{dv:+.1f}"
                        ly_lbl=(by+bh+2) if h>=0 else (by-7)
                        s.append(f"0 0 0 rg BT /F1 5 Tf {bx-2} {ly_lbl} Td ({lv}) Tj ET")
            # Legend below chart
            lg_y=cy_b-42
            lg_cols=3
            col_w=cw/lg_cols
            for ti,(tk,_) in enumerate(usable):
                r,g,b=colors[ti%len(colors)]
                col=ti%lg_cols;row=ti//lg_cols
                lx=cx_l+col*col_w
                ly=lg_y-row*12
                if ly<35: break
                s.append(f"{r:.2f} {g:.2f} {b:.2f} rg {lx} {ly} 9 9 re f")
                s.append(f"0 0 0 RG 0.3 w {lx} {ly} 9 9 re S")
                nm=tank_names.get(tk,tk)
                if len(nm)>24: nm=nm[:22]+".."
                s.append(f"0 0 0 rg BT /F1 7 Tf {lx+12} {ly+1} Td ({e(nm)}) Tj ET")
            return "\n".join(s)
        # Build page streams
        page_streams=[]
        for pi,ch in enumerate(cks): page_streams.append(ps(ch,pi+1))
        # Write PDF
        xo=[];buf=[];pos=[0]
        def w(sd):
            d=sd if isinstance(sd,bytes) else sd.encode("latin-1","replace");buf.append(d);pos[0]+=len(d)
        w("%PDF-1.4\n");xo.append(pos[0]);w("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n");xo.append(pos[0])
        pids=[3+i*2 for i in range(tp)];w(f"2 0 obj\n<< /Type /Pages /Kids [{' '.join(f'{p} 0 R' for p in pids)}] /Count {tp} >>\nendobj\n")
        fs=3+tp*2
        for pi,stream_txt in enumerate(page_streams):
            st=stream_txt.encode("latin-1","replace");po=3+pi*2;so=4+pi*2;xo.append(pos[0])
            w(f"{po} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PW} {PH}] /Contents {so} 0 R /Resources << /Font << /F1 {fs} 0 R /F2 {fs+1} 0 R >> >> >>\nendobj\n")
            xo.append(pos[0]);w(f"{so} 0 obj\n<< /Length {len(st)} >>\nstream\n");w(st);w(b"\nendstream\nendobj\n")
        xo.append(pos[0]);w(f"{fs} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
        xo.append(pos[0]);w(f"{fs+1} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")
        to=fs+1;xp=pos[0];w("xref\n");w(f"0 {to+1}\n");w("0000000000 65535 f \n")
        for o in xo: w(f"{o:010d} 00000 n \n")
        w(f"trailer\n<< /Size {to+1} /Root 1 0 R >>\nstartxref\n{xp}\n%%EOF\n")
        with open(path,"wb") as f:
            for ch2 in buf: f.write(ch2 if isinstance(ch2,bytes) else ch2.encode("latin-1","replace"))

if __name__=='__main__':
    TankApp().run()
