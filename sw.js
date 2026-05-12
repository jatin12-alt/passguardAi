const CACHE_NAME = 'passguardai-pwa-v1';
const PRECACHE = [
  './index.html',
  './password-strength-checker.html',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/passguard-logo.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match('./password-strength-checker.html'))
    );
    return;
  }
  event.respondWith(
    caches.match(request).then((hit) => hit || fetch(request))
  );
});
