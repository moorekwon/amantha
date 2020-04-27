[POSTMAN API URL](https://documenter.getpostman.com/view/9448838/SzYevFGb?version=latest)

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

<u>**실제 production**</u>에서 사용할 인증 방식

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

### Refer Through Email

- URL: `/auth/`

- Method: `POST`

- 해당 유저의 email 정보로 상세 프로필정보 접근하기

- Request Sample

  - URL: http://13.209.3.115:88/api/auth/

  - Body

    ```json
    {
        "email": "hjk@hjk.com"
    }
    ```

- Response Sample

  ```json
  {
      "userProfile": {
          "pk": 7,
          "email": "hjk@hjk.com",
          "gender": "여자",
          "status": "pass",
          "averageStar": 3.67,
          "currentRibbon": 45,
          "profilePercentage": 53.3,
          "images": [
              {
                  "pk": 1,
                  "image": "https://amantha.s3.amazonaws.com/profile_images/casey-horner-4rDCa5hBlCs-unsplash.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200427%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200427T052545Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=0f566f0289a9ef6174cb018607a2946a103c9de93a37fa811a547db5df44fc80"
              },
              {
                  "pk": 2,
                  "image": "https://amantha.s3.amazonaws.com/profile_images/hjk.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200427%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200427T052545Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=391a1b03ad3c7f04244dbc8e8c36793345d2dd33b03532d6a9cd7050b6b11c1c"
              },
              {
                  "pk": 3,
                  "image": "https://amantha.s3.amazonaws.com/profile_images/hjk8.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200427%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200427T052545Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=5fe078e9df18f225648cadb932f94def2b01bcd28280498b0b3b1990e6fddfa1"
              }
          ],
          "info": {
              "nickname": "권효진",
              "birth": "1995-02-11",
              "age": 26,
              "school": "",
              "major": "",
              "job": "",
              "company": "",
              "region": "서울",
              "tall": null,
              "bodyShape": "보통체형",
              "personalities": [
                  "차분한",
                  "귀여운",
                  "유머있는"
              ],
              "bloodType": "AB형",
              "smoking": "비흡연",
              "drinking": "",
              "religion": "",
              "introduce": "안녕하세요 ^^"
          },
          "stories": [
              {
                  "pk": 1,
                  "story": 1,
                  "content": "조용한 까페"
              },
              {
                  "pk": 2,
                  "story": 3,
                  "content": "네모네모 로직"
              }
          ],
          "tags": {
              "dateStyle": [
                  {
                      "name": "광란의 댄스 배틀"
                  }
              ],
              "lifeStyle": [
                  {
                      "name": "여유를 즐겨요"
                  },
                  {
                      "name": "욜로라이프를 즐겨요"
                  }
              ],
              "charm": [
                  {
                      "name": "화를 잘 안 내요"
                  }
              ],
              "relationshipStyle": []
          },
          "idealTypeInfo": [
              {
                  "ageFrom": 25,
                  "ageTo": 35,
                  "region": "서울",
                  "region2": "경기",
                  "tallFrom": 174,
                  "tallTo": 180,
                  "bodyShape": "",
                  "personalities": [],
                  "religion": "",
                  "smoking": "",
                  "drinking": ""
              }
          ],
          "ribbonHistory": [
              {
                  "pk": 1,
                  "paidRibbon": 0,
                  "currentRibbon": 50,
                  "when": "2020-04-27 11:52"
              },
              {
                  "pk": 11,
                  "paidRibbon": -5,
                  "currentRibbon": 45,
                  "when": "2020-04-27 11:52"
              }
          ]
      }
  }
  ```



### User Login

- URL: `/auth/token/`

- Method: `POST`

- 가입심사를 합격한(`status`가 `pass`인) 유저 로그인

- Request Sample

  - URL: http://13.209.3.115:88/api/auth/token/

  - Body

    ```json
    {
        "email": "hjk@hjk.com",
        "password": "hjk"
    }
    ```

- Response Sample

  ```json
  {
      "token": "f3bba546a7eb77117aeef9091461b961d742f571",
      "user": {
          "pk": 1,
          "email": "hjk@hjk.com",
          "gender": "여자",
          "status": "pass"
      }
  }
  ```



### User List

- URL: `/auth/token/`

- Method: `GET`

- 전체 유저의 상세프로필 정보 (부분 혹은 전체)

- Request Sample

  - URL: http://13.209.3.115:88/api/auth/token/

- Response Sample

  유저의 상태에 따라 분류
  
  - `on_screening`(가입심사 중), `pass`(가입심사 합격), `fail`(가입심사 불합격)
  - `pass` 상태의 유저는 `login`과 `logout`으로 분류
  
  ```json
  {
      "superusers": [
          "man1@man.com",
          "man2@man.com",
          "man3@man.com",
          "man4@man.com",
          "man5@man.com",
          "man6@man.com"
      ],
      "login": [
          {
              "pk": 7,
              "email": "hjk@hjk.com",
              "gender": "여자",
              "status": "pass"
          },
          {
              "pk": 12,
              "email": "dhl@dhl.com",
              "gender": "남자",
              "status": "pass"
          },
          {
              "pk": 13,
              "email": "dok@dok.com",
              "gender": "남자",
              "status": "pass"
          }
      ],
      "logout": [],
      "onScreening": [
          {
              "pk": 8,
              "email": "ebk@ebk.com",
              "gender": "여자",
              "status": "on_screening"
          },
          {
              "pk": 9,
              "email": "szj@szj.com",
              "gender": "여자",
              "status": "on_screening"
          }
      ],
      "fail": [
          {
              "pk": 10,
              "email": "hbb@hbb.com",
              "gender": "남자",
              "status": "fail"
          }
      ]
  }
  ```



### User Signup

- URL: `/auth/create/`

- Method: `POST`

- 가입심사 중(`status`가 `on_screening`)인 상태로 계정 생성(회원가입)

- Request Sample

  - URL: http://13.209.3.115:88/api/auth/create/

  - Body

    ```json
    {
        "email": "ksk@ksk.com",
        "password": "ksk",
        "gender": "남자"
    }
    ```

- Response Sample

  ```json
  {
      "token": "d632fa674825c92ffced89302a46f8f1bd98a284",
      "user": {
          "pk": 17,
          "email": "ksk@ksk.com",
          "gender": "남자",
          "status": "on_screening"
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

- **User별 Image, Info, Story, Tag 정보, 보유 ribbon, pick받은 이성, 등 전체 정보 표시**

  - *어떤 정보까지 모두 넣어야 할지 의견 필요*

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

  ```json
  {
      "userProfile": {
          "pk": 1,
          "email": "esb@esb.com",
          "gender": "여자",
          "status": "pass",
          "averageStar": 3.72,
          "currentRibbon": 10,
          "profilePercentage": 71.4,
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
              }
          ],
          "info": {
              "nickname": "은순이",
              "birth": "1995-02-23",
              "age": 26,
              "school": "",
              "major": "정치외교학",
              "job": "회사원",
              "company": "",
              "region": "서울",
              "tall": null,
              "bodyShape": "보통체형",
              "personalities": ["외향적인", "지적인", "4차원인"],
              "bloodType": "B형",
              "smoking": "비흡연",
              "drinking": "",
              "religion": "",
              "introduce": "안녕하세요 ^^"
          },
          "stories": [
              {
                  "pk": 1,
                  "story": 1,
                  "content": "조용한 카페"
              }
          ],
          "tags": {
              "dateStyle": [
                  {
                      "name": "광란의 댄스 배틀"
                  }
              ],
              "lifeStyle": [
                  {
                      "name": "퇴근 후엔 운동"
                  },
                  {
                      "name": "여행 자주 가요"
                  },
                  {
                      "name": "여유를 즐겨요"
                  }
              ],
              "charm": [],
              "relationshipStyle": [
                  {
                      "name": "가벼운 연애 추구"
                  },
                  {
                      "name": "카톡보단 전화"
                  }
              ]
          },
          "idealTypeInfo": [],
          "ribbonHistory": [
              {
                  "pk": 1,
                  "paidRibbon": 10,
                  "currentRibbon": 10,
                  "when": "2020-04-22 00:41"
              }
          ]
      }
  }
  ```



### User Image

#### User Image Add

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

    **form-data** 체크, KEY에서 **File** 체크, VALUE에서 이미지 파일 선택 ***(POSTMAN에서는 파일이름이 한글일 경우 에러가 뜸..)***

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
              "image": "https://amantha.s3.amazonaws.com/profile_images/hjk.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200421%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200421T160903Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=54084ee615a19d70851cc42f319f4fd670a2d7f9bf634f1018d731a23881bc0e"
          },
          {
              "pk": 2,
              "image": "https://amantha.s3.amazonaws.com/profile_images/hjk2.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200421%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200421T160903Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=fd9fe1cdbe0a0e19214a66b42a349dbb4e52b29a8710438c5bf107fd76c158ab"
          },
          {
              "pk": 3,
              "image": "https://amantha.s3.amazonaws.com/profile_images/hjk8.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200421%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200421T160903Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=f3fcb6ded829d19a518ef62245ab46c0de929398f7ddaec7008f08ae2a6ce6a5"
          }
      ]
  }
  ```



