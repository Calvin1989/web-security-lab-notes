\# Web 漏洞复现报告：文件上传漏洞



\## 1. 漏洞概述



\* 漏洞名称：文件上传漏洞

\* 漏洞类型：文件类型校验缺陷 / 不安全文件上传

\* 风险等级：高

\* 复现环境：DVWA

\* 测试方式：本地授权靶场测试

\* 影响范围：头像上传、图片上传、附件上传、简历上传、工单附件、后台素材上传等文件上传功能点。



本次测试在本地 DVWA 靶场中完成，安全等级设置为 Low。通过 File Upload 模块上传一个无害 PHP 测试文件，发现服务端未严格限制上传文件类型，导致 `.php` 文件可以被上传到 Web 可访问目录中，并且可以被服务器执行。



本次测试仅使用 `echo` 输出固定文本进行无害验证，不涉及 WebShell、命令执行、反弹连接或真实目标测试。



\## 2. 漏洞原理



文件上传漏洞的核心问题是：网站没有严格校验用户上传的文件类型、文件内容和文件存储位置，导致攻击者可以上传非预期类型的文件。



通俗理解：



```text

网站本来只想让用户上传图片，

但它没有检查清楚，

结果 PHP 脚本文件也被上传成功了。

如果上传目录还能执行 PHP，

那么访问这个文件时，服务器就会运行里面的 PHP 代码。

```



正常情况下，上传功能应该只允许用户上传业务需要的文件，例如图片、PDF、Word 文档等。



但在本案例中，DVWA Low 模式没有严格限制文件后缀和文件内容，导致测试用的 PHP 文件被上传到：



```text

hackable/uploads/

```



并且可以通过浏览器访问执行。



\## 3. 复现环境



\* 系统环境：Windows

\* Web 环境：小皮面板 / PHP / MySQL

\* 靶场名称：DVWA

\* 靶场地址：`http://127.0.0.1/dvwa`

\* 使用工具：Chrome、Burp Suite、记事本

\* 测试账号：本地靶场测试账号

\* 漏洞模块：File Upload

\* 安全等级：Low / Impossible



\## 4. 复现步骤



\### 4.1 定位测试点



进入 DVWA 后，将安全等级设置为 Low，选择左侧菜单中的：



```text

File Upload

```



该页面提供文件上传功能，页面提示为上传图片。



截图：



```text

screenshots/file-upload/01-upload-page.png

```



该功能属于典型的文件上传测试点，需要关注以下内容：



\* 是否限制文件后缀；

\* 是否校验文件 MIME 类型；

\* 是否检查文件真实内容；

\* 上传后的文件是否可访问；

\* 上传目录是否允许脚本执行。



\### 4.2 创建无害 PHP 测试文件



创建测试文件：



```text

upload-test.php

```



文件内容如下：



```php

<?php

echo "file upload test success";

?>

```



截图：



```text

screenshots/file-upload/02-test-file-content.png

```



该文件只输出固定文本：



```text

file upload test success

```



如果上传后访问该文件并看到这段文本，说明服务器执行了该 PHP 文件。



\### 4.3 上传 PHP 文件



在 DVWA 的 File Upload 页面选择：



```text

upload-test.php

```



点击上传后，页面提示上传成功：



```text

../../hackable/uploads/upload-test.php succesfully uploaded!

```



截图：



```text

screenshots/file-upload/03-upload-success.png

```



该结果说明，在 Low 安全等级下，服务端允许上传 `.php` 文件，未对文件类型进行有效限制。



\### 4.4 访问上传后的文件



浏览器访问上传后的文件路径：



```text

http://127.0.0.1/dvwa/hackable/uploads/upload-test.php

```



页面返回：



```text

file upload test success

```



截图：



```text

screenshots/file-upload/04-access-uploaded-file.png

```



该结果说明上传的 PHP 文件不仅被保存到了服务器，而且可以通过 Web 路径访问并执行。



这是文件上传漏洞中非常关键的风险点：如果上传目录允许脚本执行，攻击者上传的脚本文件可能被服务器解析执行。



\### 4.5 Burp Suite 抓包分析



使用 Burp Suite 抓取上传文件时的请求。



截图：



```text

screenshots/file-upload/05-burp-upload-request.png

```



请求中的关键内容包括：



