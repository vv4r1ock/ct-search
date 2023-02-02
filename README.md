# ct-search
CT日志子域收集工具

## CT是什么?
目前全球有数百家CA机构(证书颁发机构)，每个CA都可以为域名颁发受信任的SSL证书。

如果CA机构未按照验证机制误签SSL证书，或CA系统被黑而签发恶意证书或伪造证书，导致这些非法签发的SSL证书流入网络，则会威胁互联网的安全。为了监督、检测、发现这些恶意或误签的数字证书，证书透明度(Certificate Transparency)应运而生。

CT机制要求当CA颁发证书时，它们也必须将证书提交到至少两个公共的CT日志，CT将公开所有证书以供人们审核。

域名的所有者可以通过CT日志监控谁在为他们拥有的域创建证书;浏览器也可以通过CT日志验证给定域的证书是否在公共日志记录中;好奇心旺盛的"路人"也可以根据CT日志来发现某个域名所存在的子域，甚至根据生成时间和id来找到同一个申请者通过工具批量化申请的其他域名......

## 食用方法

```console
usage: ct-exposer.py [-h] -d DOMAIN [-u] [-m]

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        domain to query for CT logs, ex: domain.com
  -u, --urls            ouput results with https:// urls for domains that
                        resolve, one per line.
  -m, --masscan         output resolved IP address, one per line. Useful for
                        masscan IP list import "-iL" format.

```