#### User Image Delete

- URL: `/user/image/<int:pk>/`

  - URL 주소에 붙은 pk 번호를 통해 User별 각 image 객체에 접근

- Method: `DELETE`

- User별 image 객체 삭제

- **현재 등록된 이미지가 3개 이하일 경우 삭제 불가능**

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



#### User Image List

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

  User의 이미지 정보 표시

  ```json
  {
      "images": [
          {
              "pk": 1,
              "image": "https://amantha.s3.amazonaws.com/profile_images/hjk.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200421%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200421T161146Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=62fc8f526a93047169e1610d21dbedfd39ce94f1bc16fb0171c858aa7744bad5"
          },
          {
              "pk": 2,
              "image": "https://amantha.s3.amazonaws.com/profile_images/hjk8.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200421%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200421T161146Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=2bc8be2a4f7fbf1a70571fac55c11475ec49c19d0a151f1d4a8bcd3e6ef76c15"
          },
          {
              "pk": 3,
              "image": "https://amantha.s3.amazonaws.com/profile_images/hjk2.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6RUVUGEFQJYBPC4O%2F20200421%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200421T161146Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=f0df6047e31703260fac1e4cf7a2e58bff91cbc8fd08e9ee2a2b412ffda63db3"
          }
      ]
  }
  ```



### User Info

