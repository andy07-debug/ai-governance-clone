// Scripted AskMod.AI chat for the replica (left panel). The demo never uses the chat, so these three
// exchanges are written for the trailer; every figure in them is one shown on the replica's screens.
// Bot messages reuse the real AskMod message markup captured from the live app (#chat-bot-tpl).
(function () {
  var SCRIPT = [
    {
      q: 'Where did the money go this week?',
      match: /(money|spend|spent|cost|budget).*(week|go|went)|where.*(money|spend)/i,
      a: 'Total spend for the last 7 days is $22,703.83: $20,617.98 infrastructure and $2,085.85 LLM. The top model is gemini-2.5-flash ($573.38), and the top assistant is ggcllmprgenie ($251.53).'
    },
    {
      q: 'Who is using ggcllmprgenie?',
      match: /ggcllmprgenie|who.*(using|uses)|top assistant/i,
      a: '116 users across 1 agent, $251.53 in total ($224.10 input, $27.43 output). It’s at 51% of its $490 budget, so it’s still in the healthy range.'
    },
    {
      q: 'Are there any critical security alerts?',
      match: /alert|security|critical|firewall|threat/i,
      a: '4 critical alerts, all on “Kubernetes Container - Uptime for proposal-autoai-gke cluster” and all flagged. Open one and select “Why was this categorized?” to see the decision strength (85%) and the gaps in the reasoning.'
    }
  ];
  var FALLBACK = 'I can answer questions about spend, assistant usage and security alerts in this workspace. Try one of the suggestions below.';

  var log = document.getElementById('chat-log');
  var chips = document.getElementById('chat-chips');
  var botTpl = document.getElementById('chat-bot-tpl');
  var input = document.querySelector('[data-testid="ChatTextInput"]');
  var send = document.querySelector('[data-testid="ChatTextSendButton"]');
  if (!log || !botTpl || !input) return;
  var scroller = log.closest('.overflow-y-auto') || log.parentElement;
  var asked = {}, busy = false;

  function now() {
    return new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
  }
  function scrollDown() { scroller.scrollTop = scroller.scrollHeight; }
  function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

  function addUser(text) {
    var el = document.createElement('div');
    el.className = 'flex flex-col items-end gap-1 mb-2';
    el.innerHTML = '<div class="max-w-[85%] rounded-[8px] rounded-tr-none bg-[#EEEAF8] px-3 py-2 text-base leading-6 break-words" style="color: var(--cw-chat-text);">' +
      esc(text) + '</div><div class="text-[10px] pr-1" style="color: var(--cw-chat-text-muted);">' + now() + '</div>';
    log.appendChild(el); scrollDown();
  }
  function addTyping() {
    var el = document.createElement('div');
    el.className = 'flex items-center gap-3 mb-2 pl-1';
    el.innerHTML = '<span class="chat-dot"></span><span class="chat-dot" style="animation-delay:.15s"></span><span class="chat-dot" style="animation-delay:.3s"></span>';
    log.appendChild(el); scrollDown();
    return el;
  }
  function addBot(text, done) {
    var frag = botTpl.content.cloneNode(true);
    var msg = frag.firstElementChild;
    var p = msg.querySelector('p');
    var time = msg.querySelector('.text-\\[10px\\]');
    if (time) time.textContent = now();
    p.textContent = '';
    log.appendChild(msg);
    var i = 0;
    (function tick() {
      i = Math.min(text.length, i + 2);
      p.textContent = text.slice(0, i);
      scrollDown();
      if (i < text.length) setTimeout(tick, 16); else if (done) done();
    })();
  }
  function renderChips() {
    if (!chips) return;
    chips.innerHTML = '';
    SCRIPT.forEach(function (s, idx) {
      if (asked[idx]) return;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'chat-chip text-left text-[13px] leading-5 px-3 py-1.5 rounded-full border border-[#D9D2F7] bg-white text-[#5928ED] hover:bg-[#F4F1FE] transition-colors';
      b.textContent = s.q;
      // fire on press: if the input box is focused it shrinks on blur (AskMod's focus:!h-28), which would
      // move the chip before a normal click completes
      b.addEventListener('pointerdown', function (e) { e.preventDefault(); ask(s.q); });
      chips.appendChild(b);
    });
    chips.style.display = chips.children.length ? '' : 'none';
  }
  function ask(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    busy = true;
    input.value = '';
    addUser(text);
    var idx = -1;
    SCRIPT.forEach(function (s, k) { if (idx < 0 && (s.q.toLowerCase() === text.toLowerCase() || s.match.test(text))) idx = k; });
    var reply = idx >= 0 ? SCRIPT[idx].a : FALLBACK;
    if (idx < 0 && SCRIPT.every(function (x, k) { return asked[k]; })) asked = {};  // offer the suggestions again
    if (idx >= 0) asked[idx] = true;
    if (chips) chips.style.display = 'none';
    var typing = addTyping();
    setTimeout(function () {
      typing.remove();
      addBot(reply, function () { busy = false; renderChips(); });
    }, 900);
  }

  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(input.value); }
  });
  if (send) send.addEventListener('click', function (e) { e.preventDefault(); ask(input.value); });
  renderChips();
  window.__chat = { ask: ask };
})();
