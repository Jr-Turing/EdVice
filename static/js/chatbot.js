// Minimal floating chat widget that talks to /api/chat
(function(){
  const logoPath = '/static/images/MainLogo.png';

  // Floating toggle button
  const btn = document.createElement('button');
  btn.className = 'edvise-chat-button';
  btn.innerHTML = `<img src="${logoPath}" alt="EdVise" />`;

  // Chat panel
  const panel = document.createElement('div');
  panel.className = 'edvise-chat-panel';
  panel.innerHTML = `
    <div class="edvise-chat-header">
      <img src="${logoPath}" alt="EdVise" />
      <div class="title">EdVise Assistant</div>
      <div class="spacer"></div>
      <button class="icon-btn" data-action="minimize" title="Minimize">_</button>
      <button class="icon-btn" data-action="close" title="Close">×</button>
    </div>
    <div class="edvise-chat-body" id="edvise-body">
      <div class="edvise-msg edvise-bot">
        <div class="edvise-avatar"><img src="${logoPath}" alt="bot"/></div>
        <div class="edvise-bubble">Hi! Ask me about careers, exams, colleges, or scholarships.
          <div class="edvise-suggestions">
            <span class="edvise-chip" data-q="Best career for maths lover?">Maths careers</span>
            <span class="edvise-chip" data-q="Upcoming exams after 12th?">Exams after 12th</span>
            <span class="edvise-chip" data-q="Government scholarships for SC/ST/OBC?">Govt scholarships</span>
          </div>
        </div>
      </div>
    </div>
    <div class="edvise-chat-footer">
      <form class="edvise-input" id="edvise-form">
        <input type="text" placeholder="Type your question..." required />
        <button type="submit">Send</button>
      </form>
    </div>`;

  function addMessage(role, text){
    const body = panel.querySelector('#edvise-body');
    const wrap = document.createElement('div');
    wrap.className = 'edvise-msg ' + (role === 'user' ? 'edvise-user' : 'edvise-bot');
    const avatar = document.createElement('div');
    avatar.className = 'edvise-avatar';
    avatar.innerHTML = `<img src="${logoPath}" alt="${role}"/>`;
    const bubble = document.createElement('div');
    bubble.className = 'edvise-bubble';
    bubble.textContent = text;
    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    body.appendChild(wrap);
    body.scrollTop = body.scrollHeight;
    return bubble;
  }

  function addThinking(){
    const body = panel.querySelector('#edvise-body');
    const wrap = document.createElement('div');
    wrap.className = 'edvise-msg edvise-bot';
    const avatar = document.createElement('div');
    avatar.className = 'edvise-avatar';
    avatar.innerHTML = `<img src="${logoPath}" alt="bot"/>`;
    const bubble = document.createElement('div');
    bubble.className = 'edvise-bubble';
    bubble.innerHTML = `<span class="edvise-typing"><span></span><span></span><span></span></span>`;
    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    body.appendChild(wrap);
    body.scrollTop = body.scrollHeight;
    return bubble;
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.body.appendChild(btn);
    document.body.appendChild(panel);

    const form = panel.querySelector('#edvise-form');
    const input = form.querySelector('input');
    const history = [];

    function openPanel(){ panel.classList.add('open'); input.focus(); }
    function closePanel(){ panel.classList.remove('open'); }

    btn.addEventListener('click', openPanel);
    panel.querySelector('[data-action="close"]').addEventListener('click', closePanel);
    panel.querySelector('[data-action="minimize"]').addEventListener('click', ()=> panel.classList.remove('open'));

    panel.addEventListener('click', (e)=>{
      const chip = e.target.closest('.edvise-chip');
      if(chip){
        input.value = chip.getAttribute('data-q') || chip.textContent;
        form.dispatchEvent(new Event('submit', {cancelable:true}));
      }
    });

    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const text = input.value.trim();
      if(!text) return;
      input.value = '';

      addMessage('user', text);
      history.push({role:'user', content:text});
      const thinkingBubble = addThinking();

      try{
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({message:text, history})
        });
        let data = {};
        try { data = await res.json(); } catch {}
        if(!res.ok) throw new Error((data && data.error) ? data.error : `HTTP ${res.status}`);
        thinkingBubble.textContent = data.reply || '(no reply)';
        history.push({role:'assistant', content:data.reply || ''});
      }catch(err){
        thinkingBubble.textContent = 'Sorry, I had trouble answering that. (' + err.message + ')';
        console.error(err);
      }
    });
  });
})();
