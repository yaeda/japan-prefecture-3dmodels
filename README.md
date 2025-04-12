# 都道府県別3Dモデル（厚さ調整あり）

このリポジトリは国土地理院が公開している[県別の立体模型](https://maps.gsi.go.jp/3d/prefecture/prefecture.html)をもとに、
**3Dプリンターでの出力用に厚みを追加したモデルを提供**することを目的としています。

元データは標高が3倍に強調されているため地形の特徴が分かりやすいのですが、3Dプリント時に**平野部が薄く壊れやすい**です。そこで、本リポジトリでは以下の２つを公開しています。

- 1.0mmの厚みを追加した都道府県のモデル（STL）
- 任意の厚みを追加するためのスクリプト

> [!NOTE]
> すべてのモデルの印刷・確認はできていません。おかしなモデルを発見したらIssueで教えて下さい。

## 都道府県モデル

- オリジナルモデル（STL）
  - オリジナルはファイル名に文字化けがあったので、ファイル名のみ変更しています。
- 1.0mmの厚みを追加したモデル（STL）

## スクリプト

```
.
├── thicken.py      # STLモデルに厚みを追加するスクリプト
└── process_all.sh  # ディレクトリ内のSTLに処理を実行するバッチスクリプト
```

## スクリプトの使用方法

### 必要なインストール

以下のPythonパッケージが必要です。

```bash
pip install trimesh numpy
```

### 個別ファイルに対して実行

```bash
python thicken.py <input_file> <output_file> <thickness>

# 例
python thicken.py original/tokyo_x3+300m.stl thicken/tokyo_x3+300m_+1.0mm.stl 1.0
```

- `input_file`に`thickness`の厚みを追加して`output_file`として保存します。
- `thickness`の単位はmmです。
- 保存されるSTLはバイナリ形式です。

### 一括実行

```bash
sh process_all.py <input_dir> <output_dir> <thickness>

# 例
sh process_all.py original thicken 1.0
```

- `input_dir`配下のすべての`*.stl`ファイルに対して`thicken.py`を実行し、`*_+1.0mm.stl`として `output_dir`に出力します。

## 元データ出典

[国土地理院 県別の立体模型](https://maps.gsi.go.jp/3d/prefecture/prefecture.html)
