(() => {
      const st = document.querySelector('.awd62-stage');
      if (!st) return { present: false };
      const cap = st.querySelector('.awd62-caption');
      const skip = st.querySelector('.awd62-skip');
      const frame = st.querySelector('.awd62-frame');
      const cv = st.querySelector('canvas.awd62-canvas');
      const audClassCount = st.querySelectorAll('[class*="aud"]').length; // 反向探針：觀眾帶已剔走應為 0（class 名拆開查，唔寫全名）
      const stageBg = getComputedStyle(st).backgroundColor; // F1：frame 上下剩餘空間底色
      const conf = [...st.querySelectorAll('.awd62-m5fx149')].map(im => ({on: im.classList.contains('on'), vis: getComputedStyle(im).display !== 'none', w: Math.round(im.getBoundingClientRect().width), h: Math.round(im.getBoundingClientRect().height)}));
      const cards = [...st.querySelectorAll('.awd63-card')].map(c => {
        const css = c.querySelector('.awd63-csscard');
        const img = c.querySelector('img');
        return { cls: (c.className||'').toString(), text: (c.innerText||'').replace(/
/g,' / ').slice(0,60),
                 hasImg: !!img, imgSrc: img ? (img.getAttribute('src')||'').slice(0,60) : null,
                 cssText: css ? (css.innerText||'').replace(/
/g,' / ').slice(0,60) : null,
                 cssHasIcon: css ? !!css.querySelector('img, .awd63-cssicon') : null,
                 titleCount: ((c.innerText||'').match(/《/g)||[]).length };
      });
      const r = el => { if(!el) return null; const b = el.getBoundingClientRect(); return {top: Math.round(b.top), bottom: Math.round(b.bottom), h: Math.round(b.height), w: Math.round(b.width), left: Math.round(b.left), right: Math.round(b.right)}; };
      return { present: true,
               caption: cap ? cap.textContent : '',
               captionHtml: cap ? cap.innerHTML.slice(0, 300) : '',
               skipVisible: !!skip && skip.getBoundingClientRect().width > 0,
               skipBox: r(skip), frameBox: r(frame), audClassCount, stageBg, confetti: conf,
               canvasBacking: cv ? {w: cv.width, h: cv.height} : null,
               canvasBox: r(cv),
               captionBox: r(cap), vh: window.innerHeight, vw: window.innerWidth,
               captionOverflowsBottom: cap ? (cap.getBoundingClientRect().bottom > window.innerHeight + 1) : null,
               cards };
    })