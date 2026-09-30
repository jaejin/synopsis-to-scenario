"""
프로젝트 초기화 스크립트
사용법: python scripts/init_project.py <project_name> [--format screenplay|web_novel]

projects/{project_name}/ 디렉토리를 생성하고
config.yaml과 state.json 초기 파일을 배치합니다.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent


FORMATS = ("screenplay", "web_novel")

# 형식별 상태 스키마 — 웹소설은 회차 진행을 추적하는 serial 필드가 추가된다
STATE_SCHEMAS = {
    "screenplay": ROOT_DIR / "prompts" / "state_schema.json",
    "web_novel": ROOT_DIR / "prompts" / "webnovel" / "state_schema.json",
}


def init_project(project_name: str, target_format: str = "screenplay") -> None:
    project_dir = ROOT_DIR / "projects" / project_name

    if project_dir.exists():
        print(f"[!] 프로젝트 '{project_name}'이 이미 존재합니다: {project_dir}")
        sys.exit(1)

    # 디렉토리 생성
    (project_dir / "input" / "references").mkdir(parents=True)
    (project_dir / "output").mkdir(parents=True)
    if target_format == "web_novel":
        for sub in ("episodes", "revision", "step_06_episode_plan"):
            (project_dir / "output" / sub).mkdir()

    # config.yaml 복사
    config_schema = ROOT_DIR / "prompts" / "config_schema.yaml"
    config_dest = project_dir / "config.yaml"
    config_text = config_schema.read_text(encoding="utf-8")
    config_text = config_text.replace("target_format: screenplay ", f"target_format: {target_format} ", 1)
    config_dest.write_text(config_text, encoding="utf-8")
    print(f"[+] config.yaml 생성: {config_dest}")

    # state.json 생성
    with open(STATE_SCHEMAS[target_format], encoding="utf-8") as f:
        state = json.load(f)

    state["project_name"] = project_name
    state["created_at"] = datetime.now().isoformat()

    state_dest = project_dir / "state.json"
    with open(state_dest, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"[+] state.json 생성: {state_dest}")

    print(f"""
[완료] 프로젝트 '{project_name}' 초기화 완료! (형식: {target_format})

다음 단계:
  1. {config_dest} 편집 → 프로젝트 설정 입력
  2. {project_dir / 'input'}/에 시놉시스 파일 배치
  3. Claude Code 세션에서 워크플로우 시작
""")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="프로젝트 초기화")
    parser.add_argument("project_name")
    parser.add_argument("--format", dest="target_format", choices=FORMATS, default="screenplay",
                        help="산출 형식 (기본 screenplay)")
    args = parser.parse_args()

    init_project(args.project_name, args.target_format)
