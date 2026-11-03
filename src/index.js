// Worker untuk kaloriku.id
// - HTTP dialihkan permanen (301) ke HTTPS
// - semua host "www." dialihkan permanen (301) ke kaloriku.id, path & query dipertahankan
// - selain itu, request dilayani sebagai aset statis dari folder repo
const CANONICAL_HOST = 'kaloriku.id';
const WWW_HOSTS = new Set([
  'www.kaloriku.id',
  'www.kaloriku.com',
  'www.kaloriku-web.isyarharun.workers.dev',
]);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();

    // Cloudflare mengirim CF-Visitor; kalau ada, itu sumber kebenaran soal skema.
    const visitor = request.headers.get('CF-Visitor') || '';
    const isPlainHttp = visitor ? /"scheme"\s*:\s*"http"/.test(visitor) : url.protocol === 'http:';

    if (isPlainHttp || WWW_HOSTS.has(host)) {
      url.protocol = 'https:';
      url.port = '';
      if (WWW_HOSTS.has(host)) url.hostname = CANONICAL_HOST;
      return Response.redirect(url.toString(), 301);
    }

    return env.ASSETS.fetch(request);
  },
};
