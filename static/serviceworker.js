const CACHE_NAME = 'tms-gaval-cache-v1';
const URLS_TO_CACHE = [
    '/',
    '/static/css/styles.css', // Suponiendo que tienes un CSS principal
    '/static/js/main.js',     // Suponiendo que tienes un JS principal
    '/static/images/logo.png', // Suponiendo que tienes un logo
    '/offline/', // Una página offline personalizada
];

// Instalación del Service Worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Cache abierto');
                return cache.addAll(URLS_TO_CACHE);
            })
    );
});

// Estrategia de Cache: Network First, then Cache
self.addEventListener('fetch', event => {
    event.respondWith(
        fetch(event.request)
            .then(response => {
                // Si la respuesta de la red es válida, la cacheamos y la devolvemos
                if (response && response.status === 200) {
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME)
                        .then(cache => {
                            cache.put(event.request, responseToCache);
                        });
                }
                return response;
            })
            .catch(() => {
                // Si la red falla, intentamos servir desde el caché
                return caches.match(event.request)
                    .then(response => {
                        if (response) {
                            return response;
                        }
                        // Si no está en caché, devolvemos una página offline genérica
                        return caches.match('/offline/');
                    });
            })
    );
});

// Activación del Service Worker y limpieza de cachés antiguas
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
