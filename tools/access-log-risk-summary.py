import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote


RISK_RULES = [
    {
        "name": "SQL Injection",
        "level": "High",
        "patterns": [
            r"(?i)(\bor\b|\band\b)\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+",
            r"(?i)\bunion\b\s+\bselect\b",
            r"(?i)\bselect\b.+\bfrom\b",
            r"(?i)\bsleep\s*\(",
            r"(?i)\binformation_schema\b",
            r"(--|#|/\*)",
            r"(%27|'|\")\s*(or|and)\s",
        ],
    },
    {
        "name": "XSS",
        "level": "Medium",
        "patterns": [
            r"(?i)<script",
            r"(?i)%3cscript",
            r"(?i)onerror\s*=",
            r"(?i)onload\s*=",
            r"(?i)<svg",
            r"(?i)<img",
            r"(?i)alert\s*\(",
        ],
    },
    {
        "name": "Directory Traversal",
        "level": "High",
        "patterns": [
            r"\.\./",
            r"\.\.\\",
            r"(?i)%2e%2e%2f",
            r"(?i)%2e%2e/",
            r"(?i)(/etc/passwd|win\.ini|\.env|config\.php)",
        ],
    },
    {
        "name": "Command Injection",
        "level": "High",
        "patterns": [
            r"(%26|&)\s*(whoami|id|dir|cat|type|ping|ipconfig|ifconfig)",
            r"(%7c|\|)\s*(whoami|id|dir|cat|type|ping|ipconfig|ifconfig)",
            r"(%3b|;)\s*(whoami|id|dir|cat|type|ping|ipconfig|ifconfig)",
            r"(?i)(cmd=|exec=|command=).*(whoami|id|dir|cat|type)",
        ],
    },
    {
        "name": "Sensitive File Upload",
        "level": "High",
        "patterns": [
            r"(?i)filename=\"[^\"]+\.(php|jsp|asp|aspx|phtml)\"",
            r"(?i)/uploads?/.*\.(php|jsp|asp|aspx|phtml)",
            r"(?i)/files?/.*\.(php|jsp|asp|aspx|phtml)",
        ],
    },
    {
        "name": "Brute Force",
        "level": "Medium",
        "patterns": [
            r"(?i)(login|brute|signin|auth)",
            r"(?i)(username=|user=).*(password=|passwd=|pwd=)",
        ],
    },
    {
        "name": "SSRF",
        "level": "High",
        "patterns": [
            r"(?i)(url=|uri=|link=|target=)https?://127\.0\.0\.1",
            r"(?i)(url=|uri=|link=|target=)https?://localhost",
            r"(?i)(url=|uri=|link=|target=)https?://0\.0\.0\.0",
            r"(?i)(url=|uri=|link=|target=)https?://10\.",
            r"(?i)(url=|uri=|link=|target=)https?://192\.168\.",
            r"(?i)(url=|uri=|link=|target=)https?://172\.(1[6-9]|2[0-9]|3[0-1])\.",
            r"(?i)169\.254\.169\.254",
        ],
    },
    {
        "name": "XXE",
        "level": "High",
        "patterns": [
            r"(?i)<!DOCTYPE",
            r"(?i)<!ENTITY",
            r"(?i)\bSYSTEM\b",
            r"(?i)file://",
        ],
    },
    {
        "name": "PHP Deserialization",
        "level": "Medium",
        "patterns": [
            r"O:\d+:\"[^\"]+\"",
            r"s:\d+:\"[^\"]*\"",
            r"a:\d+:\{",
        ],
    },
]


def extract_ip(line: str) -> str:
    match = re.match(r"^(\S+)", line)
    return match.group(1) if match else "unknown"


def detect_risks(line: str):
    decoded = unquote(line)
    findings = []

    for rule in RISK_RULES:
        matched_patterns = []
        for pattern in rule["patterns"]:
            if re.search(pattern, decoded):
                matched_patterns.append(pattern)

        if matched_patterns:
            findings.append({
                "name": rule["name"],
                "level": rule["level"],
                "patterns": matched_patterns,
            })

    return findings


def summarize_log(log_path: Path, max_examples: int):
    total_lines = 0
    risk_counter = Counter()
    level_counter = Counter()
    ip_counter = Counter()
    examples = defaultdict(list)

    with log_path.open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            total_lines += 1
            line = line.strip()
            if not line:
                continue

            ip = extract_ip(line)
            ip_counter[ip] += 1

            findings = detect_risks(line)
            for finding in findings:
                risk_counter[finding["name"]] += 1
                level_counter[finding["level"]] += 1

                if len(examples[finding["name"]]) < max_examples:
                    examples[finding["name"]].append({
                        "ip": ip,
                        "line": line,
                        "level": finding["level"],
                    })

    return {
        "total_lines": total_lines,
        "risk_counter": risk_counter,
        "level_counter": level_counter,
        "ip_counter": ip_counter,
        "examples": examples,
    }


def build_markdown(summary, log_path: Path) -> str:
    lines = []

    lines.append("# Web Access Log 风险摘要")
    lines.append("")
    lines.append(f"- 日志文件：`{log_path}`")
    lines.append(f"- 总行数：{summary['total_lines']}")
    lines.append("")

    lines.append("## 1. 风险等级统计")
    lines.append("")
    lines.append("| 风险等级 | 命中次数 |")
    lines.append("|---|---|")
    for level, count in summary["level_counter"].most_common():
        lines.append(f"| {level} | {count} |")
    if not summary["level_counter"]:
        lines.append("| 无明显命中 | 0 |")
    lines.append("")

    lines.append("## 2. 风险类型统计")
    lines.append("")
    lines.append("| 风险类型 | 命中次数 |")
    lines.append("|---|---|")
    for risk, count in summary["risk_counter"].most_common():
        lines.append(f"| {risk} | {count} |")
    if not summary["risk_counter"]:
        lines.append("| 无明显命中 | 0 |")
    lines.append("")

    lines.append("## 3. Top 来源 IP")
    lines.append("")
    lines.append("| IP | 请求次数 |")
    lines.append("|---|---|")
    for ip, count in summary["ip_counter"].most_common(10):
        lines.append(f"| {ip} | {count} |")
    lines.append("")

    lines.append("## 4. 风险样例")
    lines.append("")
    if not summary["examples"]:
        lines.append("未发现明显风险样例。")
    else:
        for risk, items in summary["examples"].items():
            lines.append(f"### {risk}")
            lines.append("")
            for item in items:
                lines.append(f"- 风险等级：{item['level']}")
                lines.append(f"- 来源 IP：`{item['ip']}`")
                lines.append("")
                lines.append("```text")
                lines.append(item["line"])
                lines.append("```")
                lines.append("")

    lines.append("## 5. 说明")
    lines.append("")
    lines.append("本脚本基于关键字和正则表达式进行基础风险识别，结果只能作为初步研判线索。真实安全运营场景中，应结合请求上下文、响应状态码、响应大小、账号身份、访问频率、业务接口含义和历史基线进行综合分析。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Summarize risky patterns in web access logs.")
    parser.add_argument("log_file", help="Path to access.log")
    parser.add_argument("-o", "--output", default="summary/log-risk-summary.md", help="Output markdown path")
    parser.add_argument("--max-examples", type=int, default=3, help="Max examples per risk type")
    args = parser.parse_args()

    log_path = Path(args.log_file)
    output_path = Path(args.output)

    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = summarize_log(log_path, args.max_examples)
    markdown = build_markdown(summary, log_path)

    output_path.write_text(markdown, encoding="utf-8")

    print(f"[OK] Risk summary written to: {output_path}")


if __name__ == "__main__":
    main()