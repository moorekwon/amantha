# 아만다 클론 앱 API 문서

Base URL: `http://13.209.3.115:88/api`



## 인증

### Basic Auth

[DRF 라이브러리](https://www.django-rest-framework.org/api-guide/authentication/#basicauthentication)에서 제공하는 토큰 인증 방식

Token 인증보다 더 빠른 인증으로, <u>**dev test용**</u>으로 사용

- 실제 production에서는 비적합

- production에서 사용하는 경우 API가 `https`를 통해서만 사용 가능해야 함



client에서는 해당 email과 password로 서명된 HTTP 기본 인증을 사용

권한이 거부된 인증되지 않은 응답은 `HTTP 401 Unauthorized` 응답을 리턴



### Token Auth

[DRF 라이브러리](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)에서 제공하는 토큰 인증 방식

**<u>실제 production</u>**에서 사용할 인증 방식

HTTP Header의 `Authorization` 키에 `Token <value>` 값을 넣어 전송

`<value>`에 들어가는 값은 Token을 발급받는 API(AuthToken)에 자격증명(email과 password)를 전달 후 받은 **token** 값을 사용

client에서는 해당 **token**을 로그인을 유지하는 동안 로컬 저장소에 저장 후, 매 HTTP Request마다 Header에 인증 값을 전송하는 형태로 세션 유지



ex) 전송하는 HTTP Header의 형태

```json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

ex) curl 사용하여 test 하는 법

```shell
curl -X GET http://13.209.3.115:88/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```



## User Account

### User Login

- URL: `/auth/token/`

- Method: `POST`

- Request Sample

  - URL: http://13.209.3.115:88/api/auth/token/

  - Body

    ```json
    {
    	"email": "esb@esb.com",
    	"password": "esb"
    }
    ```

- Response Sample

  ```json
  {
      "token": "0e1e2a89b67b0ed80ed5b62d40794919959f3886",
      "user": {
          "pk": 1,
          "email": "esb@esb.com",
          "gender": "여자"
      }
  }
  ```



### User List

- URL: `/auth/token/`

- Method: `GET`

- Request Sample

  - URL: http://13.209.3.115:88/api/auth/token/

- Response Sample

  ```json
  {
      "login": [
          {
              "pk": 2,
              "email": "hjk@hjk.com",
              "gender": "여자"
          }
      ],
      "logout": [
          {
              "pk": 1,
              "email": "esb@esb.com",
              "gender": "여자"
          }
      ]
  }
  ```



### User Signup

- URL: `/auth/create/`

- Method: `POST`

- Request Sample

  - URL: http://13.209.3.115:88/api/auth/create/

  - Body

    ```json
    {
    	"email": "hjk@hjk.com",
    	"password": "hjk",
    	"gender": "여자"
    }
    ```

- Response Sample

  ```json
  {
      "token": "6c870788d5afc2689728571ac7de03350842c1a8",
      "user": {
          "pk": 2,
          "email": "hjk@hjk.com",
          "gender": "여자"
      }
  }
  ```




### User Logout

- URL: `/auth/logout/`

- Method: `GET`

- Request Sample

  - URL: http://13.209.3.115:88/api/auth/logout/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: esb@esb.com
       - Password: esb

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  ```json
  "로그아웃 되었습니다."
  ```



## User Social Account

### Kakaotalk Login

- URL: `/auth/kakao/`

- Method: `POST`

- 카카오톡 로그인 링크 주소: https://kauth.kakao.com/oauth/authorize?client_id=76b2956e73b28279536c31c5fe24562a&redirect_uri=http://13.209.3.115:88/api/auth/kakao/&response_type=code

  - ***아마 위 주소를 iOS팀에게 받아야 하는 것 같아요***

- 카카오톡 연결 계정: email *(email 외 gender 등 연결정보 사이트에서 설정할 수 있음)*

- Request Sample

  - URL: http://13.209.3.115:88/api/auth/kakao/

  - Body

    user의 access token 값을 받아 gender 정보와 함께 json 형식으로 Body 정보에 넣음

    ```json
    {
    	"accessToken": "FASowF-QPcTiwc1gIVxwGdkso4usMvOQl3d2pgorDNQAAAFxSTSrcQ",
    	"gender": "여자"
    }
    ```

- Response Sample

  ```json
  {
      "user": {
          "pk": 2,
          "email": "raccoonhj33@naver.com"
      },
      "token": "f7711b3626fce957a0d00370215f46e55362d5f1"
  }
  ```



### Apple Login

*추후 업데이트*



## User Profile

### User All Info View

- URL: `/user/profile/`

- Method: `GET`

- **User별 Image, Info, Story, Tag 정보, 보유 ribbon, 등 전체 정보 표시**

