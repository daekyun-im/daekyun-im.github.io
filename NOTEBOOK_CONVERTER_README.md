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
- `_posts/2025-12-24-your_notebook.md` 파일을 생성합니다
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
# 변환
python convert_notebook.py my_notebook.ipynb

# Git에 추가 및 커밋 (하나의 .md 파일만!)
git add _posts/*.md
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
