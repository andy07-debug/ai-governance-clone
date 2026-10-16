// Click router for the static AI Governance replica.
// Each captured screen lives in <template id="v-<name>">. Clicks on known controls swap the screen;
// the header and AskMod chat panel stay mounted across screens (as in the live app), the mode dropdown
// and the conversation drawer are layered over whatever screen is open, and fullscreen is toggled in place.
(function () {
  var mount = document.getElementById('mount');
  mount.style.display = 'contents';
  var current = null;     // page view currently rendered
  var overlay = null;     // '07a-…' / '07b-…' when a shell overlay is open
  var fullscreen = false;
  var fsUndo = null;

  var norm = function (s) { return (s || '').replace(/\s+/g, ' ').trim(); };
  var tplOf = function (name) { return document.getElementById('v-' + name); };
  var OVERLAYS = ['07a-shell-mode-dropdown', '07b-shell-hamburger'];
  var isOverlay = function (n) { return OVERLAYS.indexOf(n) >= 0; };
  // The New Policy modal is a separate template here, but in the live app it never changes the URL.
  var MODAL = '04c-policies-newpolicy-modal';
  var urlOf = function (n) { return n === MODAL ? '04-policies' : n; };

  function setHash(name, push) {
    if (location.hash === '#' + name) return;
    if (push) window.history.pushState(null, '', '#' + name);
    else window.history.replaceState(null, '', '#' + name);
  }

  // ---------- pages ----------
  function show(name, push) {
    var tpl = tplOf(name);
    if (!tpl) return;
    if (isOverlay(name)) { openOverlay(name, push); return; }
    closeOverlay(true);
    var wasFs = fullscreen;
    if (wasFs) exitFullscreen();
    var frag = tpl.content.cloneNode(true);
    // Keep the live header (when it reads the same) and the live chat panel, so drafts and state survive.
    var liveHeader = mount.querySelector('.h-20'), newHeader = frag.querySelector('.h-20');
    if (liveHeader && newHeader && norm(liveHeader.textContent) === norm(newHeader.textContent)) newHeader.replaceWith(liveHeader);
    var liveSide = document.getElementById('sidebar'), newSide = frag.querySelector('#sidebar');
    if (liveSide && newSide) {
      ['class', 'style', 'data-panel-size'].forEach(function (a) { liveSide.setAttribute(a, newSide.getAttribute(a)); });
      newSide.replaceWith(liveSide);
    }
    if (window.destroyCharts) window.destroyCharts();
    mount.replaceChildren(frag);
    current = name;
    if (window.initCharts) window.initCharts(mount);
    if (wasFs) enterFullscreen();
    setHash(urlOf(name), push !== false);
  }
  window.__show = show;
  window.__cloneState = function () { return overlay || current; };

  // ---------- shell overlays (layered, never re-render the page underneath) ----------
  function openOverlay(name, push) {
    closeOverlay(true);
    if (!current) show('00-home', false);
    var frag = tplOf(name).content;
    var node = frag.querySelector(name === '07a-shell-mode-dropdown' ? '.p-dropdown-panel' : '.p-sidebar-mask');
    if (!node) return;
    node = node.cloneNode(true);
    node.setAttribute('data-overlay', '');
    mount.appendChild(node);
    if (name === '07a-shell-mode-dropdown') {
      var dd = mount.querySelector('.h-20 .p-dropdown'), src = frag.querySelector('.h-20 .p-dropdown');
      var label = norm(((dd && dd.querySelector('.p-dropdown-label')) || {}).textContent);
      node.querySelectorAll('li.p-dropdown-item').forEach(function (li) {
        var on = norm(li.getAttribute('aria-label')) === label;
        li.classList.toggle('p-highlight', on); li.classList.toggle('p-focus', on);
        ['aria-selected', 'data-p-highlight', 'data-p-focused'].forEach(function (a) { li.setAttribute(a, String(on)); });
      });
      if (dd && src) {
        dd.setAttribute('data-overlay-restore', dd.className);
        dd.className = src.className;
        var trig = dd.querySelector('.p-dropdown-trigger'), srcTrig = src.querySelector('.p-dropdown-trigger');
        if (trig && srcTrig) { trig.setAttribute('data-overlay-restore', trig.innerHTML); trig.innerHTML = srcTrig.innerHTML; trig.setAttribute('aria-expanded', 'true'); }
      }
      var search = node.querySelector('input');
      if (search) setTimeout(function () { search.focus(); }, 0);
    }
    overlay = name;
  }
  function closeOverlay(silent) {
    if (!overlay) return false;
    mount.querySelectorAll('[data-overlay]').forEach(function (n) { n.remove(); });
    var dd = mount.querySelector('.h-20 .p-dropdown[data-overlay-restore]');
    if (dd) { dd.className = dd.getAttribute('data-overlay-restore'); dd.removeAttribute('data-overlay-restore'); }
    var trig = mount.querySelector('.p-dropdown-trigger[data-overlay-restore]');
    if (trig) { trig.innerHTML = trig.getAttribute('data-overlay-restore'); trig.removeAttribute('data-overlay-restore'); trig.setAttribute('aria-expanded', 'false'); }
    overlay = null;
    return true;
  }

  // ---------- fullscreen (from the live DOM diff), applied and reverted in place ----------
  function enterFullscreen() {
    var panels = document.querySelectorAll('[data-panel]');
    var right = panels[panels.length - 1];
    if (!right) return;
    var undo = [];
    var setAttr = function (el, a, val) {
      var old = el.getAttribute(a);
      undo.push(function () { old === null ? el.removeAttribute(a) : el.setAttribute(a, old); });
      el.setAttribute(a, val);
    };
    var side = document.getElementById('sidebar');
    if (side) {
      setAttr(side, 'style', 'flex: 0 1 0px; overflow: hidden;');
      setAttr(side, 'class', side.className.replace('w-[45%] w-[45%]', 'w-0 w-[45%]'));
      setAttr(side, 'data-panel-size', '0.0');
    }
    setAttr(right, 'style', 'flex: 100 1 0px; overflow: hidden;');
    setAttr(right, 'data-panel-size', '100.0');
    var handle = document.querySelector('[data-resize-handle]');
    if (handle) {
      var hp = handle.parentNode, hn = handle.nextSibling;
      handle.remove();
      undo.push(function () { hp.insertBefore(handle, hn); });
    }
    var box = [].filter.call(right.querySelectorAll('div'), function (d) {
      return d.className === 'w-full h-full ' && d.firstElementChild && d.firstElementChild.className === 'w-full h-full overflow-auto';
    })[0];
    if (box) {
      setAttr(box, 'class', 'w-full h-full fixed inset-0 z-20 bg-white');
      var inner = box.querySelector('.relative.h-full.overflow-auto');
      if (inner) setAttr(inner, 'class', 'relative h-screen');
      // charts are live Chart.js canvases (charts.js) and resize themselves, like the live app
    }
    var btn = document.querySelector('[title="Toggle Fullscreen"]');
    var svg = btn && btn.querySelector('svg');
    if (svg) {
      var min = document.getElementById('fs-minimize').content.firstElementChild.cloneNode(true);
      svg.replaceWith(min);
      undo.push(function () { min.replaceWith(svg); });
    }
    var group = document.querySelector('[data-panel-group]');
    if (group) {
      var bubble = document.getElementById('fs-bubble').content.firstElementChild.cloneNode(true);
      group.parentElement.insertBefore(bubble, group);
      undo.push(function () { bubble.remove(); });
    }
    fsUndo = undo;
    fullscreen = true;
  }
  function exitFullscreen() {
    if (fsUndo) fsUndo.reverse().forEach(function (f) { f(); });
    fsUndo = null;
    fullscreen = false;
  }

  // ---------- navigation tables ----------
  var SECTIONS = {
    'LLM Studio Analytics': '01-llm-analytics',
    'Firewall Overview': '02-firewall',
    'Live Events': '03-live-events',
    'Policies': '04-policies',
    'Traffic Analysis': '05-traffic'
  };
  var TRAFFIC_HUB = {
    'Projects': '05a-traffic-projects',
    'Statistics': '05d-traffic-statistics',
    'Applications': '05e-traffic-applications',
    'Error logs': '05f-traffic-errorlogs'
  };
  var RBAC_TABS = {
    'Access Management': '06-rbac-access',
    'RBAC Configuration': '06b-rbac-usergroups',
    'User Groups': '06b-rbac-usergroups',
    'Configuration': '06c-rbac-config-modules',
    'Modules': '06c-rbac-config-modules',
    'Permissions': '06d-rbac-config-permissions',
    'Roles': '06e-rbac-config-roles',
    'Mapping': '06f-rbac-config-mapping'
  };

  function route(t) {
    var v = current;
    var inHeader = t.closest('.h-20');
    var panel = t.closest('[data-panel]');
    var panels = [].slice.call(document.querySelectorAll('[data-panel]'));
    var inRight = panel && panels.indexOf(panel) === panels.length - 1;
    var hit = t.closest('button, a, li, [role="button"], .cursor-pointer, .p-dropdown');
    var isBtn = hit && hit.tagName === 'BUTTON';
    var text = norm(hit ? hit.textContent : t.textContent);

    // ----- shell overlays: handled first, like PrimeReact's outside-click listeners -----
    if (overlay === '07a-shell-mode-dropdown') {
      if (t.closest('.p-dropdown-panel')) {
        var item = t.closest('li');
        if (item && /^AI Governance/.test(norm(item.textContent))) { closeOverlay(); if (current !== '00-home') show('00-home'); return true; }
        return true; // search box, list scrolling, other modes: stay put
      }
      closeOverlay();
      if (inHeader && t.closest('.p-dropdown')) return true; // trigger toggles closed
      // otherwise fall through: the outside click also reaches its target
    } else if (overlay === '07b-shell-hamburger') {
      if (t.closest('[title="Click to close sidebar"]') || !t.closest('.p-sidebar')) { closeOverlay(); return true; }
      return true;
    }

    // ----- fullscreen controls -----
    if (t.closest('[title="Toggle Fullscreen"]')) { fullscreen ? exitFullscreen() : enterFullscreen(); return true; }
    if (t.closest('.maximizeChatButton')) { exitFullscreen(); return true; }
    var closeMsgs = t.closest('[aria-label="Close messages"]');
    if (closeMsgs) { [].slice.call(closeMsgs.parentElement.children).forEach(function (c) { c.remove(); }); return true; }

    // ----- global shell -----
    if (inHeader && t.closest('.p-dropdown')) { show('07a-shell-mode-dropdown'); return true; }
    if (inHeader && t.closest('[title="Open sidebar"]')) { show('07b-shell-hamburger'); return true; }
    if (inHeader && isBtn) return true; // cost-pill refresh etc.: inert in a static copy
    if (t.closest('[data-testid="headerProjectsButton"]')) { show('07c-shell-projects'); return true; }

    if (!inRight) return false;

    // Outer AI Governance breadcrumb home -> landing grid.
    if (t.closest('span.p-1.text-indigo-600, button[title="Back to home"]')) { if (v !== '00-home') show('00-home'); return true; }

    // ----- landing grid -----
    if (v === '00-home') {
      var h3 = hit && hit.querySelector('h3');
      if (h3 && SECTIONS[norm(h3.textContent)]) { show(SECTIONS[norm(h3.textContent)]); return true; }
      if (isBtn && text === 'RBAC') { show('06-rbac-access'); return true; }
      return false;
    }

    // ----- policies -----
    if (/^04/.test(v)) {
      if (v === '04c-policies-newpolicy-modal') {
        var modalCard = t.closest('.animate-slideUp');
        if (!modalCard || (isBtn && text === 'Cancel') || (isBtn && !text && hit.closest('.border-b'))) { show('04-policies', false); return true; }
        if (isBtn && text === 'Deploy Policy') return true; // static copy: no submit
        return false;
      }
      if (isBtn && /Change Logs/.test(text)) { if (v !== '04b-policies-changelogs') show('04b-policies-changelogs'); return true; }
      if (isBtn && /Policies Deck/.test(text)) { if (v !== '04-policies') show('04-policies'); return true; }
      if (isBtn && /New Policy/.test(text)) { show('04c-policies-newpolicy-modal', false); return true; }
      return false;
    }

    // ----- traffic analysis / smart LLM load balancer -----
    if (/^05/.test(v)) {
      if (t.closest('main .p-breadcrumb-home')) { show('05-traffic'); return true; }
      if (t.closest('main .p-breadcrumb') && text === 'Projects') { if (v !== '05a-traffic-projects') show('05a-traffic-projects'); return true; }
      if (t.closest('main .p-breadcrumb')) return true;
      if (v === '05-traffic' && TRAFFIC_HUB[text]) { show(TRAFFIC_HUB[text]); return true; }
      if (v === '05a-traffic-projects' && isBtn) {
        if (text === 'View Usage') { show('05b-traffic-project-usage'); return true; }
        if (text === 'Model Configuration') { show('05c-traffic-model-config'); return true; }
      }
      if (v === '05c-traffic-model-config') {
        var head = t.closest('a.p-accordion-header-link');
        if (head && !t.closest('button')) { toggleAccordion(head); return true; }
      }
      return false;
    }

    // ----- RBAC -----
    if (/^06/.test(v)) {
      if (hit && RBAC_TABS[text]) {
        var already = RBAC_TABS[text] === v ||
          (text === 'RBAC Configuration' && /^06[b-f]/.test(v)) ||
          (text === 'Configuration' && /^06[c-f]/.test(v));
        if (!already) show(RBAC_TABS[text]);
        return true;
      }
      return false;
    }
    return false;
  }

  // PrimeReact accordion: only the tab that was open at capture time has its content in the DOM
  // (collapsed panels are unmounted), so that one tab can collapse/expand; the others stay closed.
  function toggleAccordion(head) {
    var content = document.getElementById(head.getAttribute('aria-controls'));
    if (!content) return;
    var open = head.getAttribute('aria-expanded') !== 'true';
    head.setAttribute('aria-expanded', String(open));
    var hdr = head.closest('.p-accordion-header'), tab = head.closest('.p-accordion-tab');
    if (hdr) { hdr.classList.toggle('p-highlight', open); hdr.setAttribute('data-p-highlight', String(open)); }
    if (tab) tab.classList.toggle('p-accordion-tab-active', open);
    var wrap = content.closest('.p-toggleable-content') || content;
    wrap.style.display = open ? '' : 'none';
    var icon = head.querySelector('svg');
    if (icon) icon.style.transform = open ? '' : 'rotate(0deg)';
  }

  // Collapsible dashboard sections (button[aria-expanded] in a <section>): hide the section body.
  function toggleSection(btn) {
    var section = btn.closest('section');
    if (!section) return false;
    var open = btn.getAttribute('aria-expanded') !== 'true';
    btn.setAttribute('aria-expanded', String(open));
    // the child of <section> holding the toggle is the header; every other child is the body
    var keep = [].filter.call(section.children, function (c) { return c.contains(btn); })[0];
    [].forEach.call(section.children, function (c) { if (c !== keep) c.style.display = open ? '' : 'none'; });
    var svg = btn.querySelector('svg.lucide-chevron-up, svg.lucide-chevron-down') || btn.querySelector('svg:last-of-type');
    if (svg) svg.style.transform = open ? '' : 'rotate(180deg)';
    return true;
  }

  // Generic segmented control: clicking a pill moves the "selected" style tokens onto it.
  // Works on tokens (not whole class strings) so pills with extra layout classes still toggle.
  var ACTIVE_MARK = /^(bg-\[#5928ED\]|bg-\[#835EF2\]|bg-indigo-600|bg-violet-600|bg-gray-200|bg-white|shadow|shadow-sm|text-white|text-indigo-700|text-\[#5928ED\])$/;
  function toggleGroup(t) {
    var btn = t.closest('button');
    if (!btn || !btn.parentElement || btn.closest('[data-overlay]')) return;
    var sibs = [].filter.call(btn.parentElement.children, function (e) { return e.tagName === 'BUTTON'; });
    if (sibs.length < 2 || sibs.length > 12) return;
    var toks = sibs.map(function (s) { return s.className.split(/\s+/).filter(Boolean); });
    var common = toks[0].filter(function (k) { return toks.every(function (ts) { return ts.indexOf(k) >= 0; }); });
    var diffs = toks.map(function (ts) { return ts.filter(function (k) { return common.indexOf(k) < 0; }); });
    var key = function (d) { return d.slice().sort().join(' '); };
    var counts = {};
    diffs.forEach(function (d) { counts[key(d)] = (counts[key(d)] || 0) + 1; });
    // active = the one sibling whose diff is unique AND carries a selected-looking token
    var cand = sibs.map(function (s, i) { return i; }).filter(function (i) {
      return (sibs.length === 2 || counts[key(diffs[i])] === 1) && diffs[i].some(function (k) { return ACTIVE_MARK.test(k); });
    });
    if (sibs.length > 2 && cand.length > 1) {
      cand = cand.filter(function (i) { return counts[key(diffs[i])] === 1 && diffs.filter(function (d, j) { return j !== i && key(d) === key(diffs[i]); }).length === 0; });
    }
    if (cand.length !== 1) return;
    var ai = cand[0], bi = sibs.indexOf(btn);
    if (ai === bi) return;
    // idle diff = the most common diff among the other siblings
    var idleKey = Object.keys(counts).filter(function (k) { return k !== key(diffs[ai]); })
      .sort(function (a, b) { return counts[b] - counts[a]; })[0];
    if (idleKey === undefined) return;
    var idle = idleKey ? idleKey.split(' ') : [];
    var act = diffs[ai];
    var activeOnly = act.filter(function (k) { return idle.indexOf(k) < 0; });
    var idleOnly = idle.filter(function (k) { return act.indexOf(k) < 0; });
    var LAYOUT = /^(-?[mp][trblxy]?-|flex$|inline-flex$|block$|inline-block$|items-|justify-|gap-|w-|h-|min-|max-)/;
    activeOnly = activeOnly.filter(function (k) { return !LAYOUT.test(k); });
    idleOnly = idleOnly.filter(function (k) { return !LAYOUT.test(k); });
    var swap = function (el, rm, add) {
      rm.forEach(function (k) { el.classList.remove(k); });
      add.forEach(function (k) { el.classList.add(k); });
    };
    swap(sibs[ai], activeOnly, idleOnly);
    swap(btn, idleOnly, activeOnly);
    ['aria-pressed', 'aria-selected', 'data-active'].forEach(function (a) {
      if (sibs[ai].hasAttribute(a)) { btn.setAttribute(a, sibs[ai].getAttribute(a)); sibs[ai].setAttribute(a, String(!(sibs[ai].getAttribute(a) === 'true'))); }
    });
  }

  // "more" / "less" on clamped log lines.
  function toggleMore(btn) {
    if (!/^(more|less)$/i.test(norm(btn.textContent))) return false;
    var box = btn.parentElement, c = null;
    for (var i = 0; i < 4 && box && !c; i++) { c = box.querySelector('.line-clamp-2, [data-unclamped]'); box = box.parentElement; }
    if (!c) return false;
    var clamped = c.classList.toggle('line-clamp-2');
    c.toggleAttribute('data-unclamped', !clamped);
    btn.textContent = clamped ? 'more' : 'less';
    return true;
  }

  document.addEventListener('click', function (e) {
    var t = e.target;
    var a = t.closest('a[href^="#"], a[href=""]');
    if (a) { var h = a.getAttribute('href').slice(1); if (!h || !tplOf(h)) e.preventDefault(); }
    if (t.closest('form') && t.closest('button')) e.preventDefault();
    if (route(t)) { e.preventDefault(); e.stopPropagation(); return; }
    var b = t.closest('button');
    if (b && b.hasAttribute('aria-expanded') && b.closest('section') && toggleSection(b)) return;
    if (b && toggleMore(b)) return;
    toggleGroup(t);
  }, true);
  document.addEventListener('submit', function (e) { e.preventDefault(); }, true);
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (overlay) closeOverlay();
    else if (current === '04c-policies-newpolicy-modal') show('04-policies', false);
  });

  // Mode dropdown search filters the list (by mode name).
  document.addEventListener('input', function (e) {
    if (!e.target.closest('.p-dropdown-panel')) return;
    var q = e.target.value.toLowerCase().trim();
    var panel = e.target.closest('.p-dropdown-panel');
    var any = false;
    panel.querySelectorAll('li.p-dropdown-item').forEach(function (li) {
      var name = li.querySelector('.p-dropdown-item-label, span, div');
      var label = norm((name || li).textContent).toLowerCase();
      var match = !q || label.indexOf(q) >= 0;
      li.style.display = match ? '' : 'none';
      any = any || match;
    });
    var ul = panel.querySelector('ul.p-dropdown-items'), em = ul && ul.querySelector('li.p-dropdown-empty-message');
    if (ul && !any && !em) {
      em = document.createElement('li');
      em.className = 'p-dropdown-empty-message';
      em.setAttribute('role', 'option');
      em.textContent = 'No results found';
      ul.appendChild(em);
    } else if (any && em) em.remove();
  });

  // PrimeReact checkbox ("Show Sub Projects").
  var CHECK_SVG = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg" class="p-icon p-checkbox-icon" data-pc-section="icon"><path d="M4.86199 11.5948C4.78717 11.5923 4.71366 11.5745 4.64596 11.5426C4.57826 11.5107 4.51779 11.4652 4.46827 11.4091L0.753985 7.69483C0.683167 7.64891 0.623706 7.58751 0.580092 7.51525C0.536478 7.44299 0.509851 7.36177 0.502221 7.27771C0.49459 7.19366 0.506156 7.10897 0.536046 7.03004C0.565935 6.95111 0.613367 6.88 0.674759 6.82208C0.736151 6.76416 0.8099 6.72095 0.890436 6.69571C0.970973 6.67046 1.05619 6.66385 1.13966 6.67635C1.22313 6.68886 1.30266 6.72017 1.37226 6.76792C1.44186 6.81567 1.4997 6.8786 1.54141 6.95197L4.86199 10.2503L12.6397 2.49483C12.7444 2.42694 12.8689 2.39617 12.9932 2.40745C13.1174 2.41873 13.2343 2.47141 13.3251 2.55705C13.4159 2.64268 13.4753 2.75632 13.4938 2.87973C13.5123 3.00315 13.4888 3.1292 13.4271 3.23768L5.2557 11.4091C5.20618 11.4652 5.14571 11.5107 5.07801 11.5426C5.01031 11.5745 4.9368 11.5923 4.86199 11.5948Z" fill="currentColor"></path></svg>';
  document.addEventListener('change', function (e) {
    var cb = e.target.closest('.p-checkbox');
    if (!cb) return;
    var on = e.target.checked;
    cb.classList.toggle('p-highlight', on);
    cb.setAttribute('data-p-highlight', String(on));
    var box = cb.querySelector('.p-checkbox-box');
    if (box) { box.setAttribute('data-p-highlight', String(on)); box.innerHTML = on ? CHECK_SVG : ''; }
  });

  // Browser Back/Forward between screens.
  window.addEventListener('hashchange', function () {
    var h = location.hash.slice(1);
    if (!h) { show('00-home', false); return; }
    if (!tplOf(h)) { setHash(urlOf(current), false); return; }
    if (h === MODAL) { setHash('04-policies', false); if (overlay) closeOverlay(); if (current !== MODAL) show(MODAL, false); return; }
    if (isOverlay(h)) { setHash(urlOf(current), false); if (overlay !== h) openOverlay(h); return; }
    if (overlay) closeOverlay();
    if (h !== current) show(h, false);
  });

  var start = (location.hash || '').slice(1);
  if (isOverlay(start)) { show('00-home', false); openOverlay(start); }  // deep link: open over home
  else show(tplOf(start) ? start : '00-home', false);
})();