- Request Sample

  - URL: http://13.209.3.115:88/api/user/profile/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: esb@esb.com
       - Password: esb

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  *tags 부분 추후 업데이트*

  ```json
  {
      "userProfile": {
          "email": "esb@esb.com",
          "gender": "여자",
          "currentRibbon": 10,
          "profilePercentage": 71.4,
          "sendMeLikeUsers": [
              "hgo@hgo.com",
              "hbb@hbb.com"
          ],
          "images": [
              {
                  "pk": 1,
                  "image": "https://amantha.s3.amazonaws.com/profile_images/esb.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200405%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200405T094447Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=40b1898f937f7072814351384b272bfd2adb312641ffecd19f6c253b3f8ec152"
              },
              {
                  "pk": 2,
                  "image": "https://amantha.s3.amazonaws.com/profile_images/esb.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200405%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200405T094447Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=40b1898f937f7072814351384b272bfd2adb312641ffecd19f6c253b3f8ec152"
              },
              {
                  "pk": 3,
                  "image": "https://amantha.s3.amazonaws.com/profile_images/esb2.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200405%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200405T094447Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=8b60f2346c82adf14a1ea8ea2785b4b55e3a7665c8680012a87e4750127f6441"
              },
              {
                  "pk": 4,
                  "image": "https://amantha.s3.amazonaws.com/profile_images/esb3.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200405%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200405T094447Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=9a5637672e810c18a15a21880c8841b974daef8ec7cd4635074df6bf1a4b24f8"
              }
          ],
          "info": {
              "pk": 1,
              "averageStar": 3.72,
              "nickname": "은순이",
              "school": "",
              "major": "정치외교학과",
              "job": "회사원",
              "company": "외국계 회사",
              "region": 1,
              "birth": "1995-04-30",
              "age": 26,
              "tall": "164",
              "bodyShape": 1,
              "personality": 2,
              "bloodType": 1,
              "smoking": 2,
              "drinking": "",
              "religion": "",
              "introduce": "안녕하세요 반가워요^^"
          },
          "stories": [
              {
                  "pk": 1,
                  "story": 1,
                  "content": "조용한 카페"
              }
          ],
          "tags": []
      }
  }
  ```



### User Image Add

- URL: `/user/image/`

- Method: `POST`

- User별 image들 추가

- 보낸 이미지 파일(들)은 AWS S3 버킷에 업로드됨

- Request Sample

  - URL: http://13.209.3.115:88/api/user/image/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hjk@hjk.com
       - Password: hjk

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    **form-data** 체크, KEY에서 **File** 체크, VALUE에서 이미지 파일 선택

    ***(POSTMAN에서는 파일이름이 한글일 경우 에러가 뜸..)***
  
    | KEY    | VALUE     |
    | ------ | --------- |
    | images | hjk2.jpeg |
    | images | hjk.jpg   |
  
- Response Sample

  ```json
  {
      "images": [
          {
              "pk": 1,
              "image": "https://amantha.s3.amazonaws.com/profile_images/hjk2.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200405%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200405T074656Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=8c1056ebf35e6ff001727ebc0842c961388c0a9b6e84a1ab2a842dfaddef6b31"
          },
          {
              "pk": 2,
              "image": "https://amantha.s3.amazonaws.com/profile_images/hjk.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200405%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200405T074656Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=4351590aa924f5321bc742d4d4e2a45115ed23457ed62cab98325ee3877276c2"
          }
      ]
  }
  ```



### User Image Delete

- URL: `/user/image/<int:pk>/`

  - URL 주소에 붙은 pk 번호를 통해 User별 각 image 객체에 접근

- Method: `DELETE`

- User별 image 객체 삭제

- Request Sample

  - URL: http://13.209.3.115:88/api/user/image/1/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hjk@hjk.com
       - Password: hjk

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  ```json
  "해당 이미지가 삭제되었습니다."
  ```



### User Image List

- URL: `/user/image/`

- Method: `GET`

- User별 image들 조회

- Request Sample

  - URL: http://13.209.3.115:88/api/user/image/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hjk@hjk.com
       - Password: hjk

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  User의 계정 정보와 이미지 정보 표시

  ```json
  {
      "user": {
          "pk": 2,
          "email": "hjk@hjk.com",
          "gender": "여자"
      },
      "images": [
          {
              "pk": 1,
              "image": "https://amantha.s3.amazonaws.com/profile_images/hjk2.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200405%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200405T080726Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=bd05ec18231f176e2f369c015db8f5e9dcf2b29847af2f5f425b137cb89865ad"
          },
          {
              "pk": 2,
              "image": "https://amantha.s3.amazonaws.com/profile_images/hjk.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200405%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200405T080726Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=3c19e70d77cba404c1475887643a9c0a8a85c7956f8fd6eb69803fd5f4734d97"
          }
      ]
  }
  ```



