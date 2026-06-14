#!/usr/bin/env python3
"""Add all 15 generated PDFs as a purchasable catalog in the store section."""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. CATALOG CSS (inject before </style>) ───────────────────────────────
catalog_css = """
/* ══════════════════════════════════════════════════════
   PDF CATALOG GRID — 15 Guides
   ══════════════════════════════════════════════════════ */
.pdf-catalog-wrap{margin-top:40px;}
.pdf-catalog-intro{text-align:center;margin-bottom:28px;}
.pdf-catalog-intro .stag{margin-bottom:6px;}
.pdf-catalog-intro .sh{font-size:clamp(26px,4.5vw,46px)!important;}
.pdf-catalog-intro .ssub{margin:8px auto 0;max-width:560px;}
.pdf-catalog-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;margin-top:28px;}
.pcc{background:#fff;border:1.5px solid #e2d4f8;border-radius:12px;padding:18px 16px;display:flex;flex-direction:column;gap:8px;transition:transform .2s,box-shadow .2s;position:relative;overflow:hidden;}
.pcc::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#7c3aed,#a855f7);}
.pcc:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(124,58,237,.12);}
.pcc-icon{font-size:28px;line-height:1;}
.pcc-badge{font-size:8px;letter-spacing:2px;text-transform:uppercase;background:rgba(124,58,237,.1);color:#7c3aed;padding:2px 8px;border-radius:3px;display:inline-block;width:fit-content;}
.pcc-badge.advanced{background:rgba(232,0,29,.1);color:#e8001d;}
.pcc-badge.women{background:rgba(236,72,153,.1);color:#db2777;}
.pcc-badge.nutrition{background:rgba(34,197,94,.1);color:#16a34a;}
.pcc-badge.hormones{background:rgba(245,158,11,.1);color:#d97706;}
.pcc-badge.recovery{background:rgba(56,189,248,.1);color:#0284c7;}
.pcc-badge.supplements{background:rgba(168,85,247,.1);color:#9333ea;}
.pcc-title{font-family:'Bebas Neue',sans-serif;font-size:17px;letter-spacing:.5px;color:#1e1b4b;line-height:1.15;}
.pcc-sub{font-size:10px;color:#6b7280;line-height:1.4;flex:1;}
.pcc-price-row{display:flex;align-items:baseline;gap:7px;margin-top:2px;}
.pcc-price{font-family:'Bebas Neue',sans-serif;font-size:24px;color:#7c3aed;line-height:1;}
.pcc-orig{font-size:11px;color:#9ca3af;text-decoration:line-through;}
.pcc-off{font-size:9px;background:#7c3aed;color:#fff;padding:1px 5px;border-radius:2px;letter-spacing:1px;}
.pcc-buy{width:100%;background:linear-gradient(135deg,#7c3aed,#a855f7);color:#fff;border:none;border-radius:6px;padding:9px 8px;font-family:'Barlow Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;cursor:pointer;transition:opacity .15s,transform .15s;margin-top:4px;}
.pcc-buy:hover{opacity:.88;transform:translateY(-1px);}
.pcc-dl{width:100%;background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;border:none;border-radius:6px;padding:9px 8px;font-family:'Barlow Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;cursor:pointer;text-align:center;text-decoration:none;display:flex;align-items:center;justify-content:center;gap:5px;margin-top:4px;}
.pcc-owned{display:flex;align-items:center;gap:5px;font-size:11px;color:#16a34a;font-weight:600;margin-top:4px;padding:7px 0;}
.pcc-owned::before{content:'✅';}
/* All Products stats bar */
.pdf-allstats{display:flex;gap:0;background:#fff;border:1px solid #e2d4f8;border-radius:10px;overflow:hidden;margin-bottom:28px;box-shadow:0 2px 10px rgba(124,58,237,.06);}
.pdf-allstat{flex:1;text-align:center;padding:14px 8px;border-right:1px solid #e2d4f8;}
.pdf-allstat:last-child{border-right:none;}
.pdf-allstat-n{font-family:'Bebas Neue',sans-serif;font-size:26px;color:#7c3aed;line-height:1;}
.pdf-allstat-l{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#9ca3af;margin-top:2px;}
/* Filter bar */
.pdf-cat-filter{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:20px;justify-content:center;}
.pcf{background:#fff;border:1.5px solid #e2d4f8;color:#6b7280;padding:5px 14px;border-radius:100px;font-family:'Barlow Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;cursor:pointer;transition:all .15s;}
.pcf:hover,.pcf.active{background:#7c3aed;border-color:#7c3aed;color:#fff;}
@media(max-width:600px){
  .pdf-catalog-grid{grid-template-columns:1fr 1fr;}
  .pcc-title{font-size:15px;}
  .pdf-allstats{flex-wrap:wrap;}
  .pdf-allstat{min-width:50%;}
}
@media(max-width:380px){
  .pdf-catalog-grid{grid-template-columns:1fr;}
}
"""
html = html.replace('</style>', catalog_css + '</style>', 1)

