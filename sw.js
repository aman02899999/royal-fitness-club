const CACHE = 'rfc-v52';
const STATIC = [
  '/',
  '/index.html',
  '/admin.html',
  '/404.html',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  '/icons/icon-180x180.png',
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
  // Only intercept same-origin GET requests; skip Firebase/Razorpay API calls
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (url.hostname.includes('firebase') || url.hostname.includes('razorpay') ||
      url.hostname.includes('googleapis') || url.hostname.includes('gstatic')) return;

  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        // Cache same-origin HTML/JS/CSS/images
        if (res.ok && url.origin === self.location.origin) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      }).catch(() => cached);
    })
  );
});
