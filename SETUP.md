# セットアップガイド - 電子書籍ツール

このドキュメントでは、電子書籍ツールのセットアップと実行方法について説明します。

## 前提条件

- Windows 10/11
- Python 3.7以上（3.10以上推奨）
- 約500MB の空きディスク容量

## インストール手順

### 1. 仮想環境の作成

```bash
# PowerShellから実行
python -m venv venv
```

### 2. 仮想環境の有効化

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

または以下のコマンドでアップグレード：

```bash
pip install --upgrade -r requirements.txt
```

## 実行方法

### 方法1: 直接実行（推奨）

```bash
python main.py
```

### 方法2: 実行スクリプトを使用

```bash
python run.py
```

### 方法3: PowerShellでの実行

```powershell
.\venv\Scripts\python.exe main.py
```

## トラブルシューティング

### PyQt6関連のエラー

**問題**: `No module named 'PyQt6'`

**解決方法**:
```bash
pip install PyQt6 PyQt6-sip --upgrade --force-reinstall
```

### 画像が表示されない

**問題**: Pillow関連のエラー

**解決方法**:
```bash
pip install Pillow --upgrade
```

### PyQt6プラグインが見つからない

**問題**: `Could not find the Qt platform plugin`

**解決方法**: 仮想環境を削除して再作成：
```bash
Remove-Item venv -Recurse -Force
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 仮想環境の削除

アンインストール時は以下を実行：

```bash
# 仮想環境を無効化
deactivate

# 仮想環境フォルダを削除
Remove-Item venv -Recurse -Force
```

## 推奨事項

- **VS Code** での開発をお勧めします
  - 拡張機能: Python, PyLance
  - `.venv` フォルダを自動で認識します

- **詳細なエラーログ**が必要な場合：
  ```bash
  python -u main.py 2>&1 | Tee-Object -FilePath error.log
  ```

## パフォーマンス最適化

大きなPNG画像を多数扱う場合：

1. 画像を事前に圧縮することを推奨
2. 1冊の書籍あたり最大500ページを目安に

## セキュリティに関する注意

このアプリケーションは、ローカルマシンのみでの使用を想定しています。
ネットワーク経由での使用は推奨しません。
