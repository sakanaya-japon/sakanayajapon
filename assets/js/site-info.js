/* ==========================================================================
   site-info.js — 営業時間・窓口URLの唯一の情報源
   変更するときはこのファイルだけを書き換える。各ページに直接URLを書かないこと。
   （既存4ページの移行は Phase 2。詳細は docs/contact-points.md）
   ========================================================================== */

const SITE_INFO = {
  // ── 営業時間（2026-09-13 確定。2026-11-07 Telegram 注文 Bot 側をこの値に合わせた） ──
  hours: {
    ja: '毎日 10:00〜19:30（国民の休日を除く）',
    en: 'Daily 10:00am–7:30pm (Closed on public holidays)',
  },
  // ── 注文の締切（2026-11-07 Telegram 注文 Bot の規則に統一） ──
  orderDeadline: {
    ja: 'ご希望の受け取り・配送時間の1時間前まで（手巻き寿司セットは3時間前まで）',
    en: 'Up to 1 hour before your delivery or pick-up time (3 hours for the hand-roll sushi set)',
  },

  // ── 店舗・会社情報 ──
  company: {
    name: 'SAKANAYA JAPON',
    established: { ja: '2024年12月19日', en: 'December 19, 2024' },
    address: {
      ja: '#72BE0, Street 174, Phum 11, Sangkat Phsar Thmey 3, Khan Daun Penh, Phnom Penh, Cambodia',
      en: '#72BE0, Street 174, Phum 11, Sangkat Phsar Thmey 3, Khan Daun Penh, Phnom Penh, Cambodia',
    },
    phone: '+855 16 881 370',
    phoneLocal: '016-881-370',
    email: 'fishstorejapan@gmail.com',
  },

  // ── 店頭受け取り（2026-11-07 追加。場所は company.address と同じ） ──
  pickup: {
    mapUrl: 'https://maps.app.goo.gl/yHL1XbLFuXfqtZuaA',
  },

  // ── 注文・問い合わせ窓口（2026-09-14 確定 → 2026-11-07 個人向け Telegram を整理） ──
  //    個人向けは「注文」と「相談」を分ける。日本語版は LINE が主、英語版は Telegram が主。
  order: {
    lineMiniApp:      'https://miniapp.line.me/2006469733-lgZj9vJ4', // 個人向け 注文（LINE 注文画面）
    lineOfficial:     'https://line.me/R/ti/p/@sakanayajapan',       // 個人向け 相談（LINE 公式アカウント）
    telegramOrderApp: 'https://t.me/sakanaya_order_bot/menu',        // 個人向け 注文（Telegram 注文画面 = @sakanaya_order_bot の Mini App）
    telegramShop:     'https://t.me/sakanayajapon',                  // 個人向け 相談（店アカウント。Telegram Business）
    telegramBot:      'https://t.me/sakanaya_bot',                   // 法人向け 注文ボット
    telegramBiz:      'https://t.me/sakanayaorder',                  // 法人向け 問い合わせ
    // 旧 個人向けグループ（telegramHome: https://t.me/+UZAm7-eLzD0yZTA1）は 2026-11-07 にサイトから外した。
    // グループ自体は存続。参照を復活させる場合はキーを戻し、docs/contact-points.md §5 を更新すること。
  },

  // ── SNS ──
  social: {
    facebook: 'https://www.facebook.com/fishstorejapan',
    telegramChannel: 'https://t.me/fishstoreJapon',
  },

  // ── 法人向け商品カタログ（sakanaya-japon Org で稼働中の本番） ──
  catalogUrl: 'https://sakanaya-japon.github.io/sakanaya-productlist/',
};