#### User Info Create

- URL: `/user/info/`

- Method: `POST`

- User 계정 생성 후 상세프로필 정보 넣기 **(처음 한 번만 POST 가능)**

- Request Sample

  - URL: http://13.209.3.115:88/api/user/info/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: szj@szj.com
       - Password: szj

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    - 필수 정보: `nickname`, `birth`

    - 옵션 정보: `school`, `major`, `job`, `company`, `region`, `tall`, `bodyShape`, `personalities`, `bloodType`, `smoking`, `drinking`, `introduce`, `religion`
    - 고정된 value를 가진 정보
      - 아래 정해진 값들만 넣을 수 있도록 **str** 형태의 값들로 이루어진 list로 고정됨
      - `region`: `서울`, `경기`, `인천`, `대전`, `충북`, `충남`, `강원`, `부산`, `경북`, `경남`, `대구`, `울산`, `광주`, `전북`, `전남`, `제주`
      - `bodyShape`: `보통체형`, `통통한`, `살짝볼륨`, `글래머`, `마른`, `슬림탄탄`
      - `personalities`: `지적인`, `차분한`, `유머있는`, `낙천적인`, `내향적인`, `외향적인`, `감성적인`, `상냥한`, `귀여운`, `섹시한`, `4차원인`, `발랄한`, `도도한`
      - `bloodType`: `AB형`, `A형`, `B형`, `O형`
      - `drinking`: `가끔 마심`, `어느정도 즐기는편`, `술자리를 즐김`, `마시지 않음`
      - `smoking`: `흡연`, `비흡연`
      - `religion`: `종교 없음`, `기독교`, `천주교`, `불교`, `원불교`, `유교`, `이슬람교`

    ```json
    {
        "nickname": "정수지",
        "birth": "1996-12-11",
        "major": "멀티미디어학과",
        "job": "프론트엔드 개발자",
        "company": "아마존",
        "bodyShape": "슬림탄탄",
        "bloodType": "O형",
        "smoking": "비흡연",
        "introduce": "수줍음이 많아요 ^^"
    }
    ```

