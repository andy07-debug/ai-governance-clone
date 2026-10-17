// v2 router for the AI Governance demo replica.
// Screens are <template id="s-<id>" data-title="…"> fragments rendered into #screen; overlays are
// <template id="o-<id>"> fragments rendered into #overlay-root. Fragments wire themselves up with:
//   data-go="<screen-id>"        navigate (pushes browser history; URL #<screen-id>)
//   data-open="<overlay-id>"     open an overlay (drawer / modal / popover) on top of the current screen
//   data-close                   close the topmost overlay (also: Escape, click on [data-backdrop])
//   data-tab="<group>:<panel>"   in-place tab switch: shows [data-panel="<group>:<panel>"], hides siblings in the group,
//                                and moves the classes in data-active-class / data-idle-class between tab buttons
//   data-toggle                  toggle aria-checked / aria-pressed (switches, checkboxes) and swap data-on-class/data-off-class
//   <canvas data-chart='{Chart.js config JSON}'>  live chart; tick formats via "_yFormat"/"_xFormat": usd|usd0|usd2|k|pct|int
// Deep links: #<screen-id> or #<screen-id>+<overlay-id>.
(function () {
  var screenEl = document.getElementById('screen');
  var overlayRoot = document.getElementById('overlay-root');
  var crumb = document.getElementById('crumb-title');
  var crumbBar = crumb && crumb.closest('.w-full.flex.items-center.justify-between');
  var modeLabel = document.querySelector('.h-20 .p-dropdown-label .ml-2');
  var current = null, overlays = [], charts = [], fullscreen = false, fsUndo = null;
  var tpl = function (p, id) { return document.getElementById(p + '-' + id); };

  // ---------- charts ----------
  var FMT = {
    usd: function (v) { return '$' + Number(v).toLocaleString('en-US'); },
    usd0: function (v) { return '$' + Math.round(Number(v)).toLocaleString('en-US'); },
    usd2: function (v) { return '$' + Number(v).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); },
    k: function (v) { v = Number(v); return Math.abs(v) >= 1000 ? (v / 1000).toFixed(v % 1000 ? 1 : 0) + 'K' : String(v); },
    pct: function (v) { return v + '%'; },
    int: function (v) { return Math.round(Number(v)).toLocaleString('en-US'); }
  };
  function initCharts(root) {
    if (!window.Chart) return;
    root.querySelectorAll('canvas[data-chart]').forEach(function (cv) {
      if (cv.__chart) return;
      var cfg;
      try { cfg = JSON.parse(cv.getAttribute('data-chart')); } catch (e) { console.error('bad chart JSON', cv, e); return; }
      var o = cfg.options = cfg.options || {};
      o.responsive = o.responsive !== false; o.maintainAspectRatio = !!o.maintainAspectRatio;
      o.scales = o.scales || {};
      ['x', 'y'].forEach(function (ax) {
        var f = cfg['_' + ax + 'Format'];
        if (f && FMT[f]) { o.scales[ax] = o.scales[ax] || {}; o.scales[ax].ticks = o.scales[ax].ticks || {}; o.scales[ax].ticks.callback = function (v) { return FMT[f](this.getLabelForValue ? (ax === 'x' && this.type === 'category' ? this.getLabelForValue(v) : v) : v); }; }
      });
      if (cfg._tooltipFormat && FMT[cfg._tooltipFormat]) {
        o.plugins = o.plugins || {}; o.plugins.tooltip = o.plugins.tooltip || {};
        o.plugins.tooltip.callbacks = { label: function (c) { return (c.dataset.label ? c.dataset.label + ': ' : '') + FMT[cfg._tooltipFormat](c.raw); } };
      }
      cv.__chart = new window.Chart(cv, cfg);
      charts.push(cv.__chart);
    });
  }
  function destroyCharts(root) {
    charts = charts.filter(function (c) {
      if (!root || root.contains(c.canvas)) { c.destroy(); return false; }
      return true;
    });
  }

  // ---------- screens ----------
  function setHash(h, push) {
    if (location.hash === '#' + h) return;
    if (push) history.pushState(null, '', '#' + h); else history.replaceState(null, '', '#' + h);
  }
  function show(id, push) {
    var t = tpl('s', id);
    if (!t) { console.warn('no screen', id); return; }
    closeAll();
    destroyCharts(screenEl);
    screenEl.replaceChildren(t.content.cloneNode(true));
    screenEl.scrollTop = 0;
    current = id;
    if (crumb) crumb.textContent = t.getAttribute('data-title') || crumb.textContent;
    // full-panel screens (Projects) cover the whole right panel and, as in the live app, the mode dropdown reads "Select Mode"
    var full = t.hasAttribute('data-fullpanel');
    if (crumbBar) crumbBar.style.display = full ? 'none' : '';
    screenEl.classList.toggle('h-full', full);
    if (modeLabel) modeLabel.textContent = full ? 'Select Mode' : 'AI Governance';
    initCharts(screenEl);
    setHash(id, push !== false);
  }

  // ---------- overlays ----------
  function open(id) {
    var t = tpl('o', id);
    if (!t) { console.warn('no overlay', id); return; }
    var wrap = document.createElement('div');
    wrap.setAttribute('data-overlay', id);
    wrap.appendChild(t.content.cloneNode(true));
    overlayRoot.appendChild(wrap);
    overlays.push(wrap);
    initCharts(wrap);
  }
  function closeTop() {
    var w = overlays.pop();
    if (w) { destroyCharts(w); w.remove(); }
  }
  function closeAll() { while (overlays.length) closeTop(); }

  // ---------- fullscreen (right panel takes the whole viewport, as in the live app) ----------
  function enterFullscreen() {
    var panels = document.querySelectorAll('[data-panel]'), right = panels[panels.length - 1], side = document.getElementById('sidebar');
    var undo = [], set = function (el, a, v) { var old = el.getAttribute(a); undo.push(function () { old === null ? el.removeAttribute(a) : el.setAttribute(a, old); }); el.setAttribute(a, v); };
    if (side) set(side, 'style', 'flex: 0 1 0px; overflow: hidden;');
    if (right) set(right, 'style', 'flex: 100 1 0px; overflow: hidden;');
    var box = right && [].filter.call(right.querySelectorAll('div'), function (d) { return d.className === 'w-full h-full ' && d.firstElementChild && d.firstElementChild.className === 'w-full h-full overflow-auto'; })[0];
    if (box) set(box, 'class', 'w-full h-full fixed inset-0 z-20 bg-white');
    fsUndo = undo; fullscreen = true;
  }
  function exitFullscreen() { if (fsUndo) fsUndo.reverse().forEach(function (f) { f(); }); fsUndo = null; fullscreen = false; }

  // ---------- chat panel width: "Expand to right" switches the chat between 50% and 75% (as observed live) ----------
  function setChatWidth(pct) {
    var panels = document.querySelectorAll('[data-panel]'), right = panels[panels.length - 1], side = document.getElementById('sidebar');
    if (side) { side.style.flex = pct + ' 1 0px'; side.setAttribute('data-panel-size', pct.toFixed(1)); }
    if (right) { right.style.flex = (100 - pct) + ' 1 0px'; right.setAttribute('data-panel-size', (100 - pct).toFixed(1)); }
  }
  function chatWidth() { var s = document.getElementById('sidebar'); return s ? parseFloat(s.style.flex) || 0 : 0; }
  function toggleChatExpand() {
    if (fullscreen) exitFullscreen();
    if (minimized) restoreChat();
    setChatWidth(chatWidth() === 50 ? 75 : 50);
  }

  // ---------- "Minimize Chat": chat panel collapses; the floating AskMod button brings it back ----------
  var minimized = null;
  function minimizeChat() {
    if (minimized) return;
    var prev = chatWidth(), handle = document.querySelector('[data-resize-handle]'), group = document.querySelector('[data-panel-group]');
    setChatWidth(0);
    if (handle) handle.style.display = 'none';
    var bubble = document.getElementById('chat-min-bubble').content.firstElementChild.cloneNode(true);
    if (group) group.parentElement.insertBefore(bubble, group);
    minimized = { prev: prev, bubble: bubble, handle: handle };
  }
  function restoreChat() {
    if (!minimized) return;
    setChatWidth(minimized.prev || 20);
    if (minimized.handle) minimized.handle.style.display = '';
    minimized.bubble.remove();
    minimized = null;
  }

  // ---------- chat-tools (⋮) menu ----------
  function closeToolsMenu() { var m = document.getElementById('chat-tools-open'); if (m) m.remove(); }
  function toggleToolsMenu(btn) {
    if (document.getElementById('chat-tools-open')) { closeToolsMenu(); return; }
    var menu = document.getElementById('chat-tools-menu').content.cloneNode(true);
    var host = btn.closest('.relative.inline-block') || btn.parentElement;
    var wrap = document.createElement('div'); wrap.id = 'chat-tools-open'; wrap.style.display = 'contents';
    wrap.appendChild(menu); host.appendChild(wrap);
  }
  function toolsMenuAction(item) {
    var id = item.getAttribute('data-testid');
    if (id === 'headerMinimizeChatButton') { closeToolsMenu(); minimizeChat(); return; }
    if (id === 'headerHistoryButton') { closeToolsMenu(); open('conversation-history'); return; }
    if (id === 'headerThinkHarderButton') {
      var on = item.getAttribute('aria-pressed') !== 'true';
      item.setAttribute('aria-pressed', String(on));
      item.querySelector('span').textContent = 'Recollect Harder ' + (on ? 'On' : 'Off');
      return;
    }
    var sw = item.querySelector('.p-inputswitch');
    if (sw) {
      var onS = sw.getAttribute('aria-checked') !== 'true';
      sw.setAttribute('aria-checked', String(onS)); sw.setAttribute('data-p-highlight', String(onS));
      sw.classList.toggle('p-highlight', onS);
      var inp = sw.querySelector('input'); if (inp) { inp.checked = onS; inp.setAttribute('aria-checked', String(onS)); }
      return;
    }
    closeToolsMenu();  // Pre-Release Quality Checklist / Log Controls: their targets were not captured
  }

  // ---------- in-place tabs / toggles ----------
  function switchTab(btn) {
    var spec = btn.getAttribute('data-tab').split(':'), group = spec[0], panel = spec[1];
    document.querySelectorAll('[data-panel^="' + group + ':"]').forEach(function (p) {
      p.hidden = p.getAttribute('data-panel') !== group + ':' + panel;
      if (!p.hidden) initCharts(p);
    });
    document.querySelectorAll('[data-tab^="' + group + ':"]').forEach(function (b) {
      var on = b === btn, act = (b.getAttribute('data-active-class') || '').split(/\s+/).filter(Boolean), idle = (b.getAttribute('data-idle-class') || '').split(/\s+/).filter(Boolean);
      (on ? idle : act).forEach(function (c) { b.classList.remove(c); });
      (on ? act : idle).forEach(function (c) { b.classList.add(c); });
      b.setAttribute('aria-selected', String(on));
    });
  }
  function toggle(el) {
    var attr = el.hasAttribute('aria-pressed') ? 'aria-pressed' : 'aria-checked';
    var on = el.getAttribute(attr) !== 'true';
    el.setAttribute(attr, String(on));
    var a = (el.getAttribute('data-on-class') || '').split(/\s+/).filter(Boolean), b = (el.getAttribute('data-off-class') || '').split(/\s+/).filter(Boolean);
    (on ? b : a).forEach(function (c) { el.classList.remove(c); });
    (on ? a : b).forEach(function (c) { el.classList.add(c); });
  }

  // ---------- events ----------
  document.addEventListener('click', function (e) {
    var t = e.target, el;
    if ((el = t.closest('a[href^="#"]')) && !el.hasAttribute('data-go')) e.preventDefault();
    if (t.closest('form') && t.closest('button')) e.preventDefault();
    if ((el = t.closest('[title="Toggle Fullscreen"]'))) { fullscreen ? exitFullscreen() : enterFullscreen(); return; }
    // AskMod chat-panel header buttons
    if ((el = t.closest('[data-testid="headerProjectsButton"]'))) { e.preventDefault(); if (current !== 'projects') show('projects'); return; }
    if ((el = t.closest('[data-testid="headerNewChatButton"]'))) { e.preventDefault(); if (window.__chat) window.__chat.reset(); return; }
    if ((el = t.closest('[data-testid="headerExpandChatButton"]'))) { e.preventDefault(); toggleChatExpand(); return; }
    if ((el = t.closest('#chat-tools-open button, #chat-tools-open .flex.w-full'))) { e.preventDefault(); toolsMenuAction(el); return; }
    if ((el = t.closest('.chatToolsPopoverBtn'))) { e.preventDefault(); toggleToolsMenu(el); return; }
    if (!t.closest('#chat-tools-open')) closeToolsMenu();
    if ((el = t.closest('.maximizeChatButton'))) { e.preventDefault(); restoreChat(); return; }
    if ((el = t.closest('[aria-label="Close messages"]'))) { e.preventDefault(); [].slice.call(el.parentElement.children).forEach(function (c) { c.remove(); }); return; }
    if ((el = t.closest('.h-20 [title="Open sidebar"]'))) { e.preventDefault(); open('conversation-history'); return; }
    if ((el = t.closest('[data-close]'))) { e.preventDefault(); closeTop(); return; }
    if ((el = t.closest('[data-backdrop]')) && el === t) { closeTop(); return; }
    if ((el = t.closest('[data-open]'))) { e.preventDefault(); open(el.getAttribute('data-open')); return; }
    if ((el = t.closest('[data-go]'))) { e.preventDefault(); var g = el.getAttribute('data-go'); if (g !== current) show(g); else closeAll(); return; }
    if ((el = t.closest('[data-tab]'))) { e.preventDefault(); switchTab(el); return; }
    if ((el = t.closest('[data-toggle]'))) { e.preventDefault(); toggle(el); return; }
  }, true);
  document.addEventListener('submit', function (e) { e.preventDefault(); }, true);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && overlays.length) closeTop(); });
  window.addEventListener('hashchange', function () { route(false); });

  function route(initial) {
    var h = decodeURIComponent(location.hash.slice(1)), parts = h.split('+'), sid = parts[0], oid = parts[1];
    if (!tpl('s', sid)) sid = 'dashboard';
    if (sid !== current || initial) show(sid, false);
    if (oid && tpl('o', oid)) { open(oid); setHash(sid, false); }
  }
  window.__v2 = { show: show, open: open, close: closeTop, state: function () { return { screen: current, overlays: overlays.map(function (w) { return w.getAttribute('data-overlay'); }) }; } };
  route(true);
})();
