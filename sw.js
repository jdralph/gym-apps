/* Offline cache for the coach tools.
   Bump CACHE when you edit any of the files below, or phones will keep
   serving the old copy. */
const CACHE = 'coach-tools-v5';

const CORE = [
  'index.html',
  'timer.html',
  'colour.html',
  'manifest-launcher.webmanifest',
  'manifest-timer.webmanifest',
  'manifest-colour.webmanifest',
  'icon-timer-180.png',
  'icon-timer-192.png',
  'icon-timer-512.png',
  'icon-colour-180.png',
  'icon-colour-192.png',
  'icon-colour-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.all(CORE.map(u => c.add(u).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;

  // Cache first: these apps never need fresh data, and a gym has no signal.
  e.respondWith(
    caches.match(req, { ignoreSearch: true }).then(hit => {
      if (hit) return hit;
      return fetch(req).then(res => {
        // Stash same-origin files and the web fonts on first successful load.
        const url = new URL(req.url);
        const keep = url.origin === location.origin ||
                     /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
        if (keep && (res.ok || res.type === 'opaque')) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
        }
        return res;
      }).catch(() => caches.match('index.html'));
    })
  );
});