```http

POST /dvwa/vulnerabilities/upload/ HTTP/1.1

Content-Type: multipart/form-data

Cookie: PHPSESSID=\*\*\*; security=low

```



请求体中可以看到上传字段和文件名：



```http

Content-Disposition: form-data; name="uploaded"; filename="upload-test.php"

Content-Type: application/octet-stream

```



该请求说明用户上传的文件名为：



```text

upload-test.php

```



服务端在 Low 模式下没有拦截该 PHP 文件，导致文件被成功上传。



\### 4.6 Impossible 模式对比



将 DVWA 安全等级切换为 Impossible，再次尝试上传同样的 PHP 文件：



```text

upload-test.php

```



页面提示：



```text

Your image was not uploaded. We can only accept JPEG or PNG images.

```



截图：



```text

screenshots/file-upload/06-impossible-compare.png

```



该结果说明 Impossible 模式下服务端对上传文件进行了更严格的限制，只允许上传指定类型的图片文件，原来的 PHP 文件上传方式不再生效。



\## 5. 漏洞验证结果



文件上传漏洞成功复现。



验证依据如下：



1\. DVWA Low 模式下，File Upload 功能允许上传 `.php` 文件；

2\. 页面返回上传成功提示，并给出了上传后的文件路径；

3\. 访问上传后的 PHP 文件，页面返回 `file upload test success`；

4\. Burp Suite 抓包显示上传请求中包含 `filename="upload-test.php"`；

5\. 在 Impossible 模式下，同样的 PHP 文件被拦截，说明该问题可以通过服务端安全校验进行修复。



关键截图：



| 截图                                                    | 说明                  |

| ----------------------------------------------------- | ------------------- |

| `screenshots/file-upload/01-upload-page.png`          | 文件上传功能页面            |

| `screenshots/file-upload/02-test-file-content.png`    | 无害 PHP 测试文件内容       |

| `screenshots/file-upload/03-upload-success.png`       | PHP 文件上传成功          |

| `screenshots/file-upload/04-access-uploaded-file.png` | 访问上传文件并执行成功         |

| `screenshots/file-upload/05-burp-upload-request.png`  | Burp 抓取上传请求         |

| `screenshots/file-upload/06-impossible-compare.png`   | Impossible 模式下上传被拦截 |



\## 6. 风险影响



文件上传漏洞可能造成以下影响：



\* 上传恶意脚本文件；

\* 上传文件被服务器解析执行；

\* 获取服务器目录信息；

\* 进一步读取或修改服务器文件；

\* 结合其他漏洞扩大攻击影响；

\* 在权限配置不当的情况下，可能导致服务器被控制。



在真实业务系统中，如果头像上传、附件上传、后台素材上传等功能存在类似问题，攻击者可能上传脚本文件，并通过访问上传路径触发服务器执行恶意代码。



本次测试只使用无害 `echo` 文件证明 PHP 文件可以被执行，不涉及真实攻击代码。



\## 7. 修复建议



建议从以下方面修复文件上传漏洞：



1\. 使用白名单限制上传文件类型，只允许业务需要的类型，例如 JPEG、PNG、PDF 等；

2\. 不仅校验文件后缀，还应校验 MIME 类型和文件真实内容；

3\. 上传文件统一重命名，避免用户控制最终文件名；

4\. 上传目录禁止执行脚本，例如禁止解析 PHP、JSP、ASP 等脚本文件；

5\. 上传文件存储到 Web 根目录之外，通过后端接口读取和返回；

6\. 限制上传文件大小，避免上传超大文件造成资源消耗；

7\. 对上传文件进行安全扫描；

8\. 对上传接口增加登录校验和权限控制；

9\. 记录上传日志，包括上传用户、文件名、文件类型、文件大小、上传时间和来源 IP；

10\. 前端校验只能作为辅助，不能替代服务端校验。



\## 8. 复测结论



\* 复测结果：通过

\* 复测说明：在 DVWA Impossible 安全等级下，再次上传 `upload-test.php` 文件时，系统提示只允许上传 JPEG 或 PNG 图片，PHP 文件无法上传成功。

\* 整改建议：真实业务系统应采用文件类型白名单、内容校验、文件重命名、上传目录禁止脚本执行、权限控制和安全日志记录等多层防护措施，避免文件上传漏洞。



