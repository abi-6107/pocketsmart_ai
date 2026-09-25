async function postJSON(url,data){
  const r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
  const j=await r.json(); if(!r.ok) throw new Error(j.detail||"Request failed"); return j;
}
function money(v){return "₹"+Number(v||0).toLocaleString("en-IN",{maximumFractionDigits:2});}
function renderResult(el,result){
  const d=result.data||{};
  let html=`<div class="result-card"><h3>${result.planner} Recommendations</h3>`;
  if(d.budget!==undefined) html+=`<div class="result-row"><b>Total Budget:</b> ${money(d.budget)} &nbsp; <b>Remaining:</b> ${money(d.remaining||0)}</div>`;
  if(d.allocation){html+=`<div class="result-grid">`;for(const [k,v] of Object.entries(d.allocation))html+=`<div class="result-row"><b>${k}</b><br>${money(v)}</div>`;html+=`</div>`;}
  const arr=d.items||d.options||[];
  for(const x of arr){html+=`<div class="result-row"><b>${x.category||x.name||"Option"}</b> — ${x.description||""} ${x.price!==undefined?`<strong>${money(x.price)}</strong>`:""} ${x.budget!==undefined?`<strong>${money(x.budget)}</strong>`:""} ${x.shopping_link?`<a class="btn small" target="_blank" href="${x.shopping_link}">View</a>`:""}</div>`}
  if(d.additional_suggestions||d.suggestions){html+=`<div class="result-row"><b>Additional Suggestions</b><ul>`;for(const s of (d.additional_suggestions||d.suggestions))html+=`<li>${s}</li>`;html+=`</ul></div>`}
  html+=`<small>Source: ${result.source}</small></div>`;el.innerHTML=html;
}
const homeForm=document.getElementById("homeForm");
if(homeForm)homeForm.addEventListener("submit",async e=>{e.preventDefault();const result=document.getElementById("homeResult");result.innerHTML="Generating...";try{const q={budget:Number(document.getElementById("homeBudget").value),room_types:[...document.getElementById("rooms").selectedOptions].map(x=>x.value),quantities:{lights:Number(document.getElementById("lights").value),fans:Number(document.getElementById("fans").value),furniture:Number(document.getElementById("furniture").value),dining:Number(document.getElementById("dining").value)},additional_information:document.getElementById("homeNotes").value};renderResult(result,await postJSON("/generate-home",q))}catch(x){result.innerHTML=`<div class="error">${x.message}</div>`}});
const partyForm=document.getElementById("partyForm");
if(partyForm)partyForm.addEventListener("submit",async e=>{e.preventDefault();const result=document.getElementById("partyResult");result.innerHTML="Generating...";try{const q={budget:Number(document.getElementById("partyBudget").value),guests:Number(document.getElementById("guests").value),event_type:document.getElementById("eventType").value,venue_type:document.getElementById("venueType").value,needs:[...document.querySelectorAll('input[name="need"]:checked')].map(x=>x.value),additional_information:document.getElementById("partyNotes").value};renderResult(result,await postJSON("/generate-party",q))}catch(x){result.innerHTML=`<div class="error">${x.message}</div>`}});
const jewelryForm=document.getElementById("jewelryForm");
if(jewelryForm)jewelryForm.addEventListener("submit",async e=>{e.preventDefault();const result=document.getElementById("jewelryResult");result.innerHTML="Generating...";try{const r=await fetch("/generate-jewelry",{method:"POST",body:new FormData(jewelryForm)});const j=await r.json();if(!r.ok)throw new Error(j.detail||"Request failed");renderResult(result,j)}catch(x){result.innerHTML=`<div class="error">${x.message}</div>`}});
const img=document.getElementById("outfitImage"), preview=document.getElementById("preview");
if(img)img.addEventListener("change",()=>{const f=img.files[0];if(!f)return;preview.src=URL.createObjectURL(f);preview.classList.remove("hidden")});
