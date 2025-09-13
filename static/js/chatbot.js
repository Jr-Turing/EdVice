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
        <div class="edvise-bubble">
          <div class="greeting-message">
            <div class="greeting-text">Hello! 👋 Welcome to EdVise Career Assistant!</div>
            <div class="greeting-subtext">I'm here to help you with career guidance, education advice, and opportunities in Jammu & Kashmir. Feel free to ask me anything!</div>
          </div>
          <div class="edvise-suggestions">
            <span class="edvise-chip" data-q="Hello">👋 Say Hello</span>
            <span class="edvise-chip" data-q="What can you help me with?">What can you do?</span>
            <span class="edvise-chip" data-q="Best career for maths lover?">Maths careers</span>
            <span class="edvise-chip" data-q="Upcoming exams after 12th?">Exams after 12th</span>
            <span class="edvise-chip" data-q="Government scholarships for students?">Scholarships</span>
            <span class="edvise-chip" data-q="Engineering colleges in J&K?">J&K Colleges</span>
          </div>
        </div>
      </div>
    </div>
    <div class="edvise-chat-footer">
      <form class="edvise-input" id="edvise-form">
        <input type="text" placeholder="Ask me about careers, exams, or colleges..." required />
        <button type="submit">Send</button>
      </form>
    </div>`;

  function addMessage(role, text, isStructured = false){
    const body = panel.querySelector('#edvise-body');
    const wrap = document.createElement('div');
    wrap.className = 'edvise-msg ' + (role === 'user' ? 'edvise-user' : 'edvise-bot');
    const avatar = document.createElement('div');
    avatar.className = 'edvise-avatar';
    avatar.innerHTML = `<img src="${logoPath}" alt="${role}"/>`;
    const bubble = document.createElement('div');
    bubble.className = 'edvise-bubble';
    
    if (isStructured && typeof text === 'object') {
      // Handle structured response
      let content = `<div class="structured-response">`;
      if (text.summary) {
        content += `<div class="response-summary">${text.summary}</div>`;
      }
      if (text.points && Array.isArray(text.points)) {
        content += `<div class="response-points">`;
        text.points.forEach((point, index) => {
          content += `<div class="response-point">
            <span class="point-number">${index + 1}.</span>
            <span class="point-text">${point}</span>
          </div>`;
        });
        content += `</div>`;
      }
      if (text.wordCount) {
        content += `<div class="word-count">Word count: ${text.wordCount}</div>`;
      }
      content += `</div>`;
      bubble.innerHTML = content;
    } else {
      bubble.textContent = text;
    }
    
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
        
        // Remove thinking bubble
        thinkingBubble.parentNode.remove();
        
        // Handle structured response
        if (data.status === 'success' && data.response) {
          addMessage('assistant', data.response, true);
          history.push({role:'assistant', content: data.response.summary || 'Career guidance provided'});
        } else if (data.status === 'error' && data.response && data.response.message) {
          addMessage('assistant', data.response.message);
          history.push({role:'assistant', content: data.response.message});
        } else if (data.reply) {
          // Fallback to old format if somehow returned
          addMessage('assistant', data.reply);
          history.push({role:'assistant', content: data.reply});
        } else {
          addMessage('assistant', 'Sorry, I couldn\'t process your request properly.');
        }
      }catch(err){
        thinkingBubble.textContent = 'Sorry, I had trouble answering that. (' + err.message + ')';
        console.error(err);
      }
    });
  });
})();
