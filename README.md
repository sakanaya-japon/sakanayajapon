# SAKANAYA JAPON — 個人向けウェブサイト

カンボジア・プノンペンの魚屋 SAKANAYA JAPON の、個人のお客様向けサイトです。

- 公開URL: https://sakanaya-japon.github.io/sakanayajapon/
  （2026-09 に個人アカウント `Sasuraimitsu` から Organization へ移管済み。旧URL `sasuraimitsu.github.io/sakanayajapon/` は移管により無効。移転案内は docs/github-inventory.md §3 手順3）
- ホスティング: GitHub Pages（`main` ブランチ / ルート直下）
- 法人向け商品カタログは別リポジトリ: https://github.com/sakanaya-japon/sakanaya-productlist

---

## 1. ファイル構成

| ファイル | 役割 |
|---|---|
| `index.html` | トップ。写真全面のヒーローに、ロゴ・店名・4項目のメニュー・Telegram/Facebook ボタン |
| `business/index.html` | 法人向け入口（商品カタログ・取引の流れ・問い合わせ） |
| `assets/css/` | `common.css`（共通）/ `business.css`（法人ページ） |
| `assets/js/` | `site-info.js`（営業時間・窓口の情報源）/ `common.js`（日英切替） |
| `menu.html` | メニュー画像1枚 + 注文ボタン |
| `howto.html` | LINE での注文方法（動画 `howtouse.mp4`） |
| `faq.html` | よくあるご質問 |
| `q&a.html` | **旧URLからの案内ページ**（`faq.html` へ自動転送。中身はない） |
| `aboutus.html` | 店舗情報・営業時間・アクセス |
| `assets/images/logo.jpg` | ロゴ（favicon / OGP 兼用） |
| `assets/images/fish-photo.jpg` | トップ背景スライドショー用 |
| `assets/images/english-menu20260207.jpg` | `menu.html` に表示するメニュー画像 |
| `howtouse.mp4` | 注文方法の説明動画（約2.8MB。ルート直下のまま） |
| `docs/` | 運用ドキュメント（サイトとしては公開されない） |

### 注意点

- `index.html` の背景スライドショーは `assets/images/` の `fish-photo.jpg` / `sashimi.jpg` / `event.jpg` を
  読もうとしますが、**現在リポジトリにあるのは `fish-photo.jpg` だけ**です。
  存在しない画像は自動でスキップされる作りなので表示は壊れませんが、実質1枚のみ表示されています。
  スライドショーにしたい場合は残り2枚を `assets/images/` に追加してください。
- ~~`q&a.html` はファイル名に `&` を含むため URL が `q%26a.html` になる~~
  → **2026-09-22 に `faq.html` へ改名済み**。旧URL `q%26a.html` には案内ページを置いて
  `faq.html` へ転送しています（GitHub Pages はサーバ側リダイレクトができないため meta refresh）。
  **案内ページは最低3か月は消さないでください**（顧客のブックマーク・外部リンクの切替期間）。
- 営業時間・住所・電話・窓口URLは `assets/js/site-info.js` が唯一の情報源です。
  ページ側には `data-info` / `data-info-href` だけを書き、値を直接書かないでください。

---

## 2. 更新のしかた（ブランチ運用ルール）

**ページの種類によって手順を変えます。** すべてに PR を要求すると緊急修正が回らず、
逆にすべて `main` 直編集にすると価格ミスがそのまま本番に出てしまうためです。

### A. `main` を直接編集してよいもの

- 文言の修正、誤字脱字
- 営業時間・お知らせの更新
- 画像の差し替え

GitHub のウェブ画面から直接編集してコミットして構いません。スマホからでも直せます。

### B. ブランチ + Pull Request が必須のもの

- **価格が表示される箇所**（法人向けページ、商品リスト）
- 注文フロー・注文先URLの変更
- `assets/` 配下の共通CSS / JS（全ページに影響するため）
- ページの新規追加・削除・改名