- Response Sample

  averageStar(별점), age(나이) 정보는 알아서 계산되어 나옴

  ```json
  {
      "info": {
          "nickname": "정수지",
          "birth": "1996-12-11",
          "age": 25,
          "school": "",
          "major": "멀티미디어학과",
          "job": "프론트엔드 개발자",
          "company": "아마존",
          "region": "",        
          "tall": "",
          "bodyShape": "슬림탄탄",
          "personalities": [],
          "bloodType": "O형",
          "smoking": "비흡연",
          "drinking": "",
          "religion": "",
          "introduce": "수줍음이 많아요 ^^"
      }
  }
  ```



#### User Info Update

- URL: `/user/info/`

- Method: `PATCH`

- 가입심사를 합격한(`status`가 `pass`인) 유저의 상세프로필 정보 (부분 혹은 전체) 수정

- Request Sample

  - URL: http://13.209.3.115:88/api/user/info/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: szj@szj.com
       - Password: szj

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    ```json
    {
        "region": "서울",
        "drinking": "가끔 마심",
        "introduce": "제 매력이 뭔지 직접 알아가 보세요 ^^"
    }
    ```

- Response Sample

  ```json
  {
      "info": {
          "nickname": "정수지",
          "birth": "1996-12-11",
          "age": 25,
          "school": "",
          "major": "멀티미디어학과",
          "job": "프론트엔드 개발자",
          "company": "아마존",
          "region": "서울",        
          "tall": "",
          "bodyShape": "슬림탄탄",
          "personalities": [],
          "bloodType": "O형",
          "smoking": "비흡연",
          "drinking": "가끔 마심",
          "religion": "",
          "introduce": "제 매력이 뭔지 직접 알아가 보세요 ^^"
      }
  }
  ```



#### User Info View

- URL: `/user/info/`

- Method: `GET`

- User별 상세프로필 정보 조회

- Request Sample

  - URL: http://13.209.3.115:88/api/user/info/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: szj@szj.com
       - Password: szj

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  User의 상세프로필 정보 표시

  ```json
  {
      "info": {
          "nickname": "정수지",
          "birth": "1996-12-11",
          "age": 25,
          "school": "",
          "major": "멀티미디어학과",
          "job": "프론트엔드 개발자",
          "company": "아마존",
          "region": "서울",        
          "tall": "",
          "bodyShape": "슬림탄탄",
          "personalities": [],
          "bloodType": "O형",
          "smoking": "비흡연",
          "drinking": "가끔 마심",
          "religion": "",
          "introduce": "제 매력이 뭔지 직접 알아가 보세요 ^^"
      }
  }
  ```



### User Story

#### User Story Add

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
    - `story`: (1, `이상적인 첫 소개팅 장소`), (2, `내 외모중 가장 마음에 드는 곳은`), (3, `남들보다 이것 하나는 자신있어요`)

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



#### User Story Update

- URL: `/user/story/`

- Method: `PATCH`

- 가입심사를 합격한(`status`가 `pass`인) 유저의 등록되어 있는 스토리 객체에 접근하여 `content`(스토리 답변) 수정

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



#### User Story Delete

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

  

