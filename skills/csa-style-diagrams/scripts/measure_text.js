// Measures the locally exported SVG's actual browser-laid-out text, not PNG pixels.
document.fonts.ready.then(() => setTimeout(() => {
  const issues = [], measured = [];
  const warn = (code, message) => issues.push({level: "warning", code, message});
  const box = r => ({left:r.left, top:r.top, right:r.right, bottom:r.bottom});
  for (const id of window.csaLabels) {
    const cell = [...document.querySelectorAll("[data-cell-id]")].find(e => e.dataset.cellId === id);
    const slot = cell?.querySelector(":scope > g > rect, :scope > g > path, :scope > g > ellipse, :scope > g > circle");
    const foreign = cell?.querySelector("foreignObject");
    const rects = [];
    if (foreign) {
      const walker = document.createTreeWalker(foreign, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {
        if (!node.textContent.trim()) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        rects.push(...[...range.getClientRects()].filter(r => r.width && r.height));
      }
    } else if (cell) {
      for (const text of cell.querySelectorAll("text")) rects.push(text.getBoundingClientRect());
    }
    if (!slot || !rects.length) {
      warn("text-unmeasured", `${id}: exported text or reserved bounds not found`);
      continue;
    }
    const actual = {
      left: Math.min(...rects.map(r => r.left)), top: Math.min(...rects.map(r => r.top)),
      right: Math.max(...rects.map(r => r.right)), bottom: Math.max(...rects.map(r => r.bottom))
    };
    const reserved = box(slot.getBoundingClientRect());
    measured.push({id, actual, reserved});
    if (actual.left < reserved.left-2 || actual.right > reserved.right+2 ||
        actual.top < reserved.top-2 || actual.bottom > reserved.bottom+2) {
      warn("text-overflow", `${id}: browser text extends beyond its reserved slot`);
    }
  }
  for (let i=0; i<measured.length; i++) {
    for (let j=i+1; j<measured.length; j++) {
      const a=measured[i], b=measured[j];
      const dx=Math.max(a.actual.left,b.actual.left)-Math.min(a.actual.right,b.actual.right);
      const dy=Math.max(a.actual.top,b.actual.top)-Math.min(a.actual.bottom,b.actual.bottom);
      if (dx<0 && dy<0) warn("rendered-text-overlap", `${a.id} / ${b.id}: text rectangles overlap`);
      else if ((dx<0 && dy>=0 && dy<4) || (dy<0 && dx>=0 && dx<4)) {
        warn("rendered-text-crowding", `${a.id} / ${b.id}: less than 4 browser pixels apart`);
      }
    }
  }
  const report=document.getElementById("csa-report");
  report.textContent=JSON.stringify({errors:0,warnings:issues.length,issues,measured});
  report.dataset.ready="1";
}, 100)).catch(error => {
  const report=document.getElementById("csa-report");
  report.textContent=JSON.stringify({errors:1,warnings:0,issues:[{level:"error",code:"browser-measurement",message:String(error)}]});
  report.dataset.ready="1";
});