```bash
# 作業ブランチを切る
git checkout main
git pull origin main
git checkout -b feature/business-page

# 編集してコミット
git add .
git commit -m "法人向けページに加工サービスの説明を追加"
git push -u origin feature/business-page

# GitHub 上で Pull Request を作成 → 内容を確認 → merge
```

### 本番反映前のプレビュー

PR を作っても GitHub Pages にはプレビューが出ません。確認方法は2つです。

1. ローカルで確認（推奨）
   ```bash
   python3 -m http.server 8000
   # ブラウザで http://localhost:8000/ を開く
   ```
2. GitHub のファイル画面で `Preview` タブを使う（CSS は反映されないため簡易確認のみ）

---

## 3. 再編計画

詳細は `docs/` を参照してください。

| ドキュメント | 内容 |
|---|---|
| `docs/github-inventory.md` | 全リポジトリの棚卸し、Organization への移管手順 |
| `docs/contact-points.md` | 営業時間・注文窓口の食い違いと統一案 |
| `docs/punch-migration.md` | `sakanaya-punch` の Organization 移管手順（先行実施） |
| `docs/apply-repo-metadata.py` | 全リポジトリの description / topics を一括設定するスクリプト |

### Phase 1（✅ 完了 / 2026-09-14）

個人向け / 法人向けの2導線を持つトップページを追加しました。

**トップページのデザイン（2026-09-14 確定）**

```
┌──────────────────────────────────────────────┐
│ [ロゴ] SAKANAYA JAPON     日本語|EN  法人のお客様 │ ← 白いヘッダー
├──────────────────────────────────────────────┤
│              （魚の写真を全面に・暗め）            │
│                   [ロゴ]                       │
│               SAKANAYA JAPON                   │
│         海のある日常を、カンボジアの食卓に。        │
│                                                │
│     (⌂) メニュー          (▤) ご注文方法          │
│     (?) よくあるご質問     (i) 店舗について        │
│                                                │
│  [✈ Telegram でチャット] [👍 Facebook でいいね！]  │
└──────────────────────────────────────────────┘
```

| ファイル | 内容 |
|---|---|
| `index.html` | 上記のトップ。CSS はインライン。写真は `fish-photo.jpg` を CSS で直接敷き、2枚目以降を JS でフェード |
| `business/index.html` | 法人向け入口。カタログ導線・加工/配送/解体ショー・注文の流れ・問い合わせ |
| `assets/css/common.css` | 法人ページ用の共通トークン・ヘッダー・フッター・ボタン |
| `assets/css/business.css` | 法人ページ専用 |
| `assets/js/site-info.js` | 営業時間・窓口URLの単一情報源（トップ・法人ページ共通） |
| `assets/js/common.js` | 日英切替、`site-info.js` の値の流し込み（トップ・法人ページ共通） |

トップの調整箇所（`index.html` の `<style>` 内）:

- 写真の暗さ: `.hero::before` の `linear-gradient(... 0.55 / 0.45 / 0.72 ...)`。数値を上げるほど暗い
- 写真の差し替え: `fish-photo.jpg` を置き換える。`sashimi.jpg` / `event.jpg` を追加すると6秒ごとに切り替わる
- 文言: 各要素の `data-ja` / `data-en` 属性

**当初計画からの変更点:** `business/index.html` に業務用商品一覧を新規実装する予定でしたが、
同等以上のものが `sakanaya-japon/sakanaya-productlist` として**既に本番稼働中**です
（GAS 連携・顧客登録・在庫表示・Excel出力・商品画像167枚）。
作り直すと価格マスターが二重管理になるため、**法人向けページからはカタログへリンクする方針に変更**しました。
根拠は `docs/github-inventory.md` の §2 を参照してください。

Phase 1 の時点では既存ページ（`menu.html` / `howto.html` / `q&a.html` / `aboutus.html`）は
変更していませんでした（ヘッダー・フッターの統一は Phase 2 で実施済み）。
旧トップ（磨りガラスのリンク集）は廃止しました。

#### 実装上の決めごと

