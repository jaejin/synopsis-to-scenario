# Synopsis to Screenplay Workflow Engine

시놉시스를 장편 영화 시나리오 또는 연재 웹소설로 전환하는 멀티 에이전트 워크플로우 엔진.

1\~3페이지 분량의 시놉시스를 입력받아, 사전 분석(비평) → 막 구조 → 비트시트 → 트리트먼트(15\~25페이지) → 초고(55\~70페이지)까지, 한국어 장편 영화 시나리오(90분, 70\~85씬)를 단계적으로 산출합니다. 같은 워크플로우로 **200화 연재 웹소설**도 설계·집필할 수 있습니다([웹소설 모드](#웹소설-모드)). Claude Code에 최적화되어 있으나, Cursor, Windsurf 등 AI 코딩 도구나 ChatGPT, Claude 웹/앱에서 프롬프트를 직접 실행해도 사용할 수 있습니다.

2편의 상업 영화를 제작했고, 10년간 영화 투자 업계에 종사했던 20년차 영화인(비개발자)이 바이브 코딩으로 만든 프로그램입니다.

## Architecture

```
[입력] 시놉시스 + 레퍼런스
         │
         ▼
┌─────────────────────────────┐
│     Orchestrator Agent      │
│  워크플로우 제어 · 체크포인트 │
└──────────┬──────────────────┘
    ┌──────┼──────────┐
    ▼      ▼          ▼
 Analyst  Writer    Critic
```

| Agent | Role | Steps |
|-------|------|-------|
| **Orchestrator** | 워크플로우 제어, 데이터 전달, 체크포인트 관리, 피드백 라우팅 | All |
| **Analyst** | 스토리 아키텍트 — 시놉시스 분석, 막 구조, 비트시트 | 0, 1, 2 |
| **Writer** | 시나리오 작가 — 이미지 시스템, 인물, 트리트먼트, 씬 리스트, 초고 | 3, 4, 5, 6, 7 |
| **Critic** | 스크립트 닥터 — 구조 진단, 서브텍스트, 이미지 일관성, 비주얼 리비전 | Checkpoints, 8 |

**설계 원칙**: Writer는 자기 산출물을 스스로 평가하지 않습니다 (자기확인 편향 방지). Critic이 먼저 리뷰하고, 사람이 최종 판단합니다.

## Workflow Pipeline

```
STEP I  [Orchestrator + Writer]  시놉시스 인터뷰 (선택 — 시놉시스가 없을 때)
STEP 0  [Analyst]  시놉시스 사전분석 (비평)
STEP 1  [Analyst]  막 구조 & 러닝타임 설계
STEP 2  [Analyst]  비트시트 (15비트, Snyder 기반)
        ──── Checkpoint A: 구조 확정 ────
STEP 3  [Writer]   이미지 시스템 설계
STEP 4  [Writer]   인물 재설계
        ──── Checkpoint B: 비주얼 전략 & 인물 확정 ────
STEP 5  [Writer]   트리트먼트 (15\~20페이지)
STEP 6  [Writer]   씬 리스트 (70\~85씬)
        ──── Checkpoint C: 초고 전 최종 리뷰 ────
STEP 7  [Writer]   초고 (55\~70페이지, 막별 분할 집필)
STEP 8  [Critic]   비주얼 리비전 (Linda Seger 프로세스)
```

각 체크포인트에서 Critic 리뷰 → 사람 승인/수정/재작업 결정.

## Project Structure

```
prompts/
├── orchestrator.md                  # 전체 실행 흐름
├── config_schema.yaml               # 프로젝트 설정 스키마
├── state_schema.json                # 진행 상태 스키마
├── analyst/
│   ├── system.md                    # Analyst 페르소나
│   ├── step_00_critique.md
│   ├── step_01_act_structure.md
│   └── step_02_beat_sheet.md
├── writer/
│   ├── system.md                    # Writer 페르소나
│   ├── step_03_image_system.md
│   ├── step_04_characters.md
│   ├── step_05_treatment.md
│   ├── step_06_scene_list.md
│   ├── step_07_first_draft.md
│   └── step_07_examples.md
└── critic/
    ├── system.md                    # Critic 페르소나
    ├── checkpoint_a.md
    ├── checkpoint_b.md
    ├── checkpoint_c.md
    └── step_08_visual_revision.md
prompts/intake/interview.md          # STEP I 시놉시스 인터뷰 (두 모드 공통)
prompts/webnovel/                    # 웹소설 모드 (아래 "웹소설 모드" 참고)
├── orchestrator.md
├── state_schema.json
├── analyst/  (system, step_00_addendum, step_01_series_structure, step_02_arc_beats)
├── writer/   (system, step_03_setting_bible ~ step_07_serial_writing)
└── critic/   (system, checkpoint_a~c, step_08_arc_revision)
scripts/
├── init_project.py                  # 프로젝트 초기화 (--format screenplay|web_novel)
├── count_chars.py                   # 웹소설 회차 분량 검증 (공백 제외)
├── test_count_chars.py              # count_chars.py 단위 테스트
└── md_to_docx.py                    # Markdown → .docx 변환
projects/                            # 프로젝트별 작업 디렉토리 (.gitignore)
└── {name}/
    ├── config.yaml
    ├── state.json
    ├── input/                       # 시놉시스 원본
    └── output/                      # 단계별 산출물
```

## Optional: 레퍼런스 파일 추가

다음 파일들은 저작권 문제로 저장소에 포함되어 있지 않지만, 배치하면 산출물 품질이 향상됩니다.

| 파일 경로 | 용도 |
|-----------|------|
| `prompts/writer/step_07_examples.md` | 시나리오 장면 예시 (few-shot) — 초고의 문체와 밀도 기준점 |
| `projects/{name}/input/references/` | 시나리오 작법 이론 레퍼런스 — Analyst/Critic의 분석 근거 |

이 파일들이 없어도 워크플로우는 정상 작동하며, 프롬프트 자체에 충분한 지침이 포함되어 있습니다.

## Quick Start

### 1. 프로젝트 초기화

```bash
python scripts/init_project.py my-project
```

### 2. 설정

`projects/my-project/config.yaml`을 편집하여 제목, 장르, 톤 등을 설정하고, `projects/my-project/input/`에 시놉시스 파일을 배치합니다.

시놉시스를 직접 쓰기 어려우면 비워 두고 Claude Code 세션에서 **"시놉시스 같이 쓰자"** 라고 요청하세요. 주인공·욕망·장애물·결말 등을 선택지와 함께 몇 개씩 물어보고, 답을 모아 시놉시스 초안을 써 줍니다(STEP I, `prompts/intake/interview.md`). 제목·장르·톤·테마도 답에 맞춰 `config.yaml`에 채워집니다.

### 3. 워크플로우 실행

Claude Code 세션에서:

```
이 프로젝트의 워크플로우를 시작해 주세요.
```

이전 세션에서 이어서 작업하려면:

```
워크플로우 이어서 진행해 주세요.
```

### 4. 최종 산출물 변환

```bash
pip install python-docx
python scripts/md_to_docx.py projects/my-project/output/final_screenplay.md
```

## 웹소설 모드

같은 시놉시스를 **200화 × 회차당 공백 제외 5,000자**(약 100만 자) 연재 웹소설로 확장합니다. 에이전트 역할 분리와 체크포인트 원칙은 시나리오 모드와 같고, 분량 단위가 **씬 → 회차**, 집필이 **막별 4분할 → 요청한 회차만큼 연재**로 바뀝니다. 실행 흐름은 `prompts/webnovel/orchestrator.md` 가 정의합니다.

### 1. 프로젝트 초기화

```bash
python scripts/init_project.py my-novel --format web_novel
```

`config.yaml` 의 `target_format` 이 `web_novel` 로 설정되고, `output/` 아래에 `episodes/` · `revision/` · `step_06_episode_plan/` 디렉토리가 함께 만들어집니다.

### 2. 설정 (`config.yaml` 의 `web_novel` 블록)

| 항목 | 기본값 | 의미 |
|------|--------|------|
| `total_episodes` | 200 | 총 회차 |
| `chars_per_episode` | 5000 | 회차당 목표 분량 (**공백 제외**) |
| `char_min` / `char_max` | 4800 / 5500 | 허용 범위 — 벗어나면 보강·압축 후 재검증 |
| `paywall_episode` | 25 | 유료 전환 회차 (0 이면 설계하지 않음) |
| `batch_size` | 10 | 한 요청이 이보다 크면 이 단위로 나눠 검증 |
| `platform` | — | 연재 플랫폼 (문체·관습 참고용) |

시놉시스가 없으면 **"시놉시스 같이 쓰자"** 라고 요청하세요. 시나리오 모드의 인터뷰에 더해, 독자가 기대할 재미 · 주인공의 무기 · 200화 동안 판이 커지는 방식 · 넣고 싶은 웹소설 장치(상태창, 사이다, 랭킹 등) · 사이다 대상을 추가로 묻습니다(`prompts/intake/interview.md` 라운드 6).

### 3. 워크플로우

```
STEP I  [Orchestrator + Writer]  시놉시스 인터뷰 (선택 — 시놉시스가 없을 때)
STEP 0  [Analyst]  시놉시스 사전분석 + 연재 적합성
STEP 1  [Analyst]  시리즈 3막 · 아크 8~10개 · 유료 전환 · 웹소설 장치 설계
STEP 2  [Analyst]  아크별 비트 (기승전결 + 아크 끝 절단)
        ──── Checkpoint A: 시리즈 구조 확정 ────
STEP 3  [Writer]   설정집 + 떡밥 원장
STEP 4  [Writer]   캐릭터 (아크별 성장 곡선, 호칭·말투 표)
        ──── Checkpoint B: 설정·캐릭터 확정 ────
STEP 5  [Writer]   아크 트리트먼트
STEP 6  [Writer]   회차 플롯표 (아크별 파일)
        ──── Checkpoint C: 집필 전 최종 리뷰 ────
STEP 7  [Writer]   연재 집필 — 요청한 회차만 쓰고 멈춤, 요청마다 분량 검증
        ──── Checkpoint D: 누적 10화 도달 후 1~10화 문체 확정 ────
STEP 8  [Critic → Writer]  아크를 다 쓰면 아크 퇴고 제안 (요청 시 실행)
```

시나리오 모드와 달라지는 부분:

| 구분 | 시나리오 모드 | 웹소설 모드 |
|------|--------------|------------|
| 분량 기준 | 70~85씬, 55~70페이지 | 200화 × 공백 제외 5,000자 |
| STEP 1 | 3막 구조 | 시리즈 3막 + 아크 8~10개 + 유료 전환 + 웹소설 장치 |
| STEP 3 | 이미지 시스템 | 설정집 + 떡밥 원장 |
| STEP 6 | 씬 리스트 | 아크별 회차 플롯표 |
| STEP 7 | 막별 4분할 초고 | 요청 단위 연재 집필 |
| 체크포인트 | A · B · C | A · B · C + D (문체 확정) |
| STEP 8 | 비주얼 리비전 | 아크 퇴고 |

#### 웹소설 장치

독자는 주제보다 **장치**를 보고 연재를 고릅니다. 그래서 구조 설계 단계에서 장치를 주제만큼 비중 있게 다룹니다(`prompts/webnovel/analyst/system.md`).

| 장치 | 내용 | 설계 단위 |
|------|------|-----------|
| **수치 성장** | 상태창, 레벨, 스킬·권능 해금, 업적·미션 보상 | 성장 사다리 (몇 화에 무엇이 오르나) |
| **사이다** | 무시·억압하던 상대를 통쾌하게 뒤집는 장면 | 사이다 대상 목록 + 회차 |
| **유머** | 오해 개그, 주변 반응, 주인공의 속마음 | 아크별 유머 비중 |
| **경쟁** | 랭킹·순위표, 기간 한정 이벤트, 히든 보상 | 이벤트 주기 |
| **관계** | 로맨스, 동료·파티, 라이벌 | 관계 진전 회차 |

- STEP 0 에서 시놉시스가 어떤 장치를 자연스럽게 지원하는지 점검하고, STEP 1 에서 쓸 장치를 골라 200화에 배분하며, STEP 2 에서 아크마다 작동 회차를 배치합니다
- **초반 속도** 기준: 1화 안에 장치 획득, 5화 안에 첫 사이다, 10화 안에 첫 수치 성장
- 장치 하나 이상을 주제·결말과 묶습니다. 톤이 무거워져도 장치를 끄지 않고 색을 바꿉니다
- Critic 은 체크포인트 A 와 STEP 8 아크 퇴고에서 장치가 빠진 아크·회차, 상태창 과다, 빌드업 없는 사이다를 진단합니다

### 4. 회차 집필 요청 (STEP 7)

설계(STEP 0~6)는 200화 전체를 한 번에 잡고, 집필은 **요청한 회차만 쓰고 멈춥니다.** 다음 회차를 스스로 이어 쓰지 않습니다.

| 요청 예시 | 처리 |
|----------|------|
| "다음 5화 써 줘" | 마지막으로 쓴 회차 다음부터 5화 |
| "31~35화 써 줘" | 30화까지 썼다면 그대로 집필. 건너뛴 회차가 있으면 "그 앞부터 이어서 쓸까요?"라고 되묻습니다 |
| "이어서 써 줘" | 몇 화를 쓸지 선택지(1 / 3 / 5 / 10화 / 이번 아크 끝까지)로 묻습니다 |
| "이번 아크 끝까지" | 현재 아크의 마지막 회차까지 |
| "15화 다시 써 줘" | 앞뒤 회차와 연결을 맞춰 재집필 (플롯표의 사건·절단·떡밥은 유지) |

요청마다 다음을 수행한 뒤 완료 알림(분량 통계, 새로 심은/회수한 떡밥 수, 아크 잔여 회차)을 보여 줍니다.

1. 요청 회차 집필 → `output/episodes/ep_NNN.md` 저장
2. `count_chars.py` 로 분량 검증 — 통과할 때까지 완료로 보고하지 않음
3. 누적 요약(`serial_summary.md`) · 떡밥 원장(`foreshadow_ledger.md`) · `state.json` 갱신

알림에는 상황에 따라 다음 제안이 붙습니다(실행은 요청을 기다립니다).

- **체크포인트 D** — 누적 10화가 처음 넘으면 1~10화 문체 확정을 권합니다. 1~10화는 독자가 연재를 계속 볼지 정하는 구간입니다
- **STEP 8 아크 퇴고** — 아크의 마지막 회차를 쓰면 권합니다. 미루면 이후 알림마다 "퇴고 대기 아크"를 표시합니다
- **유료 전환 구간** — `paywall_episode` 직전 3화를 쓰면 전환 직전 훅 확인을 권합니다

### 5. 연속성 유지

원고 전체(약 100만 자)를 매번 읽지 않고, 요청마다 **설정집 · 떡밥 원장 · 누적 요약** 세 문서와 해당 아크 플롯표, 직전 회차 전문만 읽고 이어 씁니다. 그래서 세 문서의 갱신은 몇 화를 쓰든 생략하지 않습니다.

이미 집필한 회차가 있는 상태에서 STEP 1~6 을 수정하면, 영향받는 회차 범위를 먼저 보여 주고 재집필 여부를 확인합니다(자동 재집필 없음).

세션을 새로 열어 **"워크플로우 이어서 진행해 주세요"** 라고 하면 진행 현황(`{마지막 회차}/{총 회차}화`, 현재 아크, 퇴고 대기 아크)을 보여 주고 몇 화를 쓸지 묻습니다.

### 6. 산출물

```
projects/my-novel/output/
├── step_00_critique.md ~ step_05_arc_treatment.md   # 설계 산출물 (STEP 3 은 설정집)
├── foreshadow_ledger.md                             # 떡밥 원장 (심기·회수 상태)
├── step_06_episode_plan/arc_01.md ~                 # 아크별 회차 플롯표
├── checkpoint_{a,b,c,d}_review.md                   # Critic 리뷰
├── serial_summary.md                                # 회차별 누적 요약
├── episodes/ep_001.md ~ ep_200.md                   # 회차 원고
└── revision/arc_XX_review.md                        # 아크 퇴고 진단
```

### 7. 분량 검증

```bash
python scripts/count_chars.py projects/my-novel/output/episodes/ --min 4800 --max 5500
python scripts/count_chars.py projects/my-novel/output/episodes/ep_011.md ep_012.md
```

- 첫 `# ` 제목 줄, 장면 전환 기호만 있는 줄(`***`, `---`, `◆` 등), HTML 주석(`<!-- -->`)은 본문에서 제외합니다
- 나머지에서 모든 공백(스페이스, 탭, 줄바꿈, 전각 공백)을 뺀 글자 수를 셉니다
- 모든 회차가 범위 안이면 종료 코드 0, 하나라도 벗어나면 1

스크립트 테스트:

```bash
python -m unittest scripts/test_count_chars.py
```

## Theoretical Foundations

| Theorist | Key Concept | Applied In |
|----------|-------------|------------|
| Syd Field | 3막 구조 | STEP 1 |
| Blake Snyder | 비트시트, 비주얼 북엔드 | STEP 2, 3 |
| Robert McKee | 이미지 시스템, 상징적 상승 | STEP 3, 8 |
| David Trottier | 화면에 보이는 것만 쓴다 | STEP 7, 8 |
| Michael Hauge | 비주얼 디테일 인물 소개 | STEP 4 |
| Linda Seger | 비주얼 리비전 프로세스 | STEP 8 |
| Tony Tost | 가상 샷 리스트 (문장=샷) | STEP 7 |
| Bong Joon-ho | 건축적 공간 메타포, 전(轉) | STEP 3, 4, 5 |
| David Mamet | "무성영화 테스트" | STEP 8 |

## Korean Screenplay Conventions

- **기본 단위**: 씬 수 (페이지 수가 아님 — 한국 시나리오는 표준화된 폰트/레이아웃이 없음)
- **90분 영화**: 70\~85씬, 55\~70페이지
- **페이지:분 비율**: 1.3\~1.5 (할리우드 Courier 12pt의 1:1이 아님)
- **용어**: 대지문, 소지문, 씬 헤딩, 대사
- **미학**: 여백의 미학 — 감독의 해석 여지를 남긴다

## Requirements

- LLM 환경 — [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://cursor.com), [Windsurf](https://windsurf.com) 등 AI 코딩 도구 또는 Claude/ChatGPT 등 LLM 대화 환경
- Python 3.8+ (유틸리티 스크립트)
- `python-docx` (최종 .docx 변환 시)

## License

This work is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

- **BY** — 출처 표시 필수
- **NC** — 상업적 사용 금지 (상업적 이용은 별도 협의)
- **SA** — 동일 조건 변경 허락 (파생물도 같은 라이선스 적용)

본 라이선스는 워크플로우 엔진(프롬프트, 스크립트, 설계 문서)에 적용됩니다. 이 도구를 사용하여 생성된 시나리오의 저작권은 사용자에게 귀속됩니다.
