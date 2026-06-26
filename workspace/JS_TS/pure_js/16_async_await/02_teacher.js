function orderCoffee(menu) {
    console.log(`${menu} 주문을 접수했습니다. 잠시만 기다리세요`)
    const availableMenu = ['아메리카노', '디카페인 아메리카노', '카페라떼',
    '바닐라라떼']
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if(availableMenu.includes(menu)) {
                resolve(`${menu}가 준비되었습니다. 맛있게 드세요 :)`)
            }else{
                reject(`죄송합니다. ${menu}는 판매하지 않습니다 :(`)
            }
        }, 2000)
    })
}
async function startOrder() {
    try {
        const result = await orderCoffee("아메리카노")
        console.log(result)
    } catch (error) {
        console.log(error)
    } finally {
        console.log("주문이 완료되었습니다")
    }
}

startOrder()