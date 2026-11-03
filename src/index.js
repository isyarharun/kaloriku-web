// Worker untuk kaloriku.id
// - www.kaloriku.id dialihkan permanen (301) ke apex kaloriku.id
// - selain itu, semua request dilayani sebagai aset statis dari folder repo
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.hostname === 'www.kaloriku.id' || url.hostname === 'www.kaloriku-web.isyarharun.workers.dev') {
      url.protocol = 'https:';
      url.hostname = 'kaloriku.id';
      url.port = '';
      return Response.redirect(url.toString(), 301);
    }

    return env.ASSETS.fetch(request);
  },
};