### User Info Create

- URL: `/user/info/`

- Method: `POST`

- User 계정 생성 후 상세프로필 정보 넣기 **(처음 한 번만 POST 가능)**

- **User의 이미지, 스토리, 관심태그, 리본 정보 외 프로필 정보 접근**

- Request Sample

  - URL: http://13.209.3.115:88/api/user/info/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hjk@hjk.com
       - Password: hjk

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    - 필수 정보: `nickname`, `birth`

    - 옵션 정보: `school`, `major`, `job`, `company`, `region`, `tall`, `bodyShape`, `personality`, `bloodType`, `smoking`, `drinking`, `introduce`, `religion`
    - 고정된 value를 가진 정보
      - 아래 정해진 값들만 넣을 수 있도록 str 형태의 값들로 이루어진 list로 고정됨
        - 각각 str 값(오른쪽)을 int 값(왼쪽)과 연결하여 숫자 형태로 접근하도록 함
      - `region`: (1, '서울'), (2, '경기'), (3, '인천'), (4, '대전'), (5, '충북'), (6, '충남'), (7, '강원'), (8, '부산'), (9, '경북'), (10, '경남'), (11, '대구'), (12, '울산'), (13, '광주'), (14, '전북'), (15, '전남'), (16, '제주')
      - `bodyShape`: (1, '보통체형'), (2, '통통한'), (3, '살짝볼륨'), (4, '글래머'), (5, '마른'), (6, '슬림탄탄')
      - `personality`: (1, '지적인'), (2, '차분한'), (3, '유머있는'), (4, '낙천적인'), (5, '내향적인'), (6, '외향적인'), (7, '감성적인'), (8, '상냥한'), (9, '귀여운'), (10, '섹시한'), (11, '4차원인'), (12, '발랄한'), (13, '도도한')
        - ***multi choice 정보(필드) 추후 업데이트 (현재는 모두 복수 선택 불가능)***
      - `bloodType`: (1, 'AB형'), (2, 'A형'), (3, 'B형'), (4, 'O형')
      - `drinking`: (1, '가끔 마심'), (2, '어느정도 즐기는편'), (3, '술자리를 즐김'), (4, '마시지 않음')
      - `smoking`: (1, '흡연'), (2, '비흡연')
      - `religion`: (1, '종교 없음'), (2, '기독교'), (3, '천주교'), (4, '불교'), (5, '원불교'), (6, '유교'), (7, '이슬람교')


    ```json
    {
        "nickname": "권효진",
        "birth": "1995-02-11",
        "major": "경영학전공",
        "job": "백엔드 개발자",
        "company": "아마존",
        "bodyShape": 1,
        "personality": 2,
        "bloodType": 1,
        "smoking": 2,
        "introduce": "안녕하세요 ^^"
    }
    ```

- Response Sample

  averageStar(별점), age(나이) 정보는 알아서 계산되어 나옴

  ```json
  {
      "info": {
          "averageStar": 3.1,
          "nickname": "권효진",
          "school": "",
          "major": "경영학전공",
          "job": "백엔드 개발자",
          "company": "아마존",
          "region": "",
          "birth": "1995-02-11",
          "age": 26,
          "tall": "",
          "bodyShape": 1,
          "personality": 2,
          "bloodType": 1,
          "smoking": 2,
          "drinking": "",
          "religion": "",
          "introduce": "안녕하세요 ^^"
      }
  }
  ```



### User Info Update

- URL: `/user/info/`

- Method: `PATCH`

- User별 상세프로필 정보 (부분 혹은 전체) 수정

- Request Sample

  - URL: http://13.209.3.115:88/api/user/info/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hjk@hjk.com
       - Password: hjk

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    ```json
    {
        "region": 1,
        "drinking": 1,
        "introduce": "만나서 반가워요 ㅎㅎ"
    }
    ```

- Response Sample

  ```json
  {
      "info": {
          "averageStar": 3.3,
          "nickname": "권효진",
          "school": "",
          "major": "경영학전공",
          "job": "백엔드 개발자",
          "company": "아마존",
          "region": 1,
          "birth": "1995-02-11",
          "age": 26,
          "tall": "",
          "bodyShape": 1,
          "personality": 2,
          "bloodType": 1,
          "smoking": 2,
          "drinking": 1,
          "religion": "",
          "introduce": "만나서 반가워요 ㅎㅎ"
      }
  }
  ```



### User Info View

- URL: `/user/info/`

- Method: `GET`

- User별 상세프로필 정보 조회