# ── 2. UPDATE STORE HEADER TEXT ───────────────────────────────────────────
html = html.replace(
    '<p class="ssub">Two comprehensive guides — pick what you need, or get both and build your complete transformation system.</p>',
    '<p class="ssub">17 expert guides — from cutting cycles to mindset mastery. Pick what you need or build your complete transformation library.</p>'
)

# ── 3. UPDATE STORE TAG ───────────────────────────────────────────────────
html = html.replace(
    '<div class="stag">Royal Knowledge Store</div>\n    <div class="sh">KNOWLEDGE GUIDES</div>',
    '<div class="stag">Royal Knowledge Store — 17 Expert Guides</div>\n    <div class="sh">KNOWLEDGE GUIDES</div>'
)

# ── 4. INSERT CATALOG HTML (after store-product-tabs closing div) ─────────
catalog_html = """
    <!-- ═══════════════════════════════════════════════════ -->
    <!-- ALL 15 PDF GUIDES CATALOG                          -->
    <!-- ═══════════════════════════════════════════════════ -->
    <div class="pdf-catalog-wrap" id="pdf-catalog-wrap">
      <div class="pdf-catalog-intro">
        <div class="stag">All 15 Expert Guides</div>
        <div class="sh">COMPLETE COLLECTION</div>
        <p class="ssub">Every guide written by Royal Fitness Club experts. One-time purchase · Instant download · Lifetime access.</p>
      </div>
      <!-- Stats -->
      <div class="pdf-allstats">
        <div class="pdf-allstat"><div class="pdf-allstat-n">15</div><div class="pdf-allstat-l">Guides</div></div>
        <div class="pdf-allstat"><div class="pdf-allstat-n">2,400+</div><div class="pdf-allstat-l">Copies Sold</div></div>
        <div class="pdf-allstat"><div class="pdf-allstat-n">4.9★</div><div class="pdf-allstat-l">Rating</div></div>
        <div class="pdf-allstat"><div class="pdf-allstat-n">₹199+</div><div class="pdf-allstat-l">From</div></div>
      </div>
      <!-- Filter -->
      <div class="pdf-cat-filter">
        <button class="pcf active" onclick="filterCatalog('all',this)">All</button>
        <button class="pcf" onclick="filterCatalog('advanced',this)">Advanced</button>
        <button class="pcf" onclick="filterCatalog('nutrition',this)">Nutrition</button>
        <button class="pcf" onclick="filterCatalog('hormones',this)">Hormones</button>
        <button class="pcf" onclick="filterCatalog('women',this)">Women</button>
        <button class="pcf" onclick="filterCatalog('training',this)">Training</button>
        <button class="pcf" onclick="filterCatalog('recovery',this)">Recovery</button>
      </div>
      <!-- Cards rendered by JS -->
      <div class="pdf-catalog-grid" id="pdf-catalog-grid"></div>
    </div>
    <div class="store-section-sep"></div>
"""

html = html.replace(
    '\n    <!-- ═══════════════════════════════════════════════════ -->\n    <!-- PRODUCT 1 — FITNESS & MINDSET GUIDANCE PDF         -->',
    catalog_html + '\n    <!-- ═══════════════════════════════════════════════════ -->\n    <!-- PRODUCT 1 — FITNESS & MINDSET GUIDANCE PDF         -->'
)

