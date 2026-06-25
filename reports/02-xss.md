\# Web 漏洞复现报告：XSS 跨站脚本漏洞



\## 1. 漏洞概述



\* 漏洞名称：XSS 跨站脚本漏洞

\* 漏洞类型：前端脚本注入 / 输出编码缺陷

\* 风险等级：中危

\* 复现环境：DVWA

\* 测试方式：本地授权靶场测试

\* 影响范围：搜索框、留言板、评论区、用户昵称、个人资料、后台公告等存在用户输入并回显到页面的功能点。



本次测试在本地 DVWA 靶场中完成，主要复现了两类 XSS 漏洞：



1\. 反射型 XSS；

2\. 存储型 XSS。



测试过程中仅使用 `alert` 弹窗进行无害验证，不涉及真实 Cookie 获取、外连请求、钓鱼页面或未授权目标测试。



\## 2. 漏洞原理



XSS 的核心问题是：网站把用户输入的内容输出到了网页中，但没有进行安全处理，导致浏览器把用户输入当成 JavaScript 代码执行。



通俗来说，网站本来应该把用户输入当成普通文字显示。例如用户输入：



```text

test

```



页面应该只显示：



```text

Hello test

```



但是如果用户输入：



```html

<script>alert('xss')</script>

```



而网站没有做 HTML 实体编码或过滤，浏览器就可能把这段内容当作脚本执行，从而弹出提示框。



\### 2.1 反射型 XSS 原理



反射型 XSS 的特点是：恶意输入通过 URL 或请求参数提交，服务端马上把这个输入返回到页面中，浏览器立即执行。



攻击流程可以理解为：



```text

攻击者构造带脚本的 URL

&#x20;       ↓

用户点击 URL

&#x20;       ↓

服务端把参数原样返回到页面

&#x20;       ↓

浏览器执行脚本

```



本案例中，DVWA 的 `XSS (Reflected)` 模块会将 `name` 参数回显到页面。如果参数中包含脚本内容，且服务端未做安全处理，就会触发反射型 XSS。



\### 2.2 存储型 XSS 原理



存储型 XSS 的特点是：恶意脚本会被保存到数据库中，之后其他用户访问相关页面时，脚本会再次被加载并执行。



攻击流程可以理解为：



```text

攻击者提交带脚本的留言

&#x20;       ↓

网站把留言保存到数据库

&#x20;       ↓

其他用户或管理员打开留言页面

&#x20;       ↓

页面输出留言内容

&#x20;       ↓

浏览器执行脚本

```



存储型 XSS 通常比反射型 XSS 危害更大，因为攻击者不需要每次都诱导用户点击特殊链接，只要恶意内容已经被保存，后续访问该页面的用户都可能受到影响。



\## 3. 复现环境



\* 系统环境：Windows

\* Web 环境：小皮面板 / PHP / MySQL

\* 靶场名称：DVWA

\* 靶场地址：`http://127.0.0.1/dvwa`

\* 使用工具：Chrome、Burp Suite

\* 测试账号：本地靶场测试账号

\* 漏洞模块：



&#x20; \* `XSS (Reflected)`

&#x20; \* `XSS (Stored)`

\* 安全等级：Low / Impossible



\## 4. 复现步骤



\## 4.1 反射型 XSS 复现



\### 4.1.1 定位测试点



进入 DVWA 后，将安全等级设置为 Low，选择左侧菜单中的：



```text

XSS (Reflected)

```



该页面提供了一个输入框，用户输入名称后，页面会将输入内容回显出来。



截图：



```text

screenshots/xss/01-reflected-page.png

```



\### 4.1.2 正常输入测试



在输入框中输入：



```text

test

```



提交后，页面返回：



```text

Hello test

```



截图：



```text

screenshots/xss/02-reflected-normal-input.png

```



该步骤说明该功能的正常逻辑是：接收用户输入，并将输入内容回显到页面中。



\### 4.1.3 构造 XSS 测试输入



在输入框中输入：



```html

<script>alert('xss')</script>

```



提交后，浏览器弹出 `xss` 提示框。



截图：



```text

screenshots/xss/03-reflected-xss-alert.png

```



该结果说明服务端没有将用户输入安全地当作普通文本处理，浏览器执行了输入中的 JavaScript 代码，反射型 XSS 漏洞成功复现。



