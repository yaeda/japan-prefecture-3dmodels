# 都道府県別3Dモデル（厚さ調整あり）

このリポジトリは国土地理院が公開している[県別の立体模型](https://maps.gsi.go.jp/3d/prefecture/prefecture.html)をもとに、**3Dプリンターでの出力用に厚みを追加し、底面を最適化したモデルを提供**することを目的としています。

元データは108万分の1スケールで作成され、標高が3倍に強調されているため、地形の特徴を把握するのに優れています。しかし、3Dプリントを行う際に以下のような課題がありました。

- 平野部が薄く壊れやすい
- 地形に対して底面が広すぎて、印刷効率が悪い

そこで、本リポジトリでは以下の2つを公開しています。

- 1.0mmの厚みを追加し、底面を地形に沿って補正した都道府県モデル（STL）
- 任意の厚みを追加し、必要に応じて底面調整も可能なスクリプト

> [!NOTE]
> すべてのモデルの印刷・確認はできていません。おかしなモデルを発見したらIssueで教えて下さい。

## 都道府県モデル

- [オリジナルモデル](https://github.com/yaeda/japan-prefecture-3dmodels/releases/download/v1.0/original.zip)
  - オリジナルはファイル名に文字化けがあったので、ファイル名のみ変更しています。
- [1.0mmの厚みを追加したモデル](https://github.com/yaeda/japan-prefecture-3dmodels/releases/download/v1.0/thicken.zip)
- [1.0mmの厚みを追加し、底面を最適化したモデル（推奨）](https://github.com/yaeda/japan-prefecture-3dmodels/releases/download/v1.1/optimized.zip)

## スクリプト

```
.
├── optimize.py     # モデルに厚みを追加し、底面を最適化するスクリプト
└── process_all.sh  # ディレクトリ内のSTLに対してバッチ処理を行うスクリプト
```

## スクリプトの使用方法

### 必要なインストール

以下のPythonパッケージが必要です。

```bash
pip install trimesh numpy shapely scipy
```

### 個別ファイルに対して実行

```bash
python optimize.py <input_file> <output_file> [thickness] [--skip-adjustment]

# 例
python optimize.py original/tokyo_x3+300m.stl optimized/tokyo_x3+300m_+1.0mm.stl 1.0
```

- `thickness`の単位はmmです（デフォルトは1.0mm）。
- `--skip-adjustment`を指定すると底面形状の補正をスキップできます。
- 出力されるSTLはバイナリ形式です。

### 一括実行

```bash
sh process_all.sh <input_dir> <output_dir> <thickness>

# 例
sh process_all.sh original optimized 1.0
```

- `input_dir`配下のすべての`*.stl`ファイルに対して`optimize.py`を実行し、`*_+<thickness>mm.stl`として `output_dir`に出力します。

## 元データ出典

[国土地理院 県別の立体模型](https://maps.gsi.go.jp/3d/prefecture/prefecture.html)
