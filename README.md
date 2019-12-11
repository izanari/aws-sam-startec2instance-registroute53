# aws-sam-startec2instance-registroute53
EC２インスタンスが起動した時に、Route53のAレコードを更新するlambda関数です
## 解決する課題
EC2インスタンスは起動する度のパブリックIPが異なります。そのため、EC2インスタンス上のウェブサーバにアクセスするURLが、起動する度に変わってしまいます。Elastic IPを使えば解決できますが、EC2インスタンス停止時には料金が発生します。よって、開発環境のように、深夜・土日にインスタンスを停止する場合は無駄な料金が発生します。

無駄な料金を発生させないために、パブリックIPアドレスをRoute53に登録し、Host名でアクセスさせます。しかし、起動する度にIPアドレスが変わってしまうため、その都度Route53への変更作業が発生します。

このLambda関数は、その変更作業を自動化するための関数です。

## 前提・事前作業
- EC２インスタンスには、パブリックIPが付与されている必要があります
- Elastic IPは不要です
- EC2インスタンスのタグに２個のタグが付与しておく必要があります
 
    |キー|バリュー|
    |--|--|
    |DNSname|hogehoge.web-integration.pro|
    |HostZoneID|AAAAAAAAAAA|

- `HostZoneID`に`DNSname`を事前に登録しておく必要があります。
  - これは、EC2のタグ設定でAレコードが乱立するのを防止することが目的です。初期利用時には、Route53の管理者へ、DNSNameと同じレコードを登録してもらってください
## 利用サービス
- CloudWatch Event
- EC2
- Lambda
- Route 53
## デプロイ方法
- デプロイはsamを使います
  - `sam deploy`でパラメータをどうするか聞かれます。
    - `IDs`には、Route53に登録したいEC2インスタンスのIDをつけてください。複数登録は可能です
  - 一度デプロイすると、`samconfig.toml`が生成されます。２回目以降は、`sam deploy`だけで実行してください
  ```
  sam package --s3-bucket bucketname
  sam deploy --guided
  ```

## 動作環境
- 下記環境で動作を確認しています
  - SAM CLI, version 0.37.0
  - boto3 1.10.35 
  - botocore 1.13.35 