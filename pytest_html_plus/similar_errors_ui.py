"""Optional report UI; group membership is embedded once and rendered on demand."""

import json


def render_similar_errors(groups, results, anchor_for_nodeid):
    names = {t["nodeid"]: t["test"] for t in results}
    payload = {
        key: {
            "message": group["message"],
            "tests": [
                {"anchor": anchor_for_nodeid(nodeid), "name": names[nodeid]}
                for nodeid in group["nodeids"]
                if nodeid in names
            ],
        }
        for key, group in groups.items()
    }
    data = json.dumps(payload).replace("<", "\\u003c").replace("&", "\\u0026")
    return (
        '<script type="application/json" id="similar-errors-data">'
        + data
        + "</script>"
        + UI
    )


UI = """
<style>
.similar-errors-badge { background:#eee; color:#444; border:1px solid #bbb;
 border-radius:3px; padding:2px 5px; font-size:.85em; cursor:pointer; }
#similar-errors-popover { position:fixed; inset:auto; margin:0; z-index:1000;
 box-sizing:border-box; width:min(360px, calc(100vw - 16px)); max-height:50vh;
 overflow:auto; background:white; color:#333; border:1px solid #bbb;
 border-radius:5px; padding:12px; box-shadow:0 3px 12px #0003; }
#similar-errors-popover a { display:block; padding:5px 0; overflow-wrap:anywhere; }
#similar-errors-popover p { overflow-wrap:anywhere; }
#similar-errors-popover .similar-errors-note { margin-top:10px; padding-top:8px;
 border-top:1px solid #e5e7eb; color:#666; font-size:.8rem; line-height:1.5; }
#similar-errors-popover .similar-errors-note code { overflow-wrap:anywhere; }
</style>
<div id="similar-errors-popover" role="dialog" aria-label="Similar errors in this report" hidden></div>
<script>
(() => {
 const groups = JSON.parse(document.getElementById('similar-errors-data').textContent);
 const panel = document.getElementById('similar-errors-popover');
 let trigger = null;
 function close(restoreFocus = false) {
   panel.hidden = true;
   if (trigger) {
     trigger.setAttribute('aria-expanded', 'false');
     if (restoreFocus) trigger.focus();
   }
   trigger = null;
 }
 document.querySelectorAll('.similar-errors-badge').forEach(button => {
   button.addEventListener('click', event => {
     event.stopPropagation();
     const same = trigger === button;
     close();
     if (same) return;
     trigger = button;
     button.setAttribute('aria-expanded', 'true');
     const group = groups[button.dataset.group];
     panel.replaceChildren();
     const title = document.createElement('strong');
     title.textContent = 'Similar errors in this report';
     const message = document.createElement('p');
     message.textContent = group.message;
     panel.append(title, message);
     group.tests.forEach(test => {
       if (test.anchor === button.closest('.test').id) return;
       const link = document.createElement('a');
       link.href = '#' + test.anchor;
       link.textContent = test.name;
       link.addEventListener('click', () => {
         close();
         if (location.hash === link.hash) revealTestFromFragment();
       });
       panel.append(link);
     });
     const note = document.createElement('div');
     note.className = 'similar-errors-note';
     note.append('Similar messages may have different causes.', document.createElement('br'), 'Disable: ');
     const command = document.createElement('code');
     command.textContent = '--plus-similar-errors=false';
     note.append(command);
     panel.append(note);
     panel.hidden = false;
     const rect = button.getBoundingClientRect();
     panel.style.left = Math.max(8, Math.min(rect.left, innerWidth - panel.offsetWidth - 8)) + 'px';
     panel.style.top = Math.max(8, Math.min(rect.bottom + 4, innerHeight - panel.offsetHeight - 8)) + 'px';
     panel.querySelector('a')?.focus();
   });
 });
 document.addEventListener('click', event => {
   if (!panel.contains(event.target)) close();
 });
 document.addEventListener('keydown', event => {
   if (event.key === 'Escape' && !panel.hidden) { event.preventDefault(); close(true); }
 });
 document.addEventListener('focusin', event => {
   if (!panel.hidden && !panel.contains(event.target) && event.target !== trigger) close();
 });
 window.addEventListener('hashchange', () => close());
 window.addEventListener('resize', () => close());
})();
</script>
"""
