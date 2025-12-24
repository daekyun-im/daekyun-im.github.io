# Jupyter Notebook to Jekyll Markdown Converter

Jupyter notebook (.ipynb) 파일을 Jekyll 블로그용 Markdown 파일로 자동 변환하는 도구입니다.

## 주요 기능

- ✅ Jupyter notebook의 모든 코드 셀을 Markdown 코드 블록으로 변환
- ✅ Markdown 셀 그대로 유지
- ✅ 코드 실행 결과 (print 출력, display 결과) 포함
- ✅ matplotlib, seaborn 등의 그래프를 base64로 인코딩하여 하나의 .md 파일에 포함
- ✅ pandas DataFrame HTML 출력 포함
- ✅ **하나의 .md 파일만 업로드하면 모든 그래프와 코드가 표시됩니다!**
- ✅ Jekyll front matter 자동 생성

## 사용 방법

### 1. 기본 사용법

```bash
python convert_notebook.py your_notebook.ipynb
```

이 명령어는:
- `your_notebook.ipynb`를 읽어서
- **현재 디렉토리**에 `your_notebook.md` 파일을 생성합니다
- **모든 그래프 이미지를 base64로 인코딩하여 .md 파일에 포함합니다**

### 2. 제목과 카테고리 지정

```bash
python convert_notebook.py your_notebook.ipynb \
    -t "나의 데이터 분석 프로젝트" \
    -c "data-science" \
    --tags python pandas matplotlib
```

### 3. 출력 경로 직접 지정

```bash
python convert_notebook.py your_notebook.ipynb -o custom_path.md
```

## 명령어 옵션

```
python convert_notebook.py [-h] [-o OUTPUT] [-t TITLE] [-c CATEGORIES]
                           [--tags TAGS [TAGS ...]] notebook

필수 인자:
  notebook              변환할 .ipynb 파일 경로

선택 인자:
  -h, --help            도움말 표시
  -o OUTPUT, --output OUTPUT
                        출력 .md 파일 경로
  -t TITLE, --title TITLE
                        포스트 제목
  -c CATEGORIES, --categories CATEGORIES
                        포스트 카테고리 (기본값: coding)
  --tags TAGS [TAGS ...]
                        포스트 태그 (기본값: python jupyter)
```

## 예제

### 예제 1: 머신러닝 프로젝트

```bash
python convert_notebook.py ml_analysis.ipynb \
    -t "타이타닉 생존 예측 분석" \
    -c "machine-learning" \
    --tags python pandas scikit-learn
```

### 예제 2: 데이터 시각화

```bash
python convert_notebook.py visualization.ipynb \
    -t "matplotlib과 seaborn으로 데이터 시각화하기" \
    -c "data-visualization" \
    --tags python matplotlib seaborn

# 결과: visualization.md 파일 생성
```

## 변환 결과

변환된 Markdown 파일은 다음과 같은 구조를 가집니다:

```markdown
---
layout: single
title: "제목"
categories: coding
tag: [python, jupyter]
toc: true
author_profile: false
---

# Markdown 셀 내용

\```python
# 코드 셀
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
\```

![output](data:image/png;base64,iVBORw0KGgoAAAANS...)
```

## 다른 폴더의 파일 변환

```bash
# Downloads 폴더의 notebook 변환
python convert_notebook.py ~/Downloads/titanic_analysis.ipynb
# 결과: 현재 디렉토리에 titanic_analysis.md 생성

# 다른 폴더의 notebook 변환
python convert_notebook.py ../notebooks/data_analysis.ipynb
# 결과: 현재 디렉토리에 data_analysis.ipynb 이름 그대로 data_analysis.md 생성
```

**중요:** 어디에 있는 파일이든 변환 가능하며, 생성된 .md 파일은 항상 **현재 작업 디렉토리**에 원본 파일명과 동일한 이름으로 저장됩니다!

## 이미지 검증 및 미리보기

변환된 .md 파일의 이미지가 올바르게 인코딩되었는지 확인하려면:

```bash
# 기본 검증
python validate_markdown.py your_notebook.md

# 검증 + HTML 미리보기 생성
python validate_markdown.py your_notebook.md --preview

# 검증 + 상세 디버그 리포트 생성 (문제 발생 시)
python validate_markdown.py your_notebook.md --debug

# 원본 notebook도 함께 분석
python validate_markdown.py your_notebook.md --debug --notebook your_notebook.ipynb
```

검증 스크립트는:
- ✅ base64 데이터에 줄바꿈 문자가 있는지 확인
- ✅ base64 데이터가 유효한지 디코딩 테스트
- ✅ PNG/JPEG 헤더가 올바른지 검증
- ✅ 각 이미지의 크기 표시
- ✅ HTML 미리보기 파일 생성 (--preview 옵션)
- ✅ 상세 디버그 리포트 생성 (--debug 옵션)

### 문제 발생 시 디버그 리포트 생성

이미지가 깨져 보이면 `--debug` 옵션으로 자동 진단 리포트를 생성하세요:

```bash
python validate_markdown.py my_analysis.md --debug --notebook my_analysis.ipynb
```

생성된 `debug_report_YYYYMMDD_HHMMSS.txt` 파일에는:
- 시스템 정보 (OS, Python 버전)
- 파일 정보 (크기, 경로)
- 각 이미지의 상세 분석 (base64 길이, 줄바꿈 여부, 디코딩 가능 여부)
- 원본 notebook의 이미지 구조 분석
- 문제 보고용 템플릿

**이 리포트 파일을 공유하면 문제를 빠르게 해결할 수 있습니다!**

## 지원하는 출력 형식

- ✅ 텍스트 출력 (print 문)
- ✅ PNG 이미지 (matplotlib, seaborn 등)
- ✅ JPEG 이미지
- ✅ SVG 이미지
- ✅ HTML (pandas DataFrame 등)
- ✅ 일반 텍스트 결과
- ✅ 에러 트레이스백

## Git에 커밋하기

변환 후 GitHub에 push하려면:

```bash
# 블로그 레포지토리의 _posts 디렉토리로 이동
cd /path/to/your-blog/_posts

# 변환 (현재 디렉토리에 .md 파일 생성)
python /path/to/convert_notebook.py /path/to/notebook.ipynb

# 또는 스크립트가 PATH에 있다면
python convert_notebook.py ~/Downloads/my_notebook.ipynb

# Git에 추가 및 커밋 (하나의 .md 파일만!)
git add *.md
git commit -m "Add: Jupyter notebook post"
git push
```

## 장점

- **하나의 파일로 모든 것 관리**: .md 파일 하나만 업로드하면 끝!
- **이미지 링크 깨질 걱정 없음**: 모든 이미지가 파일에 포함되어 있습니다
- **간편한 버전 관리**: 여러 파일을 관리할 필요 없이 하나의 파일만 관리
- **즉시 사용 가능**: 추가 패키지 설치 불필요 (Python 표준 라이브러리만 사용)

## 주의사항

- **파일 크기**: base64 인코딩은 원본 이미지보다 약 33% 더 큽니다. 그래프가 많은 경우 .md 파일이 커질 수 있습니다.
- **GitHub 제한**: 일반적으로 문제없지만, 매우 큰 파일(100MB+)은 GitHub에서 경고가 발생할 수 있습니다.
- **Python 버전**: Python 3.6 이상 필요