- **日英切替**: `data-ja` / `data-en` 属性でテキストを差し替え、リンクを含むブロックは
  `data-lang="ja"` / `data-lang="en"` で出し分ける。選択は `localStorage` に保存（例外は握りつぶす）
- **JS が動かない場合**: HTML に日本語の既定値を書いてあるため、そのまま日本語で表示される。
  トップの背景写真も CSS で直接指定しているので JS なしで表示される。
  CSS は `display: block` で指定しており、`display: revert` 非対応ブラウザでも本文が消えない
- **アイコンは自前の SVG**。外部の Font Awesome に依存しない
- **窓口URLの直書き禁止**: 新規ページでは `data-info-href="order.xxx"` を使い、
  実体は `assets/js/site-info.js` にだけ書く

#### 動作確認済みの項目

- `index.html` / `business/index.html` の HTML タグ構造
- 内部リンクがすべて実在
- `data-info` 12件がすべて `SITE_INFO` に定義済み
- `common.js` / `site-info.js` の構文
- ローカル配信で全アセットが 200 を返すこと

### Phase 2（進行中）

- ✅ **既存4ページのヘッダー・フッターを新トップと統一**（2026-09-14。下記参照）
- ✅ **既存4ページにも `site-info.js` を適用し、営業時間・窓口URLの直書きをなくした**（2026-09-22）
- ✅ **`q&a.html` → `faq.html` へ改名**（旧URLに案内ページを設置。2026-09-22）
- ✅ **画像を `assets/images/` へ整理**（2026-09-22）
- ⬜ 法人向け「加工」「配送」「新規取引」の詳細ページ追加（**内容の確定待ち**）

#### 単一情報源化・改名・画像整理（✅ 2026-09-22）

**`site-info.js` への一本化**

`menu` / `howto` / `faq` / `aboutus` の営業時間・締切・住所・電話・Email・窓口URLを
すべて `data-info` / `data-info-href` に置き換えました（全38箇所）。
値を変えるときは `assets/js/site-info.js` **だけ**を書き換えます。

- HTML には日本語（英語ブロックには英語）の既定値を残してあるので、
  JS が読めなくても正しい値が表示されます
- 外部リンクの `target="_blank"` と `rel="noopener noreferrer"` は `common.js` が自動で付けます
- **遷移先は一切変えていません。** 既存のリンクを「同じ宛先を指すキー」に機械的に置き換えただけです
  （どの窓口に着地させるかは事業判断のため。未解決の不整合は下記「申し送り」を参照）

**`faq.html` への改名**

`q&a.html` は `&` のせいで URL が `q%26a.html` になり、共有時に壊れやすい名前でした。
`faq.html` に改名し、旧URLには案内ページ（3秒後に自動転送・`noindex`・`canonical` 付き）を置いています。

**画像の整理**

`logo.jpg` / `fish-photo.jpg` / `english-menu20260207.jpg` を `assets/images/` へ移動し、
参照22箇所（favicon・OGP の絶対URL・CSS背景・スライドショーのJS配列）を更新しました。
`howtouse.mp4` は画像ではないためルート直下に残しています。

> ⚠️ **OGP画像のURLが変わりました。** 既に Facebook / LINE で共有済みの投稿は、
> キャッシュされた古いURL（`/sakanayajapon/logo.jpg` 等）を参照するため
> プレビュー画像が表示されなくなることがあります。リンク自体は正常に開きます。
> 気になる場合は Facebook のシェアデバッガーでキャッシュを更新してください。

#### 申し送り（要判断）

`site-info.js` 化の作業中に見つけた、**表示内容の不整合**です。直すには事業判断が要るため手を付けていません。