#### User Story List

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

  User의 현재 등록된 스토리 정보 표시

  ```json
  {
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

#### User All Tag View

- URL: `/user/tag/`

- Method: `GET`

- 해당 유저의 **전체** 등록한 관심태그 조회

- Request Sample

  - URL: http://13.209.3.115:88/api/user/tag/

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

  User가 등록한 전체 태그 정보 표시

  ```json
  {
      "tags": {
          "dateStyle": [
              {
                  "name": "광란의 댄스 배틀"
              }
          ],
          "lifeStyle": [
              {
                  "name": "퇴근 후엔 운동"
              },
              {
                  "name": "여행 자주 가요"
              },
              {
                  "name": "여유를 즐겨요"
              }
          ],
          "charm": [],
          "relationshipStyle": [
              {
                  "name": "가벼운 연애 추구"
              },
              {
                  "name": "카톡보단 전화"
              }
          ]
      }
  }
  ```



#### User Tag Date Style Update

- URL: `/user/tag/date/`

- Method: `PATCH`

- 해당 유저의 **데이트 스타일** 태그 수정**(추가)**

- Request Sample

  - URL: http://13.209.3.115:88/api/user/tag/date/

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
        "dateStyle": [
            {"name": "광란의 댄스 배틀"}
        ]
    }
    ```

- Response Sample

  ```json
  {
      "dateStyle": [
          {
              "name": "광란의 댄스 배틀"
          }
      ],
      "lifeStyle": [],
      "charm": [],
      "relationshipStyle": []
  }
  ```



#### User Tag Life Style Update

- URL: `/user/tag/life/`

- Method: `PATCH`

- 해당 유저의 **라이프 스타일** 태그 수정(추가)

- Request Sample

  - URL: http://13.209.3.115:88/api/user/tag/life/

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
        "lifeStyle": [
            {"name": "퇴근 후엔 운동"},
            {"name": "여행 자주 가요"},
            {"name": "여유를 즐겨요"}
        ]
    }
    ```

- Response Sample

  ```json
  {
      "dateStyle": [],
      "lifeStyle": [
          {
              "name": "퇴근 후엔 운동"
          },
          {
              "name": "여행 자주 가요"
          },
          {
              "name": "여유를 즐겨요"
          }
      ],
      "charm": [],
      "relationshipStyle": []
  }
  ```



#### User Tag Relationship Style Update

- URL: `/user/tag/relationship/`

- Method: `PATCH`

- 해당 유저의 **연애 스타일** 태그 수정(추가)

- Request Sample

  - URL: http://13.209.3.115:88/api/user/tag/relationship/

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
        "relationshipStyle": [
            {"name": "가벼운 연애 추구"},
            {"name": "카톡보단 전화"}
        ]
    }
    ```

- Response Sample

  ```json
  {
      "dateStyle": [],
      "lifeStyle": [],
      "charm": [],
      "relationshipStyle": [
          {
              "name": "가벼운 연애 추구"
          },
          {
              "name": "카톡보단 전화"
          }
      ]
  }
  ```



#### User Tag Charm Update

- URL: `/user/tag/charm/`

- Method: `PATCH`

- 해당 유저의 **나만의 매력** 태그 수정(추가)

