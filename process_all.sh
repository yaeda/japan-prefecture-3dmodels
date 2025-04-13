#!/bin/bash

# 引数で指定：入力ディレクトリ、出力ディレクトリ、厚み（mm）
INPUT_DIR=${1:-original}
OUTPUT_DIR=${2:-optimized}
THICKNESS=${3:-1.0}

echo "📂 入力ディレクトリ: $INPUT_DIR"
echo "📁 出力ディレクトリ: $OUTPUT_DIR"
echo "📏 厚み: ${THICKNESS}mm"

# 出力ディレクトリが存在しない場合は作成
mkdir -p "$OUTPUT_DIR"

# 処理対象ファイルを1つずつ処理
for file in "$INPUT_DIR"/*.stl; do
    # 元のファイル名（拡張子除く）
    filename=$(basename "$file" .stl)

    # 新しいファイル名（_+Nmm を追加）
    output_filename="${filename}_+${THICKNESS}mm.stl"

    # 出力パス
    output_path="$OUTPUT_DIR/$output_filename"

    echo "▶️ 処理中: $file → $output_path"

    # Pythonスクリプトを実行
    python3 optimize.py "$file" "$output_path" "$THICKNESS"

    echo "✅ 完了: $output_path"
done
