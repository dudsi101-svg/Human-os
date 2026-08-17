/* Human OS — service worker (offline-first dla aplikacji lokalnej).
   Wersję podbijaj przy każdej zmianie plików powłoki — stary cache jest
   sprzątany w `activate`. Brak sieci nigdy nie blokuje aplikacji: całość
   działa z cache; sieć służy tylko do cichej aktualizacji powłoki. */
const CACHE = "human-os-v1";
const SHELL = [
  "./human_os_app.html",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-512.png",
  "./icons/icon-180.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* cache-first + ciche odświeżenie w tle (stale-while-revalidate),
   wyłącznie GET w obrębie własnego origin — żadnych żądań na zewnątrz */
self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  e.respondWith(
    caches.match(req, { ignoreSearch: true }).then((hit) => {
      const refresh = fetch(req)
        .then((res) => {
          if (res && res.ok) caches.open(CACHE).then((c) => c.put(req, res.clone()));
          return res;
        })
        .catch(() => hit);
      return hit || refresh;
    })
  );
});