# ── 5. REPLACE PDF_PRODUCTS + add catalog JS ─────────────────────────────
old_products = """const PDF_PRODUCTS = {
  anabolic_full_guide: {
    desc: 'Anabolic Full Guide — Complete PDF',
    amount: 29900,
    theme: '#e8001d',
    localKey: 'bm_pdf_anabolic',
    buyBtnId: 'pdf-buy-btn',
    dlBtnId: 'pdf-download-btn',
    badgeId: 'pdf-purchased-badge',
    getUrl: ()=>ANABOLIC_PDF_URL,
  },
  fitness_mindset: {
    desc: 'Fitness & Mindset Guidance — Complete PDF',
    amount: 29900,
    theme: '#0066cc',
    localKey: 'bm_pdf_fitness',
    buyBtnId: 'fm-buy-btn',
    dlBtnId: 'fm-download-btn',
    badgeId: 'fm-purchased-badge',
    getUrl: ()=>FITNESS_MINDSET_PDF_URL,
  },
};"""

new_products = """const PDF_PRODUCTS = {
  anabolic_full_guide: {
    desc: 'Anabolic Full Guide — Complete PDF',
    amount: 29900,
    theme: '#e8001d',
    localKey: 'bm_pdf_anabolic',
    buyBtnId: 'pdf-buy-btn',
    dlBtnId: 'pdf-download-btn',
    badgeId: 'pdf-purchased-badge',
    getUrl: ()=>ANABOLIC_PDF_URL,
  },
  fitness_mindset: {
    desc: 'Fitness & Mindset Guidance — Complete PDF',
    amount: 29900,
    theme: '#0066cc',
    localKey: 'bm_pdf_fitness',
    buyBtnId: 'fm-buy-btn',
    dlBtnId: 'fm-download-btn',
    badgeId: 'fm-purchased-badge',
    getUrl: ()=>FITNESS_MINDSET_PDF_URL,
  },
  // ── 15 generated expert guides ──
  pdf_01:{desc:'Advanced Cutting Cycle 12-Week Protocol',amount:29900,theme:'#e8001d',localKey:'bm_pdf_01',getUrl:()=>'/generated_pdfs/01_Advanced_Cutting_Cycle_12Weeks.pdf'},
  pdf_02:{desc:'Advanced Bulking Cycle with Peptides',amount:29900,theme:'#7c3aed',localKey:'bm_pdf_02',getUrl:()=>'/generated_pdfs/02_Advanced_Bulking_Cycle_with_Peptides.pdf'},
  pdf_03:{desc:'Beginner Steroid Cycle Full Guide',amount:29900,theme:'#e8001d',localKey:'bm_pdf_03',getUrl:()=>'/generated_pdfs/03_Beginner_Steroid_Cycle_Full_Guide.pdf'},
  pdf_04:{desc:'30-Day Keto Indian Vegetarian Plan',amount:24900,theme:'#16a34a',localKey:'bm_pdf_04',getUrl:()=>'/generated_pdfs/04_30Day_Keto_Indian_Vegetarian_Plan.pdf'},
  pdf_05:{desc:'Female Vegetarian Weight Loss Plan',amount:24900,theme:'#db2777',localKey:'bm_pdf_05',getUrl:()=>'/generated_pdfs/05_Female_Vegetarian_Weight_Loss_Plan.pdf'},
  pdf_06:{desc:'Complete Peptide Protocol Bible',amount:34900,theme:'#7c3aed',localKey:'bm_pdf_06',getUrl:()=>'/generated_pdfs/06_Complete_Peptide_Protocol_Bible.pdf'},
  pdf_07:{desc:'SARMs Complete Scientific Handbook',amount:34900,theme:'#7c3aed',localKey:'bm_pdf_07',getUrl:()=>'/generated_pdfs/07_SARMs_Complete_Scientific_Handbook.pdf'},
  pdf_08:{desc:'TRT & Hormone Optimization Guide',amount:34900,theme:'#d97706',localKey:'bm_pdf_08',getUrl:()=>'/generated_pdfs/08_TRT_Hormone_Optimization_Guide.pdf'},
  pdf_09:{desc:'Science of Muscle Hypertrophy',amount:29900,theme:'#7c3aed',localKey:'bm_pdf_09',getUrl:()=>'/generated_pdfs/09_Science_of_Muscle_Hypertrophy.pdf'},
  pdf_10:{desc:'Ultimate Fat Loss Masterclass',amount:29900,theme:'#e8001d',localKey:'bm_pdf_10',getUrl:()=>'/generated_pdfs/10_Ultimate_Fat_Loss_Masterclass.pdf'},
  pdf_11:{desc:"Women's Complete Body Transformation",amount:24900,theme:'#db2777',localKey:'bm_pdf_11',getUrl:()=>'/generated_pdfs/11_Womens_Complete_Body_Transformation.pdf'},
  pdf_12:{desc:'Indian Bodybuilder Nutrition Bible',amount:29900,theme:'#16a34a',localKey:'bm_pdf_12',getUrl:()=>'/generated_pdfs/12_Indian_Bodybuilder_Nutrition_Bible.pdf'},
  pdf_13:{desc:'Pre-Workout Optimization Guide',amount:19900,theme:'#9333ea',localKey:'bm_pdf_13',getUrl:()=>'/generated_pdfs/13_PreWorkout_Optimization_Guide.pdf'},
  pdf_14:{desc:'Natural Testosterone Optimization',amount:29900,theme:'#d97706',localKey:'bm_pdf_14',getUrl:()=>'/generated_pdfs/14_Natural_Testosterone_Optimization.pdf'},
  pdf_15:{desc:'Recovery, Sleep & CNS Restoration',amount:19900,theme:'#0284c7',localKey:'bm_pdf_15',getUrl:()=>'/generated_pdfs/15_Recovery_Sleep_CNS_Restoration.pdf'},
};

// ── PDF CATALOG DATA ──────────────────────────────────────────────────────
const PDF_CATALOG = [
  {id:'pdf_01',icon:'🔥',badge:'advanced',cat:'ADVANCED',title:'Advanced Cutting Cycle',sub:'12-Week Complete Protocol · Steroid + Cardio',orig:599,price:299},
  {id:'pdf_02',icon:'💪',badge:'advanced',cat:'ADVANCED',title:'Advanced Bulking Cycle',sub:'With Peptides · Mass Building Protocol',orig:599,price:299},
  {id:'pdf_03',icon:'🧬',badge:'advanced',cat:'ADVANCED',title:'Beginner Steroid Cycle',sub:'Full Guide · Safe Entry-Level Protocol',orig:499,price:299},
  {id:'pdf_04',icon:'🥗',badge:'nutrition',cat:'NUTRITION',title:'30-Day Keto Indian Plan',sub:'Vegetarian · Desi-Friendly Meal Templates',orig:399,price:249},
  {id:'pdf_05',icon:'👩',badge:'women',cat:'WOMEN',title:'Female Weight Loss Plan',sub:'Vegetarian · Hormone-Safe Protocol',orig:399,price:249},
  {id:'pdf_06',icon:'⚗️',badge:'hormones',cat:'HORMONES',title:'Peptide Protocol Bible',sub:'Complete Scientific Reference Guide',orig:699,price:349},
  {id:'pdf_07',icon:'🔬',badge:'hormones',cat:'HORMONES',title:'SARMs Scientific Handbook',sub:'Complete Research-Backed Edition',orig:699,price:349},
  {id:'pdf_08',icon:'⚡',badge:'hormones',cat:'HORMONES',title:'TRT Hormone Guide',sub:'Optimization & Monitoring Protocols',orig:699,price:349},
  {id:'pdf_09',icon:'🏋️',badge:'training',cat:'TRAINING',title:'Science of Hypertrophy',sub:'Muscle Growth Mechanisms & Methods',orig:499,price:299},
  {id:'pdf_10',icon:'🎯',badge:'training',cat:'TRAINING',title:'Fat Loss Masterclass',sub:'Ultimate Evidence-Based Protocol',orig:499,price:299},
  {id:'pdf_11',icon:'💃',badge:'women',cat:'WOMEN',title:"Women's Transformation",sub:'Complete Body Recomposition Guide',orig:399,price:249},
  {id:'pdf_12',icon:'🍛',badge:'nutrition',cat:'NUTRITION',title:'Indian Nutrition Bible',sub:'Bodybuilder Edition · Desi Macros',orig:499,price:299},
  {id:'pdf_13',icon:'⚡',badge:'supplements',cat:'SUPPLEMENTS',title:'Pre-Workout Guide',sub:'Optimization & Stacking Protocols',orig:299,price:199},
  {id:'pdf_14',icon:'🧪',badge:'hormones',cat:'HORMONES',title:'Natural Testosterone',sub:'Optimization Without Compounds',orig:499,price:299},
  {id:'pdf_15',icon:'😴',badge:'recovery',cat:'RECOVERY',title:'Recovery & CNS Restore',sub:'Sleep, HRV & Nervous System Guide',orig:299,price:199},
];

function renderCatalog(){
  const grid=document.getElementById('pdf-catalog-grid');
  if(!grid)return;
  grid.innerHTML=PDF_CATALOG.map(p=>{
    const owned=isOwnedPDF(p.id);
    const url=PDF_PRODUCTS[p.id]?.getUrl();
    return `<div class="pcc" data-cat="${p.badge}">
      <div class="pcc-icon">${p.icon}</div>
      <div class="pcc-badge ${p.badge}">${p.cat}</div>
      <div class="pcc-title">${p.title}</div>
      <div class="pcc-sub">${p.sub}</div>
      <div class="pcc-price-row">
        <div class="pcc-price">₹${p.price}</div>
        <div class="pcc-orig">₹${p.orig}</div>
        <div class="pcc-off">${Math.round((1-p.price/p.orig)*100)}% OFF</div>
      </div>
      ${owned
        ? `<a class="pcc-dl" href="${url||'#'}" ${url?'download target="_blank"':''}>📥 DOWNLOAD PDF</a>`
        : `<button class="pcc-buy" onclick="buyCatalogPDF('${p.id}','${p.title}',${p.price*100})">📥 BUY — ₹${p.price}</button>`
      }
    </div>`;
  }).join('');
}

function isOwnedPDF(id){
  const p=PDF_PRODUCTS[id];
  if(!p)return false;
  try{const d=JSON.parse(localStorage.getItem(p.localKey)||'null');if(d&&d.purchased)return true;}catch(e){}
  return false;
}

function filterCatalog(cat,btn){
  document.querySelectorAll('.pcf').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.pcc').forEach(c=>{
    c.style.display=(cat==='all'||c.dataset.cat===cat)?'':'none';
  });
}

async function buyCatalogPDF(productId,title,amountPaise){
  if(!user){toast('Please log in first!','gold');forceLogin();return;}
  const prod=PDF_PRODUCTS[productId];
  if(!prod){toast('Product not found.','gold');return;}
  try{
    toast('Preparing secure checkout...','gold');
    await _loadRzp();
    let orderData={orderId:null,keyId:'rzp_live_SzivmCT3vTvTAK',amount:amountPaise,currency:'INR'};
    try{
      const r=await firebase.functions().httpsCallable('createPDFOrder')({itemId:productId});
      orderData={...orderData,...r.data};
    }catch(cfErr){console.warn('[buyCatalogPDF] createPDFOrder unavailable:',cfErr.message);}
    const rzp=new Razorpay({
      key:orderData.keyId,
      amount:orderData.amount,
      currency:orderData.currency,
      order_id:orderData.orderId||undefined,
      name:'Royal Fitness Club',
      description:title+' — PDF Guide',
      prefill:{name:user.name||'',email:user.email||'',contact:user.phone||''},
      theme:{color:prod.theme||'#7c3aed'},
      handler:async function(resp){
        localStorage.setItem(prod.localKey,JSON.stringify({purchased:true,date:new Date().toISOString(),pid:resp.razorpay_payment_id||''}));
        renderCatalog(); // refresh cards to show download buttons
        toast('📥 Payment successful! Your guide is ready to download.','gold');
        if(resp.razorpay_order_id&&resp.razorpay_payment_id&&resp.razorpay_signature){
          try{
            await firebase.functions().httpsCallable('recordPDFPurchase')({
              orderId:resp.razorpay_order_id,
              paymentId:resp.razorpay_payment_id,
              signature:resp.razorpay_signature,
              itemId:productId,
            });
          }catch(e){/* offline — localStorage owns it */}
        }
      },
    });
    rzp.open();
  }catch(err){
    console.error('[buyCatalogPDF]',err);
    toast('Payment setup failed. Please try again.','fire');
  }
}"""

html = html.replace(old_products, new_products)

# ── 6. CALL renderCatalog in initPDFStore ─────────────────────────────────
html = html.replace(
    'async function initPDFStore(){\n  renderFMReader(false);',
    'async function initPDFStore(){\n  renderFMReader(false);\n  renderCatalog();'
)

# ── 7. After Firestore check, refresh catalog cards too ───────────────────
html = html.replace(
    "localStorage.setItem(PDF_PRODUCTS[id].localKey,JSON.stringify({purchased:true}));\n          showPDFPurchased(id);",
    "localStorage.setItem(PDF_PRODUCTS[id].localKey,JSON.stringify({purchased:true}));\n          showPDFPurchased(id);\n          renderCatalog();"
)

print("Writing file...")
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done.")
