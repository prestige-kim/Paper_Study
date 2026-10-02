# Paper Study 검증 기록

이 디렉터리는 `dev` 브랜치의 개발 자료입니다. 설치할 때 복사할 필요가 없습니다.

## 검증 방법과 범위

- 날짜: 2026-10-02, macOS 환경.
- 배포 패키지: `skills/paper-study/`, 초기 구현 커밋 `4e97212de2f6a6fbf5e918aff70526fdcb591d69`.
- 설치 인식: Codex CLI 0.159.3의 app-server `skills/list`로 새 임시 Git 프로젝트의 `.agents/skills/paper-study/`를 확인했습니다. 모델 호출 없이 이름·활성화·repo 범위·UI 메타데이터를 확인했습니다.
- 구조: 공식 `skill-creator` 검증기와 자체 패키지 검사를 실행했습니다. 참조·개인 경로 의존성·UI·스킬 안의 라이선스·독립 복사를 검사하고, 라이선스와 참조 문서가 빠진 설치본의 거부를 확인했습니다.
- 행동: 실제 PDF를 입력한 Codex 평가 작업자가 답변을 만들고, 주 작업자(Codex)가 원문 텍스트·표·페이지 이미지와 대조합니다. 두 작업자는 새 문맥에서 빠른 요약/학습 노트 및 비판/비교를 실행하며, 경계 입력 담당 작업자는 기존 작업자에게 별도 지시를 전달해 실행합니다. 리뷰 논문은 학습 노트 작업자에게 추가 요청했습니다. 기대 답안은 실행 작업자에게 제공하지 않습니다. 사람 전문가의 검토는 포함하지 않았습니다.
- 도구: 구조 검사 Python 3.12.14·PyYAML 6.0.3, 페이지 추출/렌더링 Poppler 26.09.0. 실행 기록은 각 작업자가 사용한 도구와 확인 범위를 별도로 기록합니다.

평가 작업자는 부모의 모델 설정을 상속했습니다. 평가 도구가 정확한 모델 ID를 제공하지 않아 모델별 점수나 성능 순위로 해석할 수 없습니다. 여러 모델·운영체제·새로운 분야에 대한 대규모 벤치마크가 아닙니다. 논문을 분석한 결과의 검증이며, 원 논문의 모델 학습이나 실험을 재현한 것은 아닙니다.

## 입력과 판본

| 입력 | 확인한 판본 | 사용 |
|---|---|---|
| Deep Residual Learning for Image Recognition | CVPR 2016 / CVF Open Access, 인쇄 pp. 770–778, PDF 9쪽. 본문에서 참조하는 탐지 부록은 미포함. | 빠른 요약·학습 노트·비판·비교 |
| Densely Connected Convolutional Networks | CVPR 2017 / CVF Open Access, 인쇄 pp. 4700–4708, PDF 9쪽. | 비교 |
| A Computational Approach to Edge Detection | IEEE TPAMI 8(6), 1986, 인쇄 pp. 679–698, PDF 20쪽. 수학적 분석과 계산·이미지 검증을 포함하는 비신경망 논문. | 논문 유형 적응 |
| 빅데이터 활용을 위한 기계학습 기술동향 | 전자통신동향분석 27(5), 2012년 10월, 인쇄 pp. 55–63, PDF 9쪽. | 리뷰·동향 논문 적응 |
| 초록만 있는 자료 | ResNet 초록 내용을 바꾸어 쓴 제한 입력 fixture. 전문·부록 없음. | 접근 범위·미확인 정보 처리 |
| 첫 페이지 이미지 | ResNet PDF 첫 페이지의 120 DPI 렌더. 다른 페이지 사용 불가. | 이미지 입력·부분 분석 |
| 존재하지 않는 PDF | `missing-paper.pdf`, 네트워크 접근 없음. | 입력 실패 대응 |

