# Figma to Code Converter

FigmaのデザインURLからすべてのページを取得し、各ページをコードに変換するスキルです。

## 出力形式オプション

| オプション | 説明 | 出力ファイル |
|-----------|------|-------------|
| `html` (デフォルト) | 純粋なHTML + CSS | `.html`, `.css` |
| `react` | React + Tailwind CSS | `.tsx` |

## 使用方法

ユーザーがFigmaのデザインURLを提供したら、出力形式を確認してコードを生成します。

### 出力形式の確認

ユーザーに出力形式を確認します：
- 「HTML/CSSで出力しますか？それともReact + Tailwindで出力しますか？」
- ユーザーが指定しない場合は `html` をデフォルトとします
- ユーザーが「React」「react」「Tailwind」などと言った場合は `react` を選択

## 実行手順

### Step 1: URLからfileKeyを抽出

FigmaのURLから`fileKey`を抽出します。
- URL形式: `https://figma.com/design/:fileKey/:fileName?node-id=...`
- `fileKey`はURLの`/design/`の直後にある文字列です

### Step 2: ページ一覧を取得

MCPツール `mcp__figma__get_metadata` を使用してページ一覧を取得します。

```
mcp__figma__get_metadata:
  nodeId: "0:1"  (ドキュメントルート)
  fileKey: <抽出したfileKey>
  clientLanguages: "html,css,typescript"
  clientFrameworks: "react" (reactの場合) または "unknown" (htmlの場合)
```

レスポンスからページノード（type="PAGE"）のIDと名前を取得します。

### Step 3: 各ページを処理

取得した各ページについて、以下を実行します：

#### 3.1 ページのデザインコンテキストを取得

```
mcp__figma__get_design_context:
  nodeId: <ページのnodeId>
  fileKey: <fileKey>
  clientLanguages: "html,css,typescript"
  clientFrameworks: "react" (reactの場合) または "unknown" (htmlの場合)
```

#### 3.2 コードを生成

**HTML/CSS出力の場合:**
- MCPから返されたReact + Tailwindコードを純粋なHTML/CSSに変換
- セマンティックなHTML構造を使用
- CSSは別ファイルに分離
- 出力: `output/<page_name>.html`, `output/<page_name>.css`

**React + Tailwind出力の場合:**
- MCPから返されたコードをそのまま使用（必要に応じて調整）
- 画像URLの定数定義を含める
- TypeScript (.tsx) ファイルとして保存
- 出力: `output/<PageName>.tsx`

### Step 4: 完了報告

生成されたファイルの一覧をユーザーに報告します。

## 出力ファイル構成

### HTML/CSS出力
```
output/
  ├── page_1.html
  ├── page_1.css
  ├── page_2.html
  ├── page_2.css
  └── ...
```

### React + Tailwind出力
```
output/
  ├── Page1.tsx
  ├── Page2.tsx
  └── ...
```

## React + Tailwind出力の形式

```tsx
// 画像アセットの定数
const imgIcon = "https://www.figma.com/api/mcp/asset/...";
const imgBackground = "https://www.figma.com/api/mcp/asset/...";

export default function PageName() {
  return (
    <div className="...">
      {/* コンポーネント内容 */}
    </div>
  );
}
```

## 注意事項

- 画像アセットは7日間有効なURLとして提供されます
- React出力の場合、Tailwind CSSがプロジェクトに設定されている必要があります
- フォントは標準のWebフォントにフォールバックします
- 各ページは独立したファイルとして生成されます

## 例

### HTML/CSS出力の例
ユーザー入力:
```
https://figma.com/design/abc123/MyDesign?node-id=0-1
HTMLで出力して
```

### React + Tailwind出力の例
ユーザー入力:
```
https://figma.com/design/abc123/MyDesign?node-id=0-1
Reactで出力して
```
