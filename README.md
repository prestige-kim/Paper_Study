# Paper Study for Codex

논문을 근거가 연결된 한국어 학습 노트로 분석하는 **Codex용 스킬**입니다.
빠른 요약, 심층 분석, 비판·재현성 검토, 여러 논문 비교를 지원합니다.
실험·계산 연구뿐 아니라 이론·정성 연구·리뷰 논문의 구조에 맞춰 분석합니다.

## 설치

Codex에 다음 요청을 입력합니다.

```text
$skill-installer https://github.com/TLAB-HGU/Paper_Study/tree/main/skills/paper-study
```

개인 저장소의 같은 경로에서도 설치할 수 있습니다.
수동 설치는 저장소를 다운로드하고 `skills/paper-study/` 폴더 전체를 다음 위치 중 하나에 복사합니다.

- 개인: `~/.agents/skills/paper-study/`
- 프로젝트: `<project>/.agents/skills/paper-study/`

이미 같은 이름의 스킬이 설치되어 있으면 기존 폴더를 백업한 뒤 교체합니다.
`~/.codex/skills/paper-study/`에 기존 설치가 있다면 함께 확인해 중복 설치를 피합니다.
설치 후 새 채팅에서 `$paper-study`를 선택합니다. 보이지 않으면 Codex를 재시작합니다.

## 사용법

논문 PDF를 첨부하거나 로컬 경로·HTML·DOI·arXiv 링크를 제공하고 요청합니다.

| 목적 | 요청 예시 |
|---|---|
| 빠른 요약 | `$paper-study 이 논문을 핵심만 5분 안에 이해할 수 있게 요약해줘.` |
| 심층 분석 | `$paper-study 이 논문을 방법·근거·한계·학습 질문까지 한국어로 분석해줘.` |
| 비판·재현성 | `$paper-study 실험 설계와 재현 가능성을 검토하고 원문 근거를 연결해줘.` |
| 논문 비교 | `$paper-study 첨부한 두 논문의 방법과 평가 조건을 비교해줘.` |

기본 결과는 채팅에 표시합니다. 파일이 필요하면 “Markdown 파일로 저장해줘”처럼 요청합니다.
모드는 요청 내용으로 결정되며, 별도 명령행 옵션이 아닙니다.

## 실행 환경

별도 Python·Node.js 환경이나 추가 LLM API 키를 요구하지 않는 지침형 스킬입니다.
로컬 입력에는 Codex의 파일 읽기 권한이, 온라인 입력에는 웹·네트워크 접근이 필요합니다.
PDF는 사용 환경의 텍스트 추출·페이지 확인 도구를 활용합니다. Poppler 또는 PyMuPDF는 선택 사항입니다.
스캔 PDF에는 이미지 읽기 또는 OCR이 필요하며, 표·그림·수식은 읽을 수 있는 범위에서 확인합니다.
도구나 전문이 없으면 확인 가능한 범위와 빠진 근거를 밝히고 필요한 입력을 안내합니다.

구체적인 처리 순서는 [입력·실패 대응](skills/paper-study/references/input-handling.md)을 참고하세요.
Codex에서 사용하는 패키지로 검증하며, 다른 제품의 호환성은 별도로 검증하지 않았습니다.

## 배포 구조와 검증

```text
skills/paper-study/
  SKILL.md
  LICENSE
  agents/openai.yaml
  references/
README.md
LICENSE
```

`main`에는 배포 파일만, `dev`에는 개발·검증 자료를 함께 보관합니다.
**초기 배포판 v0.1.0 / 2026-10-02:** 패키지 형식·독립 복사·Codex 스킬 인식 검사와
논문 4편을 사용한 9개 분석·부분 입력·실패 대응 사례를 검증했습니다.
검증 기록은 [dev의 검증 보고서](https://github.com/TLAB-HGU/Paper_Study/blob/dev/validation/README.md)에서 확인할 수 있습니다.
스킬은 원문 대조를 돕는 지침이며 모든 논문·모델·환경에서의 정확도를 보증하지 않습니다.

[공식 Codex 설치 안내](https://learn.chatgpt.com/docs/build-skills) · [MIT License](LICENSE)
스킬의 MIT 라이선스는 분석 대상 논문과 데이터의 이용 조건을 변경하지 않습니다.
