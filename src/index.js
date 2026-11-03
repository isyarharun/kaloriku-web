// Worker untuk kaloriku.id
// - HTTP dialihkan permanen (301) ke HTTPS
// - semua host "www." dialihkan permanen (301) ke kaloriku.id, path & query dipertahankan
// - pengecualian: /app-ads.txt disajikan langsung di host apa pun (crawler AdMob
//   memverifikasi host persis seperti yang terdaftar di Play Store, tanpa redirect)
// - selain itu, request dilayani sebagai aset statis dari folder repo
const CANONICAL_HOST = 'kaloriku.id';
const WWW_HOSTS = new Set([
  'www.kaloriku.id',
  'www.kaloriku.com',
  'www.kaloriku-web.isyarharun.workers.dev',
]);
const DIRECT_PATHS = new Set(['/app-ads.txt']);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();

    // Cloudflare mengirim CF-Visitor; kalau ada, itu sumber kebenaran soal skema.
    const visitor = request.headers.get('CF-Visitor') || '';
    const isPlainHttp = visitor ? /"scheme"\s*:\s*"http"/.test(visitor) : url.protocol === 'http:';

    if (DIRECT_PATHS.has(url.pathname)) {
      return env.ASSETS.fetch(request);
    }

    if (isPlainHttp || WWW_HOSTS.has(host)) {
      url.protocol = 'https:';
      url.port = '';
      if (WWW_HOSTS.has(host)) url.hostname = CANONICAL_HOST;
      return Response.redirect(url.toString(), 301);
    }

    return env.ASSETS.fetch(request);
  },
};
