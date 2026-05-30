const CACHE_NAME = 'rice-box-online-v8';
const BASE_PATH = new URL(self.registration.scope).pathname;
const ASSETS = [
  BASE_PATH,
  `${BASE_PATH}index.html`,
  `${BASE_PATH}manifest.json`,
  `${BASE_PATH}assets/hero-rice-box.png`,
  `${BASE_PATH}assets/menu-krapao.png`,
  `${BASE_PATH}assets/menu-oyster-pork.png`,
  `${BASE_PATH}assets/menu-fried-rice.png`,
  `${BASE_PATH}assets/menu-garlic-pork.png`,
  `${BASE_PATH}assets/app-screenshot-mobile.png`,
  `${BASE_PATH}assets/app-screenshot-desktop.png`,
  `${BASE_PATH}icons/apple-touch-icon.png`,
  `${BASE_PATH}icons/icon-72.png`,
  `${BASE_PATH}icons/icon-96.png`,
  `${BASE_PATH}icons/icon-128.png`,
  `${BASE_PATH}icons/icon-144.png`,
  `${BASE_PATH}icons/icon-152.png`,
  `${BASE_PATH}icons/icon-180.png`,
  `${BASE_PATH}icons/icon-192.png`,
  `${BASE_PATH}icons/icon-384.png`,
  `${BASE_PATH}icons/icon-512.png`,
  `${BASE_PATH}icons/icon-maskable-512.png`,
  `${BASE_PATH}docs/business-plan.md`,
  `${BASE_PATH}docs/ops-manual.md`,
  `${BASE_PATH}docs/costing-forecast.md`
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.map((key) => (key === CACHE_NAME ? null : caches.delete(key))))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request)
        .then((response) => {
          const copy = response.clone();
          if (response.ok && event.request.url.startsWith(self.location.origin)) {
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          }
          return response;
        })
        .catch(() => {
          if (event.request.mode === 'navigate') {
            return caches.match(`${BASE_PATH}index.html`);
          }
          return undefined;
        });
    })
  );
});