\### 4.1.4 Burp Suite 抓包分析



使用 Burp Suite 抓取反射型 XSS 请求。



截图：



```text

screenshots/xss/04-burp-reflected-xss-request.png

```



请求中的关键参数为：



```http

GET /dvwa/vulnerabilities/xss\_r/?name=%3Cscript%3Ealert%28%27xss%27%29%3C%2Fscript%3E HTTP/1.1

Cookie: PHPSESSID=\*\*\*; security=low

```



其中：



```text

%3Cscript%3Ealert%28%27xss%27%29%3C%2Fscript%3E

```



是 URL 编码后的：



```html

<script>alert('xss')</script>

```



该请求说明恶意脚本内容是通过 `name` 参数提交到服务端，并被服务端返回到页面中执行。



\### 4.1.5 Impossible 模式对比



将 DVWA 安全等级切换为 Impossible，再次提交相同测试输入：



```html

<script>alert('xss')</script>

```



截图：



```text

screenshots/xss/05-impossible-compare.png

```



在 Impossible 模式下，页面没有弹窗，而是将脚本内容作为普通文本显示，说明服务端对输出内容进行了安全处理，浏览器没有继续把用户输入当作脚本执行。



\---



\## 4.2 存储型 XSS 复现



\### 4.2.1 定位测试点



将 DVWA 安全等级设置为 Low，选择左侧菜单中的：



```text

XSS (Stored)

```



该页面是一个留言板，用户可以提交 Name 和 Message，提交后的内容会显示在页面中。



截图：



```text

screenshots/xss/06-stored-page.png

```



\### 4.2.2 正常留言测试



提交普通留言：



```text

Name: test

Message: hello

```



提交后，页面正常显示留言内容。



截图：



```text

screenshots/xss/07-stored-normal-message.png

```



该步骤说明该功能的正常逻辑是：用户提交留言后，服务端会保存留言内容，并在页面中展示。



\### 4.2.3 构造存储型 XSS 输入



提交以下内容：



```text

Name: xss

Message: <script>alert('stored-xss')</script>

```



提交后，浏览器弹出 `stored-xss` 提示框。



截图：



```text

screenshots/xss/08-stored-xss-submit.png

```



该结果说明留言内容中的脚本被浏览器执行，存储型 XSS 初步触发成功。



\### 4.2.4 刷新页面验证存储效果



关闭弹窗后，再次刷新 Stored XSS 页面，页面仍然触发 `stored-xss` 弹窗。



截图：



```text

screenshots/xss/09-stored-xss-alert.png

```



该结果说明恶意脚本已经被保存到数据库中。只要页面再次加载留言内容，浏览器就会执行保存下来的脚本。



这也是存储型 XSS 与反射型 XSS 的主要区别：



```text

反射型 XSS：脚本通常跟着 URL 参数走，访问一次触发一次。

存储型 XSS：脚本被保存到数据库，后续访问页面时也会触发。

```



\### 4.2.5 Burp Suite 抓包分析



使用 Burp Suite 抓取提交留言的 POST 请求。



截图：



```text

screenshots/xss/10-burp-stored-xss-request.png

```



请求中的关键内容为：



```http

POST /dvwa/vulnerabilities/xss\_s/ HTTP/1.1

Cookie: PHPSESSID=\*\*\*; security=low



txtName=xss\&mtxMessage=%3Cscript%3Ealert%28%27stored-xss%27%29%3C%2Fscript%3E\&btnSign=Sign+Guestbook

```



其中：



```text

%3Cscript%3Ealert%28%27stored-xss%27%29%3C%2Fscript%3E

```



是 URL 编码后的：



```html

<script>alert('stored-xss')</script>

```



该请求说明恶意脚本通过留言板的 `mtxMessage` 参数提交到服务端，并被服务端保存和展示。



\### 4.2.6 Impossible 模式对比



将 DVWA 安全等级切换为 Impossible，再次提交：



```text

Name: xss

Message: <script>alert('stored-xss')</script>

```



截图：



```text

screenshots/xss/11-stored-impossible-compare.png

```



在 Impossible 模式下，页面将脚本内容作为普通文本显示，没有执行 JavaScript。说明服务端对留言内容进行了安全处理，避免浏览器将用户输入当作脚本执行。



