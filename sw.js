const CACHE = 'rfc-v68';
const STATIC = [
  '/',
  '/index.html',
  '/admin.html',
  '/landing.html',
  '/offline.html',
  '/404.html',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  '/icons/icon-180x180.png',
  '/opensearch.xml',
  '/sitemap.xml',
  '/robots.txt',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(STATIC)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// ── PUSH NOTIFICATION CLICK ──────────────────────────────────────
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || '/';
  if(e.action === 'dismiss') return;
  e.waitUntil(
    clients.matchAll({type:'window', includeUncontrolled:true}).then(list => {
      // Focus existing tab if open
      const existing = list.find(c => c.url.includes('royal-fitness-club') || c.url === url);
      if(existing) return existing.focus();
      // Open new tab
      return clients.openWindow('https://royal-fitness-club-7adc1.web.app');
    })
  );
});

// ── PUSH EVENT (for FCM / server-sent pushes) ────────────────────
self.addEventListener('push', e => {
  if(!e.data) return;
  let data = {};
  try { data = e.data.json(); } catch(_){ data = { title: 'Royal Fitness Club', body: e.data.text() }; }
  e.waitUntil(
    self.registration.showNotification(data.title || 'Royal Fitness Club', {
      body: data.body || '',
      icon: '/icons/icon-192x192.png',
      badge: '/icons/icon-72x72.png',
      vibrate: [200,100,200],
      tag: data.tag || 'rfc-push',
      renotify: true,
      data: { url: data.url || '/' }
    })
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (url.hostname.includes('firebase') || url.hostname.includes('razorpay') ||
      url.hostname.includes('googleapis') || url.hostname.includes('gstatic') ||
      url.hostname.includes('fontawesome') || url.hostname.includes('fonts.g')) return;

  const isNavigation = e.request.mode === 'navigate' || e.request.destination === 'document';

  // ── HTML / navigation → NETWORK-FIRST ──
  // Serving the page cache-first meant returning users kept an old
  // index.html until the cache version changed. Network-first delivers
  // the latest app on every visit, with cache/offline fallback when down.
  // Only cache final, same-origin, non-redirected 200s — a cached redirect
  // replayed for a navigation throws ("redirected response used for navigation").
  const cacheable = res => res && res.ok && !res.redirected &&
    res.type === 'basic' && url.origin === self.location.origin;

  if (isNavigation) {
    e.respondWith(
      fetch(e.request).then(res => {
        if (cacheable(res)) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone)).catch(() => {});
        }
        return res;
      }).catch(() =>
        caches.match(e.request)
          .then(c => c || caches.match('/index.html'))
          .then(c => c || caches.match('/offline.html'))
          .then(c => c || new Response('<h1>Offline</h1>', { status: 503, headers: { 'Content-Type': 'text/html' } }))
      )
    );
    return;
  }

  // ── Static assets → STALE-WHILE-REVALIDATE ──
  // Fast from cache, refreshed in the background so updates self-propagate.
  e.respondWith(
    caches.match(e.request).then(cached => {
      const network = fetch(e.request).then(res => {
        if (cacheable(res)) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone)).catch(() => {});
        }
        return res;
      }).catch(() => cached || new Response('', { status: 503, statusText: 'Offline' }));
      return cached || network;
    })
  );
});
