#!/bin/bash

# miniconda가 존재하지 않을 경우 설치
## TODO
if ! command -v conda &> /dev/null; then
    echo "Conda(혹은 Miniconda)가 설치되어 있지 않습니다. 설치를 진행합니다."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p "$HOME/miniconda"
    rm miniconda.sh
    export PATH="$HOME/miniconda/bin:$PATH"
else
    echo "Conda가 이미 설치되어 있으므로 설치를 건너뜁니다."
fi

# Conda 환경 생성 및 활성화
## TODO
export PATH="$HOME/miniconda/bin:$PATH"
# (bash 외의 쉘 대비)
eval "$(conda shell.bash hook)"

# 이미 같은 이름의 환경이 있을 수 있으므로, 있으면 제거 후 재생성할 수도 있음
conda remove -n myenv --all -y 2>/dev/null || true
conda create -n myenv python=3.9 -y
conda activate myenv


## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "가상환경 활성화: 성공"
else
    echo "가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
## TODO
# (mypy 포함, 필요시 다른 패키지도 추가)
pip install --upgrade pip
pip install mypy

# Submission 폴더 파일 실행
cd submission || { echo "submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    ## TODO
    # 파일명에서 확장자 .py 제거 (예: '1.py' -> '1')
    base_name=$(basename "$file" .py)

    input_file="../${base_name}_input"
    output_file="../${base_name}_output"

    if [[ -f "$input_file" ]]; then
        echo "Executing $file (input: $input_file -> output: $output_file)"
        python "$file" < "$input_file" > "$output_file"
    else
        echo "[WARNING] 입력 파일 $input_file 이 없습니다. $file 실행 스킵."
    fi
done

# mypy 테스트 실행행
## TODO
echo "Running mypy..."
mypy *.py

# 가상환경 비활성화
## TODO
conda deactivate
