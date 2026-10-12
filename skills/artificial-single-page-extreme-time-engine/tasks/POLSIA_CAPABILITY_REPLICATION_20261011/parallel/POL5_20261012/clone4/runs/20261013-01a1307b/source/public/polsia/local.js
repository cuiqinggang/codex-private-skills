// Local interactions on captured source DOM. No production API, analytics or authentication.
(() => {
  'use strict';
  const root = document.getElementById('root');
  const statesReady = fetch('/polsia/states.json').then(r => { if (!r.ok) throw new Error('页面状态暂不可用'); return r.json(); });
  let state = 'initial', idea = '', name = '', busy = false, languagePortal, languageTrigger;
  const notice = (message, container = document.querySelector('.login-content,.onboarding-content,.about-tx__content,.marketing-page-inner') || root) => {
    container.querySelector('.polsia-local-notice')?.remove();
    const box = document.createElement('div'); box.className = 'polsia-local-notice'; box.role = 'alert'; box.tabIndex = -1;
    const text = document.createElement('p'); text.textContent = message; box.append(text);
    const link = document.createElement('a'); link.href = '/workspace'; link.textContent = '打开本地工作区'; box.append(link);
    container.append(box); box.focus();
  };
  const localAuth = () => notice('这是本地工作区。Google 登录与邮件验证尚未接入，不会向原站提交账号或发送邮件。可以直接进入本地工作区，或返回创建公司。');
  async function renderState(next) {
    try {
      const states = await statesReady; const markup = states[next]; if (!markup) throw new Error('未知页面状态');
      const holder = document.createElement('div'); holder.innerHTML = markup;
      const capturedRoot = holder.firstElementChild;
      if (capturedRoot?.id !== 'root') throw new Error('页面状态缺少根节点');
      state = next; root.replaceChildren(...Array.from(capturedRoot.childNodes));
      const textarea = root.querySelector('textarea'); if (textarea) textarea.value = idea;
      const companyName = root.querySelector('#onboarding-company-name'); if (companyName) companyName.value = name;
      const website = root.querySelector('#onboarding-company-website'); if (website) website.value = idea;
      updateForm(); bindLanguage();
      (textarea || companyName)?.focus();
    } catch (error) { notice(error.message || '页面状态读取失败'); }
  }
  function updateForm() {
    const form = root.querySelector('.onboarding-form'); if (!form) return;
    const button = form.querySelector('button[type=submit]');
    if (button) button.disabled = busy || !idea.trim() || (state === 'existing' && name.trim().length < 2);
  }
  async function saveCompany() {
    if (busy || !idea.trim() || (state === 'existing' && name.trim().length < 2)) return;
    if (idea.trim().length > 1200) { notice('本地公司目标最多1200字，请精简后保存。'); return; }
    const companyName = state === 'existing' ? name.trim() : (idea.trim().split(/[。！？\n]/)[0].slice(0, 60) || '新公司');
    if (companyName.length > 80) { notice('本地公司名称最多80字，请精简后保存。'); return; }
    busy = true; updateForm();
    try {
      const response = await fetch('/api/companies', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ name: companyName, goal: idea.trim() }) });
      const value = await response.json();
      if (!response.ok || typeof value.id !== 'string') throw new Error(value.error || '公司保存失败');
      localStorage.setItem('company-lab-selection', value.id);
      location.assign('/workspace');
    } catch (error) { notice(error.message || '公司保存失败，请检查本地服务。'); }
    finally { busy = false; updateForm(); }
  }
  document.addEventListener('input', event => {
    if (event.target.matches('.onboarding-textarea,#onboarding-company-website')) idea = event.target.value;
    if (event.target.matches('#onboarding-company-name')) name = event.target.value;
    updateForm();
  });
  document.addEventListener('submit', event => {
    if (event.target.matches('.onboarding-form')) { event.preventDefault(); saveCompany(); }
    if (event.target.matches('.login-form')) { event.preventDefault(); localAuth(); }
  });
  document.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (button?.closest('.polsia-landing .slides')) { location.assign('/new'); return; }
    if (button?.closest('.login-content') && button.type !== 'submit') { localAuth(); return; }
    if (button?.classList.contains('onboarding-back')) { renderState(state === 'idea' ? 'choice' : 'initial'); return; }
    if (button?.classList.contains('onboarding-cta') && button.type !== 'submit') {
      const buttons = Array.from(root.querySelectorAll('.onboarding-buttons .onboarding-cta'));
      if (state === 'initial') renderState(buttons.indexOf(button) === 0 ? 'choice' : 'existing');
      else if (state === 'choice') {
        if (buttons.indexOf(button) === 0) idea = '为本地小型餐厅提供社交媒体内容、客户答复与可审核营销计划。';
        renderState('idea');
      }
      return;
    }
    if (button?.classList.contains('about-tx__speaker-btn')) toggleSoundtrack();
    const link = event.target.closest('a');
    if (link && (link.getAttribute('href')?.startsWith('mailto:') || /^https?:\/\//i.test(link.getAttribute('href') || ''))) {
      event.preventDefault(); notice('这是原站内容中的外部链接。本地页面保留其外观，未发送消息或连接外部系统。');
    }
  });

  function closeLanguage() {
    languagePortal?.remove(); languagePortal = undefined;
    if (languageTrigger) { languageTrigger.setAttribute('aria-expanded', 'false'); languageTrigger.dataset.state = 'closed'; }
  }
  async function openLanguage(trigger) {
    if (languagePortal && trigger === languageTrigger) { closeLanguage(); return; }
    closeLanguage(); languageTrigger = trigger;
    try {
      const states = await statesReady, holder = document.createElement('div'); holder.innerHTML = states.language;
      languagePortal = holder.firstElementChild; document.body.append(languagePortal);
      const box = trigger.getBoundingClientRect(), width = languagePortal.offsetWidth;
      const left = Math.max(16, Math.min(box.right - width, innerWidth - width - 16)), top = box.bottom + 4;
      languagePortal.style.transform = `translate(${left}px, ${top}px)`;
      languagePortal.style.setProperty('--radix-popper-available-width', `${innerWidth - 32}px`);
      languagePortal.style.setProperty('--radix-popper-available-height', `${innerHeight - top - 16}px`);
      languagePortal.style.setProperty('--radix-popper-anchor-width', `${box.width}px`);
      languagePortal.style.setProperty('--radix-popper-anchor-height', `${box.height}px`);
      trigger.setAttribute('aria-expanded', 'true'); trigger.dataset.state = 'open';
      const search = languagePortal.querySelector('input'), options = Array.from(languagePortal.querySelectorAll('[role=option]'));
      const nativeSelect = trigger.parentElement.querySelector('select');
      const nativeOptions = Array.from(nativeSelect?.options || []).filter(option => option.value);
      const indicator = languagePortal.querySelector('.polsia-select__item-indicator')?.cloneNode(true);
      const selectedIndex = Math.max(0, nativeOptions.findIndex(option => option.value === (nativeSelect?.value || 'auto')));
      options.forEach((option, index) => {
        const selected = index === selectedIndex; option.setAttribute('aria-selected', String(selected)); option.dataset.state = selected ? 'checked' : 'unchecked';
        option.querySelector('.polsia-select__item-indicator')?.remove(); if (selected && indicator) option.prepend(indicator.cloneNode(true));
      });
      let highlighted = 0;
      const highlight = index => { const visible = options.filter(option => !option.hidden); highlighted = Math.max(0, Math.min(index, visible.length - 1)); options.forEach(option => option.removeAttribute('data-highlighted')); visible[highlighted]?.setAttribute('data-highlighted', ''); visible[highlighted]?.scrollIntoView({ block: 'nearest' }); };
      const choose = option => {
        const index = options.indexOf(option), selected = nativeOptions[index];
        if (selected) { if (nativeSelect) nativeSelect.value = selected.value; trigger.firstElementChild.textContent = selected.text; localStorage.setItem('polsia-public-language', selected.value); document.documentElement.lang = selected.value === 'auto' ? 'zh-Hans' : selected.value; }
        closeLanguage(); trigger.focus();
      };
      search.addEventListener('input', () => { const query = search.value.trim().toLowerCase(); options.forEach(option => { option.hidden = !option.textContent.toLowerCase().includes(query); }); highlight(0); });
      options.forEach(option => option.addEventListener('click', () => choose(option)));
      search.addEventListener('keydown', event => { if (event.key === 'ArrowDown' || event.key === 'ArrowUp') { event.preventDefault(); highlight(highlighted + (event.key === 'ArrowDown' ? 1 : -1)); } else if (event.key === 'Enter') { event.preventDefault(); const visible = options.filter(option => !option.hidden); if (visible[highlighted]) choose(visible[highlighted]); } });
      search.focus();
    } catch (error) { closeLanguage(); notice(error.message || '语言菜单读取失败'); }
  }
  function bindLanguage() {
    document.querySelectorAll('.public-language-selector__trigger').forEach(trigger => {
      if (trigger.dataset.localBound) return; trigger.dataset.localBound = 'true';
      const nativeSelect = trigger.parentElement.querySelector('select');
      const stored = localStorage.getItem('polsia-public-language');
      const selected = Array.from(nativeSelect?.options || []).find(option => option.value === stored);
      if (selected) { nativeSelect.value = selected.value; trigger.firstElementChild.textContent = selected.text; document.documentElement.lang = selected.value === 'auto' ? 'zh-Hans' : selected.value; }
      trigger.addEventListener('click', () => openLanguage(trigger));
    });
  }
  document.addEventListener('pointerdown', event => { if (languagePortal && !languagePortal.contains(event.target) && !languageTrigger?.contains(event.target)) closeLanguage(); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && languagePortal) { closeLanguage(); languageTrigger?.focus(); } });
  bindLanguage();

  // Original Cst/Dst speaker frames and rhythm, rendered locally without the source bundle.
  const speakerButton = document.querySelector('.about-tx__speaker-btn');
  const speakerFrames = [
    `   ♪ ♫ ♪\n  ╭───────╮\n  │▓▓▓▓▓▓▓│\n  │▓▓▓▓▓▓▓│\n  ├───────┤\n  │ ◉   ◉ │\n  │   ▽   │\n  └───┬───┘\n    ══╧══`,
    `   ♫ ♪ ♫\n  ╭───────╮\n  │▒▒▒▒▒▒▒│\n  │▒▒▒▒▒▒▒│\n  ├───────┤\n  │ ◉   ◉ │\n  │   ▽   │\n  └───┬───┘\n    ══╧══`,
    `   ♪ ♫ ♪\n  ╭───────╮\n  │▓▓▓▓▓▓▓│\n  │▓▓▓▓▓▓▓│\n  ├───────┤\n  │ ─   ─ │\n  │   ▽   │\n  └───┬───┘\n    ══╧══`,
  ];
  let soundtrack, wantsSoundtrack = false, speakerTimer;
  function animateSpeaker(playing) {
    if (!speakerButton) return;
    clearTimeout(speakerTimer);
    speakerButton.setAttribute('aria-pressed', String(playing));
    speakerButton.setAttribute('aria-label', playing ? '暂停配乐' : '播放配乐');
    const display = frame => { speakerButton.querySelector('.about-tx__speaker').textContent = playing ? speakerFrames[frame] : speakerFrames[frame].replace(/[♪♫]/g, ' '); };
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { display(0); return; }
    const tick = sequence => {
      if (!sequence.length) sequence = playing
        ? (Math.random() < .2 ? [[2,150],[0,500 + Math.random() * 700]] : [[1,260],[0,200],[1,260],[0,500 + Math.random() * 700]])
        : [[2,150],[0,1800 + Math.random() * 2600]];
      const [frame, delay] = sequence[0]; display(frame);
      speakerTimer = setTimeout(() => tick(sequence.slice(1)), delay);
    };
    tick([]);
  }
  async function toggleSoundtrack() {
    if (!speakerButton) return;
    if (!soundtrack) {
      soundtrack = new Audio('/audio/background.wav'); soundtrack.preload = 'none'; soundtrack.loop = true;
      soundtrack.addEventListener('play', () => { if (!wantsSoundtrack) soundtrack.pause(); else animateSpeaker(true); });
      soundtrack.addEventListener('pause', () => animateSpeaker(false));
    }
    wantsSoundtrack = !wantsSoundtrack;
    if (!wantsSoundtrack) { soundtrack.pause(); animateSpeaker(false); return; }
    try { await soundtrack.play(); }
    catch { if (wantsSoundtrack) { wantsSoundtrack = false; animateSpeaker(false); notice('本地原配乐暂不能播放，请检查音频资产与浏览器播放权限。'); } }
  }
  if (speakerButton) animateSpeaker(false);
  addEventListener('pagehide', () => { clearTimeout(speakerTimer); soundtrack?.pause(); });

  // Source Ust/qst: responsive doctrine title and scroll-linked cloud/fade/sticky layers.
  const church = document.querySelector('.church-page');
  if (church) {
    const title = church.querySelector('.church-title'), finale = church.querySelector('.church-finale');
    const background = church.querySelector('.church-bg'), mask = church.querySelector('.church-fade-mask'), sticky = church.querySelector('.church-join-sticky');
    let queued = false;
    const fitTitle = () => {
      const style = getComputedStyle(title), left = parseFloat(style.paddingLeft) || 0, right = parseFloat(style.paddingRight) || 0;
      const available = title.clientWidth - left - right; title.style.fontSize = '100px';
      const intrinsic = title.scrollWidth - left - right; if (intrinsic > 0) title.style.fontSize = `${100 * available / intrinsic}px`;
    };
    const update = () => {
      queued = false; const shift = Math.max(-innerHeight, Math.min(0, finale.getBoundingClientRect().top - innerHeight)), value = `${shift.toFixed(1)}px`;
      background.style.transform = `translateY(${value})`; mask.style.transform = `translateY(${value})`;
      sticky.style.transform = `translateX(-50%) translateY(${value})`; sticky.style.pointerEvents = shift < -innerHeight * .5 ? 'none' : 'auto';
    };
    const queue = () => { if (!queued) { queued = true; requestAnimationFrame(update); } };
    fitTitle(); update(); document.fonts?.ready.then(fitTitle);
    addEventListener('resize', () => { fitTitle(); queue(); }, { passive: true }); addEventListener('scroll', queue, { passive: true });
  }

  // Source Wst/Qst/Xst/Zst: local PNG raster to the original 38×23 "Polsia" ASCII effect.
  const merchandise = document.querySelector('.giftshop-shell');
  if (merchandise) {
    const motion = matchMedia('(prefers-reduced-motion: reduce)'), letters = 'Polsia', scramble = '#$%&*+<>/\\|=_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    const cleanup = [];
    merchandise.querySelectorAll('.giftshop-card').forEach(card => {
      const image = card.querySelector('img'), art = card.querySelector('.giftshop-card__ascii'), stamp = card.querySelector('.giftshop-card__stamp [aria-hidden=true]');
      const stampText = stamp?.textContent || ''; let hover = false, focus = false, interval, frame, generation = 0, raster;
      const rasterize = () => {
        try {
          const canvas = document.createElement('canvas'); canvas.width = 38; canvas.height = 23;
          const context = canvas.getContext('2d', { willReadFrequently: true }); if (!context) return;
          context.drawImage(image, 0, 0, 38, 23); const data = context.getImageData(0, 0, 38, 23).data, values = [];
          for (let i = 0; i < data.length; i += 4) { const alpha = data[i + 3] / 255, gray = (.299 * data[i] + .587 * data[i + 1] + .114 * data[i + 2]) / 255; values.push(gray * alpha + 1 - alpha); }
          const threshold = Math.max(...values) - .05, foreground = values.filter(value => value <= threshold), minimum = foreground.length ? Math.min(...foreground) : 0;
          const span = (foreground.length ? Math.max(...foreground) - minimum : 1) || 1; return values.map(value => value > threshold ? -1 : (value - minimum) / span);
        } catch { return undefined; }
      };
      const stop = () => { generation++; clearInterval(interval); cancelAnimationFrame(frame); interval = undefined; frame = undefined; art.textContent = ''; if (stamp) stamp.textContent = stampText; };
      const start = async () => {
        stop(); if (!hover && !focus) return; const current = generation;
        if (!image.complete || !image.naturalWidth) { try { await image.decode(); } catch { return; } }
        if (current !== generation || (!hover && !focus)) return;
        raster ||= rasterize(); if (!raster) return; let tick = 0;
        const paint = () => {
          const step = tick++; art.textContent = Array.from({ length: 23 }, (_, row) => Array.from({ length: 38 }, (_, column) => {
            const index = row * 38 + column, density = raster[index] ?? -1, noise = Math.abs(Math.sin(index * 12.9898 + step * 78.233) * 43758.5453) % 1;
            return density >= 0 && noise + .07 >= density ? letters[(index + step) % letters.length] : ' ';
          }).join('')).join('\n');
        };
        paint(); if (!motion.matches) interval = setInterval(paint, 90);
        if (stamp && !motion.matches) {
          const started = performance.now(); const animateStamp = now => {
            const progress = Math.min(1, (now - started) / 1100); if (progress >= 1) { stamp.textContent = stampText; return; }
            const revealed = Math.floor(progress * stampText.length); stamp.textContent = Array.from(stampText, (letter, index) => index < revealed || /\s/.test(letter) ? letter : scramble[(Math.floor(progress * 70) + index * 13) % scramble.length]).join(''); frame = requestAnimationFrame(animateStamp);
          }; frame = requestAnimationFrame(animateStamp);
        }
      };
      card.addEventListener('pointerenter', event => { if (event.pointerType !== 'touch') { hover = true; start(); } });
      card.addEventListener('pointerleave', () => { hover = false; focus ? start() : stop(); }); card.addEventListener('pointercancel', () => { hover = false; focus ? start() : stop(); });
      card.addEventListener('focus', () => { focus = true; start(); }); card.addEventListener('blur', () => { focus = false; hover ? start() : stop(); });
      motion.addEventListener('change', () => (hover || focus) ? start() : stop()); cleanup.push(stop);
    });
    addEventListener('pagehide', () => cleanup.forEach(stop => stop()));
  }

  const landing = document.querySelector('.polsia-landing');
  if (landing) {
    const slides = Array.from(landing.querySelectorAll('.slide')), fade = Array.from(landing.querySelectorAll('.fade-block'));
    const logo = landing.querySelector('.logo'), hint = landing.querySelector('.scroll-hint');
    let active = 0, queued = false;
    function update() {
      queued = false; const style = getComputedStyle(landing), height = innerHeight, scroll = scrollY;
      const top = parseInt(style.getPropertyValue('--banner-h')) + parseInt(style.getPropertyValue('--terminal-h'));
      const hero = parseInt(style.getPropertyValue('--logo-h-hero')), small = parseInt(style.getPropertyValue('--logo-h-small'));
      const size = hero + (small - hero) * Math.max(0, Math.min(1, scroll / parseInt(style.getPropertyValue('--logo-shrink-range'))));
      logo.style.height = `${size}px`; const cutoff = top + parseInt(style.getPropertyValue('--logo-pad')) + size + 12;
      fade.forEach(element => { if (!element.classList.contains('entered')) return; const box = element.getBoundingClientRect(); if (box.bottom >= 0 && box.top <= height) element.style.opacity = String(Math.max(0, Math.min(1, (box.top + 20 - cutoff) / 140))); });
      hint.classList.toggle('hidden', scroll > 4);
      let maximum = 0; slides.forEach((slide, index) => { const box = slide.getBoundingClientRect(), visible = Math.max(0, Math.min(box.bottom, height) - Math.max(box.top, 0)) / height; if (visible > maximum) { maximum = visible; active = index; } });
      const kind = ['hero', 'never-hire', 'mens', 'church'][active], dark = slides[active].dataset.bg === 'dark'; landing.dataset.slideKind = kind;
      logo.classList.toggle('on-dark', dark); landing.querySelector('.signin-link').classList.toggle('on-dark', dark); landing.querySelector('.scroll-hint-label').classList.toggle('on-dark', dark);
    }
    const queue = () => { if (!queued) { queued = true; requestAnimationFrame(update); } };
    const observer = new IntersectionObserver(entries => { entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('entered'); observer.unobserve(entry.target); } }); queue(); }, { threshold: .15, rootMargin: '0px 0px -10% 0px' });
    fade.forEach(element => observer.observe(element));
    const backgrounds = new IntersectionObserver(entries => { entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('bg-loaded'); backgrounds.unobserve(entry.target); } }); }, { rootMargin: '50% 0px 50% 0px' });
    slides.slice(1).forEach(slide => backgrounds.observe(slide));
    addEventListener('scroll', queue, { passive: true }); addEventListener('resize', queue);
    document.addEventListener('keydown', event => { if (event.defaultPrevented || languagePortal || event.target.closest('input,textarea,select,[role=combobox],[role=listbox]') || event.target.isContentEditable) return; if (event.key === 'ArrowDown' || event.key === 'ArrowUp') { event.preventDefault(); slides[Math.max(0, Math.min(slides.length - 1, active + (event.key === 'ArrowDown' ? 1 : -1)))].scrollIntoView({ behavior: 'smooth', block: 'start' }); } });
    const messages = ['> 欢迎来到 Polsia', '> 正在部署营销活动...', '> 正在处理自主任务...', '> 正在回复客户邮件...', '> 正在制作新的 UGC 视频...', '> 正在开展竞争研究...', '> 正在修复安全漏洞...'];
    const rotator = landing.querySelector('.t-line-rotator'); let message = 2;
    setInterval(() => { rotator.style.opacity = '0'; setTimeout(() => { message = (message + 1) % messages.length; rotator.textContent = messages[message]; rotator.style.opacity = '1'; }, 300); }, 5000);
    requestAnimationFrame(update);
  }
})();// Local page adapter only.
