# jinddo

# “맛 취향”반영 맛집 추천 시스템
---
<br>

![image](https://github.com/user-attachments/assets/bf4ab0e5-0d9b-452e-a4f6-c4bf9ba471c1)

<br>

## 팀원
---
- **김도형, 노충완, 윤종헌, 이현정, 허홍**
---
<br>


## 프로젝트 설명
---
개인화된 경험이 더욱 중요시되는 현대 사회에서 소비자는 자신의 취향에 맞는 맛집을 찾는 경우가 많습니다. 그러나 기존에 존재하는 맛집 추천 서비스들은 주로 평점 기반으로 식당을 추천합니다. 이는 개인의 ’맛’ 취향을 충분히 반영하지 못하며, 결과적으로 소비자에게 최적의 선택을 제공하지 못하게 됩니다.


궁극적으로 이 시스템은 **취향 맞춤형 추천을 하여 소비자 만족도를 높이는 맛 취향 맞춤 맛집 추천 서비스를 제공하는 것을 목표로 합니다.**

## Sources
| Source | Link |
| --- | --- |
| Project Details | [Final_Project_TEAM_3_jinddo_Notion](https://www.notion.so/jinddo-1070f0574c9180eb9598f002f358ba1f?pvs=4) |
| Data files | [Final_Project_TEAM_3_jinddo_Google_Drive](https://drive.google.com/drive/folders/1aYTy7Nf_6gi3Hzg8SPMRutISFvGKluzb) |

<br>

## 개발환경
---
Python version = 3.10


![Python Icon](https://img.icons8.com/color/48/python--v1.png) ![Numpy Icon](https://img.icons8.com/color/48/numpy.png) ![JupyterNotebook Icon](https://img.icons8.com/fluency/48/jupyter.png) ![VSCode Icon](https://img.icons8.com/dusk/64/visual-studio.png) ![pandas Icon](https://img.icons8.com/color/48/pandas.png) ![slack Icon](https://img.icons8.com/doodle/48/slack-new.png) ![google_drive Icon](https://img.icons8.com/color/48/google-drive--v2.png) ![notion Icon](https://img.icons8.com/color/48/notion--v1.png) 

<br>

## Github Convention
___
기본 브랜치: main

- COMMIT_TYPE
    - feat : 새로운 기능 추가
    - fix : 버그 수정
    - docs : 문서 추가 및 수정
    - style : 코드 포맷팅, 세미콜론 누락, 오타 수정 등
    - test : 테스트코드
    - refactor : 코드 리팩토링
    - chore : 빌드 업무 수정, 패키지 매니저 수정
- COMMIT_SUMMARY
    - 영어로 작성
    - 마침표를 붙이지 않음
    - 50자를 넘기지 않음

<br>

## Github Upload Procedure
---
1. create (if not already created) a branch with appropriate branch name (eg. feat/crawling/naver)
```bash
git checkout -b branch_name
```

- If the branch is already created, simply do

```bash
git checkout branch_name
```

2. add modified files that needs to be pushed
```bash
git add .
```

3. commit changes with appropriate commit message
```bash
git commit -m '[#(issue_ID)] COMMIT_TYPE: COMMIT_SUMMARY ([related MR_ID])'
```

4. push the commit to local branch
```bash
git push origin branch_name
```

5. Go to github repository and click on 'Compare & Pull Request'
6. compare and Merge. Delete the branch after merged
7. Delete the branch in local repository
```bash
git checkout main
git branch -D branch_name
```

<br>

## Github Ground Rules
---
1. Create Issue for the current task that you are working on
2. Notify teammates after pull requests
3. **Never** push anything or work on main branch
