# ChatGPT로파일자동분류.py

import os
import shutil

# 다운로드 폴더 경로
DOWNLOADS_PATH = r"C:\Users\student\Downloads"

# 파일 확장자별 대상 폴더 매핑
EXTENSION_MAP = {
    "images": [".jpg", ".jpeg"],
    "data": [".csv", ".xlsx"],
    "docs": [".txt", ".doc", ".pdf"],
    "archive": [".zip"]
}

# 각 확장자에 맞는 폴더로 이동
def organize_downloads(download_path):
    for folder, extensions in EXTENSION_MAP.items():
        target_folder = os.path.join(download_path, folder)
        
        # 폴더가 없으면 생성
        os.makedirs(target_folder, exist_ok=True)

        # 파일 목록 순회
        for filename in os.listdir(download_path):
            file_path = os.path.join(download_path, filename)

            # 폴더가 아니라 파일일 때만
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(filename.lower())  # 확장자 소문자로 처리

                if ext in extensions:
                    target_path = os.path.join(target_folder, filename)
                    print(f"Moving {filename} → {target_folder}")
                    shutil.move(file_path, target_path)

# 실행
if __name__ == "__main__":
    organize_downloads(DOWNLOADS_PATH)
    print("✅ 정리 완료!")