| 箇所 | 現状 | 論点 |
|---|---|---|
| `faq.html` 英語版「How can I place an order?」 | Telegram チャンネル（`t.me/fishstoreJapon`）へ誘導 | 日本語版は LINE 注文システム。`docs/contact-points.md` の統一案では個人の主窓口は LINE Mini App |
| `aboutus.html` 英語版の CTA ボタン | 同上（Telegram チャンネル） | 日本語版は LINE Mini App。英語話者だけ別の窓口に着地している |
| 各ページのフッターの住所 | 短縮形を直書き（5ページ） | `site-info.js` の `company.address` は完全形。フッターを長くしてよいか |

#### ヘッダー・フッターの統一（✅ 2026-09-14）

`menu.html` / `howto.html` / `faq.html`（当時は `q&a.html`）/ `aboutus.html` の4ページが
`assets/css/common.css` と `common.js` を読み込むようになり、
ヘッダー・フッター・言語切替がトップページと同じものになりました。

| 変更前 | 変更後 |
|---|---|
| ページごとに `<nav>` を直書き（`position: fixed` + `body { padding-top }`） | 共通の `.site-header`（白帯60px・丸ロゴ・`position: sticky`） |
| フッターなし | 共通の `.site-footer`（全ページへのリンク + 住所） |
| ページごとに `switchLang()` を実装し、本文の上に切替ボタンを置いていた | ヘッダーの `.lang-toggle` に統一。切替は `common.js` が担当し、選択は `localStorage` に保存される |
| ヘッダーから法人向けページへ行けない | `.biz-link`（法人のお客様）をトップと同じ位置に追加 |

実装メモ:

- `common.css` は各ページの `<style>` **より前**に読み込む。
  同じ詳細度ならページ側が勝つので、ページ固有の見た目はそのまま残せる
- ヘッダーの値（高さ60px・ロゴ40px丸・店名19px/800・`--navy-logo`）は
  トップページ `index.html` の `<style>` と**同じ値を二重に持っている**。
  片方だけ直すと見た目がずれるため、変更時は必ず両方を直すこと
- 言語別の本文は `data-lang="ja"` / `data-lang="en"` に統一。
  `faq.html` の検索（`searchQA`）はページ固有のためページ側に残してある
- `body` を縦 flex にし、`.site-footer` に `margin-top: auto` を付けた。
  内容が短いページでもフッターが画面下端まで下がる
- 右下の追従ボタンがフッターのリンクに被らないよう、
  4ページのフッターには `.has-float`（下側に110pxの逃げ）を付けている
- 読み込まれていない Font Awesome（`<i class="fa-brands">`）に依存していた
  Telegram アイコンを絵文字に置き換えた（アイコンが表示されていなかったため）

ヘッダー・フッターの幅はトップに合わせて 1100px（`--maxw-wide`）です。
`business/index.html` は本文が 960px（`--maxw`）のままなので、
ヘッダーの左右が本文よりわずかに外側に出ます。気になる場合は本文幅を揃えてください。

#### 動作確認済みの項目（Phase 2）

- 6ページすべての HTML タグ構造（開始・終了タグの対応）
- 内部リンクとアセットがすべて実在、ローカル配信で全て 200
- ヘッダーの実測値が4ページで一致（高さ60px / ロゴ40px丸 / 店名19px・weight800 / `position: sticky`）
- 言語切替が日英どちらでも正しく動作（`aria-pressed`・本文の出し分け・`localStorage` への保存）
- 内容が短いページでもフッターが画面下端に接すること

### 着手前に確定が必要な事項

~~`docs/contact-points.md` §4 の6項目~~ → **2026-09-14 に全6項目が確定し、ページへの反映も完了しました。**

確定した内容（詳細は `docs/contact-points.md` §4）:

| 項目 | 確定値 |
|---|---|
| 営業時間 | 毎日 10:00〜19:30（国民の休日を除く）。定休日なし |
| Facebook | `facebook.com/fishstorejapan` に統一 |
| LINE ID | `@sakanayajapan` のまま（変更すると友だち追加リンクが切れるため） |
| LINE 公式アカウント | 個人のお客様向け問い合わせ窓口として残す |
| 法人向け Telegram | 旧グループは廃止。現行は `@sakanayaorder` |

Phase 1 に着手できる状態です。
