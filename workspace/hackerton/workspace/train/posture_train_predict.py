import argparse
import os
import joblib
import cv2
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix


LANDMARK_COUNT = 33
COORDS_PER_LANDMARK = 3


def normalize_pose(pose: np.ndarray) -> np.ndarray:
    """
    pose shape: (33, 3)
    각 landmark의 x, y, z 좌표를 받는다.

    정규화 목적:
    1. 사람 위치가 화면 어디 있든 중심을 맞춤
    2. 사람 크기가 달라도 비슷한 스케일로 맞춤
    """

    pose = pose.astype(float)
    normalized = pose.copy()

    # MediaPipe 기준:
    # 11: left_shoulder, 12: right_shoulder
    # 23: left_hip, 24: right_hip

    left_hip = pose[23]
    right_hip = pose[24]
    hip_center = (left_hip + right_hip) / 2.0

    # 골반 중심을 기준점으로 이동
    normalized = normalized - hip_center

    left_shoulder = pose[11]
    right_shoulder = pose[12]
    shoulder_center = (left_shoulder + right_shoulder) / 2.0

    # 어깨 중심과 골반 중심 사이 거리로 스케일 정규화
    torso_size = np.linalg.norm(shoulder_center - hip_center)

    if torso_size < 1e-6:
        # 예외 상황에서는 전체 landmark 범위로 대체
        bbox_size = np.linalg.norm(np.ptp(normalized, axis=0))
        torso_size = bbox_size if bbox_size > 1e-6 else 1.0

    normalized = normalized / torso_size

    return normalized.reshape(-1)


def load_dataset_from_csv(csv_path: str):
    """
    CSV 구조:
    0번 컬럼: 이미지 파일명
    1번 컬럼: 라벨
    2번 이후: 33개 landmark의 x, y, z 좌표 = 99개 숫자
    """

    df = pd.read_csv(csv_path, header=None)

    if df.shape[1] != 101:
        raise ValueError(
            f"CSV 컬럼 수가 예상과 다릅니다. 현재 컬럼 수: {df.shape[1]}, 예상 컬럼 수: 101"
        )

    file_names = df.iloc[:, 0].astype(str)
    labels = df.iloc[:, 1].astype(str)

    landmark_values = df.iloc[:, 2:].astype(float).values

    # (샘플 수, 99) -> (샘플 수, 33, 3)
    poses = landmark_values.reshape(len(df), LANDMARK_COUNT, COORDS_PER_LANDMARK)

    # 정규화
    X = np.array([normalize_pose(pose) for pose in poses])

    return X, labels, file_names


def train_model(csv_path: str, model_path: str):
    X, labels, file_names = load_dataset_from_csv(csv_path)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(labels)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("\n==============================")
    print("학습 완료")
    print("==============================")
    print(f"전체 데이터 수: {len(X)}")
    print(f"클래스 수: {len(label_encoder.classes_)}")
    print(f"테스트 정확도: {accuracy:.4f}")

    print("\n클래스 목록:")
    for idx, class_name in enumerate(label_encoder.classes_):
        print(f"{idx}: {class_name}")

    print("\n분류 리포트:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=label_encoder.classes_
        )
    )

    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(
        cm,
        index=label_encoder.classes_,
        columns=label_encoder.classes_
    )
    cm_df.to_csv("confusion_matrix.csv", encoding="utf-8-sig")

    bundle = {
        "model": model,
        "label_encoder": label_encoder
    }

    joblib.dump(bundle, model_path)

    print(f"\n모델 저장 완료: {model_path}")
    print("혼동 행렬 저장 완료: confusion_matrix.csv")


def extract_pose_from_image(image_path: str):
    """
    새 이미지에서 MediaPipe로 33개 landmark 추출
    """

    import mediapipe as mp

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"이미지를 읽을 수 없습니다: {image_path}")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    mp_pose = mp.solutions.pose

    with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5
    ) as pose_detector:

        result = pose_detector.process(image_rgb)

        if not result.pose_landmarks:
            return None

        landmarks = result.pose_landmarks.landmark

        pose_array = []

        for lm in landmarks:
            pose_array.append([lm.x, lm.y, lm.z])

        pose_array = np.array(pose_array)

        return normalize_pose(pose_array)


def predict_image(image_path: str, model_path: str):
    bundle = joblib.load(model_path)

    model = bundle["model"]
    label_encoder = bundle["label_encoder"]

    features = extract_pose_from_image(image_path)

    if features is None:
        print("사람 자세를 감지하지 못했습니다.")
        return

    features = features.reshape(1, -1)

    pred = model.predict(features)[0]
    proba = model.predict_proba(features)[0]

    label = label_encoder.inverse_transform([pred])[0]

    print("\n==============================")
    print("이미지 예측 결과")
    print("==============================")
    print(f"이미지: {image_path}")
    print(f"예측 자세: {label}")

    top_indices = np.argsort(proba)[::-1][:3]

    print("\n상위 예측 확률:")
    for idx in top_indices:
        class_name = label_encoder.inverse_transform([idx])[0]
        print(f"{class_name}: {proba[idx] * 100:.2f}%")


def predict_webcam(model_path: str):
    """
    웹캠으로 실시간 자세 예측
    q 키를 누르면 종료
    """

    import mediapipe as mp

    bundle = joblib.load(model_path)

    model = bundle["model"]
    label_encoder = bundle["label_encoder"]

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("웹캠을 열 수 없습니다.")

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose_detector:

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose_detector.process(frame_rgb)

            predicted_label = "No pose"
            confidence = 0.0

            if result.pose_landmarks:
                landmarks = result.pose_landmarks.landmark

                pose_array = []
                for lm in landmarks:
                    pose_array.append([lm.x, lm.y, lm.z])

                pose_array = np.array(pose_array)

                features = normalize_pose(pose_array).reshape(1, -1)

                pred = model.predict(features)[0]
                proba = model.predict_proba(features)[0]

                predicted_label = label_encoder.inverse_transform([pred])[0]
                confidence = np.max(proba) * 100

                mp_drawing.draw_landmarks(
                    frame,
                    result.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

            text = f"{predicted_label} / {confidence:.1f}%"

            cv2.putText(
                frame,
                text,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2
            )

            cv2.imshow("MediaPipe Posture Classifier", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=["train", "image", "webcam"],
        required=True,
        help="train: CSV 학습 / image: 이미지 예측 / webcam: 웹캠 실시간 예측"
    )

    parser.add_argument(
        "--csv",
        type=str,
        default="fitness_poses_csvs_out_full_list.csv",
        help="학습용 CSV 경로"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="posture_model.joblib",
        help="저장 또는 불러올 모델 경로"
    )

    parser.add_argument(
        "--image",
        type=str,
        default=None,
        help="예측할 이미지 경로"
    )

    args = parser.parse_args()

    if args.mode == "train":
        train_model(args.csv, args.model)

    elif args.mode == "image":
        if args.image is None:
            raise ValueError("--image 경로를 입력해야 합니다.")
        predict_image(args.image, args.model)

    elif args.mode == "webcam":
        predict_webcam(args.model)


if __name__ == "__main__":
    main()