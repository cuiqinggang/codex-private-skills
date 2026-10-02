async (page) => {
  let cfg = {};
  const record = {at:new Date().toISOString(), operation:cfg.operation, requested:null, transitions:[]};
  const trigger = page.getByRole('button', {name:'选择 ChatGPT 模型', exact:true});
  const menu = page.getByRole('menu', {name:'选择 ChatGPT 模型', exact:true});
  const safety = async () => {
    if (!page.url().startsWith('https://chatgpt.com/')) throw Error('WRONG_ORIGIN');
    if (await page.getByRole('button',{name:/^(登录|登入|注册|Log in|Sign up)$/i}).count()) throw Error('AUTH_UI_STOP');
    if (await page.getByText(/^(Verify you are human|验证您是真人|验证身份|多重验证|CAPTCHA)$/i).count()) throw Error('SECURITY_UI_STOP');
    if (await trigger.count() !== 1 || !(await trigger.isVisible())) throw Error('CONTROL_UNAVAILABLE');
    if (await page.getByRole('textbox',{name:'询问 ChatGPT',exact:true}).count() !== 1) throw Error('COMPOSER_UNAVAILABLE');
  };
  try {
    await safety();
    cfg = await page.evaluate(() => JSON.parse(sessionStorage.getItem('__ltmvh_model_effort_v1') || '{}'));
    record.operation=cfg.operation; record.requested=cfg.target || null;
    if (await menu.isVisible()) await page.keyboard.press('Escape');
    const normalize = (value) => ({'中':'Medium','高':'High',Medium:'Medium',High:'High'}[String(value || '').trim()] || null);
    const displayFor = (canonical, localeSample) => /[中高]/.test(localeSample) ? (canonical === 'Medium' ? '中' : '高') : canonical;
    const beforeRaw = (await trigger.innerText()).trim();
    const before = normalize(beforeRaw);
    const target = normalize(cfg.target);
    record.originalRaw = beforeRaw; record.original = before; record.actualRaw = beforeRaw; record.actual = before;
    record.conversationUrl = page.url();
    if (cfg.operation === 'read') { record.status='READ'; return record; }
    if (cfg.operation !== 'set') throw Error('UNSUPPORTED_OPERATION');
    record.transitions.push('SET_REQUESTED');
    if (!target) { record.status='UNAVAILABLE'; record.reason='TARGET_NOT_ALLOWED_OR_DISCOVERED'; record.changed=false; return record; }
    if (!before) { record.status='UNAVAILABLE'; record.reason='ORIGINAL_OUTSIDE_CERTIFIED_RANGE'; record.changed=false; return record; }
    if (before === target) { record.status='READBACK_MATCH'; record.changed=false; return record; }
    await trigger.click();
    const strength = menu.getByRole('menuitem',{name:'强度',exact:true});
    if (await strength.count() !== 1 || !(await strength.isEnabled())) throw Error('STRENGTH_UNAVAILABLE');
    const status = menu.getByRole('status');
    const announcement = (await status.innerText()).trim();
    if (!announcement.startsWith(beforeRaw+'，')) throw Error('MENU_READBACK_MISMATCH');
    record.beforeAnnouncement=announcement;
    await safety();
    await strength.press(before==='Medium'?'ArrowRight':'ArrowLeft');
    record.transitions.push('UI_CHANGED'); record.changed=true;
    await page.waitForTimeout(200);
    const afterAnnouncement = (await status.innerText()).trim();
    record.afterAnnouncement=afterAnnouncement;
    await page.keyboard.press('Escape');
    record.actualRaw=(await trigger.innerText()).trim();
    record.actual=normalize(record.actualRaw);
    await safety();
    const targetRaw=displayFor(target,beforeRaw);
    if (record.actual !== target || !afterAnnouncement.startsWith(targetRaw+'，')) throw Error('READBACK_MISMATCH');
    record.transitions.push('READBACK_MATCH'); record.status='READBACK_MATCH';
    record.completedAt=new Date().toISOString(); return record;
  } catch (error) {
    record.status='FAIL'; record.reason=error.message;
    if (await menu.isVisible().catch(()=>false)) await page.keyboard.press('Escape').catch(()=>{});
    record.actual=await trigger.count().then(async n=>n===1?(await trigger.innerText()).trim():null).catch(()=>null);
    return record;
  }
}
