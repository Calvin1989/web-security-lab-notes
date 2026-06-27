# Burp Suite 基础使用备忘

## 1. 文档说明

本文档记录本项目中使用 Burp Suite 进行 Web 漏洞验证时的基础操作流程，重点服务于 DVWA、Pikachu 等本地授权靶场环境。

Burp 在本项目中的作用不是“自动打漏洞”，而是帮助完成：

- 抓取浏览器与 Web 服务之间的 HTTP 请求；
- 观察参数、Cookie、请求方法和响应内容；
- 使用 Repeater 手工修改请求并复测；
- 保存关键请求证据，支撑漏洞报告编写；
- 对比修复前后请求响应差异。

## 2. 基础代理配置

### 2.1 Burp 监听地址

默认代理监听地址通常为：

```text
127.0.0.1:8080
```

在 Burp 中确认路径：

```text
Proxy -> Proxy settings -> Proxy listeners
```

### 2.2 浏览器代理

浏览器或代理插件中配置：

```text
HTTP Proxy: 127.0.0.1
Port: 8080
```

只建议在本地测试浏览器中开启代理，避免影响日常浏览器流量。

### 2.3 HTTPS 证书

如果测试 HTTPS 站点，需要在浏览器中安装 Burp CA 证书。本项目主要使用本地 HTTP 靶场，因此不依赖 HTTPS 证书配置。

## 3. 常用模块

| 模块 | 用途 |
|---|---|
| Proxy | 拦截、查看和转发浏览器请求 |
| HTTP history | 查看请求历史，筛选关键请求 |
| Repeater | 手工修改请求并重复发送 |
| Decoder | 编码、解码 URL / Base64 等内容 |
| Comparer | 对比两个响应或请求差异 |
| Intruder | 参数枚举与爆破测试，本项目仅用于理解，不作为主要交付证据 |

## 4. 抓包基本流程

1. 打开 Burp，确认 Proxy listener 正常启动；
2. 浏览器配置代理到 `127.0.0.1:8080`；
3. 打开 DVWA 或 Pikachu 本地靶场；
4. 在 Burp 中关闭或开启 Intercept，根据需要控制请求；
5. 在页面执行一次正常业务操作；
6. 到 `Proxy -> HTTP history` 中找到对应请求；
7. 右键发送到 Repeater；
8. 在 Repeater 中修改参数并发送；
9. 观察响应状态码、响应长度、页面内容和错误信息；
10. 保存关键请求截图或复制脱敏后的请求片段到报告中。

## 5. HTTP history 观察重点

分析请求时重点看以下字段：

- 请求方法：`GET`、`POST`；
- URL 路径和 Query 参数；
- 请求体中的表单参数或 JSON 字段；
- Cookie，例如 `PHPSESSID=***; security=low`；
- Referer 和 Origin；
- User-Agent；
- 响应状态码，例如 `200`、`302`、`403`、`500`；
- 响应长度变化；
- 响应正文中的报错、回显或权限数据。

单个字段通常不能直接证明漏洞，需要结合页面表现和响应内容一起判断。

## 6. Repeater 手工验证思路

### 6.1 SQL 注入

正常请求示例：

```http
GET /dvwa/vulnerabilities/sqli/?id=1&Submit=Submit HTTP/1.1
Cookie: PHPSESSID=***; security=low
```

测试时修改 `id` 参数：

```text
id=1'
id=1' OR '1'='1
id=1' UNION SELECT null,null-- -
```

观察是否出现数据库报错、结果集变化或异常回显。

### 6.2 XSS

关注反射点或存储点，例如：

```text
name=<script>alert(1)</script>
message=<img src=x onerror=alert(1)>
```

验证时要同时记录：

- 请求参数；
- 页面是否执行脚本；
- 修复后是否进行输出编码。

### 6.3 文件上传

重点观察上传请求中的：

- `Content-Type: multipart/form-data`；
- `filename`；
- 文件 MIME 类型；
- 上传路径回显；
- 上传后访问路径。

示例关注点：

```http
Content-Disposition: form-data; name="uploaded"; filename="test.php"
Content-Type: application/octet-stream
```

### 6.4 越权访问

对比两个用户请求中的身份字段：

- URL 中的 `id`；
- 表单中的 `user_id`；
- Cookie / Session；
- 返回页面中的用户信息。

常见验证方式是保持当前登录态不变，只修改对象 ID，观察是否返回其他用户数据。

### 6.5 命令执行

关注参数是否被拼接到系统命令中：

```text
ip=127.0.0.1
ip=127.0.0.1 && whoami
ip=127.0.0.1 | id
```

报告中应强调：漏洞验证发生在本地靶场，不对真实系统执行破坏性命令。

## 7. 报告取证规范

截图或请求片段中应注意脱敏：

- `PHPSESSID` 统一写成 `PHPSESSID=***`；
- 遮挡本地用户名和真实路径；
- 不展示无关浏览器账号、插件信息；
- 请求中如有密码、token、key、secret，应替换为 `***`；
- 只保留与漏洞判断有关的参数和响应证据。

推荐报告证据格式：

```text
验证方式：Burp Repeater 手工修改参数并复测
关键参数：id
测试 payload：1' OR '1'='1
观察结果：响应中返回非预期数据，说明服务端未正确限制查询逻辑
复测结论：修复后同类 payload 不再改变查询结果
```

## 8. 常见排错

| 问题 | 排查方向 |
|---|---|
| 浏览器无法访问页面 | 检查 Burp 是否启动、代理端口是否正确 |
| Burp 没有请求记录 | 检查浏览器代理是否启用、是否走了其他代理插件 |
| 页面一直卡住 | Intercept 可能开启但请求未放行 |
| 登录态失效 | Cookie 被覆盖或安全等级改变，重新登录靶场 |
| 请求太多不好找 | 使用 HTTP history 过滤 Host、Method、Status 或关键词 |
| 截图里有敏感信息 | 重新截图或打码后再提交到仓库 |

## 9. 本项目中的使用原则

- 以手工验证为主，自动化工具结果只作为辅助；
- 每类漏洞至少保留一张 Burp 请求证据截图；
- 不把本地靶场结论夸大成真实生产系统风险；
- 报告重点写清楚漏洞成因、复现步骤、影响、修复建议和复测结论；
- 所有测试仅限本地授权环境。
