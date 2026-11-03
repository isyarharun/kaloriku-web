// Worker untuk kaloriku.id
// - HTTP dialihkan permanen (301) ke HTTPS
// - www.kaloriku.id dialihkan permanen (301) ke apex kaloriku.id, path & query dipertahankan
// - selain itu, semua request dilayani sebagai aset statis dari folder repo
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Cloudflare mengirim CF-Visitor; kalau ada, itu sumber kebenaran soal skema.
    const visitor = request.headers.get('CF-Visitor') || '';
    const isPlainHttp = visitor ? /"scheme"\s*:\s*"http"/.test(visitor) : url.protocol === 'http:';

    if (isPlainHttp || url.hostname === 'www.kaloriku.id') {
      url.protocol = 'https:';
      url.hostname = 'kaloriku.id';
      url.port = '';
      return Response.redirect(url.toString(), 301);
    }

    return env.ASSETS.fetch(request);
  },
};
