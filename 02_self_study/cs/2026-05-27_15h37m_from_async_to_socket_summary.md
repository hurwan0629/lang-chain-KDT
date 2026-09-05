> [이전 공부](C:\Construction_Process_of_an_AI_Video_Object_Detection_and_Analysis_Platform_Utilizing_LangChain\workspace\personal\cs_learning\2026-05-27_15h37m_from_async_to_socket.md)를 최종적으로 한번에 설명하는 공간입니다.

# 흐름
1. `async`에 대한 의문
2. 해결 후 `socket`에 대한 탐구

# python의 async 탐구
첫 발단은 `iterable` 객체와 `yield`, `for` 등에 대해서 알아본 후, 이전부터 이해하는 데 시간이 상대적으로 오래 걸리는 편이었던 `asynchronous`. 즉, 비동기 함수에 대한 탐구를 하려 하였습니다.

*이전에도 공부를 하였지만 1, 2회차에는 만족스럽지 못하여 3번째 공부가 되었습니다.*

## async 기본
`C`, `Java`, `Python` 등의 프로그래밍 언어는 대부분 비동기를 지원합니다. 이때 **동기**와 **비동기**에 대한 개념이 존재하는데, **동기**는 작업중 스레드를 점유하여 다른 작업이 같이 실행되게 하지 못하는 작업을 말하며 **비동기**는 정 반대로 쉬어가도 되는 작업에서 다른 작업에 작업의 권한을 양보하는 방식의 작업을 말합니다.

파이썬에는 라이브러리 없이 기본적으로 `async`와 `await` 키워드를 지원합니다. `async`는 `async def func1()`과 같이 사용하며 `coro = func1()`을 사용하면 실행된 결과를 반환하는 것이 아닌 **코루틴 함수**에 대한 객체를 반환합니다. **코루틴 함수**란 실행을 중단하고 나중에 재개할 수 있는 함수를 말하며 `func1() == func1()` 의 결과가 `False`로 나오는 것을 통해 해당 `async` 함수는 코루틴 함수 객체를 반환한다는 것을 알 수 있습니다.

