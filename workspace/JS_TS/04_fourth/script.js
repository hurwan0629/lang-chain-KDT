/*
        참조 타입
        값의 주소(참조)를 저장하며, 여러 값을 묶어 관리할 수 있음

        Object: 키와 값의 쌍으로 이루어진 객체
        let user = { name: "김사과", age: 20}
        Array: 여러 값을 순서대로 저장
        let scores = [90, 80, 70]
        Function: 실행 가능한 코드 블록
        function hello() { console.log("안녕하세요") }
        let hello = function() { console.log("안녕하세요") }

        원시 타입의 저장 방식
        - 값 그 자체가 변수에 직접 저장
        - 숫자나 문자열을 변수에 넣으면, 그 변수 안에 실제 값이 들어감
        - 다른 변수에 복사하면 완전히 새로운 값이 복사되며, 한쪽을 변경해도 다른 쪽에는 영향을 주지 않음

        참조 타입의 저장 방식
        - 값이 저장된 위치(주소)를 변수에 저장
        - 객체나 배열을 변수에 담으면, 변수에는 실제 데이터가 아니라 데이터가 있는 곳의 주소가 들어감
        - 다른 변수에 할당하면 같은 데이터를 가리키게 되고, 한쪽에서 값을 수정하면 다른 쪽에서도 변경된 결과가 보임
*/

const user = { name: "김사과", age: 20}
const scores = [1,2,3,4,5,6,7,8,9,10]

console.log(scores)
console.log(typeof(scores));

for(let i=1;i<8;i++){
  scores[i] = null
}
console.log(scores)
console.log(typeof(scores));