#!/bin/bash
# chmod +x script.sh
# ./script.sh


# Miniconda 설치 여부 확인
if [ ! -d "$HOME/miniconda" ]; then
    echo "Miniconda가 설치되어 있지 않습니다. 설치를 진행합니다."
    curl -L https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o Miniconda3.sh
    bash Miniconda3.sh -b -p $HOME/miniconda
    rm Miniconda3.sh
    export PATH="$HOME/miniconda/bin:$PATH"
else
    echo "Miniconda가 이미 설치되어 있습니다. 설치를 건너뜁니다."
fi

# Miniconda 활성화
export PATH="$HOME/miniconda/bin:$PATH"
eval "$(conda shell.bash hook)"
conda activate base

# Mypy 설치 여부 확인 및 설치
if ! python -c "import mypy" &> /dev/null; then
    echo "Mypy가 설치되어 있지 않습니다. 설치를 진행합니다."
    conda install -y mypy
else
    echo "Mypy가 이미 설치되어 있습니다. 설치를 건너뜁니다."
fi

# 동적 경로 설정
script_dir=$(dirname "$0")
input_dir="$script_dir/input"
output_dir="$script_dir/output"
submission_dir="$script_dir/submission"

# 디렉터리 생성 및 확인
mkdir -p "$input_dir"
mkdir -p "$output_dir"
mkdir -p "$submission_dir"

if [[ ! -d "$input_dir" ]] || [[ -z $(ls -A "$input_dir") ]]; then
    echo "[ERROR] Input directory '$input_dir' does not exist or is empty."
    exit 1
fi

if [[ ! -d "$submission_dir" ]] || [[ -z $(ls -A "$submission_dir"/*.py 2>/dev/null) ]]; then
    echo "[ERROR] No Python files found in '$submission_dir'."
    exit 1
fi

# 모든 파이썬 파일 실행
for file in "$submission_dir"/*.py; do
    filename=$(basename "$file" .py)
    input_file="$input_dir/${filename}_input"
    output_file="$output_dir/${filename}_output"

    if [[ ! -f "$input_file" ]]; then
        echo "[WARNING] Input file '$input_file' does not exist. Skipping $filename."
        continue
    fi

    echo "Executing $filename with input=$input_file and output=$output_file"
    python "$file" < "$input_file" > "$output_file"
done

# mypy 테스트 수행
echo "Running mypy tests..."
mypy "$submission_dir"/*.py

echo "All tasks are complete."
