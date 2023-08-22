
脚本主要用于js文件敏感信息内容提取工作

## 使用方法：

### 1、配置环境
```
pip3 install argparse
```
### 2、使用方法
```
python3 js_search.py -h
```
<img width="909" alt="image" src="https://github.com/bingtangbanli/jsfinderPro/assets/77956516/9e7b9687-abb3-4157-801b-1af89c9e05d9">

```
使用示例：
Usage:python3 jsfinderPro.py -u https://xxx.com/js/app.beeb81af.js -g regex_file/convention.txt
Usage:python3 jsfinderPro.py -l 测试.js -g regex_file/convention.txt 
Usage:python3 jsfinderPro.py -l 测试的文件夹 -g regex_file/convention.txt -t 5
Usage:使用前请提前清空result文件夹，信息提取的结果会保存到result文件中
```
<img width="913" alt="image" src="https://github.com/bingtangbanli/jsfinderPro/assets/77956516/f6e32e4f-7b50-4fdc-aa22-4366eb86cbc2">

### 3、结果展示

<img width="728" alt="image" src="https://github.com/bingtangbanli/jsfinderPro/assets/77956516/4b555d61-cbd8-4798-a7ac-557bb4ac7d1f">


### 4、js敏感信息规则修改

目前正则匹配的文件在regex_file/convention.txt中，可以通过修改配置文件中的正则，修改匹配js文件中的内容

#### 最新的正则内容如下,请自行替换regex_file/convention.txt文件的内容：
```
大陆手机号: \b1[3456789]\d{9}\b
身份证: \b\d{17}[\dXx]\b
邮箱: \b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b
银行卡: \b\d{16,19}\b
域名: (?i)\b(?:[a-zA-Z0-9-]+\.)+(?:com|net|org|io|co|edu|gov|mil|biz|info|me|us|ca|uk|de|fr|it|es|au|nz|jp|kr|cn|ru|br|in|mx|nl)\b
路径: (?:https?://|/|\.\./|\./|/[\w-]+)/(?:[\w/.?%&=-]*|[\w-]+)
URL: (?i)\b((?:https?|ftp|file):\/\/[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,63}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/=]*))\b
JWT: \bey[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\b
JDBC: jdbc:[a-zA-Z]+:\/\/[^\s]*
authHeader: (?i)\bAuthorization:\s*(?:Bearer|Basic|Digest)\s+(?:[A-Za-z0-9-._~+/]+=*|[\w%]{2}==)\b
账户密码: (?:username|user|account)\s*[:=]\s*['\"](.*?)['\"]\s*,\s*(?:password|pass)\s*[:=]\s*['\"](.*?)['\"]
ticket: \bjsapi_ticket\b
加密算法: (?i)\b(AES|DES|3DES|RC4|RSA|ECC|SM2|SM3|SM4|Blowfish|HMAC)\b
密钥: (?i)(?:encryption|secret|private|api|auth|access|key)\s*[:=]\s*["\']?([0-9a-fA-F]{32,})["\']?
偏移量: (?i)(?:iv|offset|init_vector)\s*[:=]\s*["\']?([0-9a-fA-F]{8,})["\']?
swagger: (?i)\b((?:https?://)?(?:[a-zA-Z0-9-\.]+)\/(?:v1|v2|v3|docs|swagger|apidocs|api-docs|open-api)?\/?(swagger|api-docs)(?:\.json)?)\b
oss: https?://[^\'")\s]*oss[^\'")\s]+
access_key: (?i)\baccess[_]?key\s*[:=]\s*["\']([^"\']+)["\']
oss_key: (?i)\boss\s*[_\s]*(?:key)?\s*[=:]\s*['\"]([A-Z0-9]+)['\"]
apikey: (?i)\bapi[_]?key\s*[=:]\s*["\']([^"\']+)["\']
apisecret: (?i)\bapi[_]?secret\s*[=:]\s*["\']([^"\']+)["\']
app_key: (?i)\bAppKey\s*:\s*["\']([^"\']+)["\']
app_secret: (?i)\bAPPSECRET\s*:\s*["\']([^"\']+)["\']
rsa_public_keys: -----BEGIN(?:\s+\w+)?\s+PUBLIC\s+KEY-----\s*(.*?)\s*-----END(?:\s+\w+)?\s+PUBLIC\s+KEY-----
rsa_private_keys: -----BEGIN(?:\s+RSA)?\s+PRIVATE\s+KEY-----\s*(.*?)\s*-----END(?:\s+RSA)?\s+PRIVATE\s+KEY-----
```
