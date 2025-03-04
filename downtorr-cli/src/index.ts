import { WebTorrent } from 'webtorrent-hybrid';

addEventListener('fetch', (event) => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request: Request): Promise<Response> {
  const client = new WebTorrent();
  const magnetURI = 'magnet:?xt=urn:btih:27d9c4b5d676ebdd6d20e2f4f39f067644be0e4f&dn=Ants+On+A+Shrimp+(2016)+%5B720p%5D+%5BWEBRip%5D+%5BYTS.MX%5D&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.tracker.cl%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.mywaifu.best%3A6969%2Fannounce&tr=udp%3A%2F%2Fu4.trakx.crim.ist%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.qu.ax%3A6969%2Fannounce&tr=udp%3A%2F%2Fttk2.nbaonlineservice.com%3A6969%2Fannounce&tr=https%3A%2F%2Ftracker.gcrenwp.top%3A443%2Fannounce&tr=https%3A%2F%2Ftracker.bjut.jp%3A443%2Fannounce&tr=https%3A%2F%2Ftracker.moeking.me%3A443%2Fannounce&tr=http%3A%2F%2Ftracker.renfei.net%3A8080%2Fannounce&tr=http%3A%2F%2Ffleira.no%3A6969%2Fannounce&tr=https%3A%2F%2Ftracker.aburaya.live%3A443%2Fannounce&tr=https%3A%2F%2Ftracker.zhuqiy.top%3A443%2Fannounce&tr=http%3A%2F%2Ftracker.bt4g.com%3A2095%2Fannounce&tr=udp%3A%2F%2Fu6.trakx.crim.ist%3A1337%2Fannounce&tr=udp%3A%2F%2Fec2-18-191-163-220.us-east-2.compute.amazonaws.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fp2p.publictracker.xyz%3A6969%2Fannounce&tr=http%3A%2F%2Fbt.okmp3.ru%3A2710%2Fannounce&tr=udp%3A%2F%2Fismaarino.com%3A1234%2Fannounce&tr=https%3A%2F%2Ftr.zukizuki.org%3A443%2Fannounce&tr=udp%3A%2F%2Ftracker.valete.tf%3A9999%2Fannounce&tr=udp%3A%2F%2Ftracker.gigantino.net%3A6969%2Fannounce&tr=udp%3A%2F%2Fudp.tracker.projectk.org%3A23333%2Fannounce&tr=udp%3A%2F%2Fd40969.acod.regrucolo.ru%3A6969%2Fannounce&tr=udp%3A%2F%2Fmartin-gebhardt.eu%3A25%2Fannounce&tr=http%3A%2F%2Ftracker.ipv6tracker.ru%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.srv00.com%3A6969%2Fannounce&tr=http%3A%2F%2Ftaciturn-shadow.spb.ru%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.netmap.top%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.0x7c0.com%3A6969%2Fannounce&tr=https%3A%2F%2Ftracker.yemekyedim.com%3A443%2Fannounce&tr=udp%3A%2F%2Ftracker.gmi.gd%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.tryhackx.org%3A6969%2Fannounce&tr=http%3A%2F%2F0123456789nonexistent.com%3A80%2Fannounce&tr=udp%3A%2F%2Fretracker.lanta.me%3A2710%2Fannounce&tr=https%3A%2F%2Fapi.ipv4online.uk%3A443%2Fannounce&tr=http%3A%2F%2Ftracker.bittor.pw%3A1337%2Fannounce&tr=http%3A%2F%2Fipv6.rer.lol%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.darkness.services%3A6969%2Fannounce&tr=udp%3A%2F%2Fwww.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fwepzone.net%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.kmzs123.cn%3A17272%2Fannounce&tr=https%3A%2F%2Ftracker.lilithraws.org%3A443%2Fannounce&tr=http%3A%2F%2Ftracker-zhuqiy.dgj055.icu%3A80%2Fannounce&tr=udp%3A%2F%2Ft.overflow.biz%3A6969%2Fannounce&tr=udp%3A%2F%2Fopentracker.io%3A6969%2Fannounce&tr=udp%3A%2F%2Fevan.im%3A6969%2Fannounce&tr=https%3A%2F%2Fretracker.x2k.ru%3A443%2Fannounce&tr=udp%3A%2F%2Fbt.ktrackers.com%3A6666%2Fannounce&tr=udp%3A%2F%2Ftracker.fnix.net%3A6969%2Fannounce&tr=udp%3A%2F%2Ftr3.ysagin.top%3A2715%2Fannounce&tr=udp%3A%2F%2Ftracker.filemail.com%3A6969%2Fannounce&tr=http%3A%2F%2Fbt1.archive.org%3A6969%2Fannounce&tr=http%3A%2F%2Fbt2.archive.org%3A6969%2Fannounce';

  return new Promise((resolve, reject) => {
    client.add(magnetURI, (torrent) => {
      torrent.files[0].getBuffer((err, buffer) => {
        if (err) {
          reject(new Response('Erro ao obter o buffer do torrent', { status: 500 }));
        } else {
          resolve(new Response(buffer, { status: 200 }));
        }
      });
    });
  });
}