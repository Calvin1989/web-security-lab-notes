\# Web 漏洞复现报告：SQL 注入



\## 1. 漏洞概述



\* 漏洞名称：SQL 注入

\* 漏洞类型：输入验证缺陷 / 注入漏洞

\* 风险等级：高

\* 复现环境：DVWA

\* 测试方式：本地授权靶场测试

\* 影响范围：用户查询、登录认证、数据检索等与数据库交互的功能点。



本次测试在本地 DVWA 靶场中完成，安全等级设置为 Low。通过对 SQL Injection 模块的 User ID 参数进行测试，发现该参数存在 SQL 注入风险。攻击者可以通过构造异常输入改变后端 SQL 查询逻辑，从而获取非预期的用户数据。



\## 2. 漏洞原理



SQL 注入漏洞产生的根本原因是服务端将用户输入直接拼接进 SQL 查询语句，未使用参数化查询或预编译语句进行安全处理。



在本案例中，User ID 参数原本应该只接收数字类型的用户编号。但在 Low 安全等级下，服务端没有对该参数进行严格校验和安全绑定，导致用户输入可以影响后端 SQL 语句结构。



当输入永真条件时，原本只查询单个用户的 SQL 逻辑被改变，最终返回了多条用户记录。这说明用户输入已经影响了后端数据库查询逻辑。



\## 3. 复现环境



\* 系统环境：Windows

\* Web 环境：小皮面板 / PHP / MySQL

\* 靶场名称：DVWA

\* 靶场地址：`http://127.0.0.1/dvwa`

\* 使用工具：Chrome、Burp Suite

\* 测试账号：本地靶场测试账号

\* 漏洞模块：SQL Injection

\* 安全等级：Low



\## 4. 复现步骤



\### 4.1 定位测试点



进入 DVWA 后，选择左侧菜单中的 SQL Injection 模块。



该页面提供了一个 User ID 查询功能，用户输入 ID 后，系统会返回对应用户的 First name 和 Surname。



截图：



`screenshots/sql-injection/01-sql-injection-page.png`



\### 4.2 正常业务请求



在 User ID 输入框中输入：



```text

1

```



提交后，页面返回 ID 为 1 的用户信息。



截图：



`screenshots/sql-injection/02-normal-query.png`



该步骤说明该功能的正常业务逻辑是：根据用户输入的 ID 查询对应用户信息。



\### 4.3 异常输入测试



在 User ID 输入框中输入单引号：



```text

'

```



提交后，页面返回 MySQL 语法错误信息。



截图：



`screenshots/sql-injection/03-error-based-test.png`



该结果说明用户输入被带入了后端 SQL 查询语句，并且异常输入影响了 SQL 语句结构。



\### 4.4 构造 SQL 注入验证输入



在 User ID 输入框中输入：



```text

1' OR '1'='1

```



提交后，页面返回了多条用户记录，而不是只返回 ID 为 1 的单条记录。



截图：



`screenshots/sql-injection/04-sqli-result.png`



该结果说明用户输入改变了原有 SQL 查询逻辑，SQL 注入漏洞成功复现。



\### 4.5 Burp Suite 抓包分析



使用 Burp Suite 代理浏览器请求，抓取正常查询请求。



正常请求截图：



`screenshots/sql-injection/05-burp-normal-request.png`



正常请求中的关键参数为：



```http

GET /dvwa/vulnerabilities/sqli/?id=1\&Submit=Submit HTTP/1.1

Cookie: PHPSESSID=\*\*\*; security=low

```



随后抓取 SQL 注入测试请求。



SQL 注入请求截图：



`screenshots/sql-injection/06-burp-sqli-request.png`



请求中的关键参数为：



```http

GET /dvwa/vulnerabilities/sqli/?id=1%27+OR+%271%27%3D%271\&Submit=Submit HTTP/1.1

Cookie: PHPSESSID=\*\*\*; security=low

```



其中：



```text

1%27+OR+%271%27%3D%271

```



是 URL 编码后的：



```text

1' OR '1'='1

```



\### 4.6 安全模式对比



将 DVWA 安全等级切换为 Impossible 后，使用相同测试输入再次提交。



截图：



`screenshots/sql-injection/07-impossible-compare.png`



在 Impossible 模式下，同样的输入未能返回多条用户记录，说明该模式下服务端已经对用户输入进行了更严格的处理，原有注入方式不再生效。



\## 5. 漏洞验证结果



漏洞成功复现。



验证依据如下：



1\. 正常输入 `1` 时，页面只返回单个用户信息；

2\. 输入单引号时，页面出现 SQL 语法错误，说明用户输入影响了 SQL 语句；

3\. 输入 `1' OR '1'='1` 后，页面返回多条用户记录；

4\. Burp Suite 抓包显示注入输入通过 `id` 参数提交到后端；

5\. 在 Impossible 模式下，同样输入未能继续返回多条数据，说明该漏洞可以通过服务端安全处理进行修复。



关键截图：



| 截图                                                     | 说明                 |

| ------------------------------------------------------ | ------------------ |

| `screenshots/sql-injection/01-sql-injection-page.png`  | SQL Injection 功能页面 |

| `screenshots/sql-injection/02-normal-query.png`        | 正常查询结果             |

| `screenshots/sql-injection/03-error-based-test.png`    | 异常输入导致 SQL 报错      |

| `screenshots/sql-injection/04-sqli-result.png`         | SQL 注入触发结果         |

| `screenshots/sql-injection/05-burp-normal-request.png` | Burp 正常请求          |

| `screenshots/sql-injection/06-burp-sqli-request.png`   | Burp 注入测试请求        |

| `screenshots/sql-injection/07-impossible-compare.png`  | Impossible 模式安全对比  |



\## 6. 风险影响



SQL 注入漏洞可能造成以下影响：



\* 未授权查询数据库内容；

\* 敏感用户信息泄露；

\* 绕过登录认证；

\* 篡改或删除数据库数据；

\* 获取数据库结构信息；

\* 在数据库账号权限过高的情况下，可能进一步影响服务器安全。



在真实业务系统中，如果登录、搜索、订单查询、用户信息查询等功能存在 SQL 注入，攻击者可能通过构造异常输入读取非授权数据，甚至进一步扩大攻击影响。



\## 7. 修复建议



建议从以下方面修复 SQL 注入漏洞：



1\. 使用参数化查询或预编译语句，避免用户输入直接拼接 SQL 语句；

2\. 对用户输入进行白名单校验，例如 ID 参数只允许数字；

3\. 关闭生产环境中的详细 SQL 错误回显，避免泄露数据库类型和 SQL 语句结构；

4\. 数据库账号遵循最小权限原则，避免 Web 应用使用高权限数据库账号；

5\. 对异常查询、批量查询、SQL 报错等行为记录安全日志并进行告警；

6\. 前端校验只能用于提升用户体验，不能作为主要安全防护措施；

7\. 对重要查询接口增加权限校验，避免用户通过修改参数查询非授权数据。



\## 8. 复测结论



\* 复测结果：通过

\* 复测说明：在 DVWA Impossible 安全等级下，使用相同 SQL 注入测试输入后，未能返回多条用户记录，说明服务端已对输入和查询逻辑进行了更严格处理。

\* 整改建议：真实业务系统应使用参数化查询、输入白名单校验、最小权限数据库账号和统一错误处理机制，避免 SQL 注入风险。



