# uchi-notify-weather-slack-bot

## Description

毎朝9時に大阪市の天気や気温、日の出・日の入時刻をSlackにお知らせするボットのバックエンドロジックです。

気象情報の取得には [Open-Meteo.com](https://open-meteo.com/) を利用しています。

このアプリケーションはAzure Functionsにデプロイすることを想定しています。

## Requirement

- Python 3.11.2
- Visual Studio Code

その他、以下に記載の「前提条件」をセットアップする必要があります。

[Visual Studio Code を使用して Azure Functions を開発する | Microsoft Learn](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-develop-vs-code?tabs=node-v3%2Cpython-v2%2Cisolated-process&pivots=programming-language-python)

## Usage

最初にPythonの仮想環境を作成します。

```
PS> python -m venv .venv
PS> .\.venv\Scripts\activate
(.venv) PS> pip install -r .\requirements.txt
```

以下を参考にして通知したい通知先のWebhook URLを取得します。

[Slack：Webhook URL取得してSlackに通知する](https://zenn.dev/hotaka_noda/articles/4a6f0ccee73a18)

``local.settings.json`` およびAzure Functionsの「構成」でアプリケーション設定に ``SlackWebhookUrl`` という変数名でWebhook URLを設定します。

以降は以下などを参考にしてロジック修正、ローカルデバッグ、デプロイなどを行ってください。

[Visual Studio Code を使用して Python 関数を作成する - Azure Functions | Microsoft Learn](https://learn.microsoft.com/ja-jp/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-decorators)

タイマー関数の手動実行については以下に記載があります。

[HTTP によってトリガーされない Azure Functions を手動で実行する | Microsoft Learn](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-manually-run-non-http)

## Install

このリポジトリをフォークしてクローンします。

```
$ git clone git@github.com:yourname/uchi-notify-weather-slack-bot.git
```

## Contribution

1. このリポジトリをフォークする
2. 変更を加える
3. 変更をコミットする
4. ブランチにプッシュする
5. プルリクエストを作成する

## License

No License

## Author

[minato](https://blog.minatoproject.com/)
