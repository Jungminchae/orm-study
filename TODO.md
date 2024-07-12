# TODO

## Contributor분들에게 요청합니다. 다음 요소들을 추가해보시겠습니까?

- [ ] `orm_study/quiz/command.py`안에 start 함수의 로직 중 `solve_quiz` 앞 뒤로 시간을 기록하는 로직이 있습니다. solve_quiz에 데코레이터를 씌우는 방식으로 코드를 수정해볼 수 있을까요?
- [ ] `orm_study/quiz/command.py`안에 새로운 command를 추가해보고 싶습니다. 명령 이름은 exam으로 해보고 싶은데요. `ost quiz exam`으로 실행하면 몇 문제를 시험 볼 것인지 물어봅니다. 문제는 최소 15문제로 하고 싶습니다. 현재 존재하는 챕터의 모든 문제를 가져와서 셔플한 뒤 입력받은 문제 수만큼 출제하고 싶어요.
