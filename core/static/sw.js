const cacheName = 'atlas-v1';
const staticAssets = [
    '/',
    '/static/manifest.json',
    // Yahan apne CSS aur images ke paths bhi add kar sakti hain
];

self.addEventListener('install', async e => {
    const cache = await caches.open(cacheName);
    await cache.addAll(staticAssets);
});

self.addEventListener('fetch', e => {
    e.respondWith(
        fetch(e.request).catch(() => caches.match(e.request))
    );
});