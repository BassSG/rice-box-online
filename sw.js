const CACHE_NAME = 'rice-box-v1';
const ASSETS = [
  '/rice-box-online/',
  '/rice-box-online/index.html',
  '/rice-box-online/manifest.json',
  '/rice-box-online/icons/icon-192.png',
  '/rice-box-online/icons/icon-512.png'
];

// ติดตั้ง Service Worker และทำการแคชข้อมูล
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Caching essential assets...');
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

// เปิดใช้งาน Service Worker และลบแคชเก่า (ถ้ามี)
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('Deleting old cache:', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// ดึงข้อมูลและให้บริการแบบ Offline
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).catch(() => {
        // หากเน็ตล่มและไม่มีข้อมูลในแคช
        if (event.request.mode === 'navigate') {
          return caches.match('/rice-box-online/index.html');
        }
      });
    })
  );
});
