"""
웹소설 회차 분량 검증 스크립트 (공백 제외 글자 수)

사용법:
  python scripts/count_chars.py <파일 또는 디렉토리>... [--min 4800] [--max 5500]

예:
  python scripts/count_chars.py projects/my-novel/output/episodes/
  python scripts/count_chars.py projects/my-novel/output/episodes/ep_011.md ep_012.md

집계 규칙:
  - 첫 번째 '# ' 제목 줄은 본문이 아니므로 제외한다
  - 장면 전환 기호만 있는 줄(***, * * *, ---, ◆ 등)은 제외한다
  - HTML 주석(<!-- ... -->)은 작업 메모이므로 제외한다
  - 나머지에서 모든 공백 문자(스페이스, 탭, 줄바꿈, 전각 공백)를 뺀 글자 수를 센다

종료 코드: 모든 회차가 범위 안이면 0, 하나라도 벗어나면 1
"""

import argparse
import re
import sys
from pathlib import Path

DEFAULT_MIN = 4800
DEFAULT_MAX = 5500

# 본문 분량에 넣지 않는 장면 전환 줄 — 작가마다 쓰는 기호가 달라 넓게 잡는다
SCENE_BREAK = re.compile(r"^[\s*\-─━=◆◇○●#~·]+$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
WHITESPACE = re.compile(r"\s")


def count_body_chars(text: str) -> int:
    text = HTML_COMMENT.sub("", text)
    lines = text.splitlines()

    body = []
    title_skipped = False
    for line in lines:
        if not title_skipped and line.startswith("# "):
            title_skipped = True
            continue
        if line.strip() and SCENE_BREAK.match(line):
            continue
        body.append(line)

    return len(WHITESPACE.sub("", "\n".join(body)))


def collect_files(targets: list[str]) -> list[Path]:
    files = []
    for target in targets:
        path = Path(target)
        if path.is_dir():
            files.extend(sorted(path.glob("ep_*.md")))
        elif path.is_file():
            files.append(path)
        else:
            print(f"[!] 경로를 찾을 수 없습니다: {target}", file=sys.stderr)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="웹소설 회차 분량(공백 제외) 검증")
    parser.add_argument("targets", nargs="+", help="회차 파일 또는 episodes 디렉토리")
    parser.add_argument("--min", type=int, default=DEFAULT_MIN, help=f"허용 하한 (기본 {DEFAULT_MIN})")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX, help=f"허용 상한 (기본 {DEFAULT_MAX})")
    args = parser.parse_args()

    files = collect_files(args.targets)
    if not files:
        print("[!] 검사할 회차 파일이 없습니다.", file=sys.stderr)
        return 1

    under, over = [], []
    print(f"{'파일':<20} {'글자 수(공백 제외)':>16}  판정")
    for path in files:
        count = count_body_chars(path.read_text(encoding="utf-8"))
        if count < args.min:
            verdict = f"미달 (-{args.min - count})"
            under.append(path.name)
        elif count > args.max:
            verdict = f"초과 (+{count - args.max})"
            over.append(path.name)
        else:
            verdict = "통과"
        print(f"{path.name:<20} {count:>16,}  {verdict}")

    print(f"\n검사 {len(files)}개 · 통과 {len(files) - len(under) - len(over)}개 · "
          f"미달 {len(under)}개 · 초과 {len(over)}개 (허용 범위 {args.min:,}~{args.max:,}자)")
    if under:
        print("미달 회차: " + ", ".join(under))
    if over:
        print("초과 회차: " + ", ".join(over))

    return 1 if under or over else 0


if __name__ == "__main__":
    sys.exit(main())
