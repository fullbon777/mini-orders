# Mini Orders - Flask 在庫管理アプリ

## 概要

Flask + SQLAlchemy を使って作成した **注文・在庫管理アプリ** です。
注文の CRUD（作成 / 更新 / 削除 / 閲覧）に加え、在庫の自動連動・補充機能を実装しました。
UI は Bootstrap を使用し、実務で使える業務アプリ風のデザインを目指しています。

---

## 主な機能

- 注文管理
  - 新規注文の作成（在庫チェック付き）
  - 注文一覧・詳細表示
  - 編集・削除
- 在庫管理
  - 在庫数の自動減算（注文数に応じて反映）
  - 商品補充機能
  - 在庫が少ない場合は警告表示（赤バッジ）
- 商品管理
  - 新規商品追加（画像も自動紐付け）
  - 商品ごとの在庫状況を確認可能
- UI / UX
  - Bootstrap によるレスポンシブデザイン
  - 商品画像を一覧に表示
  - 在庫を超える数量を入力すると「保存ボタンが無効化」される

---

## 技術スタック

- Python 3.x
- Flask
- SQLAlchemy
- WTForms
- Bootstrap 5
- SQLite

---

## ディレクトリ構成

このアプリのフォルダ構成は以下の通りです：

```text
mini-orders/
├── app.py              # Flask アプリ本体
├── models.py           # DB モデル定義（Product, Order, Stock など）
├── forms.py            # WTForms のフォーム定義
├── requirements.txt    # 必要ライブラリ一覧
├── templates/          # HTML テンプレート（Jinja2）
│   ├── base.html
│   ├── index.html
│   ├── new_order.html
│   ├── orders.html
│   ├── order_detail.html
│   ├── edit_order.html
│   └── products.html
└── static/             # 静的ファイル（CSS / 画像）
    ├── style.css
    └── images/
        ├── apple.jpg
        ├── orange.jpg
        └── peach.jpg
```
## セットアップ方法

### 1. クローン
```bash
git clone https://github.com/yourname/mini-orders.git
cd mini-orders
```

### 2. 仮想環境と依存関係
```bash
python -m venv venv
source venv/bin/activate   # Windows は venv\Scripts\activate
pip install -r requirements.txt
```

### 3. DB 初期化
```bash
アプリ実行時に instance/app.db が自動生成されます。手動初期化は不要です。
```

### 4. 実行
```bash
flask run
ブラウザで http://127.0.0.1:5000 を開くとアプリが利用できます。
```
