# Bell 対とテレポーテーション

前：[[02_量子ビットと量子測定]]　案内：[[00_学習案内]]　次：[[04_光の連続変数とGaussian操作]]

## Bell 状態

**Bell 対**：2 量子ビットの最大もつれ状態の一つである。
基準となる状態を

$$
|\Phi^+\rangle_{AB}=\frac{|00\rangle+|11\rangle}{\sqrt2}
$$

とする。
$|00\rangle$ に $H_A$、続いて $\operatorname{CNOT}_{A\to B}$ を適用すると作れる。
この状態は $X_AX_B$ と $Z_AZ_B$ の固有値がともに $+1$ である。
各片側だけを見れば $\rho_A=I/2$ なので、片側に未知の情報が複製されているわけではない。

残りの Bell 状態は、片側に $X,Z,XZ$ を作用させて得られる。
したがって Bell 対の残留 Pauli 誤りを 4 クラスに分類できる。
両側に誤りがある場合も

$$
(M\otimes I)|\Phi^+\rangle=(I\otimes M^T)|\Phi^+\rangle
$$

によって片側へ移せる。
$Y^T=-Y$ の符号は大域位相なので、Pauli クラスには影響しない。
これが論文の Bell 安定化子による「同値類」の考え方の出発点である。

## 状態転送の導出

未知の入力 $|\psi\rangle_Q=\alpha|0\rangle+\beta|1\rangle$ と Bell 対 $AB$ を用意する。
入力と $A$ に $\operatorname{CNOT}_{Q\to A}$、次に $H_Q$ を適用する。
初期状態を展開して整理すると

$$
\begin{aligned}
|\psi\rangle_Q|\Phi^+\rangle_{AB}
\longmapsto\frac12\bigl(&|00\rangle_{QA}|\psi\rangle_B
+|01\rangle_{QA}X|\psi\rangle_B\\
&+|10\rangle_{QA}Z|\psi\rangle_B
+|11\rangle_{QA}XZ|\psi\rangle_B\bigr).
\end{aligned}
$$

測定結果を $m_Q,m_A$ とすれば、生き残る $B$ の状態は $X^{m_A}Z^{m_Q}|\psi\rangle$ である。
逆の補正 $Z^{m_Q}X^{m_A}$ を施すと元の状態を得る。
各結果の確率は $1/4$ であり、結果の 2 ビットから $\alpha,\beta$ を読み出すことはできない。
入力側は測定で消費されるため、状態の複製にもならない。

この測定は回路を逆にたどると、入力と $A$ の $ZZ$ と $XX$ を同時に測る **Bell 測定**に相当する。
両演算子は、2 箇所で反交換するため全体として可換である。
論理 Bell 測定でも、符号化した $\bar Z\bar Z$ と $\bar X\bar X$ の結果を復号する。

## Pauli フレーム

**Pauli フレーム**：既知の補正を毎回物理的に実施せず、古典ビットとして記録する方法である。
テレポーテーション後に $X$ が必要だとわかっていれば、その記録を後続ゲートや測定の解釈に反映できる。
たとえば $Z$ 測定の直前に既知の $X$ があると測定符号が反転するので、結果のビットを反転して読む。

ゲートをまたぐとフレームも変える。
$HXH=Z$ なので、$H$ の前の既知の $X$ は $H$ の後では既知の $Z$ になる。
CNOT では

$$
X_C\mapsto X_CX_T,\quad Z_C\mapsto Z_C,\quad
X_T\mapsto X_T,\quad Z_T\mapsto Z_CZ_T.
$$

この規則でフレームを更新する。
「既知の補正」と「未知の残留誤り」は別であり、補正コマンドを誤りとして数えると評価が変わってしまう。

## 不完全な Bell 資源から誘導される雑音

理想 Bell 状態の片側に $P_a$ が確率 $p_a$ で起きているとする。
Bell 測定とフレーム補正が理想的なら、テレポーテーション出力にも同じ Pauli クラスが残る。
したがって入力密度行列に対するチャネルは

$$
\Lambda(\rho)=\sum_a p_aP_a\rho P_a^\dagger.
$$

Bell 資源は、このチャネルの **Choi 状態**として読める。
Choi 状態とは、恒等チャネルと対象チャネルを Bell 対の両側に作用させた $(\mathrm{id}\otimes\Lambda)(|\Phi^+\rangle\langle\Phi^+|)$ である。
資源の 4 クラス分布と、理想テレポーテーションの雑音が対応する理由をこの式で確認できる。

> [!note] 対応の適用範囲
> 注入ゲート、Bell 測定、記憶や後続処理にも雑音があれば、それらを追加して評価する。
> 資源の誤り率だけをオンラインゲート全体の誤り率として使うことはできない。

## 資源によるゲート実行

教材の補足として、Bell 対の出力側へあらかじめゲート $U$ を作用させた資源を考える。
テレポーテーション後の状態は $UP_m|\psi\rangle$ なので、目標 $U|\psi\rangle$ に合わせる補正は $UP_m^\dagger U^\dagger$ になる。
$U$ が Clifford ならこの補正も Pauli であり、フレーム処理に収まる。
非 Clifford では補正や測定適応が増えるため、対応する魔法状態や消費回路を別に準備する。

論文との対応：第 III 節の composability、付録 B の `eq:primary_residual_channel`、付録 D の `eq:interface_cycle`。

次：[[04_光の連続変数とGaussian操作]]