원본 PDF·추출 전문·페이지 이미지는 저장소에 포함하지 않습니다. [inputs.json](inputs.json)에 출처와 SHA-256을 기록하고, [abstract-only.txt](abstract-only.txt)에는 직접 작성한 제한 입력만 제공합니다. 원본 권리와 이용 조건은 각 논문에 따릅니다. 출처 URL의 현재 접근 성공과 로컬 PDF 판본의 확인은 별개이며, CVF 페이지 조회는 403, IEEE DOI 페이지는 브라우저 확인 요구로 전문을 읽지 못했습니다. ETRI의 공식 PDF에서는 제목·저자·발행연도·페이지를 확인했습니다. 이번 행동 검증은 모두 제공된 로컬 입력을 사용했습니다.

## 기록

- [사용 요청](cases.json)과 [의미 중심 평가 기준](criteria.json)
- [패키지 검사 결과](package-check.json)
- [Codex 스킬 인식 결과](discovery-check.json)
- [개인·랩실 저장소의 공개 다운로드 설치 결과](installation-check.json): 공식 `skill-installer`의 ZIP 다운로드로 각각 임시 설치했고, 스킬 파일 6개와 포함된 라이선스가 검증 패키지와 모두 일치했습니다. 배포 `main` 커밋은 `8ddb940`이며, 설치로 기존 개인 스킬을 덮어쓰지 않았습니다.
- `outputs/`: 실제 사용자 답변, `runs/`: 실행 작업자가 보고한 참조·도구·확인 범위

결과와 수치의 최종 원문 대조는 [results.json](results.json)에 기록합니다. 문구·제목·정규식 일치만으로 논문 해석의 정확도를 채점하지 않습니다. 공개 답변과 로그에서는 개인 절대 경로를 재현용 상대 경로로 치환하고, 논문 파일 링크는 입력 목록을 가리키도록 바꿨습니다. 분석 내용은 유지하며 변경 전후 해시는 [publication.json](publication.json)에 기록합니다. 로그의 `human_reading_checks`는 실제 수행 주체를 명확히 하도록 `agent_reading_checks`로 정정했습니다.

## 재검증

Python 3.9+와 PyYAML은 개발용 검사에만 필요합니다. 분석 스킬 자체의 설치 의존성이 아닙니다.

```bash
python3 -m pip install PyYAML
python3 validation/check_package.py skills/paper-study
python3 validation/check_discovery.py skills/paper-study
```

인식 검사에는 `codex` CLI와 Git이 필요합니다. CLI가 PATH에 없다면 `--codex-executable /path/to/codex`로 지정합니다. Codex app-server는 사용자 상태 DB 접근이 필요하므로 읽기만 허용하는 샌드박스에서는 실행이 실패할 수 있습니다. 사용자 설정을 변경하거나 모델 턴을 시작하지 않습니다.

행동 검증은 다음 순서로 반복합니다.

1. `inputs.json`의 논문 판본을 확보해 작업용 `sources/`에 두고 SHA-256과 페이지 범위를 확인합니다. 다른 파일이면 판본·페이지 차이를 기록하고 기존 위치를 무조건 재사용하지 않습니다.
2. `abstract-only.txt`를 `sources/`로 복사하고, ResNet 첫 페이지를 이미지로 렌더링합니다. `missing-paper.pdf`는 만들지 않습니다.
3. 설치한 `$paper-study`에 `cases.json`의 요청을 전달합니다. 부분 입력 사례에서는 다른 전문·웹·기억으로 근거를 보충하지 않습니다. 반복 평가에서는 모델 ID·추론 수준·클라이언트·도구·스킬 판본도 기록합니다.
4. 각 답변과 확인 범위를 보관하고, 별도 검토자가 `criteria.json`에 따라 원문과 대조합니다. 수치·평가 조건·출처 오류가 있으면 실패로 기록하고 지침을 수정한 뒤 해당 사례를 재실행합니다.

이번 이미지 입력은 PDF 전체를 스캔한 파일을 직접 처리한 검증이 아닙니다. 전체 스캔 PDF, 실제 OCR 엔진, HTML 전문·온라인 DOI/arXiv 버전 해결, 순수 증명 논문과 정성 연구, 다른 제품의 호환성은 후속 검증 대상입니다.

[공식 스킬 평가 안내](https://developers.openai.com/blog/eval-skills)