- Request Sample

  - URL: http://13.209.3.115:88/api/user/tag/charm/

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
        "charm": [
            {"name": "화를 잘 안 내요"}
        ]
    }
    ```

- Response Sample

  ```json
  {
      "dateStyle": [],
      "lifeStyle": [],
      "charm": [
          {
              "name": "화를 잘 안 내요"
          }
      ],
      "relationshipStyle": []
  }
  ```



### User Ideal Type

#### User Ideal Type Create

- URL: `/user/ideal/`

- Method: `POST`

- 가입심사를 합격한(`status`가 `pass`인) 유저의 이상형 정보 **(첫) 설정** ***(이후 여기서 정보 수정 불가)***

- Request Sample

  - URL: http://13.209.3.115:88/api/user/ideal/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hbb@hbb.com
       - Password: hbb

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    - 옵션 정보: `ageFrom`, `ageTo`, `region`, `tallFrom`, `tallTo`, `bodyShape`, `personalities`, `religion`, `region2`, `smoking`, `drinking`
      - *나이와 키는 범위로 지정하기 때문에 'From', 'To' 붙여서 각각 두 개의 정보씩 필요 (추후 더 나은 방법 고려)*
    - 고정된 value를 가진 정보 (User Info Create와 value 같음)
      - 아래 정해진 값들만 넣을 수 있도록 **str** 형태의 값들로 이루어진 list로 고정됨
      - `region`, `region2`: `서울`, `경기`, `인천`, `대전`, `충북`, `충남`, `강원`, `부산`, `경북`, `경남`, `대구`, `울산`, `광주`, `전북`, `전남`, `제주`
      - `bodyShape`: `보통체형`, `통통한`, `살짝볼륨`, `글래머`, `마른`, `슬림탄탄`
      - `personalities`: `지적인`, `차분한`, `유머있는`, `낙천적인`, `내향적인`, `외향적인`, `감성적인`, `상냥한`, `귀여운`, `섹시한`, `4차원인`, `발랄한`, `도도한`
      - `drinking`: `가끔 마심`, `어느정도 즐기는편`, `술자리를 즐김`, `마시지 않음`
      - `smoking`: `흡연`, `비흡연`
      - `religion`: `종교 없음`, `기독교`, `천주교`, `불교`, `원불교`, `유교`, `이슬람교`

    ```json
    {
        "tallFrom": 160,
        "tallTo": 165,
        "ageFrom": 23,
        "ageTo": 27,
        "religion": "기독교",
        "drinking": "가끔 마심"
    }
    ```

- Response Sample

  ```json
  {
      "idealTypeInfo": {
          "ageFrom": 23,
          "ageTo": 27,
          "region": "",
          "region2": "",
          "tallFrom": 160,
          "tallTo": 165,
          "bodyShape": "",
          "personalities": [],
          "religion": "기독교",
          "smoking": "",
          "drinking": "가끔 마심"
      }
  }
  ```



#### User Ideal Type Update

- URL: `/user/ideal/`

- Method: `PATCH`

- 가입심사를 합격한(`status`가 `pass`인) 유저의 등록되어 있는 이상형 정보 **수정**

- Request Sample

  - URL: http://13.209.3.115:88/api/user/ideal/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hbb@hbb.com
       - Password: hbb

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    기존에 저장되어 있는 데이터는 수정하지 않을 경우 그대로 보존 ***(아예 수정 정보들로 전체 정보를 업데이트 해야 하는지 협의 필요)***

    ```json
    {
        "bodyShape": "보통체형",
        "drinking": "마시지 않음"
    }
    ```

- Response Sample

  **기존 저장되어 있는 데이터에 추가되거나 수정됨**

  ```json
  {
      "idealTypeInfo": {
          "ageFrom": 23,
          "ageTo": 27,
          "region": "",
          "region2": "",
          "tallFrom": 160,
          "tallTo": 165,
          "bodyShape": "보통체형",
          "personalities": [],
          "religion": "기독교",
          "smoking": "",
          "drinking": "마시지 않음"
      }
  }
  ```



#### User Ideal Type View

- URL: `/user/ideal/`

- Method: `GET`

- 가입심사를 합격한(`status`가 `pass`인) 유저의 **맞춤 이성 리스트** 조회

- Request Sample

  - URL: http://13.209.3.115:88/api/user/ideal/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hbb@hbb.com
       - Password: hbb

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  User의 이상형과 가장 유사한 이성 리스트 표시

  - *email 외 다른 고유값으로 접근하도록 변경 가능*

  ```json
  {
      "idealPartners": [
          "hjk@hjk.com",
          "szj@szj.com"
      ]
  }
  ```



### User Ribbon

#### User Ribbon Add

- URL: `/user/ribbon/`

- Method: `POST`

- 가입심사를 합격한(`status`가 `pass`인) 유저의 리본사용내역 추가

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

  - **추가된 내역 obj 표시**

  - currentRibbon(현재보유리본), when(날짜) 정보는 알아서 추가됨
  
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



#### User Ribbon History

- URL: `/user/ribbon/`

- Method: `GET`

- 가입심사를 합격한(`status`가 `pass`인) 유저의 리본 지급 내역 조회

- **처음 토큰이 생성되면(계정 생성하면), 관리자 기본 지급으로 리본 10개 생성(obj)**

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

  - User의 현재까지 리본 사용내역 객체별로 정보 표시
  - User의 계정이 처음 생성되면 paidRibbon, currentRibbon 10개씩 기본 지급 설정

  ```json
  {
      "ribbonHistory": [
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



### User Pick

#### User Pick Add

- URL: `/user/pick/`

- Method: `POST`

- partner의 email 정보를 통해 해당 partner의 pk값에 접근 ***(email이 아닌 다른 user를 식별할 수 있는 고유값으로 접근할 수 있음)***

- Request Sample

  - URL: http://13.209.3.115:88/api/user/pick/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hbb@hbb.com
       - Password: hbb

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    pick할 이성의 emall 정보 기입

    ```json
    {
        "partner": "hjk@hjk.com"
    }
    ```

- Response Sample

  해당 user와 pick한 이성의 pk값, pick 보낸 시간 표시

  `hbb@hbb.com` 유저의 pk 값이 `5`, `hjk@hjk.com` 유저의 pk 값이 `1`

  ```json
  {
      "user": 5,
      "partner": 1,
      "created": "2020-04-12 02:59"
  }
  ```



#### User Pick List

- URL: `/user/pick/`

- Method: `GET`

- 해당 user를 pick한 이성과 해당 user가 pick한 이성 조회

- Request Sample

  - URL: http://13.209.3.115:88/api/user/pick/

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

  User의 현재 pick한 이성 및 pick받은 이성 표시

  - *각 리스트는 email 외 다른 고유값으로 접근하도록 변경 가능*
  
  ```json
  {
      "pickFrom": [
          "hbb@hbb.com"
      ],
      "pickTo": [
          "hgo@hgo.com",
          "hbb@hbb.com"
      ]
  }
  ```



### User Star

#### User Screening List

- URL: `/user/screening/`

- Method: `GET`

- 가입심사 중(`status`가 `on_screening`)인  이성 리스트 불러오기

- Request Sample

  - URL: http://13.209.3.115:88/api/user/screening/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hgo@hgo.com
       - Password: hgo

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |



- Response Sample

  ```
  [
      "ebk@ebk.com",
      "szj@szj.com"
  ]
  ```



#### User Star Add

- URL: `/user/star/`

- Method: `POST`

- 이성 가입심사 별점(1~5) 보내기

- Request Sample

  - URL: http://13.209.3.115:88/api/user/star/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hgo@hgo.com
       - Password: hgo

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

  - Body

    - 가입심사하는 이성의 emall 정보와 별점 기입
    - **가입심사를 불합격한(`status`가 `fail`인) 이성에게는 별점을 보낼 수 없음**
    
    ```json
    {
        "partner": "hjk@hjk.com",
        "star": 4
    }
    ```


- Response Sample

  해당 user와 partner의 각 pk값, 보낸 별점, 그리고 보낸 시간 표시

  ```json
  {
      "user": 2,
      "partner": 4,
      "star": 4,
      "created": "2020-04-13 02:36"
  }
  ```



#### User Star List

- URL: `/user/star/`

- Method: `GET`

- 해당 user가 가입심사한 이성과 해당 user를 가입심사한 이성 및 별점 조회

- Request Sample

  - URL: http://13.209.3.115:88/api/user/star/

  - 자격 증명(유저 인증) **(아래 두 가지 방법 중 하나만 사용)**

    1. Basic Auth <u>**(test 할 때 사용)**</u>

       Login 되어있는 user의 email과 password를 **Authorization** 정보에 넣음

       - TYPE: Basic Auth
       - Username: hgo@hgo.com
       - Password: hgo

    2. Token Auth **<u>(production 때 사용)</u>**

       Login 되어있는 user의 token 값을 `Token <token 값>` 형태로 **Headers** 정보에 넣음

       | KEY           | VALUE                                          |
       | ------------- | ---------------------------------------------- |
       | Authorization | Token 8c6d86245a1a886a65253c4ac1e6920518b6bb94 |

- Response Sample

  User가 가입심사한 이성과 보낸 별점(`StarTo`) 및 User를 가입심사한 이성과 받은 별점(`StarFrom`) 표시

  - *각 리스트는 email 외 다른 고유값으로 접근하도록 변경 가능*
  
  ```json
  {
      "StarTo": [
          [
              "hjk@hjk.com",
              5
          ],
          [
              "szj@szj.com",
              4
          ]
      ],
      "StarFrom": [
          [
              "hjk@hjk.com",
              5
          ],
          [
              "szj@szj.com",
              2
          ]
      ]
  }
  ```



## User Thema

### User Thema List

- URL: `/user/thema/`

- Method: `GET`

- 가입심사를 합격한(`status`가 `pass`인) 유저에게 맞는 테마별 이성 리스트 조회 *(현재 남자 테마 4개, 여자 테마 4개)*

- Request Sample

  - URL: http://13.209.3.115:88/api/user/thema/

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

  테마별 맞춤 이성 소개 리스트

  - *각 테마별 리스트는 email 외 다른 고유값으로 접근하도록 변경 가능*

  ```json
  {
      "neitherDrinksNorSmokes": [
          "hgo@hgo.com",
          "dhl@dhl.com",
          "wyc@wyc.com"
      ],
      "fourYearsOlder": [
          "hbb@hbb.com"
      ],
      "over180Tall": [
          "sjb@sjb.com",
          "shk@shk.com"
      ],
      "churchMen": [
          "hgo@hgo.com"
      ]
  }
  ```



## User Expression

### User Expression List

- URL: `/user/expression/`

- Method: `GET`

- **가입심사를 합격한(`status`가 `pass`인) 유저가 보낸 표현과 받은 표현 조회 (별점 4점 이상 보낸 / 받은 이성)**

- Request Sample

  - URL: http://13.209.3.115:88/api/user/expression/

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

  별점 4점 이상 보낸 이성과 받은 이성 리스트

  ```json
  {
      "ReceivedPartners": [
          "hgo@hgo.com",
          "dhl@dhl.com"
      ],
      "SentPartners": [
          "hgo@hgo.com"
      ]
  }
  ```




### Restaurants Category List

- URL: `/restaurants/category/<category_name>/`

- Method: `GET`

- 카테고리 별 가게 리스트 데이터

- Request Sample

  - URL: http://13.209.3.115:88/restaurants/category/강원도원주맛집베스트20곳/

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

  - 각 Category 별로 Restaurants 정보를 제공 

  ```json
   [
    {
        "id": 21,
        "restaurant": 21,
        "category": "강원도원주맛집베스트20곳",
        "thumbnail": "https://wps-web-clone.s3.amazonaws.com/https%3A/mp-seoul-image-production-s3.mangoplate.com/341890/261386_1582692232865_35208%3Ffit%3Daround%7C512%3A512%26crop%3D512%3A512%3B%2A%2C%2A%26output-format%3Djpg%26output-quality%3D80?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA3FVIADFZ45JSAID7%2F20200409%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200409T104645Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=8fa436e03ffbdda790638b77826f52d1b201d1d32ca3757ce9ab3034619cbaf4",
        "date_joined": "2020-04-09 17:53",
        "date_update": "2020-04-09 17:53"
    },
    {
        "id": 22,
        "restaurant": 22,
        "category": "강원도원주맛집베스트20곳",
        "thumbnail": "https://wps-web-clone.s3.amazonaws.com/https%3A/mp-seoul-image-production-s3.mangoplate.com/348050/933379_1575600903888_3288%3Ffit%3Daround%7C512%3A512%26crop%3D512%3A512%3B%2A%2C%2A%26output-format%3Djpg%26output-quality%3D80?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA3FVIADFZ45JSAID7%2F20200409%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200409T104645Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=1005334353f09009cc9ed121623e791702eaf1d569f504abe98ca0cd77a72e6f",
        "date_joined": "2020-04-09 17:53",
        "date_update": "2020-04-09 17:53"
    }
  ]
  
  ```

