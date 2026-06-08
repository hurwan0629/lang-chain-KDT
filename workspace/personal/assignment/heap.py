# 최소 힙 구하기
rand_heap = [1, 2, 3, 4, 12, 6]

# 레벨에 따른 인덱스 시작 위치 찾기
# 시작, 끝+1
def find_level_index(level: int):
  return 2**level-1

# 특정 인덱스 노드의 자식 인덱스 찾기
def find_children(index: int):
  return index*2+1, index*2+2

# 특정 부모 인덱스에서 시작해서 아래로 내려가며 최소 힙 조건 맞추기
def normalize_sub(p_index: int, heap: list):
    while True:
        l_child, r_child = find_children(p_index)

        # 왼쪽 자식도 없으면 리프 노드
        if l_child >= len(heap):
            break

        # 일단 왼쪽 자식을 더 작은 자식 후보로 둠
        smaller_child = l_child

        # 오른쪽 자식이 있고, 오른쪽이 더 작으면 후보 변경
        if r_child < len(heap) and heap[r_child] < heap[l_child]:
            smaller_child = r_child

        # 부모가 더 작은 자식보다 크면 교환
        if heap[p_index] > heap[smaller_child]:
            heap[p_index], heap[smaller_child] = heap[smaller_child], heap[p_index]

            # 교환된 위치에서 계속 아래로 검사
            p_index = smaller_child
        else:
            break


def heapify(heap: list):
    # 마지막 부모 인덱스
    last_parent = (len(heap) - 2) // 2

    # 마지막 부모부터 루트까지 거꾸로 normalize
    for i in range(last_parent, -1, -1):
        normalize_sub(i, heap)

heapify(rand_heap)
print(rand_heap)