/* Front-door visit counter. Same Supabase table as the bookshop sites (book = 'front-door').
   No cookies, no personal data: page, event kind, referrer host, and the time. */
(function () {
  var ENDPOINT = 'https://kvjientfaaewancbmzrr.supabase.co/rest/v1/events';
  var KEY = 'sb_publishable_AISP1QyNwBJJFrKDZNjIAA_zYdxWnFQ';
  var book = 'front-door';
  var ref = '';
  try {
    var q = new URLSearchParams(location.search);
    var src = q.get('src') || q.get('utm_source');
    if (src) { try { sessionStorage.setItem('fd_src', src); } catch (e) {} }
    else { try { src = sessionStorage.getItem('fd_src'); } catch (e) {} }
    ref = src || (document.referrer ? new URL(document.referrer).host : '');
  } catch (e) {}
  function send(kind, extra) {
    var body = JSON.stringify({ book: book, kind: kind, ref: ref, target: extra || null, ua_mobile: /Mobi|Android/i.test(navigator.userAgent) });
    try {
      fetch(ENDPOINT, { method: 'POST', keepalive: true, mode: 'cors',
        headers: { 'Content-Type': 'application/json', 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Prefer': 'return=minimal' },
        body: body });
    } catch (e) {}
  }
  send('view');
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a');
    if (!a || !a.href) return;
    if (a.href.indexOf('amazon.') !== -1) send('amazon', (a.href.match(/\/dp\/([A-Z0-9]{10})/) || [])[1] || null);
    /* clicks through to a shelf site are logged as lookinside with a door: target */
    else if (a.dataset.door) send('lookinside', 'door:' + a.dataset.door);
  }, true);
})();
