
/**
 * GTI Capability Taxonomy Drilldown
 * - Collapsible Level-1 sections with caret
 * - Platform counters (Level-1 and Level-2): selected/total
 * - Works with taxonomy_dedup.json or taxonomy.json and config.json
 */
(async function () {
    const taxonomyEl = document.getElementById('taxonomy');
    const detailsEl  = document.getElementById('details');
    const platformSel= document.getElementById('platformSelect');
    const reloadBtn  = document.getElementById('reloadBtn');
    const statusEl   = document.getElementById('status');
  
    let TAXONOMY = null;
    let CONFIG   = null;
    let idToPlatforms = {}; // ID -> [platform names]
  
    reloadBtn.addEventListener('click', () => initialize(true));
    platformSel.addEventListener('change', () => render());
  
    async function fetchJSON(path){
      try{
        const res = await fetch(path, {cache:'no-cache'});
        if(!res.ok) throw new Error(`HTTP ${res.status} for ${path}`);
        return await res.json();
      }catch(err){
        console.warn(`Fetch failed for ${path}:`, err);
        return null;
      }
    }
  
    function setStatus(msg){ statusEl.textContent = msg; }
  
    function normalizeID(id){ return (id || '').replace(/\\_/g,'_').replace(/\\\\_/g,'_').trim(); }
  
    function buildIdToPlatforms(){
      idToPlatforms = {};
      (CONFIG?.platforms || []).forEach(p => {
        (p.capabilities || []).forEach(raw => {
          const id = normalizeID(raw);
          if(!idToPlatforms[id]) idToPlatforms[id] = new Set();
          idToPlatforms[id].add(p.name);
        });
      });
      // convert to arrays for UI
      Object.keys(idToPlatforms).forEach(id => idToPlatforms[id] = Array.from(idToPlatforms[id]));
    }
  
    function populatePlatformFilter(){
      platformSel.innerHTML = '<option value="">— All Platforms —</option>';
      (CONFIG?.platforms || []).forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.name;
        opt.textContent = p.name;
        platformSel.appendChild(opt);
      });
    }
  
    function clearSelected(){ document.querySelectorAll('.selected').forEach(e=>e.classList.remove('selected')); }
  
    function showDetails(node){
      clearSelected();
      const match = Array.from(document.getElementsByClassName('level-2'))
        .find(e => e.dataset.id === node.ID);
      if(match) match.classList.add('selected');
  
      const mapped = idToPlatforms[node.ID] || [];
      detailsEl.classList.remove('empty');
      detailsEl.innerHTML = `
        <h3 style="margin-top:0">${node.Level2} <small>(${node.ID})</small></h3>
        <p>${node.Description || 'No description available.'}</p>
        <div class="badges"><strong>Platforms mapped:</strong><br/>
          ${mapped.length ? mapped.map(n => `<span class="platform-badge">${n}</span>`).join('') : '<em>None</em>'}
        </div>
      `;
    }
  
    /** Counter helpers */
    function level2Counts(id, selectedPlatform){
      const list = idToPlatforms[id] || [];
      const total = list.length;
      const selected = selectedPlatform ? (list.includes(selectedPlatform) ? 1 : 0) : null;
      return {total, selected};
    }
  
    function level1Counts(level1, selectedPlatform){
      const set = new Set();
      (level1.Level2s || []).forEach(l2 => {
        const id = normalizeID(l2.ID);
        (idToPlatforms[id] || []).forEach(p => set.add(p));
      });
      const total = set.size;
      let selected = null;
      if(selectedPlatform){
        selected = set.has(selectedPlatform) ? 1 : 0;
      }
      return {total, selected};
    }
  
    /** Render taxonomy with collapsible Level-1 and counters */
    function render(){
      taxonomyEl.innerHTML = '';
      detailsEl.innerHTML = 'Select a capability to see its description and mapped platforms.';
      detailsEl.classList.add('empty');
  
      if(!TAXONOMY || TAXONOMY.length === 0){
        taxonomyEl.innerHTML = `<div class="empty">No taxonomy data found. Check <code>taxonomy.json</code>.</div>`;
        return;
      }
  
      const selectedPlatform = platformSel.value || '';
  
      
TAXONOMY.forEach(L0 => {
    const l0 = document.createElement('div');
    l0.className = 'capability level-0';
    l0.textContent = L0.Level0 || L0.RefCode || 'Level 0';
    taxonomyEl.appendChild(l0);
  
    (L0.Level1s || []).forEach(L1 => {
      // Level-1 block wrapper
      const block = document.createElement('div');
      block.className = 'l1-block';
      taxonomyEl.appendChild(block);
  
      // Header with caret & counter
      const header = document.createElement('div');
      header.className = 'l1-header capability level-1';
      const caret = document.createElement('span');
      caret.className = 'caret'; // <-- no 'open' class initially
      header.appendChild(caret);
  
      const title = document.createElement('span');
      title.textContent = L1.Level1 || L1.Ref || 'Level 1';
      header.appendChild(title);
  
      const c1 = level1Counts(L1, selectedPlatform);
      const badge = document.createElement('span');
      badge.className = 'count-badge';
      badge.innerHTML = c1.selected === null
        ? `<span class="strong">${c1.total}</span> <span class="sep">platforms</span>`
        : `<span class="strong">${c1.selected}</span>/<span>${c1.total}</span> <span class="sep">platforms</span>`;
      header.appendChild(badge);
  
      block.appendChild(header);
  
      // L2 list
      const list = document.createElement('div');
      list.className = 'l2-list collapsed'; // <-- collapsed by default
      block.appendChild(list);
  
      // Toggle collapse
      header.addEventListener('click', () => {
        const isOpen = caret.classList.contains('open');
        if(isOpen){
          caret.classList.remove('open');
          list.classList.add('collapsed');
        }else{
          caret.classList.add('open');
          list.classList.remove('collapsed');
        }
      });
  
      // Populate Level-2 rows (respect platform filter)
      (L1.Level2s || []).forEach(L2 => {
        const id = normalizeID(L2.ID);
        const counts = level2Counts(id, selectedPlatform);
  
        if(selectedPlatform && counts.selected === 0) return;
  
        const l2 = document.createElement('div');
        l2.className = 'capability level-2';
        l2.dataset.id = id;
        l2.title = L2.Description || '';
        l2.innerHTML = `
          <span>${L2.Level2} <small>(${id})</small></span>
          <span class="count-badge">
            ${counts.selected === null
              ? `<span class="strong">${counts.total}</span> <span class="sep">platforms</span>`
              : `<span class="strong">${counts.selected}</span>/<span>${counts.total}</span> <span class="sep">platforms</span>`
            }
          </span>
        `;
        l2.addEventListener('click', () => showDetails({ Level2: L2.Level2, ID: id, Description: L2.Description }));
        list.appendChild(l2);
      });
    });
  });
  
    }
  
    async function initialize(forceReload=false){
      setStatus('Loading taxonomy & config…');
  
      // Prefer the deduplicated taxonomy if present; fall back to taxonomy.json
      const tryPaths = forceReload
        ? ['taxonomy_dedup.json','taxonomy.json']
        : (TAXONOMY ? [] : ['taxonomy_dedup.json','taxonomy.json']);
  
      TAXONOMY = TAXONOMY || await (async () => {
        for(const p of tryPaths){
          const data = await fetchJSON(p);
          if(data) return data;
        }
        return null;
      })();
  
      CONFIG   = (!forceReload && CONFIG) || await fetchJSON('config.json');
  
      if(!TAXONOMY){
        statusEl.textContent = 'taxonomy.json not found.';
        taxonomyEl.innerHTML = `<div class="empty">No taxonomy data found. Ensure <code>taxonomy_dedup.json</code> or <code>taxonomy.json</code> is in this folder.</div>`;
        return;
      }
      if(!CONFIG){
        statusEl.textContent = 'config.json not found.';
        taxonomyEl.insertAdjacentHTML('beforeend', `<div class="empty">No platform mapping (<code>config.json</code>) found. Counters will show 0.</div>`);
        CONFIG = { platforms: [] };
      }
  
      buildIdToPlatforms();
      populatePlatformFilter();
      render();
      setStatus('Ready.');
    }
  
    // Kick off
    initialize(false);
  })();
  