![asyncio 참고 이미지](https://mblogthumb-phinf.pstatic.net/MjAyMTA1MjBfMjQx/MDAxNjIxNTE4MjU1Mjg2.aEAwOCZiG9wgB8vTb7VIBW9gqVgYdnz8jNIHfxq8FxMg.7Md8l-hbiCEaLwsvQOXXjub0rz411VG7kbek6AObHB0g.PNG.aspasia_388/1_60iugGBHMF7PPSn-fdQrHQ.png?type=w800)

이렇게 만들어진 `coro`객체는 기본적으로 `await`를 통해 실행될 수 있습니다. `await`는 코루틴 함수 객체를 실행시켜주며 해당 작업을 실행하는 동안 다른 작업을 실행하라는 스레드 권한 양보와 작업중에 `I/O`작업에 의한 대기 시, 코드를 더이상 진행하지 말라는 의미를 가집니다.


## asyncio 라이브러리
`Python`이 기본적으로 지원하는 `async`와 `await`는 하나의 코드에서 동시에 2가지 이상의 코드를 돌리지 못하게 합니다. `await coro`를 하면 현재 코루틴은 `coro`의 결과가 나올 때까지 멈춥니다. 이때 다른 작업을 대신 실행해줄 `Event Loop`가 없다면 비동기의 이점을 살리기 어렵기 때문에, Python에서는 일반적으로 `asyncio`를 통해 여러 코루틴을 Task로 관리합니다.

`asyncio`는 내부적으로 비동기 작업, **`Event Loop`**를 돌리며 그 위에서 `Coroutine` 객체를 감싸주는 `Task`를 만들어 관리합니다. 이 덕분에 하나의 `Coroutine`이 전체 스레드의 진행을 방해하는 일이 사라졌습니다.

- `Task`는 내부적으로 감싸는 `Coroutine`을 실행 및 관리해주고, 상태를 나타내주는 객체입니다.
- `Event Loop`는 이러한 `Task`들이 올라와 작업이 완료되어 값을 응답받을 수 있는지 확인을 해주는 비동기 작업입니다.
- `Future`는 요청한 값이 준비 되었는지를 나타내는 객체입니다.

위 3가지 요소를 통해 스레드 자원 낭비 없는 비동기 작업들이 수행되게 됩니다.

![asyncio 참고 이미지](https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fa5wtm5ha679yjxu4wjca.jpg)

## asyncio와 OS
우리가 일반적으로 설치해서 사용하는 프로그램을 **사용자 프로그램**이라고 부릅니다. 이때, 사용자 프로그램은 신뢰하기도 위험하고 신뢰할 수 있어도 권한을 아무렇게나 주게되면 작업의 순서가 흐트러져 원활한 장치의 사용이 어려워지기 때문에 **사용자 프로그램은 모두 운영체제 위에서 돌아가게 됩니다.**

운영체제는 프로그램들이 보내는 파일 권한 요청에 따라 작업을 수행해줍니다. 예를 들어서 `프로그램A`가 운영체제에 `a.txt` 읽어줘 라고 한다면 운영체제는 `a.txt`를 읽어서 `프로그램A`의 메모리 공간으로 전달해줍니다.

![소켓통신 참고 이미지](https://mark-kim.blog/static/9953b7852494334a2750c89c97fc1ba0/954eb/socket_read_write.webp)

이때, 운영체제가 직접 관리를 해주어도 모든 요청을 수락할 순 없기 때문에 (보안 등의 이유로) 최초 요청 시 `fd`라는 파일 디스크립터 라는 권한을 받게 됩니다. 이는 보통 `[파일] [r(ead) | w(rite) | execute(x)]`의 형태로 구성이 되며 이는 기본 `fd`인 0(`stdin`), 1(`stdout`), 2(`error`) 이후, `fd3` 부터 발급받을 수 있게 됩니다. 이후 프로그램은 이 `fd`를 이용하여 커널에게 `읽기`/`쓰기`와 같은 작업을 요청하고, 커널은 `fd`가 가리키는 파일이나 소켓 같은 자원에 대해 작업을 수행합니다.

위에서 이해했던 `asyncio`의 `Event Loop`의 동작 방식에는 설명하였듯, OS에게 비동기 작업을 요청한 뒤 응답을 기다리지 않고 비동기로 다른 작업을 수행한다 하였습니다. 이때, 운영체제에게서 발급받은 `fd`를 바탕으로 OS에게 해당 `fd`를 사용할 수 있을 때에 깨우라는 요청을 넣은 뒤 스레드 속 해당 작업들은 잠들게 됩니다. 이후에 OS가 알람을 소켓을 통해 보낸 뒤 CPU가 쉬게 된다면 `Event Loop`에서 잠들어있던 작업들이 깨어나 작업을 재개하게 됩니다.

## 소켓과 스트림
소켓과 스트림은 데이터를 전달하는 여러 방식 중 하나로
- 소켓: 네트워크를 통한 통신의 끝 점
- 스트림: 해당 데이터가 흐르는 통로
- 버퍼: 원활한 흐름 관리를 위한 임시 저장공간

으로 이루어져

`[프로그램A] --- [소켓][IP:포트] --- [버퍼] --- [TCP연결] --- [버퍼] --- [IP:포트][소켓] --- [프로그램B]`와 같이 통신이 됩니다.

이때, Python의 `Event Loop`는 OS에게 특정 `fd`가 읽기/쓰기 가능한 상태가 되면 알려달라고 등록해두고, OS가 준비 완료 이벤트를 알려주면 해당 이벤트를 바탕으로 잠들어 있던 Task를 다시 실행합니다.

이를 통해 비동기 작업이 진행되게 됩니다.
