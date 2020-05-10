# pytest
## pytest 설치
$ python -m pip install pytest <br>
$ python -m pip install pytest-cov <br>
## pytest 실행
$ pytest -v [test_file_name] <br>
$ pytest -v -s [test_file_name] <br>
=> 실행되는거 모두 보여지도록 <br>
$ pytest -v --cov=. <br>
=> coverage % 확인가능(모두 100%가 되면 모든걸 test했다는 의미) <br>
$ coverage html <br>
=> coverage 된 부분과 missing된 부분 알 수 있다. <br>
## output 파일 생성하기
$ pytest -v --cov=. > output.txt <br>
git bash 에서 실행, coverage결과를 output.txt파일에 저장
