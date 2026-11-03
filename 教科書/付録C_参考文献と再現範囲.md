# 参考文献と再現範囲

案内：[[00_学習案内]]

## この教材の一次資料

対象は作業フォルダーに提供された `main.tex`、`references.bib`、`fig1.png`〜`fig9.png` である。
論文名は *Modular optical fault-tolerant quantum computation via an interface between verified resources and online logical operations*、著者は Kosuke Fukui、Takaya Matsuura、Yohji Chin、Shohei Kiryu、Takaya Hoshi、Kan Takase、Warit Asavanant である。
フォルダーの識別は arXiv `2610.32838v1` だが、教材の記述は手元の原稿内容を基準にした。
他版の変更や公開先の最新内容まで同一であるとは確認していない。

教材の `sources` フォルダーに原稿と参考文献のコピー、`assets` に原図のコピーを置く。
コピーは参照のためで、原資料の権利は各権利者に帰属する。
独自に加えた符号語、途中計算、練習問題、Python 検算は原論文の図表や数値実験と区別した。

## 基礎へ戻る文献

以下は対象論文の参考文献から、教材の学習経路に関係するものを選んだ。
書誌は提供された `references.bib` を基準とする。
GKP 原提案のリンクは外部原著ページでも確認した。
他の文献は全内容を再解析したという意味ではなく、追加学習のための原著の案内である。

| 内容 | 文献 | 教材の対応 |
|---|---|---|
| 振動子への量子ビット符号化 | Gottesman, Kitaev, Preskill, *Encoding a qubit in an oscillator*, PRA 64, 012310 (2001). [原著](https://arxiv.org/abs/quant-ph/0008040) | [[05_GKP符号と変位誤り]] |
| Gaussian 量子情報 | Weedbrook et al., *Gaussian quantum information*, RMP 84, 621 (2012) | [[04_光の連続変数とGaussian操作]] |
| アナログ GKP 復号 | Fukui, Tomita, Okamoto, *Analog quantum error correction with encoding a qubit into an oscillator*, PRL 119, 180507 (2017) | [[06_GKP尤度とアナログ復号]] |
| 検証資源とテレポーテーション | Knill, *Quantum computing with realistically noisy devices*, Nature 434, 39–44 (2005) | [[10_再帰工場とソフト復号]] |
| ポストセレクションの閾値解析 | Aliferis, Gottesman, Preskill, *Accuracy threshold for postselected quantum computation*, QIC 8, 181–244 (2008) | [[11_選別と独立評価]] |
| ソフト判定とテレポーテーション復号 | Goto, Uchikawa, *Fault-tolerant quantum computation with a soft-decision decoder for error correction and detection by teleportation*, Scientific Reports 3, 2044 (2013) | [[10_再帰工場とソフト復号]] |
| QRL の柔軟な回路 | Alexander, Menicucci, *Flexible quantum circuits using scalable continuous-variable cluster states*, PRA 93, 062326 (2016) | [[09_MBQCとQRL]] |
| 2 次元クラスターのゲート雑音 | Larsen, Neergaard-Nielsen, Andersen, *Architecture and noise analysis of continuous-variable quantum gates using two-dimensional cluster states*, PRA 102, 042608 (2020) | [[13_雑音モデルと共分散]] |
| マクロノード処理 | Walshe et al., *Streamlined quantum computing with macronode cluster states*, PRA 104, 062427 (2021) | [[09_MBQCとQRL]] |
| 光学 GKP の QND 雑音 | Fukui, *High-threshold fault-tolerant quantum computation with the Gottesman–Kitaev–Preskill qubit under noise in an optical setup*, PRA 107, 052414 (2023) | [[13_雑音モデルと共分散]] |
| 符号自己同型と Clifford | Sayginel et al., *Fault-Tolerant Logical Clifford Gates from Code Automorphisms*, PRX Quantum 6, 030343 (2025) | [[08_C4の論理ゲートを導く]] |
| 魔法状態 | Bravyi, Kitaev, *Universal quantum computation with ideal Clifford gates and noisy ancillas*, PRA 71, 022316 (2005) | [[09_MBQCとQRL]] |

原稿の引用キー `MenicucciQRL2020` は、実際の書誌では Larsen らの 2020 年論文を指す。
引用キーの人名だけで書誌の著者を推測しない。

## 数式から検算できる範囲

GKP 奇数区間の積分、巻き込み和、C4 代数、Hadamard の置換、トランスバーサル CNOT、独立入力の尤度周辺化、共分散再帰は、教材内の定義から検算できる。
報告された $(k,n)$ から Jeffreys 分位点や CP 上限を再計算できる。
名目費用の $3637.8947$ と比 $12.6316$ も、指定の漸化式から計算できる。
これらを付属スクリプトで確認する。

## 原稿だけでは再現できない範囲

対象論文の Data Availability は、データとソフトウェアに商業上機微な情報があり、公開せず、合理的な請求に対し連絡著者から入手可能としている。
今回提供されたファイルにも、学習済み木モデル、完全な 523 特徴量の定義、回路索引付き遷移表、独立標本の全記録は含まれていない。
したがって原稿の記述だけから、報告された Monte Carlo 試験を独立に再実行したとはいえない。

とくに 12 子資源の平均誤り率だけを入力して同じ値を得るような単純漸化式を、代替モデルとして捏造しない。
親復号はアナログ値、シンドローム、子スロット、フレーム、学習済みスコアに依存する。
本文中の数値結果は著者の報告値であり、付属コードの検算は報告値の算術と教材の代数を対象にする。

## 読み残しを判断する

QRL の全光学ネットワークから測定パターンと雑音係数を再導出したい場合は、上表の QRL 原著をモード順序と符号規約までそろえて読む。
実際の GKP 状態生成を設計したい場合は、原稿付録 A の光源文献から特定の方式を選び、生成率、品質、損失を評価する。
この教材は、それらの実装を選ぶ前に必要な、対象論文の式と性能主張を読むための基礎を扱う。