- Request Sample

  - URL: http://13.209.3.115:88/api/user/info/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: esb@esb.com
       - Password: esb

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  User의 계정 정보와 상세프로필 정보 표시

  ```json
  {
      "user": {
          "pk": 1,
          "email": "esb@esb.com",
          "gender": "여자"
      },
      "info": {
          "averageStar": 3.5,
          "nickname": "권효진",
          "school": "",
          "major": "경영학전공",
          "job": "백엔드 개발자",
          "company": "아마존",
          "region": 1,
          "birth": "1995-02-11",
          "age": 26,
          "tall": "",
          "bodyShape": 1,
          "personality": 2,
          "bloodType": 1,
          "smoking": 2,
          "drinking": 1,
          "religion": "",
          "introduce": "만나서 반가워요 ㅎㅎ"
      }
  }
  ```



### User Story Add

- URL: `/user/story/`

- Method: `POST`

- Request Sample

  - URL: http://13.209.3.115:88/api/user/story/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hjk@hjk.com
       - Password: hjk

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    story 정보의 value는 아래 str 형태의 값들로 이루어진 list로 고정됨

    - 각각 str 값(오른쪽)을 int 값(왼쪽)과 연결하여 숫자 형태로 접근하도록 함
    - `story`: (1, 이상적인 첫 소개팅 장소), (2, 내 외모중 가장 마음에 드는 곳은), (3, 남들보다 이것 하나는 자신있어요)

    ```json
    {
        "story": 3,
        "content": "네모네모 로직"
    }
    ```

- Response Sample

  ```json
  {
      "story": {
          "pk": 2,
          "story": 3,
          "content": "네모네모 로직"
      }
  }
  ```



### User Story Update

- URL: `/user/story/`

- Method: `PATCH`

- 해당 유저의 등록되어 있는 스토리 객체에 접근하여 `content`(스토리 답변) 수정

- Request Sample

  - URL: http://13.209.3.115:88/api/user/story/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: ycs@ycs.com
       - Password: ycs

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    ```json
    {
        "story": 1,
        "content": "조용한 식당"
    }
    ```

- Response Sample

  ```json
  {
      "story": {
          "pk": 11,
          "story": 1,
          "content": "조용한 식당"
      }
  }
  ```



### User Story Delete

- URL: `/user/story/<int:pk>/`

  - URL 주소에 붙은 pk 번호를 통해 User별 각 story 객체에 접근

- Method: `DELETE`

- Request Sample

  - URL: http://13.209.3.115:88/api/user/story/1/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hjk@hjk.com
       - Password: hjk

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  ```json
  "해당 스토리가 삭제되었습니다."
  ```

  

### User Story List

- URL: `/user/story/`

- Method: `GET`

- Request Sample

  - URL: http://13.209.3.115:88/api/user/story/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: esb@esb.com
       - Password: esb

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  User의 계정 정보와 현재 등록된 스토리 정보 표시

  ```json
  {
      "user": {
          "pk": 1,
          "email": "esb@esb.com",
          "gender": "여자"
      },
      "stories": [
          {
              "pk": 1,
              "story": 1,
              "content": "조용한 카페"
          }
      ]
  }
  ```



### User Tag

*multiple choice 필드 추후 업데이트*



### User Ribbon Add

- URL: `/user/ribbon/`

- Method: `POST`

- 해당 유저의 리본사용내역 추가

- Request Sample

  - URL: http://13.209.3.115:88/api/user/ribbon/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hjk@hjk.com
       - Password: hjk

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    ```json
    {
        "paidRibbon": -5
    }
    ```

- Response Sample

  currentRibbon(현재보유리본), when(날짜) 정보는 알아서 추가됨

  ```json
  {
      "ribbon": {
          "pk": 2,
          "paidRibbon": -5,
          "currentRibbon": 7,
          "when": "2020-04-08 01:07"
      }
  }
  ```



### User Ribbon History

- URL: `/user/ribbon/`

- Method: `GET`

- 처음 토큰이 생성되면(계정 생성하면), 관리자 기본 지급으로 리본 10개 생성(obj)

- Request Sample

  - URL: http://13.209.3.115:88/api/user/ribbon/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hjk@hjk.com
       - Password: hjk

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  - User의 계정 정보와 현재까지 리본 사용내역 객체별로 정보 표시
- User의 계정이 처음 생성되면 paidRibbon, currentRibbon 10개씩 기본 지급 설정
  
  ```json
  {
      "user": {
          "pk": 1,
          "email": "hjk@hjk.com",
          "gender": "여자"
      },
      "ribbons": [
          {
              "pk": 1,
              "paidRibbon": 10,
              "currentRibbon": 10,
              "when": "2020-04-07 19:52"
          },
          {
              "pk": 2,
              "paidRibbon": -5,
              "currentRibbon": 5,
              "when": "2020-04-08 01:07"
          }
      ]
  }
  ```