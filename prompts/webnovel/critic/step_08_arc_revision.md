# Critic → Writer — STEP 8: 아크 퇴고 (웹소설)

아크의 마지막 회차를 쓴 뒤, 사용자가 요청하면 실행한다. 체크포인트 D(1~10화 문체 확정)에서도 이 문서를 쓴다.

## 입력 컨텍스트

- `projects/{name}/output/episodes/ep_{아크 시작}.md` ~ `ep_{아크 끝}.md` — 대상 회차 원고 전부
- `projects/{name}/output/step_06_episode_plan/arc_XX.md` — 해당 아크 플롯표
- `projects/{name}/output/step_03_setting_bible.md`
- `projects/{name}/output/step_04_characters.md`
- `projects/{name}/output/foreshadow_ledger.md`
- `projects/{name}/output/serial_summary.md`

아크가 길어 한 번에 읽기 어려우면 10화씩 진단한 뒤 합친다.

## 1단계: 분량 재확인

```
python scripts/count_chars.py projects/{name}/output/episodes/ep_{시작}.md ... ep_{끝}.md --min {char_min} --max {char_max}
```

결과 표를 리뷰 첫머리에 붙인다. 범위를 벗어난 회차는 그 자체로 결함이다.

## 2단계: Critic 진단 — 8개 패스

각 패스는 **회차 번호 + 인용**으로 문제 위치를 적는다.

| # | 패스 | 찾는 것 |
|---|------|---------|
| 1 | 첫 문단 | 직전 절단을 3문장 안에 못 받는 회차, 요약으로 시작하는 회차 |
| 2 | 절단 | 절단이 약하거나 없는 회차, 같은 유형 3연속 |
| 3 | 진전 | 공회전 회차, 같은 정보를 2회 이상 서술한 구간(분량 채우기) |
| 4 | 리듬 | 고구마 3화 초과, 보상 간격 5화 초과 (플롯표가 아니라 **실제 원고** 기준) |
| 5 | 서술 | 감정 이름표, 정보 덤프, 시점 이탈, 4문장 이상 문단, 대사·서술 혼합 문단 |
| 6 | 연속성 | 설정집·캐릭터 표·누적 요약과 어긋나는 표기·호칭·능력·사실 |
| 7 | 떡밥 | 계획대로 심거나 회수하지 않은 떡밥, 원장 상태와 원고 불일치 |
| 8 | 장치 | 플롯표에 배정된 장치(성장·사이다·유머·경쟁·관계)가 원고에서 작동하지 않는 회차, 상태창 과다, 빌드업 없는 사이다 |

STEP 8에서는 예외적으로 **수정 방향**까지 적는다 (예: "37화 둘째 장면 — 설정 설명 6문단 → 주인공이 필요한 순간 발견하는 방식으로 분산"). 구체적 문장은 쓰지 않는다.

### 체크포인트 D 모드 (1~10화)

위 8개 패스에 다음을 추가한다:
- **1화 첫 5문장**에 주인공·상황·이상 신호가 있는가
- **5화 이내**에 주인공의 목표가 확정되는가
- 문체 기준표 작성: 평균 문단 길이, 대사 비율, 내면 서술 비율, 절단 방식 — 이후 집필이 따를 기준

## 3단계: 판정

- 패스 8개 모두 문제 없음 → `pass`
- 문제 있는 패스 1~2개 → `conditional_pass` (Writer가 반영 후 진행)
- 문제 있는 패스 3개 이상, 또는 연속성(6) 치명 충돌 → `rework_needed` (사용자 보고)

## 출력 형식

```markdown
# 아크 {k} 퇴고 진단 ({시작}~{끝}화)   ← 체크포인트 D면 "체크포인트 D: 문체 확정 (1~10화)"

## 종합 평가: [pass | conditional_pass | rework_needed]

## 분량
(count_chars.py 결과 표)

## 패스별 진단
### 1. 첫 문단
| 회차 | 위치·인용 | 문제 | 수정 방향 |
...
### 7. 떡밥

## (체크포인트 D만) 문체 기준표
| 항목 | 1~10화 실측 | 이후 기준 |

## 수정 대상 회차 목록
```

저장:
- 아크 퇴고: `projects/{name}/output/revision/arc_XX_review.md`
- 체크포인트 D: `projects/{name}/output/checkpoint_d_review.md`

## 4단계: Writer 반영

1. `prompts/webnovel/writer/system.md` 로 페르소나 전환
2. "수정 대상 회차 목록"의 회차만 수정해 같은 파일에 덮어쓴다
3. 수정한 회차를 `count_chars.py` 로 재검증
4. 수정으로 사실관계가 바뀌었으면 `serial_summary.md` 해당 회차 요약과 `foreshadow_ledger.md` 를 갱신
5. 수정 내역을 리뷰 파일 끝에 `## 반영 결과` 로 추가 (회차별 한 줄)
