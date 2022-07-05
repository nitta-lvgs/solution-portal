# 概要
ソリューション開発部のポータルサイトのLaravelフレームワーク

## document
- [環境構築エビデンス](https://docs.google.com/spreadsheets/d/1h-S6wxaZ6ifdDnD2-nwoaFXaL1eyZiEvUwilejhKw-8/edit#gid=0)

## ローカル環境構築手順
### 環境情報
- PHP 8.1.7 
- Laravel Framework 9.19.0
- MySQL 8.0.29 
- React 18.2.0
- Vite 2.9.13

## ローカル環境作成
1. docker環境の準備(Docker for macをインストール)
2. gitリポジトリをローカルに落とす
3. alias設定 "alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'"
4. コンテナ起動 "sail up -d"

### sailコマンド
- [コマンド一覧](https://zenn.dev/t_arase/articles/28268f308c6dbd)
- コンテナ起動　"sail up -d"
- コンテナ停止　"sail down"
- キャッシュが残ってると@viteのディレクティブが動作しない　"sail php artisan view:clear"
- ビルド:　"sail npm run dev"
- HMRを行わずに静的ビルド:　"sail npm run build"
```
dev_server.enabledをfalse
ping_before_using_manifestをtrue
のどちらかの対応で、localhostで確認できる
```