\## 5. 漏洞验证结果



XSS 漏洞成功复现。



验证依据如下：



1\. 反射型 XSS 中，普通输入 `test` 被正常回显；

2\. 反射型 XSS 中，输入 `<script>alert('xss')</script>` 后浏览器弹窗；

3\. Burp Suite 抓包显示脚本内容通过 `name` 参数提交到服务端；

4\. 存储型 XSS 中，普通留言可以正常保存和显示；

5\. 存储型 XSS 中，留言内容包含脚本时，浏览器执行了脚本；

6\. 刷新 Stored XSS 页面后仍然触发弹窗，说明脚本已经被保存；

7\. Burp Suite 抓包显示脚本内容通过 `mtxMessage` 参数提交；

8\. 在 Impossible 模式下，同样输入被作为普通文本处理，未继续执行脚本。



关键截图：



| 截图                                                  | 说明                      |

| --------------------------------------------------- | ----------------------- |

| `screenshots/xss/01-reflected-page.png`             | 反射型 XSS 测试页面            |

| `screenshots/xss/02-reflected-normal-input.png`     | 反射型 XSS 正常输入回显          |

| `screenshots/xss/03-reflected-xss-alert.png`        | 反射型 XSS 弹窗验证            |

| `screenshots/xss/04-burp-reflected-xss-request.png` | Burp 抓取反射型 XSS 请求       |

| `screenshots/xss/05-impossible-compare.png`         | 反射型 XSS Impossible 模式对比 |

| `screenshots/xss/06-stored-page.png`                | 存储型 XSS 测试页面            |

| `screenshots/xss/07-stored-normal-message.png`      | 存储型 XSS 正常留言            |

| `screenshots/xss/08-stored-xss-submit.png`          | 存储型 XSS 提交后弹窗           |

| `screenshots/xss/09-stored-xss-alert.png`           | 存储型 XSS 刷新后仍然触发         |

| `screenshots/xss/10-burp-stored-xss-request.png`    | Burp 抓取存储型 XSS 提交请求     |

| `screenshots/xss/11-stored-impossible-compare.png`  | 存储型 XSS Impossible 模式对比 |



\## 6. 风险影响



XSS 漏洞可能造成以下影响：



\* 在用户浏览器中执行恶意 JavaScript；

\* 篡改页面内容，影响用户判断；

\* 构造伪造表单，诱导用户提交敏感信息；

\* 在用户登录状态下发起非预期请求；

\* 结合其他漏洞进一步扩大攻击影响；

\* 存储型 XSS 可能影响所有访问相关页面的用户或管理员。



在真实业务系统中，如果评论区、留言板、个人资料、后台公告等功能存在存储型 XSS，攻击者只需要提交一次恶意内容，后续访问该页面的用户都可能受到影响。



\## 7. 修复建议



建议从以下方面修复 XSS 漏洞：



1\. 对所有输出到 HTML 页面中的用户输入进行 HTML 实体编码；

2\. 根据不同输出位置采用不同编码方式，例如 HTML 正文、HTML 属性、JavaScript 字符串、URL 参数需要分别处理；

3\. 对用户输入进行白名单校验，限制不必要的特殊字符；

4\. 对富文本内容使用安全的 HTML 清洗库，只允许安全标签和属性；

5\. 设置合理的 Content Security Policy，降低脚本执行风险；

6\. 对 Cookie 设置 `HttpOnly` 和 `SameSite` 属性，降低脚本利用后的影响；

7\. 避免直接使用 `innerHTML` 等危险方式拼接用户输入；

8\. 前端校验只能作为辅助措施，不能替代服务端安全处理；

9\. 对异常输入和高风险请求记录安全日志并进行告警。



\## 8. 复测结论



\* 复测结果：通过

\* 复测说明：在 DVWA Impossible 安全等级下，反射型 XSS 和存储型 XSS 的测试输入均未被浏览器当作 JavaScript 执行，页面将脚本内容作为普通文本显示。

\* 整改建议：真实业务系统应在服务端对用户输入进行校验，并在输出到页面时进行上下文相关的安全编码，同时配合 CSP、HttpOnly Cookie 和安全日志监控降低 XSS 风险。



